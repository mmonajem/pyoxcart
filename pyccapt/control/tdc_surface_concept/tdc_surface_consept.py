import threading
import time
from queue import Queue

import numpy as np

# local imports
from pyccapt.control.devices import initialize_devices
from pyccapt.control.tdc_surface_concept import scTDC

QUEUE_DATA = 0
QUEUE_ENDOFMEAS = 1


class BufDataCB4(scTDC.buffered_data_callbacks_pipe):
    """
    The class inherits from python wrapper module scTDC and class: buffered_data_callbacks_pipe
    """

    def __init__(self, lib, dev_desc, data_field_selection, dld_events,
                 max_buffered_data_len=500000):
        '''
        Initialize the base class: scTDC.buffered_data_callbacks_pipe

        Args:
            lib (scTDClib): A scTDClib object.
            dev_desc (int): Device descriptor as returned by sc_tdc_init_inifile(...).
            data_field_selection (int): A 'bitwise or' combination of SC_DATA_FIELD_xyz constants.
            dld_events (bool): True to receive DLD events, False to receive TDC events.
            max_buffered_data_len (int): Number of events buffered before invoking callbacks.
        '''
        super().__init__(lib, dev_desc, data_field_selection, max_buffered_data_len, dld_events)

        self.queue = Queue()
        self.end_of_meas = False

    def on_data(self, d):
        """
        This class method function:
            1. Makes a deep copy of numpy arrays in d
            2. Inserts basic values by simple assignment
            3. Inserts numpy arrays using the copy method of the source array

        Args:
            d (dict): Data dictionary.

        Returns:
            None
        """
        dcopy = {}
        for k in d.keys():
            if isinstance(d[k], np.ndarray):
                dcopy[k] = d[k].copy()
            else:
                dcopy[k] = d[k]
        self.queue.put((QUEUE_DATA, dcopy))
        if self.end_of_meas:
            self.end_of_meas = False
            self.queue.put((QUEUE_ENDOFMEAS, None))

    def on_end_of_meas(self):
        """
        This class method sets end_of_meas to True.

        Returns:
            True (bool)
        """
        self.end_of_meas = True
        return True


def errorcheck(device, bufdatacb, bufdatacb_raw, retcode):
    """
    This function checks return codes for errors and does cleanup.

    Args:
        retcode (int): Return code.
        bufdatacb (BufDataCB4): A BufDataCB4 object.
        bufdatacb_raw (BufDataCB4): A BufDataCB4 object.
        device (scTDC.Device): A scTDC.Device object.

    Returns:
        int: 0 if success return code or return code > 0, -1 if return code is error code or less than 0.
    """
    if retcode < 0:
        print(device.lib.sc_get_err_msg(retcode))
        bufdatacb.close()
        bufdatacb_raw.close()
        device.deinitialize()
        return -1
    else:
        return 0


def save_data_thread(variables, xx_list, yy_list, tt_list, voltage_data, pulse_data, flag_stop_data_thread):
    """
    This function saves the data in a separate thread.

    Args:
        variables (share_variables.Variables): A share_variables.Variables object.
        xx_list (list): A list of x coordinates.
        yy_list (list): A list of y coordinates.
        tt_list (list): A list of time coordinates.
        voltage_data (list): A list of voltage values.
        pulse_data (list): A list of pulse values.
        flag_stop_data_thread (bool): A flag to stop the thread.

    Returns:
        None
    """
    while not flag_stop_data_thread:
        # Sleep for 5 minutes
        time.sleep(300)
        xx = xx_list.copy()
        yy = yy_list.copy()
        tt = tt_list.copy()
        voltage = voltage_data.copy()
        pulse = pulse_data.copy()

        # Acquire the lock before accessing the shared data
        np.save(variables.path + "/x_data.npy", np.array(xx))
        np.save(variables.path + "/y_data.npy", np.array(yy))
        np.save(variables.path + "/t_data.npy", np.array(tt))
        np.save(variables.path + "/voltage_data.npy", np.array(voltage))
        np.save(variables.path + "/pulse_data.npy", np.array(pulse))

        print("Data saved.")


