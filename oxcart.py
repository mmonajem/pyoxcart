# OXCART
# Python Script for doing an experiments
com_port_idx_V_dc = 2
com_port_idx_V_p = 0


# ex_time = 90  # Experiment time in second
# ex_freq = 30 # Experiment main loop frequency in Hz
# vdc_min = 2000 # Minimum value which reached by v_dc
# vdc_max = 15000 # Maximum value which reached by v_dc
# vdc_step = 5 # Increase or decrease vdc in each steps
# v_p_min = 15 # Minimum value which the v_dc start
# v_p_max = 100 # Maximum value which reached by v_dc


# package needed to list available COM ports
import serial.tools.list_ports
import pyvisa as visa
import nidaqmx
import scTDC
import variables
import email_send
import tweet_send
# import tdc_hdf5

# package needed
import time
import datetime
import h5py
import os
import threading
import numpy as np
import sys

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
        return

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



def clear_up(task_counter):
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
    print('Clean up is finished')

def main_ex_loop(task_counter, main_v_dc, main_v_p, main_counter, counts_target,
                 temperature, main_chamber_vacuum):

    # # reading DC HV
    # v_dc = (command_v_dc(">S0A?")[5:-1])
    # variables.specimen_voltage = float(v_dc)
    #
    # # reading pulser power supply voltage
    # v_p = com_port_v_p.query('MEASure:VOLTage?')[:-3]
    # variables.pulse_voltage = float(v_p)

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

    # print('V_dc = ', variables.specimen_voltage, 'V')
    # print('V_p = ', variables.pulse_voltage, 'V')
    # print('# count:', variables.count_temp)
    # print('Total Ions:', variables.total_ions)
    # print('counts_target', counts_target * variables.pulse_frequency * 1000)
    # print('counts_measured', counts_measured * variables.pulse_frequency * 1000)
    # print('Error', counts_error * variables.pulse_frequency * 1000)

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
    main_chamber_vacuum.append(variables.vacuum_main)

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
    # Sleep for 2 seconds in order to update variables from GUI
    time.sleep(2)
    print('ex_time:', variables.ex_time, 'ex_freq:', 'ex_freq:', variables.ex_freq, 'vdc_min:', variables.vdc_min, 'vdc_max:', variables.vdc_max,
          'vdc_step_up:', variables.vdc_step_down, 'vdc_step_up:', variables.vdc_step_down, 'v_p_min:', variables.v_p_min, 'v_p_max:', variables.v_p_max)

    variables.start_time = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
    # Initialization of devices
    initialize_v_dc()
    logger.info('High voltage is initialized')
    initialize_v_p()
    logger.info('Pulser is initialized')
    # device = initialize_tdc()
    task_counter = initialize_counter()
    logger.info('Edge counter is initialized')
    # Starting tdc hdf5 streaming
    # threading.Thread(target=tdc_hdf5.hdf5_streaming(device)).start()
    # start the timer for main experiment
    variables.specimen_voltage = variables.vdc_min
    variables.pulse_voltage_min = variables.v_p_min * (1 / variables.pulse_amp_per_supply_voltage)
    variables.pulse_voltage_max = variables.v_p_max * (1 / variables.pulse_amp_per_supply_voltage)
    variables.pulse_voltage = variables.v_p_min
    main_v_dc = []
    main_v_p = []
    main_counter = []
    time_ex_s = []
    time_ex_m = []
    time_ex_h = []
    temperature = []
    main_chamber_vacuum = []
    counts_target = ((variables.detection_rate/100) * variables.pulse_frequency) / variables.pulse_frequency
    variables.start_flag = True
    logger.info('Starting the main loop')
    start_main_ex = time.time()
    for steps in range(variables.ex_time * variables.ex_freq):
        if steps == 0:
            # Turn on the v_dc and v_p
            com_port_v_p.write('OUTPut ON')
            command_v_dc("F1")
            # start the Counter
            task_counter.start()
            # Wait for 3 second before starting the experiment
            time.sleep(3)
            # Change the start flag for reset plotting
            # variables.start_flag == True
        # main loop
        start = datetime.datetime.now()
        main_ex_loop(task_counter, main_v_dc, main_v_p, main_counter, counts_target, temperature, main_chamber_vacuum)
        end = datetime.datetime.now()
        time_ex_s.append(int(end.strftime("%S")))
        time_ex_m.append(int(end.strftime("%M")))
        time_ex_h.append(int(end.strftime("%H")))
        if variables.stop_flag == False:
            if (1000 / variables.ex_freq) > ((end - start).microseconds / 1000):  # time in milliseconds
                time.sleep(((1000 / variables.ex_freq) - ((end - start).microseconds / 1000)) / 1000)
            else:
                print('Experiment loop takes longer than initialized frequency Seconds')
                logger.error('Experiment loop takes longer than initialized frequency Seconds')
                break
        else:
            print('Experiment is stopped by user')
            logger.info('Experiment is stopped by user')
            # wait for 5 second
            time.sleep(5)
            break
        end_main_ex_loop = time.time()
        variables.elapsed_time = end_main_ex_loop - start_main_ex

    print('experiment is finished')
    logger.info('Experiment is finished')

    # save hdf5 file
    with h5py.File(variables.path + '\\%s_data.h5' %variables.hdf5_path, "w") as f:
        f.create_dataset("high_voltage", data=main_v_dc, dtype='f')
        f.create_dataset("pulse_voltage", data=main_v_p, dtype='f')
        f.create_dataset("events", data=main_counter, dtype='i')
        f.create_dataset('temperature', data=temperature, dtype='f')
        f.create_dataset("time_s", data=time_ex_s, dtype='i')
        f.create_dataset("time_m", data=time_ex_m, dtype='i')
        f.create_dataset("time_h", data=time_ex_h, dtype='i')
        f.create_dataset("x", (0,), dtype='f')
        f.create_dataset("y", (0,), dtype='f')
        f.create_dataset("t", (0,), dtype='f')
        f.create_dataset("trigger#", (0,), dtype='f')
    logger.info('HDF5 file is created')
    variables.end_time = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )

    clear_up(task_counter)
    logger.info('Variables and devices is cleared')
    # save new variable
    with open('./png/counter.txt', 'w') as f:
        f.write(str(variables.counter + 1))
        logger.info('Experiment counter is increased')

    # Adding results of the experiment to the log file
    logger.info('Total number of Ions is: %s' % variables.total_ions)
    # send a Tweet
    message_tweet = 'The Experiment %s finished' % variables.hdf5_path
    if variables.tweet == True:
        tweet_send.send_tweet(message_tweet)
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

# if __name__ == "__main__":
#     main(ex_time_g=60, ex_freq_g=20, vdc_min_g=2000, vdc_max_g=15000, vdc_step_g=5, v_p_min_g=15, v_p_max_g=100)
