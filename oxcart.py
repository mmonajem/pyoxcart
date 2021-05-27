# OXCART

# Python Script for doing an experiments
com_port_idx_V_dc = 4
com_port_idx_V_p = 0


# package needed to list available COM ports
import serial.tools.list_ports
import pyvisa as visa
import nidaqmx
import scTDC
import variables
import email_send
import tweet_send
import multiprocessing


# package needed
import time
import datetime
import h5py
import os
import threading
import numpy as np
import sys

manager_x = multiprocessing.Manager()
manager_y = multiprocessing.Manager()
manager_t = multiprocessing.Manager()
manager_start_counter = multiprocessing.Manager()
variables.x = manager_x.list()
variables.y = manager_y.list()
variables.t = manager_t.list()
variables.start_counter = manager_start_counter.list()

# get available COM ports and store as list
com_ports = list(serial.tools.list_ports.comports())
# Setting the com port of V_dc
com_port_v_dc = serial.Serial(
    port=com_ports[com_port_idx_V_dc].device,  # chosen COM port
    baudrate=115200,  # 115200
    bytesize=serial.EIGHTBITS,  # 8
    parity=serial.PARITY_NONE,  # N
    stopbits=serial.STOPBITS_ONE  # 1
)

# set the port for v_p
resources = visa.ResourceManager('@py')
com_port_v_p = resources.open_resource('ASRL4::INSTR')

class UCB2(scTDC.usercallbacks_pipe):
    def __init__(self, lib, dev_desc):
        super().__init__(lib, dev_desc)  # <-- mandatory
        self.x = []
        self.y = []
        self.t = []
        self.start_counter = []

    def on_millisecond(self):
        pass  # do nothing (one could also skip this function definition altogether)

    def on_start_of_meas(self):
        pass  # do nothing

    def on_end_of_meas(self):
        variables.x = self.x
        variables.y = self.y
        variables.t = self.t
        variables.start_counter = self.start_counter

    def on_tdc_event(self, tdc_events, nr_tdc_events):
        pass
        # for i in range(nr_tdc_events):  # iterate through tdc_events
        #     # see class tdc_event_t in scTDC.py for all accessible fields
        #     t = tdc_events[i].time_data

    def on_dld_event(self, dld_events, nr_dld_events):
        for i in range(nr_dld_events):  # iterate through dld_events
            # see class dld_event_t in scTDC.py for all accessible fields
            self.t.append(dld_events[i].sum)
            self.x.append(dld_events[i].dif1)
            self.y.append(dld_events[i].dif2)
            self.start_counter.append(dld_events[i].start_counter)


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



# Initialize the V_dc for the experiment
def initialize_v_dc():
    # configure the COM port to talk to. Default values: 115200,8,N,1
    if com_port_v_dc.is_open:
        com_port_v_dc.flushInput()
        com_port_v_dc.flushOutput()

        cmd_list = [">S1 3.0e-4", ">S0B 0", ">S0 %s" % variables.vdc_min, "F0", ">S0?", ">DON?",
                    ">S0A?"]
        for cmd in range(len(cmd_list)):
            command_v_dc(cmd_list[cmd])
    else:
        print("Couldn't open Port!")
        exit()


def initialize_v_p():
    try:
        com_port_v_p.query('*RST')
    except:

        com_port_v_p.write('VOLT %s' % (variables.v_p_min * (1 / variables.pulse_amp_per_supply_voltage)))


def initialize_tdc():
    device = scTDC.Device(autoinit=False)
    retcode, errmsg = device.initialize()
    if retcode < 0:
        print("Error during initialization : ({}) {}".format(errmsg, retcode))
        return 0

    return device


def initialize_counter():
    task_counter = nidaqmx.Task()
    task_counter.ci_channels.add_ci_count_edges_chan("Dev1/ctr0")
    # reference the terminal you want to use for the counter here
    task_counter.ci_channels[0].ci_count_edges_term = "PFI0"

    return task_counter


# apply command to the V_dc
def command_v_dc(cmd):
    com_port_v_dc.write(
        (cmd + '\r\n').encode())  # send cmd to device # might not work with older devices -> "LF" only needed!
    time.sleep(0.005)  # small sleep for response
    response = ''
    while com_port_v_dc.in_waiting > 0:
        response = com_port_v_dc.readline()  # all characters received, read line till '\r\n'
    return response.decode("utf-8")