def run_experiment_measure(variables, x_plot, y_plot, t_plot, main_v_dc_plot, counter_plot, lock):
    """
    Measurement function: This function is called in a process to read data from the queue.

    Args:
        variables (share_variables.Variables): A share_variables.Variables object.
        x_plot (multiprocessing.Array): A multiprocessing.Array object.
        y_plot (multiprocessing.Array): A multiprocessing.Array object.
        t_plot (multiprocessing.Array): A multiprocessing.Array object.
        main_v_dc_plot (multiprocessing.Array): A multiprocessing.Array object.
        counter_plot (multiprocessing.Value): A multiprocessing.Value object.
        lock (multiprocessing.Lock): A multiprocessing.Lock object.

    Returns:
        int: Return code.
    """

    # surface concept tdc specific binning and factors
    TOFFACTOR = 27.432 / (1000 * 4)  # 27.432 ps/bin, tof in ns, data is TDC time sum
    DETBINS = 4900
    BINNINGFAC = 2
    XYFACTOR = 80 / DETBINS * BINNINGFAC  # XXX mm/bin
    XYBINSHIFT = DETBINS / BINNINGFAC / 2  # to center detector

    device = scTDC.Device(autoinit=False)
    retcode, errmsg = device.initialize()

    if retcode < 0:
        print("Error during init:", retcode, errmsg)
        print(f"{initialize_devices.bcolors.FAIL}Error: Restart the TDC manually "
              f"(Turn it On and Off){initialize_devices.bcolors.ENDC}")
        return -1
    else:
        print("TDC is successfully initialized")

    DATA_FIELD_SEL = (scTDC.SC_DATA_FIELD_DIF1 |
                      scTDC.SC_DATA_FIELD_DIF2 |
                      scTDC.SC_DATA_FIELD_TIME |
                      scTDC.SC_DATA_FIELD_START_COUNTER)
    DATA_FIELD_SEL_raw = (scTDC.SC_DATA_FIELD_TIME |
                          scTDC.SC_DATA_FIELD_CHANNEL |
                          scTDC.SC_DATA_FIELD_START_COUNTER)

    bufdatacb = BufDataCB4(device.lib, device.dev_desc, DATA_FIELD_SEL, dld_events=True)
    bufdatacb_raw = BufDataCB4(device.lib, device.dev_desc, DATA_FIELD_SEL_raw, dld_events=False)

    xx_list = []
    yy_list = []
    tt_list = []
    xx = []
    yy = []
    tt = []
    voltage_data = []
    pulse_data = []
    start_counter = []

    channel_data = []
    time_data = []
    tdc_start_counter = []
    voltage_data_tdc = []
    pulse_data_tdc = []

    retcode = bufdatacb.start_measurement(100)
    if errorcheck(device, bufdatacb, bufdatacb_raw, retcode) < 0:
        print("Error during read:", retcode, device.lib.sc_get_err_msg(retcode))
        print(f"{initialize_devices.bcolors.FAIL}Error: Restart the TDC manually "
              f"(Turn it On and Off){initialize_devices.bcolors.ENDC}")
        return -1

    # Define a lock
    data_lock = threading.Lock()
    flag_stop_data_thread = False
    # Create a thread
    data_thread = threading.Thread(target=save_data_thread, args=(variables, xx_list, yy_list, tt_list,
                                                                  voltage_data, pulse_data, flag_stop_data_thread))
    data_thread.daemon = True

    # Start the thread
    data_thread.start()

    events_detected = 0
    events_detected_tmp = 0
    start_time = time.time()
    pulse_frequency = variables.pulse_frequency * 1000
    loop_time = 0
    while not variables.flag_stop_tdc:
        start_time_loop = time.time()
        eventtype, data = bufdatacb.queue.get()
        eventtype_raw, data_raw = bufdatacb_raw.queue.get()
        specimen_voltage = variables.specimen_voltage
        pulse_voltage = variables.pulse_voltage
        if eventtype == QUEUE_DATA:
            # correct for binning of surface concept
            xx_dif = data["dif1"]
            length = len(xx_dif)
            if length > 0:
                events_detected_tmp += length
                events_detected += length
                yy_dif = data["dif2"]
                tt_dif = data["time"]
                start_counter.extend(data["start_counter"].tolist())
                xx_tmp = (((xx_dif - XYBINSHIFT) * XYFACTOR) * 0.1).tolist()  # from mm to in cm by dividing by 10
                yy_tmp = (((yy_dif - XYBINSHIFT) * XYFACTOR) * 0.1).tolist()  # from mm to in cm by dividing by 10
                tt_tmp = (tt_dif * TOFFACTOR).tolist()  # in ns

                xx.extend(xx_tmp)
                yy.extend(yy_tmp)
                tt.extend(tt_tmp)
                dc_voltage_tmp = np.tile(specimen_voltage, len(xx_tmp)).tolist()
                v_p_voltage_tmp = np.tile(pulse_voltage, len(xx_tmp)).tolist()

                with data_lock:
                    xx_list.extend(xx_dif.tolist())
                    yy_list.extend(yy_dif.tolist())
                    tt_list.extend(tt_dif.tolist())
                    voltage_data.extend(dc_voltage_tmp)
                    pulse_data.extend(v_p_voltage_tmp)

                length = len(xx_tmp)
                counter = counter_plot.value
                x_plot[counter:counter + length] = xx_tmp
                y_plot[counter:counter + length] = yy_tmp
                t_plot[counter:counter + length] = tt_tmp
                main_v_dc_plot[counter:counter + length] = dc_voltage_tmp
                counter_plot.value += length

        if eventtype_raw == QUEUE_DATA:
            channel_data_tmp = data_raw["channel"].tolist()
            if len(channel_data_tmp) > 0:
                tdc_start_counter.extend(data_raw["start_counter"].tolist())
                time_data.extend(data_raw["time"].tolist())
                # raw data
                channel_data.extend(channel_data_tmp)
                voltage_data_tdc.extend((np.tile(specimen_voltage, len(channel_data_tmp))).tolist())
                pulse_data_tdc.extend((np.tile(pulse_voltage, len(channel_data_tmp))).tolist())

        # Update the counter

        # Calculate the detection rate
        # Check if the detection rate interval has passed
        current_time = time.time()
        if current_time - start_time >= 0.5:
            detection_rate = events_detected_tmp * 100 / pulse_frequency
            variables.detection_rate_current = detection_rate * 2  # to get the rate per second
            variables.detection_rate_current_plot = detection_rate * 2  # to get the rate per second
            variables.total_ions = events_detected
            # Reset the counter and timer
            events_detected_tmp = 0
            start_time = current_time



        elif eventtype == QUEUE_ENDOFMEAS:
            retcode = bufdatacb.start_measurement(100, retries=10)  # retries is the number of times to retry
            if retcode < 0:
                print("Error during read (error code: %s - error msg: %s):" % (retcode,
                                                                               device.lib.sc_get_err_msg(retcode)))
                variables.flag_tdc_failure = True
                break

        # else:  # unknown event
        #     break

        if time.time() - start_time_loop > 0.2:
            loop_time += 1

    flag_stop_data_thread = True
    print("for %s times loop time took longer than 0.2 second" % loop_time)
    variables.total_ions = events_detected
    print("TDC Measurement stopped")
    np.save(variables.path + "/x_data.npy", np.array(xx_list))
    np.save(variables.path + "/y_data.npy", np.array(yy_list))
    np.save(variables.path + "/t_data.npy", np.array(tt_list))
    np.save(variables.path + "/voltage_data.npy", np.array(voltage_data))
    np.save(variables.path + "/pulse_data.npy", np.array(pulse_data))

    variables.extend_to('x', xx)
    variables.extend_to('y', yy)
    variables.extend_to('t', tt)
    variables.extend_to('dld_start_counter', start_counter)
    variables.extend_to('main_v_dc_dld_surface_concept', voltage_data)
    variables.extend_to('main_p_dld_surface_concept', pulse_data)

    variables.extend_to('channel', channel_data)
    variables.extend_to('time_data', time_data)
    variables.extend_to('tdc_start_counter', tdc_start_counter)
    variables.extend_to('main_v_dc_tdc_surface_concept', voltage_data_tdc)
    variables.extend_to('main_p_tdc_surface_concept', pulse_data_tdc)
    print("data save in share variables")
    time.sleep(0.1)
    bufdatacb.close()
    bufdatacb_raw.close()
    device.deinitialize()

    variables.flag_finished_tdc = True

    return 0


def experiment_measure(variables, x_plot, y_plot, t_plot, main_v_dc_plot, counter_plot, lock):
    # from line_profiler import LineProfiler
    #
    # lp1 = LineProfiler()
    #
    # lp1.add_function(run_experiment_measure)
    #
    # # Run the profiler
    # lp1(run_experiment_measure)(variables, x_plot, y_plot, t_plot, main_v_dc_plot, counter_plot, lock)
    # # Save the profiling result to a file
    # lp1.dump_stats('./../../experiment_measure.lprof')

    run_experiment_measure(variables, x_plot, y_plot, t_plot, main_v_dc_plot, counter_plot, lock)
