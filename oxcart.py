"""
This is the main script for doing experiment.
It contains the main control loop of experiment.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""

import time
import datetime
import h5py
import multiprocessing
from multiprocessing.queues import Queue
import threading
import numpy as np

# Serial ports and NI
import serial.tools.list_ports
import pyvisa as visa
import nidaqmx
# Local project scripts
import tdc
import tdc_new
import variables
from devices import email_send, tweet_send, initialize_devices


def logging():
    """
    logging function
    """
    import logging
    # Gets or creates a logger
    logger = logging.getLogger(__name__)
    # set log level
    logger.setLevel(logging.INFO)
    # define file handler and set formatter
    file_handler = logging.FileHandler(variables.path + '\\logfile.log', mode='w')
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)

    # Logs
    # logger.debug('A debug message')
    # logger.info('An info message')
    # logger.warning('Something is not right.')
    # logger.error('A Major error has happened.')
    # logger.critical('Fatal error. Cannot continue')

    return logger


class OXCART:
    """
    OXCART class
    """

    def __init__(self, queue_x, queue_y, queue_t, queue_dld_start_counter,
                 queue_channel, queue_time_data, queue_tdc_start_counter, lock1, lock2):
        # Queues for sharing data between tdc and main process
        # dld queues
        self.queue_x = queue_x
        self.queue_y = queue_y
        self.queue_t = queue_t
        self.queue_dld_start_counter = queue_dld_start_counter
        self.lock1 = lock1
        # TDC queues
        self.queue_channel = queue_channel
        self.queue_time_data = queue_time_data
        self.queue_tdc_start_counter = queue_tdc_start_counter
        self.lock2 = lock2

    # Initialize the V_dc for the experiment
    def initialize_v_dc(self):
        """
        Initializing the high voltage function
        """
        # Setting the com port of V_dc
        self.com_port_v_dc = serial.Serial(
            port=initialize_devices.com_ports[variables.com_port_idx_V_dc].device,  # chosen COM port
            baudrate=115200,  # 115200
            bytesize=serial.EIGHTBITS,  # 8
            parity=serial.PARITY_NONE,  # N
            stopbits=serial.STOPBITS_ONE  # 1
        )
        # configure the COM port to talk to. Default values: 115200,8,N,1
        if self.com_port_v_dc.is_open:
            self.com_port_v_dc.flushInput()
            self.com_port_v_dc.flushOutput()

            cmd_list = [">S1 3.0e-4", ">S0B 0", ">S0 %s" % variables.vdc_min, "F0", ">S0?", ">DON?",
                        ">S0A?"]
            for cmd in range(len(cmd_list)):
                self.command_v_dc(cmd_list[cmd])
        else:
            print("Couldn't open Port!")
            exit()

    def initialize_v_p(self):
        """
        Initializing the pulser function
        """
        # set the port for v_p
        resources = visa.ResourceManager('@py')
        self.com_port_v_p = resources.open_resource('ASRL4::INSTR')

        try:
            self.com_port_v_p.query('*RST')
        except:

            self.com_port_v_p.write('VOLT %s' % (variables.v_p_min * (1 / variables.pulse_amp_per_supply_voltage)))

    def initialize_counter(self):
        """
        Initializing the edge counter function
        """
        task_counter = nidaqmx.Task()
        task_counter.ci_channels.add_ci_count_edges_chan("Dev1/ctr0")
        # reference the terminal you want to use for the counter here
        task_counter.ci_channels[0].ci_count_edges_term = "PFI0"

        return task_counter

    # apply command to the V_dc
    def command_v_dc(self, cmd):
        """
        Initializing the high voltage function
        """
        self.com_port_v_dc.write(
            (cmd + '\r\n').encode())  # send cmd to device # might not work with older devices -> "LF" only needed!
        time.sleep(0.005)  # small sleep for response
        response = ''
        while self.com_port_v_dc.in_waiting > 0:
            response = self.com_port_v_dc.readline()  # all characters received, read line till '\r\n'
        return response.decode("utf-8")



    def reader_queue_dld(self):
        """
        reader of DLD queues function
        This function is called continuously by a separate thread
        """
        while True:
            while not self.queue_x.empty() or not self.queue_y.empty() or not self.queue_t.empty() or not self.queue_dld_start_counter.empty():
                with self.lock1:
                    length = self.queue_x.get()
                    variables.x = np.append(variables.x, length)
                    variables.y = np.append(variables.y, self.queue_y.get())
                    variables.t = np.append(variables.t, self.queue_t.get())
                    variables.dld_start_counter = np.append(variables.dld_start_counter,
                                                            self.queue_dld_start_counter.get())
                    variables.main_v_dc_dld = np.append(variables.main_v_dc_dld, np.tile(variables.specimen_voltage, len(length)))
                    variables.main_v_p_dld = np.append(variables.main_v_p_dld, np.tile(variables.pulse_voltage, len(length)))
            # If end of experiment flag is set break the while loop
            if variables.end_experiment:
                break

    def reader_queue_tdc(self):
        """
        reader of TDC queues function
        This function is called continuously by a separate thread
        """
        while True:
            while not self.queue_channel.empty() or not self.queue_time_data.empty() or not self.queue_tdc_start_counter.empty():
                with self.lock2:
                    length = self.queue_channel.get()
                    variables.channel = np.append(variables.channel, length)
                    variables.time_data = np.append(variables.time_data, self.queue_time_data.get())
                    variables.tdc_start_counter = np.append(variables.tdc_start_counter,
                                                            self.queue_tdc_start_counter.get())
                    variables.main_v_dc_tdc = np.append(variables.main_v_dc_tdc, np.tile(variables.specimen_voltage, len(length)))
                    variables.main_v_p_tdc = np.append(variables.main_v_p_tdc, np.tile(variables.pulse_voltage, len(length)))
            # If end of experiment flag is set break the while loop
            if variables.end_experiment:
                break

    def main_ex_loop(self, task_counter, counts_target):
        """
        Function that is called in each loop of main function
        1- Read the number of detected Ions(in TDC or Counter mode)
        2- Calculate the error of detection rate of desire rate
        3- Regulate the high voltage and pulser
        """
        # # reading DC HV
        # v_dc = (command_v_dc(">S0A?")[5:-1])
        # variables.specimen_voltage = float(v_dc)
        #
        # # reading pulser power supply voltage
        # v_p = com_port_v_p.query('MEASure:VOLTage?')[:-3]
        # variables.pulse_voltage = float(v_p)

        if variables.counter_source == 'TDC' and not variables.raw_mode:
            variables.total_ions = len(variables.x)

        elif variables.counter_source == 'pulse_counter' or variables.raw_mode:
            # reading detector MCP pulse counter and calculating pulses since last loop iteration
            variables.total_ions = task_counter.read(number_of_samples_per_channel=1)[0]

        variables.count_temp = variables.total_ions - variables.count_last
        variables.count_last = variables.total_ions

        # saving the values of high dc voltage, pulse, and current iteration ions
        variables.main_v_dc = np.append(variables.main_v_dc, variables.specimen_voltage)
        variables.main_v_p = np.append(variables.main_v_p, variables.pulse_voltage)
        variables.main_counter = np.append(variables.main_counter, variables.count_temp)
        # averaging count rate of N_averg counts
        variables.avg_n_count = variables.ex_freq * (
                sum(variables.main_counter[-variables.cycle_avg:]) / variables.cycle_avg)

        counts_measured = variables.avg_n_count / (variables.pulse_frequency * 1000)

        counts_error = counts_target - counts_measured  # deviation from setpoint

        # simple proportional control with averaging
        if counts_error > 0:
            voltage_step = counts_error * variables.vdc_step_up
        elif counts_error <= 0:
            voltage_step = counts_error * variables.vdc_step_down

        # update v_dc
        if variables.specimen_voltage < variables.vdc_max:
            if variables.specimen_voltage >= variables.vdc_min:
                # sending VDC via serial
                variables.specimen_voltage = variables.specimen_voltage + voltage_step
                self.command_v_dc(">S0 %s" % (variables.specimen_voltage))

        # update pulse voltage v_p
        new_vp = variables.specimen_voltage * variables.pulse_fraction * \
                 (1 / variables.pulse_amp_per_supply_voltage)
        if new_vp < variables.pulse_voltage_max and new_vp > variables.pulse_voltage_min:
            self.com_port_v_p.write('VOLT %s' % new_vp)
            variables.pulse_voltage = new_vp * variables.pulse_amp_per_supply_voltage

        variables.main_temperature = np.append(variables.main_temperature, variables.temperature)
        variables.main_chamber_vacuum = np.append(variables.main_chamber_vacuum, float(variables.vacuum_main))

    def clear_up(self, task_counter):
        """
        Clear global variables and deinitializing high voltage and pulser  function
        """
        def cleanup_variables():
            """
            Clear up all the global variables
            """
            variables.stop_flag = False
            variables.end_experiment = False
            variables.start_flag = False
            variables.elapsed_time = 0.0
            variables.total_ions = 0
            variables.specimen_voltage = 0.0
            variables.detection_rate = 0.0
            variables.detection_rate_elapsed = 0.0
            variables.pulse_voltage = 0.0
            variables.total_count = 0
            variables.count = 0
            variables.count_temp = 0
            variables.count_last = 0
            variables.avg_n_count = 0
            variables.index_plot = 0
            variables.index_save_image = 0
            variables.index_wait_on_plot_start = 0
            variables.index_plot_save = 0
            variables.index_plot = 0

            variables.x = np.zeros(0)
            variables.y = np.zeros(0)
            variables.t = np.zeros(0)
            variables.dld_start_counter = np.zeros(0)

            variables.channel = np.zeros(0)
            variables.time_data = np.zeros(0)
            variables.tdc_start_counter = np.zeros(0)

            variables.main_v_dc = np.zeros(0)
            variables.main_v_p = np.zeros(0)
            variables.main_counter = np.zeros(0)
            variables.main_temperature = np.zeros(0)
            variables.main_chamber_vacuum = np.zeros(0)
            variables.main_v_dc_dld = np.zeros(0)
            variables.main_v_p_dld = np.zeros(0)
            variables.main_v_dc_tdc = np.zeros(0)
            variables.main_v_p_tdc = np.zeros(0)

        print('starting to clean up')
        # save the data to the HDF5

        # Switch off the v_dc
        self.command_v_dc('F0')
        self.com_port_v_dc.close()

        # Switch off the v_p
        self.com_port_v_p.write('VOLT 0')
        self.com_port_v_p.write('OUTPut OFF')
        self.com_port_v_p.close()

        # Interrupt the TDC
        # device.interrupt_measurement()

        if variables.counter_source == 'pulse_counter' or variables.raw_mode:
            # Close the task of counter
            task_counter.stop()
            task_counter.close()
        # Zero variables
        cleanup_variables()
        print('Clean up is finished')

def main():
    """
    Main function for doing experiments
    1- Initialize all the devices (High voltage, pulser, TDC or Edge-Counter)
    2- Create and start reader DLD and TDC thread
    3- Create and start the TDC process if TDC is selected in GUI
    4- Iterate over the main loop of experiments and control the experiment frequency
    5- Stop the experiment if stop condition is achieved
    6- Deinitialize devices
    7- Save the data
    8- Send email and tweet
    """
    # Initialize logger
    logger = logging()
    logger.info('Experiment is starting')

    variables.start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    # Create and start the TDC process and related queues
    if variables.counter_source == 'TDC':
        queue_x = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_y = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_t = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_dld_start_counter = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_channel = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_time_data = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_tdc_start_counter = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_stop_measurement = Queue(maxsize=1, ctx=multiprocessing.get_context())
        # tdc_process = multiprocessing.Process(target=tdc.experiment_measure, args=(queue_x,
        #                                                                            queue_y, queue_t,
        #                                                                            queue_dld_start_counter,
        #                                                                            queue_channel,
        #                                                                            queue_time_data,
        #                                                                            queue_tdc_start_counter,
        #                                                                            queue_stop_measurement))
        # tdc_process.daemon = True
        # tdc_process.start()
        tdc_process = multiprocessing.Process(target=tdc_new.experiment_measure, args=(variables.raw_mode, queue_x,
                                                                                       queue_y, queue_t,
                                                                                       queue_dld_start_counter,
                                                                                       queue_channel,
                                                                                       queue_time_data,
                                                                                       queue_tdc_start_counter,
                                                                                       queue_stop_measurement))
        tdc_process.daemon = True
        tdc_process.start()
    else:
        queue_x = None
        queue_y = None
        queue_t = None
        queue_dld_start_counter = None
        queue_channel = None
        queue_time_data = None
        queue_tdc_start_counter = None
        queue_stop_measurement = None

    # Lock that is used by TDC and DLD threads
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    # Create the experiment object
    experiment = OXCART(queue_x, queue_y, queue_t, queue_dld_start_counter,
                        queue_channel, queue_time_data,
                        queue_tdc_start_counter, lock1, lock2)
    # Initialize high voltage
    experiment.initialize_v_dc()
    logger.info('High voltage is initialized')
    # Initialize pulser
    experiment.initialize_v_p()
    logger.info('Pulser is initialized')

    if variables.counter_source == 'pulse_counter' or variables.raw_mode:
        task_counter = experiment.initialize_counter()
        logger.info('Edge counter is initialized')
    else:
        task_counter = None
    # start the timer for main experiment
    variables.specimen_voltage = variables.vdc_min
    variables.pulse_voltage_min = variables.v_p_min * (1 / variables.pulse_amp_per_supply_voltage)
    variables.pulse_voltage_max = variables.v_p_max * (1 / variables.pulse_amp_per_supply_voltage)
    variables.pulse_voltage = variables.v_p_min

    time_ex_s = np.zeros(0)
    time_ex_m = np.zeros(0)
    time_ex_h = np.zeros(0)
    time_counter = np.zeros(0)

    counts_target = ((variables.detection_rate / 100) * variables.pulse_frequency) / variables.pulse_frequency
    logger.info('Starting the main loop')

    if variables.counter_source == 'TDC':
        if not variables.raw_mode:
            read_dld_queue_thread = threading.Thread(target=experiment.reader_queue_dld)
            read_dld_queue_thread.setDaemon(True)
            read_dld_queue_thread.start()
        elif variables.raw_mode:
            read_tdc_queue_thread = threading.Thread(target=experiment.reader_queue_tdc)
            read_tdc_queue_thread.setDaemon(True)
            read_tdc_queue_thread.start()
    total_steps = variables.ex_time * variables.ex_freq
    steps = 0
    ex_time_temp = variables.ex_time
    # Main loop of experiment
    while steps < total_steps:
        # Only for initializing every thing at firs iteration
        if steps == 0:
            # Turn on the v_dc and v_p
            experiment.com_port_v_p.write('OUTPut ON')
            time.sleep(0.5)
            experiment.command_v_dc("F1")
            time.sleep(0.5)
            if variables.counter_source == 'pulse_counter' or variables.raw_mode:
                # start the Counter
                task_counter.start()

            variables.start_flag = True
            # Wait for 4 second to all devices get ready
            time.sleep(4)
            # Total experiment time variable
            start_main_ex = time.time()

            print('Experiment is started')
            logger.info('Experiment is started')
        # Measure time
        start = datetime.datetime.now()
        # main loop function
        experiment.main_ex_loop(task_counter, counts_target)
        end = datetime.datetime.now()
        # print('control loop takes:', ((end - start).microseconds / 1000), 'ms')
        # If the main experiment function takes less than experiment frequency we have to waite
        if (1000 / variables.ex_freq) > ((end - start).microseconds / 1000):  # time in milliseconds
            sleep_time = ((1000 / variables.ex_freq) - ((end - start).microseconds / 1000))
            time.sleep(sleep_time / 1000)
            # end2 = datetime.datetime.now()
            # print('wait for remaining cycle time', sleep_time, 'ms')
            # print('Entire control loop time:', ((end2 - start).microseconds / 1000), 'ms')
        else:
            print(
                f"{initialize_devices.bcolors.WARNING}Warning: Experiment loop takes longer than initialized frequency Seconds{initialize_devices.bcolors.ENDC}")
            logger.error('Experiment loop takes longer than initialized frequency Seconds')

        time_ex_s = np.append(time_ex_s, int(end.strftime("%S")))
        time_ex_m = np.append(time_ex_m, int(end.strftime("%M")))
        time_ex_h = np.append(time_ex_h, int(end.strftime("%H")))
        end_main_ex_loop = time.time()
        variables.elapsed_time = end_main_ex_loop - start_main_ex


        # Counter of iteration
        time_counter = np.append(time_counter, steps)
        steps += 1
        if variables.stop_flag:
            print('Experiment is stopped by user')
            logger.info('Experiment is stopped by user')
            if variables.counter_source == 'TDC':
                queue_stop_measurement.put(True)
            time.sleep(1)
            break
        if variables.max_ions <= variables.total_ions:
            print('Total number of Ions is achieved')
            logger.info('Total number of Ions is achieved')
            if variables.counter_source == 'TDC':
                queue_stop_measurement.put(True)
            time.sleep(1)
            break
        if variables.ex_time != ex_time_temp:
            total_steps = variables.ex_time * variables.ex_freq - steps
            ex_time_temp = variables.ex_time
    # Stop the TDC process
    try:
        if variables.counter_source == 'TDC':
            tdc_process.join(3)
            if tdc_process.is_alive():
                tdc_process.terminate()
                tdc_process.join(1)
                # Release all the resources of the TDC process
                tdc_process.close()
    except:
        print(
            f"{initialize_devices.bcolors.WARNING}Warning: The TDC process cannot be terminated properly{initialize_devices.bcolors.ENDC}")

    variables.end_experiment = True
    time.sleep(1)
    # Stop the TDC and DLD thread
    if variables.counter_source == 'TDC':
        if not variables.raw_mode:
            read_dld_queue_thread.join(1)
        elif variables.raw_mode:
            read_tdc_queue_thread.join(1)

    if variables.counter_source == 'TDC':
        variables.total_ions = len(variables.x)

    time.sleep(1)
    print('Experiment is finished')
    logger.info('Experiment is finished')

    # Check the length of arrays to be equal
    if variables.counter_source == 'TDC':
        if all(len(lst) == len(variables.x) for lst in [variables.x, variables.y,
                                                    variables.t, variables.dld_start_counter,
                                                    variables.main_v_dc_dld, variables.main_v_dc_dld]):
            logger.warning('dld data have not same length')

        if all(len(lst) == len(variables.channel) for lst in [variables.channel, variables.time_data,
                                                          variables.tdc_start_counter,
                                                          variables.main_v_dc_tdc, variables.main_v_p_tdc]):
            logger.warning('tdc data have not same length')

    # save hdf5 file
    with h5py.File(variables.path + '\\%s_data.h5' % variables.hdf5_path, "w") as f:
        f.create_dataset("oxcart/high_voltage", data=variables.main_v_dc, dtype='f')
        f.create_dataset("oxcart/pulse_voltage", data=variables.main_v_p, dtype='f')
        f.create_dataset("oxcart/num_events", data=variables.main_counter, dtype='i')
        f.create_dataset('oxcart/temperature', data=variables.main_temperature, dtype='f')
        f.create_dataset('oxcart/main_chamber_vacuum', data=variables.main_chamber_vacuum, dtype='f')
        f.create_dataset("oxcart/time_counter", data=time_counter, dtype='i')

        f.create_dataset("time/time_s", data=time_ex_s, dtype='i')
        f.create_dataset("time/time_m", data=time_ex_m, dtype='i')
        f.create_dataset("time/time_h", data=time_ex_h, dtype='i')

        f.create_dataset("dld/x", data=variables.x, dtype='i')
        f.create_dataset("dld/y", data=variables.y, dtype='i')
        f.create_dataset("dld/t", data=variables.t, dtype='i')
        f.create_dataset("dld/start_counter", data=variables.dld_start_counter, dtype='i')
        f.create_dataset("dld/high_voltage", data=variables.main_v_dc_dld, dtype='f')
        f.create_dataset("dld/pulse_voltage", data=variables.main_v_dc_dld, dtype='f')

        f.create_dataset("tdc/channel", data=variables.channel, dtype='i')
        f.create_dataset("tdc/time_data", data=variables.time_data, dtype='i')
        f.create_dataset("tdc/start_counter", data=variables.tdc_start_counter, dtype='i')
        f.create_dataset("tdc/high_voltage", data=variables.main_v_dc_tdc, dtype='f')
        f.create_dataset("tdc/pulse_voltage", data=variables.main_v_p_tdc, dtype='f')

    logger.info('HDF5 file is created')
    variables.end_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    # Save new value of experiment counter
    with open('./png/counter.txt', 'w') as f:
        f.write(str(variables.counter + 1))
        logger.info('Experiment counter is increased')

    # Adding results of the experiment to the log file
    logger.info('Total number of Ions is: %s' % variables.total_ions)
    # send a Tweet
    if variables.tweet:
        message_tweet = 'The Experiment %s finished\n' \
                        'Total number of Ions is: %s' % (variables.hdf5_path,
                                                         variables.total_ions)
        tweet_send.tweet_send(message_tweet)
        logger.info('Tweet is sent')

    # send an email
    subject = 'Oxcart Experiment {} Report'.format(variables.hdf5_path)
    elapsed_time_temp = float("{:.3f}".format(variables.elapsed_time))
    message = 'The experiment was started at: {}\n' \
              'The experiment was ended at: {}\n' \
              'Experiment duration: {}\n' \
              'Total number of ions: {}\n'.format(variables.start_time,
                                                  variables.end_time, elapsed_time_temp, variables.total_ions)

    if len(variables.email) > 3:
        logger.info('Email is sent')
        email_send.send_email(variables.email, subject, message)

    # save setup parameters and run statistics in a txt file
    with open(variables.path + '\\parameters.txt', 'w') as f:
        f.write('Experiment Name: ' + variables.hdf5_path + '\r\n')
        f.write('Detection Rate  (%): %s\r\n' % (variables.detection_rate))
        f.write('Maximum Number of Ions: %s\r\n' % variables.max_ions)
        f.write('Control Refresh freq. (Hz): %s\r\n' % variables.ex_freq)
        f.write('Time bins (Sec): %s\r\n' % (1/variables.ex_freq))
        f.write('Cycle for Avg.: %s\r\n' % variables.cycle_avg)
        f.write('K_p Upwards: %s\r\n' % variables.vdc_step_up)
        f.write('K_p Downwards: %s\r\n' % variables.vdc_step_down)
        f.write('Experiment Elapsed Time (Sec): %s\r\n' % "{:.3f}".format(variables.elapsed_time))
        f.write('Experiment Total Ions: %s\r\n' % variables.total_ions)
        f.write('Email: ' + variables.email + '\r\n')
        f.write('Twitter: %s\r\n' % variables.tweet)
        f.write('Specimen start Voltage (V): %s\r\n' % variables.vdc_min)
        f.write('Specimen Stop Voltage (V): %s\r\n' % variables.vdc_max)
        f.write('Specimen Max Achieved Voltage (V): %s\r\n' % "{:.3f}".format(variables.specimen_voltage))
        f.write('Pulse start Voltage (V): %s\r\n' % variables.v_p_min)
        f.write('Pulse Stop Voltage (V): %s\r\n' % variables.v_p_max)
        f.write('Specimen Max Achieved Pulse Voltage (V): %s\r\n' % "{:.3f}".format(variables.pulse_voltage))

    # Clear up all the variables and deinitialize devices
    experiment.clear_up(task_counter)
    logger.info('Variables and devices is cleared')