def clear_up(task_counter, device_tdc):
    print('starting to clean up')
    # save the data to the HDF5

    # Switch off the v_dc
    command_v_dc('F0')
    # com_port_v_dc.close()

    # Switch off the v_p
    com_port_v_p.write('VOLT 0')
    com_port_v_p.write('OUTPut OFF')
    # com_port_v_p.close()

    # Interrupt the TDC
    # device.interrupt_measurement()

    # Close the task of counter
    task_counter.stop()
    task_counter.close()
    # Zero variables
    cleanup_variables()

    if variables.counter_source == 'TDC':
        device_tdc.deinitialize()
    print('Clean up is finished')


def main_ex_loop(ucb, task_counter, main_v_dc, main_v_p, main_counter, counts_target,
                 temperature, main_chamber_vacuum):
    # # reading DC HV
    # v_dc = (command_v_dc(">S0A?")[5:-1])
    # variables.specimen_voltage = float(v_dc)
    #
    # # reading pulser power supply voltage
    # v_p = com_port_v_p.query('MEASure:VOLTage?')[:-3]
    # variables.pulse_voltage = float(v_p)

    # Start the measurement of TDC
    if variables.counter_source == 'TDC':
        ucb.do_measurement(int(1000/variables.ex_freq)) # Time of measurement in ms
    if variables.counter_source == 'TDC':
        variables.total_ions = len(variables.x)
    elif variables.counter_source == 'pulse_counter':
        # reading detector MCP pulse counter and calculating pulses since last loop iteration
        variables.total_ions = task_counter.read(number_of_samples_per_channel=1)[0]

    variables.count_temp = variables.total_ions - variables.count_last
    variables.count_last = variables.total_ions

    # saving the values of high dc voltage, pulse, and current iteration ions
    main_v_dc.append(variables.specimen_voltage)
    main_v_p.append(variables.pulse_voltage)
    main_counter.append(variables.count_temp)
    # averaging count rate of N_averg counts
    variables.avg_n_count = variables.ex_freq * (sum(main_counter[-variables.cycle_avg:]) / variables.cycle_avg)

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
        command_v_dc(">S0 %s" % (variables.specimen_voltage))

    # update pulse voltage v_p
    new_vp = variables.specimen_voltage * variables.pulse_fraction * \
             (1 / variables.pulse_amp_per_supply_voltage)
    variables.pulse_voltage = new_vp * variables.pulse_amp_per_supply_voltage

    if new_vp < variables.pulse_voltage_max or new_vp > variables.pulse_voltage_min:
        com_port_v_p.write('VOLT %s' % new_vp)

    temperature.append(variables.temperature)
    main_chamber_vacuum.append(float(variables.vacuum_main))


def cleanup_variables():
    variables.stop_flag = False
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
    variables.avg_n_count = 0
    variables.index_plot = 0
    variables.index_save_image = 0


