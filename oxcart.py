# OXCART

# Python Script for doing an experiments
com_port_idx_V_dc = 4
com_port_idx_V_p = 0

# package needed
import time
import datetime
import h5py
import multiprocessing
from multiprocessing.queues import Queue
import threading
import numpy as np

# package needed to list available COM ports
import serial.tools.list_ports
import pyvisa as visa
import nidaqmx
import scTDC

import tdc
import variables
import email_send
import tweet_send

# get available COM ports and store as list
com_ports = list(serial.tools.list_ports.comports())


def logging():
    # Gets or creates a logger
    import logging
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


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class OXCART:

    def __init__(self, queue_x, queue_y, queue_t, queue_dld_start_counter,
                 queue_channel, queue_time_data, queue_tdc_start_counter, lock1, lock2):
        self.queue_x = queue_x
        self.queue_y = queue_y
        self.queue_t = queue_t
        self.queue_dld_start_counter = queue_dld_start_counter
        self.queue_channel = queue_channel
        self.queue_time_data = queue_time_data
        self.queue_tdc_start_counter = queue_tdc_start_counter
        self.lock1 = lock1
        self.lock2 = lock2

    # Initialize the V_dc for the experiment
    def initialize_v_dc(self):

        # Setting the com port of V_dc
        self.com_port_v_dc = serial.Serial(
            port=com_ports[com_port_idx_V_dc].device,  # chosen COM port
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

        # set the port for v_p
        resources = visa.ResourceManager('@py')
        self.com_port_v_p = resources.open_resource('ASRL4::INSTR')

        try:
            self.com_port_v_p.query('*RST')
        except:

            self.com_port_v_p.write('VOLT %s' % (variables.v_p_min * (1 / variables.pulse_amp_per_supply_voltage)))

    def initialize_counter(self):
        task_counter = nidaqmx.Task()
        task_counter.ci_channels.add_ci_count_edges_chan("Dev1/ctr0")
        # reference the terminal you want to use for the counter here
        task_counter.ci_channels[0].ci_count_edges_term = "PFI0"

        return task_counter

    # apply command to the V_dc
    def command_v_dc(self, cmd):
        self.com_port_v_dc.write(
            (cmd + '\r\n').encode())  # send cmd to device # might not work with older devices -> "LF" only needed!
        time.sleep(0.005)  # small sleep for response
        response = ''
        while self.com_port_v_dc.in_waiting > 0:
            response = self.com_port_v_dc.readline()  # all characters received, read line till '\r\n'
        return response.decode("utf-8")

    def clear_up(self, task_counter):
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

        if variables.counter_source == 'pulse_counter':
            # Close the task of counter
            task_counter.stop()
            task_counter.close()
        # Zero variables
        self.cleanup_variables()
        print('Clean up is finished')

    def reader_queue_dld(self):
        while True:
            while not self.queue_x.empty() or not self.queue_y.empty() or not self.queue_t.empty() or not self.queue_dld_start_counter.empty():
                with self.lock1:
                    variables.x = np.append(variables.x, self.queue_x.get())
                    variables.y = np.append(variables.y, self.queue_y.get())
                    variables.t = np.append(variables.t, self.queue_t.get())
                    variables.dld_start_counter = np.append(variables.dld_start_counter,
                                                            self.queue_dld_start_counter.get())
                    variables.main_v_dc_dld = np.append(variables.main_v_dc_dld, variables.specimen_voltage)
                    variables.main_v_p_dld = np.append(variables.main_v_p_dld, variables.pulse_voltage)
            if variables.end_experiment:
                break

    def reader_queue_tdc(self):
        while True:
            while not self.queue_channel.empty() or not self.queue_time_data.empty() or not self.queue_tdc_start_counter.empty():
                with self.lock2:
                    variables.channel = np.append(variables.channel, self.queue_channel.get())
                    variables.time_data = np.append(variables.time_data, self.queue_time_data.get())
                    variables.tdc_start_counter = np.append(variables.tdc_start_counter,
                                                            self.queue_tdc_start_counter.get())
                    variables.main_v_dc_tdc = np.append(variables.main_v_dc_tdc, variables.specimen_voltage)
                    variables.main_v_p_tdc = np.append(variables.main_v_p_tdc, variables.pulse_voltage)
            if variables.end_experiment:
                break

    def main_ex_loop(self, task_counter, counts_target):
        # # reading DC HV
        # v_dc = (command_v_dc(">S0A?")[5:-1])
        # variables.specimen_voltage = float(v_dc)
        #
        # # reading pulser power supply voltage
        # v_p = com_port_v_p.query('MEASure:VOLTage?')[:-3]
        # variables.pulse_voltage = float(v_p)

        if variables.counter_source == 'TDC':
            variables.total_ions = len(variables.x)

        elif variables.counter_source == 'pulse_counter':
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

    def cleanup_variables(self):
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


def main():
    # Initialize logger
    logger = logging()
    logger.info('Experiment is starting')

    variables.start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    # Wait for 3 second before starting the experiment
    if variables.counter_source == 'TDC':
        queue_x = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_y = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_t = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_dld_start_counter = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_channel = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_time_data = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_tdc_start_counter = Queue(maxsize=-1, ctx=multiprocessing.get_context())
        queue_start_measurement = Queue(maxsize=1, ctx=multiprocessing.get_context())
        queue_stop_measurement = Queue(maxsize=1, ctx=multiprocessing.get_context())
        tdc_process = multiprocessing.Process(target=tdc.experiment_measure, args=(queue_x,
                                                                                   queue_y, queue_t,
                                                                                   queue_dld_start_counter,
                                                                                   queue_channel,
                                                                                   queue_time_data,
                                                                                   queue_tdc_start_counter,
                                                                                   queue_start_measurement,
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
        queue_start_measurement = None
        queue_stop_measurement = None

    # Initialization of devices
    lock1 = threading.Lock()
    lock2 = threading.Lock()
    experiment = OXCART(queue_x, queue_y, queue_t, queue_dld_start_counter,
                        queue_channel, queue_time_data,
                        queue_tdc_start_counter, lock1, lock2)
    experiment.initialize_v_dc()
    logger.info('High voltage is initialized')

    experiment.initialize_v_p()
    logger.info('Pulser is initialized')

    if variables.counter_source == 'pulse_counter':
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
        read_dld_queue_thread = threading.Thread(target=experiment.reader_queue_dld)
        read_dld_queue_thread.setDaemon(True)
        read_dld_queue_thread.start()
        read_tdc_queue_thread = threading.Thread(target=experiment.reader_queue_tdc)
        read_tdc_queue_thread.setDaemon(True)
        read_tdc_queue_thread.start()
    total_steps = variables.ex_time * variables.ex_freq
    steps = 0
    while steps < total_steps:
        if steps == 0:
            # Turn on the v_dc and v_p
            experiment.com_port_v_p.write('OUTPut ON')
            time.sleep(0.5)
            experiment.command_v_dc("F1")
            time.sleep(0.5)
            if variables.counter_source == 'pulse_counter':
                # start the Counter
                task_counter.start()

            variables.start_flag = True
            time.sleep(8)
            if variables.counter_source == 'TDC':
                queue_start_measurement.put(True)
            # Total experiment time variable
            start_main_ex = time.time()

            print('Experiment is started')
            logger.info('Experiment is started')
        # main loop
        start = datetime.datetime.now()

        experiment.main_ex_loop(task_counter, counts_target)
        end = datetime.datetime.now()
        # print('control loop takes:', ((end - start).microseconds / 1000), 'ms')
        if (1000 / variables.ex_freq) > ((end - start).microseconds / 1000):  # time in milliseconds
            sleep_time = ((1000 / variables.ex_freq) - ((end - start).microseconds / 1000))
            time.sleep(sleep_time / 1000)
            # end2 = datetime.datetime.now()
            # print('wait for remaining cycle time', sleep_time, 'ms')
            # print('Entire control loop time:', ((end2 - start).microseconds / 1000), 'ms')
        else:
            print(
                f"{bcolors.WARNING}Warning: Experiment loop takes longer than initialized frequency Seconds{bcolors.ENDC}")
            logger.error('Experiment loop takes longer than initialized frequency Seconds')
            # break

        time_ex_s = np.append(time_ex_s, int(end.strftime("%S")))
        time_ex_m = np.append(time_ex_m, int(end.strftime("%M")))
        time_ex_h = np.append(time_ex_h, int(end.strftime("%H")))
        end_main_ex_loop = time.time()
        variables.elapsed_time = end_main_ex_loop - start_main_ex

        total_steps = variables.ex_time * variables.ex_freq
        time_counter = np.append(time_counter, steps)
        steps += 1
        if variables.stop_flag:
            print('Experiment is stopped by user')
            logger.info('Experiment is stopped by user')
            queue_stop_measurement.put(True)
            time.sleep(1)
            break
        if variables.max_ions <= variables.total_ions:
            print('Total number of Ions is achieved')
            logger.info('Total number of Ions is achieved')
            queue_stop_measurement.put(True)
            time.sleep(1)
            break

    if variables.counter_source == 'TDC':
        tdc_process.join(3)
        if tdc_process.is_alive():
            tdc_process.terminate()
            tdc_process.join(1)
            # Release all the resources of the TDC process
            tdc_process.close()

    variables.end_experiment = True
    time.sleep(1)
    if variables.counter_source == 'TDC':
        read_dld_queue_thread.join(1)
        read_tdc_queue_thread.join(1)

    variables.total_ions = len(variables.x)
    time.sleep(1)
    print('Experiment is finished')
    logger.info('Experiment is finished')

    # save hdf5 file
    if all(len(lst) == len(variables.x) for lst in [variables.x, variables.y,
                                                    variables.t, variables.dld_start_counter,
                                                    variables.main_v_dc_dld, variables.main_v_dc_dld]):
        logger.warning('dld data have not same length')
    else:
        pass

    if all(len(lst) == len(variables.channel) for lst in [variables.channel, variables.time_data,
                                                          variables.tdc_start_counter,
                                                          variables.main_v_dc_tdc, variables.main_v_p_tdc]):
        logger.warning('tdc data have not same length')

    else:
        pass
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

    # save new value of experiment counter
    with open('./png/counter.txt', 'w') as f:
        f.write(str(variables.counter + 1))
        logger.info('Experiment counter is increased')

    # Adding results of the experiment to the log file
    logger.info('Total number of Ions is: %s' % variables.total_ions)
    # send a Tweet
    message_tweet = 'The Experiment %s finished\n' \
                    'Total number of Ions is: %s' % (variables.hdf5_path,
                                                     variables.total_ions)
    if variables.tweet == True:
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
        f.write('Detection Rate: %s\r\n' % (variables.detection_rate))
        f.write('Maximum Number of Ions: %s\r\n' % variables.max_ions)
        f.write('Control Refresh freq.: %s\r\n' % variables.ex_freq)
        f.write('Cycle for Avg.: %s\r\n' % variables.cycle_avg)
        f.write('K_p Upwards: %s\r\n' % variables.vdc_step_up)
        f.write('K_p Downwards: %s\r\n' % variables.vdc_step_down)
        f.write('Experiment Elapsed Time: %s\r\n' % "{:.3f}".format(variables.elapsed_time))
        f.write('Experiment Total Ions: %s\r\n' % variables.total_ions)
        f.write('Email: ' + variables.email + '\r\n')
        f.write('Twitter: %s\r\n' % variables.tweet)
        f.write('Specimen start Voltage: %s\r\n' % variables.vdc_min)
        f.write('Specimen Stop Voltage: %s\r\n' % variables.vdc_max)
        f.write('Specimen Max Achieved Voltage: %s\r\n' % "{:.3f}".format(variables.specimen_voltage))
        f.write('Pulse start Voltage: %s\r\n' % variables.v_p_min)
        f.write('Pulse Stop Voltage: %s\r\n' % variables.v_p_max)
        f.write('Specimen Max Achieved Pulse Voltage: %s\r\n' % "{:.3f}".format(variables.pulse_voltage))

    experiment.clear_up(task_counter)
    logger.info('Variables and devices is cleared')
