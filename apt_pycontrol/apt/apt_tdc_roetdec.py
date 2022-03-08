"""
This is the main script for doing experiment.
It contains the main control loop of experiment.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""

import time
import datetime
import multiprocessing
from multiprocessing.queues import Queue
import threading
import numpy as np

# Serial ports and NI
import serial.tools.list_ports
# Local project scripts
from apt_pycontrol.tdc_roentdec import tdc
from apt_pycontrol.devices import email_send, initialize_devices
from apt_pycontrol.tools import hdf5_creator, experiment_statistics, variables
from apt_pycontrol.tools import loggi


class APT_LASER:
    """
    apt_simple class

    """

    def __init__(self, queue_x, queue_y, queue_tof, queue_time_stamp, lock1):
        """
        This is the constructor class that accepts several initialized queues objects corresponding
        to various parameters of the groups like dld,TDC,DRS. This constructor also objects used for
        creating locks on resources to reduce concurrent access on resources and reduce dirty read.
        """
        # Queues for sharing data between tdc and main process
        # dld queues
        self.com_port_v_dc = None
        self.queue_x = queue_x
        self.queue_y = queue_y
        self.queue_tof = queue_tof
        self.queue_time_stamp = queue_time_stamp
        self.lock1 = lock1

    def initialize_v_dc(self):
        """
        This class method initializes the high voltage parameter: v_dc.
        The function utilizes the serial library to communicate over the
        COM port serially and read the corresponding v_dc parameter.

        It exits if it is not able to connect on the COM Port.

        Attributes:
            Accepts only the self (class object)

        Returns:
            Does not return anything
        """
        # Setting the com port of V_dc
        self.com_port_v_dc = serial.Serial(
            port=initialize_devices.com_ports[variables.COM_PORT_idx_V_dc].device,  # chosen COM port
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

    # apply command to the V_dc
    def command_v_dc(self, cmd):
        """
        This class method is used to send commands on the high voltage parameter: v_dc.
        The function utilizes the serial library to communicate over the
        COM port serially and read the corresponding v_dc parameter.

        Attributes:
            Accepts only the self (class object)

        Returns:
            Returns the response code after executing the command.
        """
        self.com_port_v_dc.write(
            (cmd + '\r\n').encode())  # send cmd to device # might not work with older devices -> "LF" only needed!
        time.sleep(0.005)  # small sleep for response
        # Intialize the response to returned as string
        response = ''
        # Read the response code after execution(command write).
        while self.com_port_v_dc.in_waiting > 0:
            response = self.com_port_v_dc.readline()  # all characters received, read line till '\r\n'
        return response.decode("utf-8")

    def reader_queue_dld(self):
        """
        This class method runs in an infinite loop and listens and reads parameters
        over the queues for the group: dld

        This function is called continuously by a separate thread in the main function.

        The values read from the queues are updates in imported "variables" file

        Attributes:
            Accepts only the self (class object)

        Returns:
            Does not return anything
        """
        while True:
            # Check if any value is present in queue to read from
            while not self.queue_x.empty() or not self.queue_y.empty() or not self.queue_tof.empty() or not self.queue_time_stamp.empty():
                # Utilize locking mechanism to avoid concurrent use of resources and dirty reads
                with self.lock1:
                    length = self.queue_x.get()
                    variables.x = np.append(variables.x, length)
                    variables.y = np.append(variables.y, self.queue_y.get())
                    variables.t = np.append(variables.t, self.queue_tof.get())
                    variables.time_stamp = np.append(variables.time_stamp,
                                                     self.queue_time_stamp.get())
                    variables.main_v_dc_dld = np.append(variables.main_v_dc_dld,
                                                        np.tile(variables.specimen_voltage, len(length)))
            # If end of experiment flag is set break the while loop
            if variables.end_experiment:
                break

    def main_ex_loop(self, counts_target):

        """
        This class method:

        1. Read the number of detected Ions(in TDC or Counter mode)
        2- Calculate the error of detection rate of desire rate
        3- Regulate the high voltage and pulser

        This function is called in each loop of main function.

        Attributes:
            counts_target: Calculated parameter(((detection_rate/100)* pulse_frequency)/pulse_frequency)

        Returns:
            Does not return anything

        """

        if variables.counter_source == 'TDC':
            variables.total_ions = len(variables.x)

        variables.count_temp = variables.total_ions - variables.count_last
        variables.count_last = variables.total_ions

        # saving the values of high dc voltage, pulse, and current iteration ions
        variables.main_v_dc = np.append(variables.main_v_dc, variables.specimen_voltage)
        variables.main_counter = np.append(variables.main_counter, variables.count_temp)
        # averaging count rate of N_averg counts
        variables.avg_n_count = variables.ex_freq * (
                sum(variables.main_counter[-variables.cycle_avg:]) / variables.cycle_avg)

        counts_measured = variables.avg_n_count / (1 + variables.pulse_frequency * 1000)

        counts_error = counts_target - counts_measured  # deviation from setpoint

        # simple proportional control with averaging
        rate = ((variables.avg_n_count * 100) / (1 + variables.pulse_frequency * 1000))
        if rate < 0.01 and variables.specimen_voltage < 5000:
            ramp_speed_factor = 2.5
        else:
            ramp_speed_factor = 1
        if counts_error > 0:
            voltage_step = counts_error * variables.vdc_step_up * ramp_speed_factor
        elif counts_error <= 0:
            voltage_step = counts_error * variables.vdc_step_down * ramp_speed_factor

        # update v_dc
        if variables.specimen_voltage < variables.vdc_max:
            if variables.specimen_voltage >= variables.vdc_min:
                specimen_voltage_temp = variables.specimen_voltage + voltage_step
                if specimen_voltage_temp > variables.specimen_voltage:
                    # sending VDC via serial
                    self.command_v_dc(">S0 %s" % (specimen_voltage_temp))
                    variables.specimen_voltage = specimen_voltage_temp

    def clear_up(self, ):
        """
        This function clears global variables and deinitialize high voltage and pulser function

        Attributes:
            Does not accept any arguments
        Returns:
            Does not return anything

        """

        def cleanup_variables():
            """
            Clear up all the global variables
            """
            variables.stop_flag = False
            variables.end_experiment = False
            variables.start_flag = False
            variables.detection_rate = 0.0
            variables.detection_rate_elapsed = 0.0
            variables.count = 0
            variables.count_temp = 0
            variables.count_last = 0
            variables.index_plot = 0
            variables.index_wait_on_plot_start = 0
            variables.index_plot_save = 0
            variables.index_plot = 0

            variables.x = np.zeros(0)
            variables.y = np.zeros(0)
            variables.t = np.zeros(0)
            variables.dld_start_counter = np.zeros(0)

            #
            variables.main_v_dc = np.zeros(0)
            variables.main_counter = np.zeros(0)
            variables.main_v_dc_dld = np.zeros(0)
            variables.main_v_dc_tdc = np.zeros(0)

        print('starting to clean up')
        # save the data to the HDF5

        # Switch off the v_dc
        self.command_v_dc('F0')
        self.com_port_v_dc.close()

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
    logger = loggi.get_logging()
    logger.info('Experiment is starting')

    variables.start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    # Create and start the TDC process and related queues
    if variables.counter_source == 'TDC' or variables.counter_source == 'TDC_Raw':
        queue_x = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_y = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_tof = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_time_stamp = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_stop_measurement = Queue(maxsize=1, ctx=multiprocessing.get_context())

        tdc_process = multiprocessing.Process(target=tdc.experiment_measure, args=(queue_x,
                                                                                   queue_y, queue_tof,
                                                                                   queue_time_stamp,
                                                                                   queue_stop_measurement))

        tdc_process.daemon = True
        tdc_process.start()

    # Initialize lock that is used by TDC and DLD threads
    # Module used: threading
    lock1 = threading.Lock()

    # Create the experiment object
    experiment = APT_LASER(queue_x, queue_y, queue_tof, queue_time_stamp,
                            lock1)

    # Initialize high voltage
    experiment.initialize_v_dc()
    logger.info('High voltage is initialized')

    # start the timer for main experiment
    time_ex_s = np.zeros(0)
    time_ex_m = np.zeros(0)
    time_ex_h = np.zeros(0)
    time_counter = np.zeros(0)

    counts_target = ((variables.detection_rate / 100) * variables.pulse_frequency) / variables.pulse_frequency
    logger.info('Starting the main loop')

    # Initialze threads that will read from the queue for the group: dld
    if variables.counter_source == 'TDC':
        read_dld_queue_thread = threading.Thread(target=experiment.reader_queue_dld)
        read_dld_queue_thread.setDaemon(True)
        read_dld_queue_thread.start()

    total_steps = variables.ex_time * variables.ex_freq
    steps = 0
    flag_achieved_high_voltage = 0
    index_time = 0
    ex_time_temp = variables.ex_time

    # Main loop of experiment
    while steps < total_steps:
        # Only for initializing every thing at firs iteration
        if steps == 0:
            # Turn on the v_dc and
            experiment.command_v_dc("F1")
            time.sleep(0.5)

            variables.start_flag = True
            # Wait for 4 second to all devices get ready
            time.sleep(4)
            # Total experiment time variable
            start_main_ex = time.time()
            logger.info('Experiment is started')
            # set the start specimen_voltage
            variables.specimen_voltage = variables.vdc_min
        # Measure time
        start = datetime.datetime.now()
        # main loop function
        experiment.main_ex_loop(counts_target)
        end = datetime.datetime.now()
        # If the main experiment function takes less than experiment frequency we have to waite
        if (1000 / variables.ex_freq) > ((end - start).microseconds / 1000):  # time in milliseconds
            sleep_time = ((1000 / variables.ex_freq) - ((end - start).microseconds / 1000))
            time.sleep(sleep_time / 1000)
        else:
            print(
                f"{initialize_devices.bcolors.WARNING}Warning: Experiment loop takes longer than %s Millisecond{initialize_devices.bcolors.ENDC}" % (
                    int(1000 / variables.ex_freq)))
            logger.error('Experiment loop takes longer than %s Millisecond' % (int(1000 / variables.ex_freq)))
            print('%s- The iteration time:' % index_time, ((end - start).microseconds / 1000))
            index_time += 1
        time_ex_s = np.append(time_ex_s, int(end.strftime("%S")))
        time_ex_m = np.append(time_ex_m, int(end.strftime("%M")))
        time_ex_h = np.append(time_ex_h, int(end.strftime("%H")))
        end_main_ex_loop = time.time()
        variables.elapsed_time = end_main_ex_loop - start_main_ex

        # Counter of iteration
        time_counter = np.append(time_counter, steps)
        steps += 1
        if variables.stop_flag:
            logger.info('Experiment is stopped by user')
            # if variables.counter_source == 'TDC' or variables.counter_source == 'TDC_Raw':
            if variables.counter_source == 'TDC':
                queue_stop_measurement.put(True)
            time.sleep(1)
            break

        if variables.criteria_ions:
            if variables.max_ions <= variables.total_ions:
                logger.info('Total number of Ions is achieved')
                if variables.counter_source == 'TDC' or variables.counter_source == 'TDC_Raw':
                    queue_stop_measurement.put(True)
                time.sleep(1)
                break
        if variables.criteria_vdc:
            if variables.vdc_max <= variables.specimen_voltage:
                if flag_achieved_high_voltage > variables.ex_freq * 10:
                    logger.info('High Voltage Max. is achieved')
                    time.sleep(1)
                    break
                flag_achieved_high_voltage += 1
        if variables.ex_time != ex_time_temp:
            total_steps = variables.ex_time * variables.ex_freq - steps
            ex_time_temp = variables.ex_time
        # Because experiment time is not a stop criteria, increase total_steps
        if not variables.criteria_time and steps + 1 == total_steps:
            total_steps += 1
    # Stop the TDC process
    try:
        # if variables.counter_source == 'TDC'or variables.counter_source == 'TDC_Raw':
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
        read_dld_queue_thread.join(1)

    if variables.counter_source == 'TDC':
        variables.total_ions = len(variables.x)

    time.sleep(1)
    logger.info('Experiment is finished')

    # Check the length of arrays to be equal
    if variables.counter_source == 'TDC':
        if all(len(lst) == len(variables.x) for lst in [variables.x, variables.y,
                                                        variables.t, variables.dld_start_counter,
                                                        variables.main_v_dc_dld]):
            logger.warning('dld data have not same length')

    # save data in hdf5 file
    hdf5_creator.hdf_creator_physic(time_counter, time_ex_s, time_ex_m, time_ex_h)

    logger.info('HDF5 file is created')
    variables.end_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    # Save new value of experiment counter
    with open('./files/counter_physic.txt', 'w') as f:
        f.write(str(variables.counter + 1))
        logger.info('Experiment counter is increased')

    # Adding results of the experiment to the log file
    logger.info('Total number of Ions is: %s' % variables.total_ions)

    # send an email
    subject = 'apt_simple Experiment {} Report'.format(variables.hdf5_path)
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
    experiment_statistics.save_statistics_apt_physic()

    # Clear up all the variables and deinitialize devices
    experiment.clear_up()
    logger.info('Variables and devices is cleared')
