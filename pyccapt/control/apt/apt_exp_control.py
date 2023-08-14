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
    This class is responsible for controlling the experiment.
    """

    def __init__(self, variables, conf, emitter):
        self.variables = variables
        self.conf = conf
        self.emitter = emitter
        self.com_port_v_p = None

        self.log_apt = None
        self.variables.start_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.sleep_time = 1 / self.variables.ex_freq

    def initialize_detector_process(self):
        """
        Initialize the detector process based on the configured settings.

        This method initializes the necessary queues and processes for data acquisition based on the configured settings.

        Args:
           None

        Returns:
           None
        """
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
                                                             self.queue_ch0, self.queue_ch1, self.queue_ch2,
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
                                                             self.queue_ch3_time, self.queue_ch3_wave,
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
        Initialize the V_dc source.

        This function initializes the V_dc source by configuring the COM port settings and sending commands to set
        the parameters.

        Args:
            None

        Returns:
            None
        """
        com_ports = list(serial.tools.list_ports.comports())
        self.com_port_v_dc = serial.Serial(
            port=com_ports[self.variables.COM_PORT_V_dc].device,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )

        if self.com_port_v_dc.is_open:
            self.com_port_v_dc.flushInput()
            self.com_port_v_dc.flushOutput()

            cmd_list = [">S1 3.0e-4", ">S0B 0", ">S0 %s" % self.variables.vdc_min, "F0", ">S0?", ">DON?", ">S0A?"]
            for cmd in range(len(cmd_list)):
                self.command_v_dc(cmd_list[cmd])
        else:
            print("Couldn't open Port!")
            exit()

    def initialize_v_p(self):
        """
        Initialize the Pulser device.

        This method initializes the Pulser device using the Visa library.

        Args:
            None

        Returns:
            None
        """
        resources = visa.ResourceManager('@py')
        self.com_port_v_p = resources.open_resource(self.variables.COM_PORT_V_p)

        try:
            self.com_port_v_p.query('*RST')
        except:
            self.com_port_v_p.write(
                'VOLT %s' % (self.variables.v_p_min * (1 / self.variables.pulse_amp_per_supply_voltage)))

    def command_v_dc(self, cmd):
        """
        Send commands to the high voltage parameter: v_dc.

        This method sends commands to the V_dc source over the COM port and reads the response.

        Args:
            cmd (str): The command to send.

        Returns:
            str: The response received from the device.
        """
        self.com_port_v_dc.write((cmd + '\r\n').encode())
        time.sleep(0.005)
        response = ''
        try:
            while self.com_port_v_dc.in_waiting > 0:
                response = self.com_port_v_dc.readline()
        except Exception as error:
            print(error)

        if isinstance(response, bytes):
            response = response.decode("utf-8")

        return response

    def reader_queue_surface_concept(self):
        """
        Read data from Surface Concept TDC queues.

        This method continuously reads data from the queues for Surface Concept TDC and updates the corresponding
        variables in the imported "variables" file.

        Args:
            None

        Returns:
            None
        """
        # surface concept tdc specific binning and factors
        TOFFACTOR = 27.432 / (1000 * 4)  # 27.432 ps/bin, tof in ns, data is TDC time sum
        DETBINS = 4900
        BINNINGFAC = 2
        XYFACTOR = 80 / DETBINS * BINNINGFAC  # XXX mm/bin
        XYBINSHIFT = DETBINS / BINNINGFAC / 2  # to center detector

        while self.variables.start_flag and not self.variables.end_experiment:
            while not self.queue_x.empty() and not self.queue_y.empty() and not self.queue_t.empty() \
                    and not self.queue_dld_start_counter.empty():
                x_data = self.queue_x.get()
                y_data = self.queue_y.get()
                t_data = self.queue_t.get()
                dld_start_counter_data = self.queue_dld_start_counter.get()
                # correct for binning of surface concept
                x_data = ((x_data - XYBINSHIFT) * XYFACTOR) / 10  # from mm to in cm by dividing by 10
                y_data = ((y_data - XYBINSHIFT) * XYFACTOR) / 10  # from mm to in cm by dividing by 10
                t_data = t_data * TOFFACTOR  # in ns

                # with self.variables.lock_data:
                self.variables.x.extend(x_data.tolist())
                self.variables.y.extend(y_data.tolist())
                self.variables.t.extend(t_data.tolist())
                self.variables.dld_start_counter.extend(dld_start_counter_data.tolist())

                voltage_data = np.tile(self.variables.specimen_voltage, len(x_data))
                self.variables.main_v_dc_dld_surface_concept.extend(voltage_data.tolist())
                self.variables.main_p_dld_surface_concept.extend(
                    np.tile(self.variables.pulse_voltage, len(x_data)).tolist())
                # with self.variables.lock_data_plot:
                self.variables.main_v_dc_plot.extend(voltage_data.tolist())
                self.variables.x_plot.extend(x_data.tolist())
                self.variables.y_plot.extend(y_data.tolist())
                self.variables.t_plot.extend(t_data.tolist())

            while not self.queue_channel.empty() and not self.queue_time_data.empty() \
                    and not self.queue_tdc_start_counter.empty():
                channel_data = self.queue_channel.get()
                time_data = self.queue_time_data.get()
                tdc_start_counter_data = self.queue_tdc_start_counter.get()

                # with self.variables.lock_data:
                self.variables.channel.extend(channel_data.tolist())
                self.variables.time_data.extend(time_data.tolist())
                self.variables.tdc_start_counter.extend(tdc_start_counter_data.tolist())

                voltage_data = np.tile(self.variables.specimen_voltage, len(channel_data))
                self.variables.main_v_dc_tdc_surface_concept.extend(voltage_data.tolist())
                self.variables.main_p_tdc_surface_concept.extend(
                    np.tile(self.variables.pulse_voltage, len(channel_data)).tolist())
            time.sleep(self.sleep_time)

    def reader_queue_roentdek(self):
        """
        Read data from RoentDek TDC queues.

        This method continuously reads data from the queues for RoentDek TDC and updates the corresponding
        variables in the imported "variables" file.

        Args:
            None

        Returns:
            None
        """
        while self.variables.start_flag and not self.variables.end_experiment:
            while not self.queue_x.empty() or not self.queue_y.empty() or not self.queue_tof.empty() \
                    or not self.queue_AbsoluteTimeStamp.empty() or not self.queue_ch0.empty() \
                    or not self.queue_ch1.empty() or not self.queue_ch2.empty() or not self.queue_ch3.empty() \
                    or not self.queue_ch4.empty() or not self.queue_ch5.empty() or not self.queue_ch6.empty() \
                    or not self.queue_ch7.empty():
                x_list = self.queue_x.get()
                y_list = self.queue_y.get()
                t_list = self.queue_tof.get()
                time_stamp_list = self.queue_AbsoluteTimeStamp.get()
                ch0_list = self.queue_ch0.get()
                ch1_list = self.queue_ch1.get()
                ch2_list = self.queue_ch2.get()
                ch3_list = self.queue_ch3.get()
                ch4_list = self.queue_ch4.get()
                ch5_list = self.queue_ch5.get()
                ch6_list = self.queue_ch6.get()
                ch7_list = self.queue_ch7.get()
                main_v_dc_dld_list = np.tile(self.variables.specimen_voltage, len(x_list))
                main_p_tdc_roentdek = np.tile(self.variables.laser_degree, len(x_list))

                # with self.variables.lock_data:
                self.variables.x.extend(x_list.tolist())
                self.variables.y.extend(y_list.tolist())
                self.variables.t.extend(t_list.tolist())
                self.variables.time_stamp.extend(time_stamp_list.tolist())
                self.variables.ch0.extend(ch0_list.tolist())
                self.variables.ch1.extend(ch1_list.tolist())
                self.variables.ch2.extend(ch2_list.tolist())
                self.variables.ch3.extend(ch3_list.tolist())
                self.variables.ch4.extend(ch4_list.tolist())
                self.variables.ch5.extend(ch5_list.tolist())
                self.variables.ch6.extend(ch6_list.tolist())
                self.variables.ch7.extend(ch7_list.tolist())
                self.variables.main_v_dc_tdc_roentdek.extend(main_v_dc_dld_list.tolist())
                self.variables.main_p_tdc_roentdek.extend(main_p_tdc_roentdek.tolist())

                # with self.variables.lock_data_plot:
                self.variables.main_v_dc_plot.extend(main_v_dc_dld_list.tolist())
                self.variables.x_plot.extend(x_list.tolist())
                self.variables.y_plot.extend(y_list.tolist())
                self.variables.t_plot.extend(t_list.tolist())
            time.sleep(self.sleep_time)

    def reader_queue_drs(self):
        """
        Read data from DRS queues.

        This method continuously reads data from the queues for DRS and updates the corresponding variables in
        the imported "variables" file.

        Args:
            None

        Returns:
            None
        """
        while self.variables.start_flag and not self.variables.end_experiment:
            while not self.queue_ch0_time.empty() or not self.queue_ch0_wave.empty() \
                    or not self.queue_ch1_time.empty() or not self.queue_ch1_wave.empty() \
                    or not self.queue_ch2_time.empty() or not self.queue_ch2_wave.empty() \
                    or not self.queue_ch3_time.empty() or not self.queue_ch3_wave.empty():
                ch0_time = self.queue_ch0_time.get()
                ch0_wave = self.queue_ch0_wave.get()
                ch1_time = self.queue_ch1_time.get()
                ch1_wave = self.queue_ch1_wave.get()
                ch2_time = self.queue_ch2_time.get()
                ch2_wave = self.queue_ch2_wave.get()
                ch3_time = self.queue_ch3_time.get()
                ch3_wave = self.queue_ch3_wave.get()

                # with self.variables.lock_data:
                self.variables.ch0_time.extend(ch0_time)
                self.variables.ch0_wave.extend(ch0_wave)
                self.variables.ch1_time.extend(ch1_time)
                self.variables.ch1_wave.extend(ch1_wave)
                self.variables.ch2_time.extend(ch2_time)
                self.variables.ch2_wave.extend(ch2_wave)
                self.variables.ch3_time.extend(ch3_time)
                self.variables.ch3_wave.extend(ch3_wave)
                voltage_data = np.tile(self.variables.specimen_voltage, len(ch0_time))
                self.variables.main_v_dc_drs.extend(voltage_data.tolist())
                self.variables.main_p_drs.extend(
                    np.tile(self.variables.pulse_voltage, len(ch0_time)).tolist())

                # with self.variables.lock_data_plot:
                self.variables.main_v_dc_plot.extend(voltage_data.tolist())
                # we have to calculate x and y from the wave data here
                self.variables.x_plot.extend(ch0_time.tolist())
                self.variables.y_plot.extend(ch0_time.tolist())
                self.variables.t_plot.extend(ch0_time.tolist())
            time.sleep(self.sleep_time)

    def main_ex_loop(self, counts_target):
        """
        Execute main experiment loop.

        This method contains all methods that iteratively run to control the experiment. It reads the number of detected
        ions, calculates the error of the desired rate, and regulates the high voltage and pulser accordingly.

        Args:
            counts_target: Target ion count

        Returns:
            None
        """
        # Update total_ions based on the counter_source...
        # Calculate count_temp and update variables...
        # Save high voltage, pulse, and current iteration ions...
        # Calculate counts_measured and counts_error...
        # Perform proportional control with averaging...
        # Update v_dc and v_p...
        # Update other experiment variables...

        if self.variables.counter_source == 'TDC':
            self.variables.total_ions = len(self.variables.x)
        elif self.variables.counter_source == 'DRS':
            pass

        # with self.variables.lock_statistics:
        self.variables.count_temp = self.variables.total_ions - self.variables.count_last
        self.variables.count_last = self.variables.total_ions

        # saving the values of high dc voltage, pulse, and current iteration ions
        # with self.variables.lock_experiment_variables:
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
        else:
            voltage_step = 0

        # update v_dc
        if not self.variables.vdc_hold and voltage_step != 0:
            # if self.variables.specimen_voltage < self.variables.vdc_max:
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

        # with self.variables.lock_statistics:
        self.variables.main_temperature.append(self.variables.temperature)
        self.variables.main_chamber_vacuum.append(float(self.variables.vacuum_main))

    def precise_sleep(self, seconds):
        """
        Precise sleep function.

        Args:
            seconds:    Seconds to sleep

        Returns:
            None
        """
        start_time = time.perf_counter()
        while time.perf_counter() - start_time < seconds:
            pass

    def run_experiment(self):
        """
        Run the main experiment.

        This method initializes devices, starts the experiment loop, monitors various criteria, and manages experiment
        stop conditions and data storage.

        Returns:
            None
        """
        # Initialize devices...
        # Start the main experiment loop...
        # Monitor various criteria...
        # Perform experiment loop...
        # Stop TDC process...
        # Handle experiment ending...
        # Save experiment counter...
        # Send email...
        # Save data in hdf5 file...
        # Save setup parameters and statistics in a txt file...
        # Clear up variables and deinitialize devices...
        # Log completion...

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
                                  now.strftime("%b-%d-%Y_%H-%M") + "_%s" % self.variables.hdf5_data_name
        p = os.path.abspath(os.path.join(__file__, "../../.."))
        self.variables.path = os.path.join(p, 'data\\%s' % self.variables.exp_name)
        self.variables.path_meta = self.variables.path + '\\meta_data\\'

        self.variables.log_path = self.variables.path_meta
        # Create folder to save the data
        if not os.path.isdir(self.variables.path):
            os.makedirs(self.variables.path, mode=0o777, exist_ok=True)
        if not os.path.isdir(self.variables.path_meta):
            os.makedirs(self.variables.path_meta, mode=0o777, exist_ok=True)

        self.log_apt = loggi.logger_creator('apt', self.variables, 'apt.log', path=self.variables.log_path)
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
            self.initialize_detector_process()
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

        desired_rate = 3  # Hz statistic rate update in the main GUI
        iterations_per_desired_rate = self.variables.ex_freq / desired_rate
        counter_statistic = 0

        desired_rate = self.variables.ex_freq  # Hz
        desired_period = 1.0 / desired_rate  # seconds

        counts_target = ((self.variables.detection_rate / 100) *
                         self.variables.pulse_frequency) / self.variables.pulse_frequency
        init_detection_rate = self.variables.detection_rate
        last_save_time = time.time()
        # Main loop of experiment
        while steps < total_steps:
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
                # Wait for 8 second to all devices get ready
                time.sleep(8)
                # Total experiment time variable
                start_main_ex = time.time()

                self.log_apt.info('Experiment is started')
            start_time = time.perf_counter()
            if self.variables.detection_rate != init_detection_rate:
                counts_target = ((self.variables.detection_rate / 100) *
                                 self.variables.pulse_frequency) / self.variables.pulse_frequency
                init_detection_rate = self.variables.detection_rate

            # with self.variables.lock_statistics:
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
            time_ex_s.append(int(end.strftime("%S")))
            time_ex_m.append(int(end.strftime("%M")))
            time_ex_h.append(int(end.strftime("%H")))
            end_main_ex_loop = time.time()
            # with self.variables.lock_statistics:
            self.variables.elapsed_time = end_main_ex_loop - start_main_ex

            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            remaining_time = desired_period - elapsed_time

            # current_time = time.time()
            # if current_time - last_save_time >= 60:  # 10 minutes in seconds
            #     # Start a new thread to save the data
            #     save_process = multiprocessing.Process(target=hdf5_creator.hdf_creator, args=(copy.copy(self.variables),
            #                                 dict(self.conf), time_counter.copy(), time_ex_s.copy(),
            #                                                                           time_ex_m.copy(),
            #                                                                           time_ex_h.copy()))
            #     save_process.start()
            #     print('save data')
            #     last_save_time = current_time

            if remaining_time > 0:
                self.precise_sleep(remaining_time)
            elif remaining_time < 0:
                print(
                    f"{initialize_devices.bcolors.WARNING}Warning: Experiment loop takes longer than %s Millisecond{initialize_devices.bcolors.ENDC}" % (
                        int(1000 / self.variables.ex_freq)))
                self.log_apt.error(
                    'Experiment loop takes longer than %s (ms). It was %s (ms)' % (int(1000 / self.variables.ex_freq),
                                                                                   elapsed_time * 1000))

                print('%s- The iteration time (ms):' % index_time, elapsed_time * 1000)
                index_time += 1

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
                                                                 self.variables.main_v_dc_dld_surface_concept,
                                                                 self.variables.main_p_dld_surface_concept]):
                self.log_apt.warning('dld data have not same length')

            if all(len(lst) == len(self.variables.channel) for lst in [self.variables.channel, self.variables.time_data,
                                                                       self.variables.tdc_start_counter,
                                                                       self.variables.main_v_dc_tdc_surface_concept,
                                                                       self.variables.main_p_tdc_surface_concept]):
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
        subject = 'Experiment {} Report'.format(self.variables.hdf5_data_name)
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
        self.log_apt.info('Variables and devices are cleared and deinitialized')

    def clear_up(self):
        """
        Clear class variables, deinitialize high voltage and pulser, and reset variables.

        This method performs the cleanup operations at the end of the experiment. It turns off the high voltage,
        pulser, and signal generator, resets global variables, and performs other cleanup tasks.

        Returns:
            None
        """

        def cleanup_variables():
            """
            Reset all the global variables.
            """
            self.variables.stop_flag = False
            self.variables.end_experiment = False
            self.variables.start_flag = False
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
            self.variables.main_v_dc_dld_surface_concept = []
            self.variables.main_p_dld_surface_concept = []
            self.variables.main_v_dc_tdc_surface_concept = []
            self.variables.main_p_tdc_surface_concept = []
            self.variables.main_v_dc_tdc_roentdek = []
            self.variables.main_p_tdc_roentdek = []

        self.log_apt.info('Starting cleanup')

        if self.conf['v_dc'] != "off":
            # Turn off the v_dc
            self.command_v_dc('F0')
            self.com_port_v_dc.close()

        if self.conf['v_p'] != "off":
            # Turn off the v_p
            self.com_port_v_p.write('VOLT 0')
            self.com_port_v_p.write('OUTPut OFF')
            self.com_port_v_p.close()

        if self.conf['signal_generator'] != "off":
            # Turn off the signal generator
            signal_generator.turn_off_signal_generator()

        # Reset variables
        cleanup_variables()
        self.log_apt.info('Cleanup is finished')
