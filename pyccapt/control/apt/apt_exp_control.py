"""
This is the main script for controlling the experiment.
It contains the main control loop of experiment.
"""
import datetime
import multiprocessing
import os
import threading
import time
from multiprocessing.queues import Queue

import numpy as np
import pyvisa as visa
import serial.tools.list_ports

from pyccapt.control.control_tools import experiment_statistics
from pyccapt.control.control_tools import hdf5_creator, loggi
from pyccapt.control.devices import email_send
from pyccapt.control.devices import initialize_devices, signal_generator
from pyccapt.control.drs import drs
from pyccapt.control.tdc_roentdec import tdc_roentdec
from pyccapt.control.tdc_surface_concept import tdc_surface_consept


class APT_Exp_Control:
    """
    APT_VOLTAGE class is a main class for controlling voltage atom probe with Surface Consept TDC.
    """

    def __init__(self, variables, conf, emitter):
        self.variables = variables
        self.conf = conf
        self.emitter = emitter
        self.com_port_v_p = None

        self.log_apt = loggi.logger_creator('apt', 'apt.log', path=variables.log_path)
        self.log_apt.info('Experiment is starting')
        self.variables.start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    def initialize_detecotr_process(self):
        print(self.conf['tdc'] == "on" and self.conf['tdc_model'] == 'Surface_Consept' \
              and self.variables.counter_source == 'TDC')
        print('dddddddddddd')
        if self.conf['tdc'] == "on" and self.conf['tdc_model'] == 'Surface_Consept' \
                and self.variables.counter_source == 'TDC':
            # Create and start the TDC process and related queues
            self.queue_x = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_y = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_t = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_dld_start_counter = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_channel = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_time_data = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_tdc_start_counter = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_stop_measurement = Queue(maxsize=1, ctx=multiprocessing.get_context())

            # Initialize and initiate a process(Refer to imported file 'tdc_new' for process function declaration )
            # Module used: multiprocessing
            self.tdc_process = multiprocessing.Process(target=tdc_surface_consept.experiment_measure,
                                                       args=(self.queue_x,
                                                             self.queue_y, self.queue_t,
                                                             self.queue_dld_start_counter,
                                                             self.queue_channel,
                                                             self.queue_time_data,
                                                             self.queue_tdc_start_counter,
                                                             self.queue_stop_measurement))

            self.tdc_process.daemon = True
            self.tdc_process.start()

            self.read_tdc_surface_concept = threading.Thread(target=self.reader_queue_surface_concept)
            self.read_tdc_surface_concept.setDaemon(True)
            self.read_tdc_surface_concept.start()
        elif self.conf['tdc'] == "on" and self.conf[
            'tdc_model'] == 'RoentDek' and self.variables.counter_source == 'TDC':
            self.queue_x = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_y = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_tof = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_AbsoluteTimeStamp = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch0 = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch1 = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch2 = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch3 = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch4 = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch5 = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch6 = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch7 = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_stop_measurement = Queue(maxsize=1, ctx=multiprocessing.get_context())

            self.tdc_process = multiprocessing.Process(target=tdc_roentdec.experiment_measure,
                                                       args=(self.queue_x, self.queue_y, self.queue_tof,
                                                             self.queue_AbsoluteTimeStamp,
                                                             self.queue_ch0, self.queue_ch1, qself.ueue_ch2,
                                                             self.queue_ch3,
                                                             self.queue_ch4, self.queue_ch5, self.queue_ch6,
                                                             self.queue_ch7,
                                                             self.queue_stop_measurement))

            self.tdc_process.daemon = True
            self.tdc_process.start()

            self.read_tdc_roentdek = threading.Thread(target=self.reader_queue_roentdek)
            self.read_tdc_roentdek.setDaemon(True)
            self.read_roentdek.start()
        elif self.conf['tdc'] == "on" and self.conf['tdc_model'] == 'DRS' and self.variables.counter_source == 'DRS':
            self.queue_ch0_time = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch0_wave = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch1_time = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch1_wave = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch2_time = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch2_wave = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch3_time = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_ch3_wave = Queue(maxsize=-1, ctx=multiprocessing.get_context())
            self.queue_stop_measurement = Queue(maxsize=1, ctx=multiprocessing.get_context())

            # Initialize and initiate a process(Refer to imported file 'drs' for process function declaration)
            # Module used: multiprocessing
            self.drs_process = multiprocessing.Process(target=drs.experiment_measure,
                                                       args=(self.queue_ch0_time, self.queue_ch0_wave,
                                                             self.queue_ch1_time, self.queue_ch1_wave,
                                                             self.queue_ch2_time, self.queue_ch2_wave,
                                                             self.queue_ch3_time, qself.ueue_ch3_wave,
                                                             self.queue_stop_measurement,
                                                             ))
            self.drs_process.daemon = True
            self.drs_process.start()

            self.read_drs = threading.Thread(target=self.reader_queue_drs)
            self.read_drs.setDaemon(True)
            self.read_drs.start()

        else:
            print("No counter source selected")

    def initialize_v_dc(self):
        """
        This class method initializes the high voltage device:.
        The function utilizes the serial library to communicate over the
        COM port serially and read the corresponding v_dc parameter.
        The COM port number has to be entered in the config file.

        It exits if it is not able to connect on the COM Port.

        Attributes:
            Accepts only the self (class object)

        Returns:
            Does not return anything
        """
        com_ports = list(serial.tools.list_ports.comports())
        # Setting the com port of V_dc
        self.com_port_v_dc = serial.Serial(
            port=com_ports[self.variables.COM_PORT_V_dc].device,  # chosen COM port
            baudrate=115200,  # 115200
            bytesize=serial.EIGHTBITS,  # 8
            parity=serial.PARITY_NONE,  # N
            stopbits=serial.STOPBITS_ONE  # 1
        )

        # configure the COM port to talk to. Default values: 115200,8,N,1
        if self.com_port_v_dc.is_open:
            self.com_port_v_dc.flushInput()
            self.com_port_v_dc.flushOutput()

            cmd_list = [">S1 3.0e-4", ">S0B 0", ">S0 %s" % self.variables.vdc_min, "F0", ">S0?", ">DON?",
                        ">S0A?"]
            for cmd in range(len(cmd_list)):
                self.command_v_dc(cmd_list[cmd])
        else:
            print("Couldn't open Port!")
            exit()

    def initialize_v_p(self):
        """
        This class method initializes the Pulser device:
        The function utilizes the serial library to communicate over the
        COM port serially and read the corresponding v_p parameter.
        The COM port number has to be enter in the config file.

        Attributes:
            Accepts only the self (class object)

        Returns:
            Does not return anything

        """

        # set the port for v_p
        resources = visa.ResourceManager('@py')
        self.com_port_v_p = resources.open_resource(self.variables.COM_PORT_V_p)

        try:
            self.com_port_v_p.query('*RST')
        except:
            self.com_port_v_p.write(
                'VOLT %s' % (self.variables.v_p_min * (1 / self.variables.pulse_amp_per_supply_voltage)))

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
        # Initialize the response to returned as string
        response = ''
        # Read the response code after execution(command write).
        try:
            while self.com_port_v_dc.in_waiting > 0:
                response = self.com_port_v_dc.readline()  # all characters received, read line till '\r\n'
        except Exception as error:
            self.log_apt.error(
                "Function - command_v_dc | error reading lines - > {}".format(error))
        try:
            response = response.decode("utf-8")
        except Exception as error:
            self.log_apt.error("Function - command_v_dc | error decoding - > {}".format(error))
            self.log_apt.info("Function - command_v_dc | response - > {}".format(response))

        return response

    def reader_queue_surface_concept(self):
        """
        This class method runs in an infinite loop and listens and reads dld queues.
        over the queues for the group: dld

        This function is called continuously by a separate thread in the main function.

        The values read from the queues are updates in imported "variables" file

        Attributes:
            Accepts only the self (class object)

        Returns:
            Does not return anything
        """
        while self.variables.start_flag:
            # Check if any value is present in queue to read from
            while not self.queue_x.empty() or not self.queue_y.empty() or not self.queue_t.empty() or not self.queue_dld_start_counter.empty():
                length = self.queue_x.get()
                self.variables.x.extend((length).tolist())
                self.variables.y.extend((self.queue_y.get()).tolist())
                self.variables.t.extend((self.queue_t.get()).tolist())
                self.variables.dld_start_counter.extend((self.queue_dld_start_counter.get()).tolist())
                self.variables.main_v_dc_dld.extend((np.tile(self.variables.specimen_voltage, len(length))).tolist())
                self.variables.main_v_p_dld.extend((np.tile(self.variables.pulse_voltage, len(length))).tolist())
            # If end of experiment flag is set break the while loop
            if self.variables.end_experiment:
                break
            while not self.queue_channel.empty() or not self.queue_time_data.empty() or not self.queue_tdc_start_counter.empty():
                length = self.queue_channel.get()
                self.variables.channel.extend(length.tolist())
                self.variables.time_data.extend((self.queue_time_data.get()).tolist())
                self.variables.tdc_start_counter.extend((self.queue_tdc_start_counter.get()).tolist())
                self.variables.main_v_dc_tdc.extend((np.tile(self.variables.specimen_voltage, len(length))).tolist())
                self.variables.main_v_p_tdc.extend((np.tile(self.variables.pulse_voltage, len(length))).tolist())
            # If end of experiment flag is set break the while loop
            if self.variables.end_experiment:
                break

    def reader_queue_roentdek(self):

        while self.variables.start_flag:
            # Check if any value is present in queue to read from
            while not self.queue_x.empty() or not self.queue_y.empty() or not self.queue_tof.empty() or not self.queue_AbsoluteTimeStamp.empty() \
                    or not self.queue_ch0.empty() or not self.queue_ch1.empty() or not self.queue_ch2.empty() or not self.queue_ch3.empty() \
                    or not self.queue_ch4.empty() or not self.queue_ch5.empty() or not self.queue_ch6.empty() or not self.queue_ch7.empty():
                # Utilize locking mechanism to avoid concurrent use of resources and dirty reads

                length = self.queue_x.get()
                self.variables.x = np.append(self.variables.x, length)
                self.variables.y = np.append(self.variables.y, self.queue_y.get())
                self.variables.t = np.append(self.variables.t, self.queue_tof.get())
                self.variables.time_stamp = np.append(self.variables.time_stamp,
                                                      self.queue_AbsoluteTimeStamp.get())
                self.variables.ch0 = np.append(self.variables.ch0, self.queue_ch0.get())
                self.variables.ch1 = np.append(self.variables.ch1, self.queue_ch1.get())
                self.variables.ch2 = np.append(self.variables.ch2, self.queue_ch2.get())
                self.variables.ch3 = np.append(self.variables.ch3, self.queue_ch3.get())
                self.variables.ch4 = np.append(self.variables.ch4, self.queue_ch4.get())
                self.variables.ch5 = np.append(self.variables.ch5, self.queue_ch5.get())
                self.variables.ch6 = np.append(self.variables.ch6, self.queue_ch6.get())
                self.variables.ch7 = np.append(self.variables.ch7, self.queue_ch7.get())

                self.variables.main_v_dc_dld = np.append(self.variables.main_v_dc_dld,
                                                         np.tile(self.variables.specimen_voltage, len(length)))

                self.variables.laser_intensity = np.append(self.variables.laser_intensity,
                                                           np.tile(self.variables.laser_degree, len(length)))

            # If end of experiment flag is set break the while loop
            if self.variables.end_experiment:
                break

    def reader_queue_drs(self):

        """
        This class method runs in an infinite loop and listens and reads DRS queues.
        over the queues for the group: DRS

        This function is called continuously by a separate thread in the main function.

        The values read from the queues are updates in imported "variables" file.
        Attributes:
            Accepts only the self (class object)

        Returns:
            Does not return anything
        """

        while self.variables.start_flag:
            # Check if any value is present in queue to read from
            while not self.queue_ch0_time.empty() or not self.queue_ch0_wave.empty() or not self.queue_ch1_time.empty() or not \
                    self.queue_ch1_wave.empty() or not self.queue_ch2_time.empty() or not \
                    self.queue_ch2_wave.empty() or not self.queue_ch3_time.empty() or not self.queue_ch3_wave.empty():
                length = self.queue_ch0_time.get()
                self.variables.ch0_time.extend(length)
                self.variables.ch0_wave.extend((self.queue_ch0_wave.get()).tolist())
                self.variables.ch1_time.extend((self.queue_ch1_time.get()).tolist())
                self.variables.ch1_wave.extend((self.queue_ch1_wave.get()).tolist())
                self.variables.ch2_time.extend((self.queue_ch2_time.get()).tolist())
                self.variables.ch2_wave.extend((self.queue_ch2_wave.get()).tolist())
                self.variables.ch3_time.extend((self.queue_ch3_time.get()).tolist())
                self.variables.ch3_wave.extend((self.queue_ch3_wave.get()).tolist())

                self.variables.main_v_dc_drs.extend((np.tile(self.variables.specimen_voltage, len(length))).tolist())
                self.variables.main_v_p_drs.extend((np.tile(self.variables.pulse_voltage, len(length))).tolist())
            # If end of experiment flag is set break the while loop
            if self.variables.end_experiment:
                break

    def main_ex_loop(self, counts_target):

        """
        This function is contain all methods that iteratively has to run to control the experiment.
        This class method:

        1. Read the number of detected Ions(in TDC or Counter mode)
        2- Calculate the error of detection rate of desire rate
        3- Regulate the high voltage and pulser

        This function is called in each loop of main function.

        Attributes:
            counts_target:

        Returns:
            Does not return anything

        """

        if self.variables.counter_source == 'TDC':
            self.variables.total_ions = len(self.variables.x)
        elif self.variables.counter_source == 'DRS':
            pass

        self.variables.count_temp = self.variables.total_ions - self.variables.count_last
        self.variables.count_last = self.variables.total_ions

        # saving the values of high dc voltage, pulse, and current iteration ions
        self.variables.main_v_dc.append(self.variables.specimen_voltage)
        self.variables.main_v_p.append(self.variables.pulse_voltage)
        self.variables.main_counter.append(self.variables.count_temp)
        # averaging count rate of N_averg counts
        self.variables.avg_n_count = self.variables.ex_freq * (
                sum(self.variables.main_counter[-self.variables.ex_freq:]) / self.variables.ex_freq)

        counts_measured = self.variables.avg_n_count / (1 + self.variables.pulse_frequency * 1000)

        # variables.avg_n_count = np.sum(variables.main_counter[-variables.ex_freq:])
        #
        # counts_measured = variables.avg_n_count / (1 + variables.pulse_frequency * 1000)

        counts_error = counts_target - counts_measured  # deviation from setpoint

        # simple proportional control with averaging
        # rate = ((variables.avg_n_count * 100) / (1 + variables.pulse_frequency * 1000))
        # if rate < 0.01 and variables.specimen_voltage < 5000:
        #     ramp_speed_factor = 2.5
        # else:
        ramp_speed_factor = 1
        if counts_error > 0:
            voltage_step = counts_error * self.variables.vdc_step_up * ramp_speed_factor
        elif counts_error <= 0:
            voltage_step = counts_error * self.variables.vdc_step_down * ramp_speed_factor

        # update v_dc
        if not self.variables.vdc_hold:
            if self.variables.specimen_voltage < self.variables.vdc_max:
                if self.variables.specimen_voltage >= self.variables.vdc_min - 50:
                    specimen_voltage_temp = self.variables.specimen_voltage + voltage_step
                    if specimen_voltage_temp != self.variables.specimen_voltage:
                        # sending VDC via serial
                        if self.conf['v_dc'] != "off":
                            self.command_v_dc(">S0 %s" % specimen_voltage_temp)

                        # update pulse voltage v_p
                        new_vp = self.variables.specimen_voltage * self.variables.pulse_fraction * \
                                 (1 / self.variables.pulse_amp_per_supply_voltage)
                        if self.variables.pulse_voltage_max > new_vp > self.variables.pulse_voltage_min:
                            if self.conf['v_p'] != "off":
                                self.com_port_v_p.write('VOLT %s' % new_vp)
                            self.variables.pulse_voltage = new_vp * self.variables.pulse_amp_per_supply_voltage

                    self.variables.specimen_voltage = specimen_voltage_temp

        self.variables.main_temperature.append(self.variables.temperature)
        self.variables.main_chamber_vacuum.append(float(self.variables.vacuum_main))

    def run_experiment(self):

        if os.path.exists("./files/counter_experiments.txt"):
            # Read the experiment counter
            with open('./files/counter_experiments.txt') as f:
                self.variables.counter = int(f.readlines()[0])
        else:
            # create a new txt file
            with open('./files/counter_experiments.txt', 'w') as f:
                f.write(str(1))  # Current time and date
        now = datetime.datetime.now()
        self.variables.exp_name = "%s_" % self.variables.counter + \
                                  now.strftime("%b-%d-%Y_%H-%M") + "_%s" % self.variables.hdf5_path
        p = os.path.abspath(os.path.join(__file__, "../../.."))
        self.variables.path = os.path.join(p,
                                           'data_voltage_pulse_mode\\%s' % self.variables.exp_name)
        self.variables.path_meta = self.variables.path + '\\meta_dta\\'
        # Create folder to save the data
        if not os.path.isdir(self.variables.path):
            os.makedirs(self.variables.path, mode=0o777, exist_ok=True)
        if not os.path.isdir(self.variables.path_meta):
            os.makedirs(self.variables.path_meta, mode=0o777, exist_ok=True)
        if self.conf['signal_generator'] == 'on':
            # Initialize the signal generator
            try:
                signal_generator.initialize_signal_generator(self.variables, self.variables.pulse_frequency)
                self.log_apt.info('Signal generator is initialized')
            except Exception as e:
                print('Can not initialize the signal generator')
                print('Make the signal_generator off in the config file or fix the error below')
                print(e)
                raise

        if self.conf['v_dc'] == 'on':
            try:
                # Initialize high voltage
                self.initialize_v_dc()
                self.log_apt.info('High voltage is initialized')
            except Exception as e:
                print('Can not initialize the high voltage')
                print('Make the v_dc off in the config file or fix the error below')
                print(e)
                raise

        if self.conf['v_p'] == 'on':
            try:
                # Initialize pulser
                self.initialize_v_p()
                self.log_apt.info('Pulser is initialized')
            except Exception as e:
                print('Can not initialize the pulser')
                print('Make the v_p off in the config file or fix the error below')
                print(e)
                raise

        if self.conf['tdc'] == 'on':
            self.initialize_detecotr_process()
        # start the timer for main experiment
        self.variables.specimen_voltage = self.variables.vdc_min
        self.variables.pulse_voltage_min = self.variables.v_p_min * (1 / self.variables.pulse_amp_per_supply_voltage)
        self.variables.pulse_voltage_max = self.variables.v_p_max * (1 / self.variables.pulse_amp_per_supply_voltage)
        self.variables.pulse_voltage = self.variables.v_p_min

        time_ex_s = []
        time_ex_m = []
        time_ex_h = []
        time_counter = []

        total_steps = self.variables.ex_time * self.variables.ex_freq
        steps = 0
        flag_achieved_high_voltage = 0
        index_time = 0
        ex_time_temp = self.variables.ex_time
        init_detection_rate = 0

        desired_rate = 3  # Hz statistic rate update in the main GUI
        iterations_per_desired_rate = self.variables.ex_freq / desired_rate
        counter_statistic = 0

        desired_rate = self.variables.ex_freq  # Hz
        desired_period = 1.0 / desired_rate  # seconds
        # Main loop of experiment
        while steps < total_steps:
            start_time = time.perf_counter()
            # Only for initializing every thing at firs iteration
            if steps == 0:
                # Turn on the v_dc and v_p
                if self.conf['v_p'] == "on":
                    self.com_port_v_p.write('OUTPut ON')
                    time.sleep(0.5)
                if self.conf['v_dc'] == "on":
                    self.command_v_dc("F1")
                    time.sleep(0.5)

                self.variables.start_flag = True
                # Wait for 4 second to all devices get ready
                time.sleep(4)
                # Total experiment time variable
                start_main_ex = time.time()

                self.log_apt.info('Experiment is started')

            if self.variables.detection_rate != init_detection_rate:
                counts_target = ((
                                         self.variables.detection_rate / 100) * self.variables.pulse_frequency) / self.variables.pulse_frequency
                init_detection_rate = self.variables.detection_rate

            self.variables.detection_rate_current = (self.variables.avg_n_count * 100) / (
                        1 + self.variables.pulse_frequency * 1000)

            # main loop function
            self.main_ex_loop(counts_target)

            # Counter of iteration
            time_counter.append(steps)
            steps += 1
            if self.variables.stop_flag:
                self.log_apt.info('Experiment is stopped by user')
                if self.conf['tdc'] != "off":
                    if self.variables.counter_source == 'TDC':
                        self.queue_stop_measurement.put(True)
                time.sleep(1)
                break

            if self.variables.criteria_ions:
                if self.variables.max_ions <= self.variables.total_ions:
                    self.log_apt.info('Total number of Ions is achieved')
                    if self.conf['tdc'] == "on":
                        if self.variables.counter_source == 'TDC':
                            self.queue_stop_measurement.put(True)
                    time.sleep(1)
                    break
            if self.variables.criteria_vdc:
                if self.variables.vdc_max <= self.variables.specimen_voltage:
                    if flag_achieved_high_voltage > self.variables.ex_freq * 10:
                        self.log_apt.info('High Voltage Max. is achieved')
                        if self.conf['tdc'] != "off":
                            if self.variables.counter_source == 'TDC':
                                self.queue_stop_measurement.put(True)
                        time.sleep(1)
                        break
                    flag_achieved_high_voltage += 1
            if self.variables.criteria_time:
                if steps + 1 == total_steps:
                    self.log_apt.info('Experiment time Max. is achieved')
                    if self.conf['tdc'] == "on":
                        if self.variables.counter_source == 'TDC':
                            self.queue_stop_measurement.put(True)
                    time.sleep(1)
                    break
            if self.variables.ex_time != ex_time_temp:
                total_steps = self.variables.ex_time * self.variables.ex_freq - steps
                ex_time_temp = self.variables.ex_time

            # Because experiment time is not a stop criteria, increase total_steps
            if not self.variables.criteria_time and steps + 1 == total_steps:
                total_steps += 1

            counter_statistic += 1
            if counter_statistic >= iterations_per_desired_rate:
                counter_statistic = 0
                self.emitter.elapsed_time.emit(self.variables.elapsed_time)
                self.emitter.total_ions.emit(self.variables.total_ions)
                self.emitter.speciemen_voltage.emit(self.variables.specimen_voltage)
                self.emitter.pulse_voltage.emit(self.variables.pulse_voltage)
                self.emitter.detection_rate.emit(self.variables.detection_rate_current)
            # Measure time
            end = datetime.datetime.now()
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            remaining_time = desired_period - elapsed_time

            if remaining_time >= 0:
                time.sleep(remaining_time)
            else:
                print(
                    f"{initialize_devices.bcolors.WARNING}Warning: Experiment loop takes longer than %s Millisecond{initialize_devices.bcolors.ENDC}" % (
                        int(1000 / self.variables.ex_freq)))
                self.log_apt.error(
                    'Experiment loop takes longer than %s Millisecond' % (int(1000 / self.variables.ex_freq)))
                print('%s- The iteration time:' % index_time, -remaining_time)
                index_time += 1
            time_ex_s.append(int(end.strftime("%S")))
            time_ex_m.append(int(end.strftime("%M")))
            time_ex_h.append(int(end.strftime("%H")))
            end_main_ex_loop = time.time()
            self.variables.elapsed_time = end_main_ex_loop - start_main_ex

        if self.conf['tdc'] == "on":
            # Stop the TDC process
            try:
                if self.variables.counter_source == 'TDC':
                    self.tdc_process.join(3)
                    if self.tdc_process.is_alive():
                        self.tdc_process.terminate()
                        self.tdc_process.join(1)
                        # Release all the resources of the TDC process
                        self.tdc_process.close()
                elif self.variables.counter_source == 'DRS':
                    self.drs_process.join(3)
                    if self.drs_process.is_alive():
                        self.drs_process.terminate()
                        self.drs_process.join(1)
                        # Release all the resources of the TDC process
                        self.drs_process.close()
            except Exception as e:
                print(
                    f"{initialize_devices.bcolors.WARNING}Warning: The TDC or DRS process cannot be terminated properly{initialize_devices.bcolors.ENDC}")
                print(e)
        self.variables.end_experiment = True
        time.sleep(1)
        if self.conf['tdc'] == "on":
            # Stop the TDC and DLD thread
            if self.variables.counter_source == 'TDC':
                try:
                    self.read_tdc_surface_concept.join(1)
                    self.read_tdc_roentdek.join(1)
                except Exception as e:
                    pass
        elif self.variables.counter_source == 'DRS':
            self.read_drs.join(1)

        if self.conf['tdc'] == "off":
            if self.variables.counter_source == 'TDC':
                self.variables.total_ions = len(self.variables.x)
        elif self.variables.counter_source == 'DRS':
            pass

        time.sleep(1)
        self.log_apt.info('Experiment is finished')

        # Check the length of arrays to be equal
        if self.variables.counter_source == 'TDC':
            if all(len(lst) == len(self.variables.x) for lst in [self.variables.x, self.variables.y,
                                                                 self.variables.t, self.variables.dld_start_counter,
                                                                 self.variables.main_v_dc_dld,
                                                                 self.variables.main_v_p_dld]):
                self.log_apt.warning('dld data have not same length')

            if all(len(lst) == len(self.variables.channel) for lst in [self.variables.channel, self.variables.time_data,
                                                                       self.variables.tdc_start_counter,
                                                                       self.variables.main_v_dc_tdc,
                                                                       self.variables.main_v_p_tdc]):
                self.log_apt.warning('tdc data have not same length')
        elif self.variables.counter_source == 'DRS':
            if all(len(lst) == len(self.variables.ch0_time) for lst in
                   [self.variables.ch0_wave, self.variables.ch1_time,
                    self.variables.ch1_wave, self.variables.ch2_time,
                    self.variables.ch2_wave, self.variables.ch3_time,
                    self.variables.ch3_wave,
                    self.variables.main_v_dc_drs, self.variables.main_v_p_drs]):
                self.log_apt.warning('tdc data have not same length')

        self.log_apt.info('HDF5 file is created')
        self.variables.end_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        # Save new value of experiment counter
        if os.path.exists("./files/counter_experiments.txt"):
            with open('./files/counter_experiments.txt', 'w') as f:
                f.write(str(self.variables.counter + 1))
                self.log_apt.info('Experiment counter is increased')

        # Adding results of the experiment to the log file
        self.log_apt.info('Total number of Ions is: %s' % self.variables.total_ions)

        # send an email
        subject = 'Oxcart Experiment {} Report'.format(self.variables.hdf5_path)
        elapsed_time_temp = float("{:.3f}".format(self.variables.elapsed_time))
        message = 'The experiment was started at: {}\n' \
                  'The experiment was ended at: {}\n' \
                  'Experiment duration: {}\n' \
                  'Total number of ions: {}\n'.format(self.variables.start_time,
                                                      self.variables.end_time, elapsed_time_temp,
                                                      self.variables.total_ions)

        if len(self.variables.email) > 3:
            self.log_apt.info('Email is sent')
            email_send.send_email(self.variables.email, subject, message)

        # save data in hdf5 file
        hdf5_creator.hdf_creator(self.variables, self.conf, time_counter, time_ex_s, time_ex_m, time_ex_h)

        # save setup parameters and run statistics in a txt file
        experiment_statistics.save_statistics_apt(self.variables)

        # Clear up all the variables and deinitialize devices
        self.clear_up()
        self.log_apt.info('Variables and devices is cleared')

    def clear_up(self):
        """
        This function clears global variables and deinitialize high voltage and pulser function
        and clear up global variables

        Attributes:
            Does not accept any arguments
        Returns:
            Does not return anything

        """

        def cleanup_variables():
            """
            Clear up all the global variables
            """
            self.variables.stop_flag = False
            self.variables.end_experiment = False
            self.variables.start_flag = False
            self.variables.detection_rate = 0.0
            self.variables.detection_rate_current = 0.0
            self.variables.count = 0
            self.variables.count_temp = 0
            self.variables.count_last = 0
            self.variables.index_plot = 0
            self.variables.index_save_image = 0
            self.variables.index_wait_on_plot_start = 0
            self.variables.index_plot_save = 0
            self.variables.index_plot = 0

            self.variables.x = []
            self.variables.y = []
            self.variables.t = []
            self.variables.dld_start_counter = []

            self.variables.channel = []
            self.variables.time_data = []
            self.variables.tdc_start_counter = []

            self.variables.ch0_time = []
            self.variables.ch0_wave = []
            self.variables.ch1_time = []
            self.variables.ch1_wave = []
            self.variables.ch2_time = []
            self.variables.ch2_wave = []
            self.variables.ch3_time = []
            self.variables.ch3_wave = []

            self.variables.main_v_dc = []
            self.variables.main_v_p = []
            self.variables.main_counter = []
            self.variables.main_temperature = []
            self.variables.main_chamber_vacuum = []
            self.variables.main_v_dc_dld = []
            self.variables.main_v_p_dld = []
            self.variables.main_v_dc_tdc = []
            self.variables.main_v_p_tdc = []
            self.log_apt.info("Function - cleanup_variables | ch1 | value - {}| type - {}".format(
                self.variables.count_temp, type(self.variables.count_temp)))

            self.log_apt.info("Function - cleanup_variables | main_v_dc_tdc | value - {}| type - {}".format(
                self.variables.main_v_dc_tdc, type(self.variables.main_v_dc_tdc)))

        self.log_apt.info('starting to clean up')

        # save the data to the HDF5

        if self.conf['v_dc'] != "off":
            # Switch off the v_dc
            self.command_v_dc('F0')
            self.com_port_v_dc.close()

        if self.conf['v_p'] != "off":
            # Switch off the v_p
            self.com_port_v_p.write('VOLT 0')
            self.com_port_v_p.write('OUTPut OFF')
            self.com_port_v_p.close()

        if self.conf['signal_generator'] != "off":
            # Turn off the signal generator
            signal_generator.turn_off_signal_generator()
        # Zero variables
        cleanup_variables()
        self.log_apt.info('Clean up is finished')