def main():
    # Initialize logger
    logger = logging()
    logger.info('Experiment is starting')

    variables.start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    # Initialization of devices

    initialize_v_dc()
    logger.info('High voltage is initialized')

    initialize_v_p()
    logger.info('Pulser is initialized')

    if variables.counter_source == 'TDC':
        device_tdc = initialize_tdc()
        ucb = UCB2(device_tdc.lib, device_tdc.dev_desc)  # opens a user callbacks pipe
        logger.info('TDC is initialized')
    else:
        device_tdc = None
        ucb = None

    task_counter = initialize_counter()
    logger.info('Edge counter is initialized')

    # start the timer for main experiment
    variables.specimen_voltage = variables.vdc_min
    variables.pulse_voltage_min = variables.v_p_min * (1 / variables.pulse_amp_per_supply_voltage)
    variables.pulse_voltage_max = variables.v_p_max * (1 / variables.pulse_amp_per_supply_voltage)
    variables.pulse_voltage = variables.v_p_min
    x = []
    y = []
    t = []
    start_counter = []
    main_v_dc = []
    main_v_p = []
    main_counter = []
    time_ex_s = []
    time_ex_m = []
    time_ex_h = []
    temperature = []
    main_chamber_vacuum = []
    counts_target = ((variables.detection_rate / 100) * variables.pulse_frequency) / variables.pulse_frequency
    logger.info('Starting the main loop')

    total_steps = variables.ex_time * variables.ex_freq
    steps = 0
    while steps < total_steps:
        if steps == 0:
            # Turn on the v_dc and v_p
            com_port_v_p.write('OUTPut ON')
            command_v_dc("F1")
            # start the Counter
            task_counter.start()
            # Wait for 3 second before starting the experiment
            time.sleep(3)
            # Total experiment time variable
            variables.start_flag = True
            start_main_ex = time.time()
        # main loop
        start = datetime.datetime.now()
        main_ex_loop(ucb, task_counter, main_v_dc, main_v_p,
                     main_counter, counts_target, temperature, main_chamber_vacuum)
        end = datetime.datetime.now()
        time_ex_s.append(int(end.strftime("%S")))
        time_ex_m.append(int(end.strftime("%M")))
        time_ex_h.append(int(end.strftime("%H")))
        print(((end - start).microseconds / 1000), 'ms')
        if variables.counter_source == 'pulse_counter':
            if (1000 / variables.ex_freq) > ((end - start).microseconds / 1000):  # time in milliseconds
                time.sleep(((1000 / variables.ex_freq) - ((end - start).microseconds / 1000)) / 1000)
                end2 = datetime.datetime.now()
                print(((end2 - start).microseconds / 1000), 'ms')
            else:
                print('Experiment loop takes longer than initialized frequency Seconds')
                logger.error('Experiment loop takes longer than initialized frequency Seconds')
                break

        if variables.stop_flag:
            print('Experiment is stopped by user')
            logger.info('Experiment is stopped by user')
            # wait for 3 second
            time.sleep(3)
            break
        if variables.max_ions <= variables.total_ions:
            print('Total number of Ions is achieved')
            logger.info('Total number of Ions is achieved')
            # wait for 3 second
            time.sleep(3)
            break
        end_main_ex_loop = time.time()
        variables.elapsed_time = end_main_ex_loop - start_main_ex

        total_steps = variables.ex_time * variables.ex_freq
        steps += 1

    if variables.counter_source == 'TDC':
        ucb.close() # closes the user callbacks pipe, method inherited from base class
    print('Experiment is finished')
    logger.info('Experiment is finished')

    # save hdf5 file
    with h5py.File(variables.path + '\\%s_data.h5' % variables.hdf5_path, "w") as f:
        f.create_dataset("high_voltage", data=main_v_dc, dtype='f')
        f.create_dataset("pulse_voltage", data=main_v_p, dtype='f')
        f.create_dataset("events", data=main_counter, dtype='i')
        f.create_dataset('temperature', data=temperature, dtype='f')
        f.create_dataset('main_chamber_vacuum', data=main_chamber_vacuum, dtype='f')
        f.create_dataset("time_s", data=time_ex_s, dtype='i')
        f.create_dataset("time_m", data=time_ex_m, dtype='i')
        f.create_dataset("time_h", data=time_ex_h, dtype='i')
        f.create_dataset("x", data=variables.x, dtype='f')
        f.create_dataset("y", data=variables.y, dtype='f')
        f.create_dataset("t", data=variables.t, dtype='f')
        f.create_dataset("start_counter", data=variables.start_counter, dtype='f')
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
        f.write('Detection Rate: %s\r\n' % (variables.pulse_fraction * variables.cycle_avg))
        f.write('Maximum Number of Ions: %s\r\n' % variables.max_ions)
        f.write('Control Refresh freq.: %s\r\n' % variables.ex_freq)
        f.write('Cycle for Avg.: %s\r\n' % variables.cycle_avg)
        f.write('K_p Downwards: %s\r\n' % variables.vdc_step_down)
        f.write('K_p Upwards: %s\r\n' % variables.vdc_step_up)
        f.write('K_p Downwards: %s\r\n' % variables.vdc_step_down)
        f.write('Experiment Elapsed Time: %s\r\n' % variables.elapsed_time)
        f.write('Experiment Total Ions: %s\r\n' % variables.total_ions)
        f.write('Email: ' + variables.email + '\r\n')
        f.write('Twitter: %s\r\n' % variables.tweet)
        f.write('Specimen start Voltage: %s\r\n' % variables.vdc_min)
        f.write('Specimen Stop Voltage: %s\r\n' % variables.vdc_max)
        f.write('Specimen Max Achieved Voltage: %s\r\n' % variables.specimen_voltage)
        f.write('Pulse start Voltage: %s\r\n' % variables.v_p_min)
        f.write('Pulse Stop Voltage: %s\r\n' % variables.v_p_max)
        f.write('Specimen Max Achieved Pulse Voltage: %s\r\n' % variables.pulse_voltage)
    clear_up(task_counter, device_tdc)
    logger.info('Variables and devices is cleared')
# if __name__ == "__main__":
#     main(ex_time_g=60, ex_freq_g=20, vdc_min_g=2000, vdc_max_g=15000, vdc_step_g=5, v_p_min_g=15, v_p_max_g=100)
