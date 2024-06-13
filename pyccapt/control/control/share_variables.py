import multiprocessing


class Variables:
    """
    Global variables class for experiment setup, statistics, and data.
    """

    def __init__(self, conf, namespace):
        """
        Initialize the global variables.

        Args:
            conf (dict): Configuration dictionary containing various settings.

        Returns:
            None
        """
        self.ns = namespace
        self.lock = multiprocessing.Lock()
        self.lock_lists = multiprocessing.Lock()
        self.lock_data_plot = multiprocessing.Lock()
        self.lock_exp = multiprocessing.Lock()
        self.lock_vacuum_tmp = multiprocessing.Lock()
        ### Device Ports
        self.ns.COM_PORT_cryo = conf['COM_PORT_cryo']
        self.ns.COM_PORT_V_dc = conf['COM_PORT_V_dc']
        self.ns.COM_PORT_V_p = conf['COM_PORT_V_p']
        self.ns.COM_PORT_gauge_mc = conf['COM_PORT_gauge_mc']
        self.ns.COM_PORT_gauge_bc = conf['COM_PORT_gauge_bc']
        self.ns.COM_PORT_gauge_ll = conf['COM_PORT_gauge_ll']
        self.ns.COM_PORT_gauge_cll = conf['COM_PORT_gauge_cll']
        self.ns.COM_PORT_signal_generator = conf["COM_PORT_signal_generator"]
        self.ns.COM_PORT_thorlab_motor = conf["COM_PORT_thorlab_motor"]

        self.ns.save_meta_interval_camera = conf['save_meta_interval_camera']
        self.ns.save_meta_interval_visualization = conf['save_meta_interval_visualization']

        ### Setup parameters
        # self.lock_setup_parameters = threading.Lock()
        self.ns.counter_source = 'pulse_counter'
        self.ns.counter = 0
        self.ns.ex_time = 0
        self.ns.max_ions = 0
        self.ns.ex_freq = 0
        self.ns.user_name = ''
        self.ns.vdc_min = 0
        self.ns.vdc_max = 0
        self.ns.vdc_step_up = 0
        self.ns.vdc_step_down = 0
        self.ns.v_p_min = 0
        self.ns.v_p_max = 0
        self.ns.pulse_fraction = 0
        self.ns.pulse_frequency = 0
        # It is the pulse amplitude per supply voltage.
        # You have to base on your own setup to change this value.
        self.ns.pulse_amp_per_supply_voltage = conf[
            'pulse_amp_per_supply_voltage']  # It is the pulse amplitude per supply voltage.
        self.ns.hdf5_path = ''
        self.ns.flag_main_gate = False
        self.ns.flag_load_gate = False
        self.ns.flag_cryo_gate = False
        self.ns.hit_display = 0
        self.ns.email = ''
        self.ns.light = False
        self.ns.alignment_window = False
        self.ns.light_switch = False
        self.ns.vdc_hold = False
        self.ns.reset_heatmap = False
        self.ns.camera_0_ExposureTime = 2000
        self.ns.camera_1_ExposureTime = 2000
        self.ns.path = ''
        self.ns.path_meta = ''
        self.ns.index_save_image = 0
        self.ns.flag_pump_load_lock = True
        self.ns.flag_pump_load_lock_click = False
        self.ns.flag_pump_load_lock_led = None
        self.ns.flag_pump_cryo_load_lock = True
        self.ns.flag_pump_cryo_load_lock_click = False
        self.ns.flag_pump_cryo_load_lock_led = None
        self.ns.flag_camera_grab = False
        self.ns.flag_camera_win_show = False
        self.ns.flag_visualization_win_show = False
        self.ns.flag_end_experiment = False
        self.ns.flag_new_min_voltage = False
        self.ns.flag_visualization_start = False
        self.ns.flag_pumps_vacuum_start = False
        self.ns.criteria_time = True
        self.ns.criteria_ions = True
        self.ns.criteria_vdc = True
        self.ns.criteria_laser = True
        self.ns.exp_name = ''
        self.ns.log_path = ''
        self.ns.fixed_laser = 0
        self.ns.laser_num_ions_per_step = 0
        self.ns.laser_increase_per_step = 0
        self.ns.laser_start = 0
        self.ns.laser_stop = 0

        ### Run statistics
        # self.lock_statistics = threading.Lock()
        self.ns.elapsed_time = 0.0
        self.ns.start_time = ''
        self.ns.end_time = ''
        self.ns.total_ions = 0
        self.ns.specimen_voltage = 0.0
        self.ns.specimen_voltage_plot = 0.0
        self.ns.detection_rate = 0.0
        self.ns.detection_rate_current = 0.0
        self.ns.detection_rate_current_plot = 0.0
        self.ns.pulse_voltage = 0.0
        self.ns.control_algorithm = ''
        self.ns.pulse_mode = ''
        self.ns.count_last = 0
        self.ns.count_temp = 0
        self.ns.avg_n_count = 0
        self.ns.index_warning_message = 0
        self.ns.index_line = 0
        self.ns.stop_flag = False
        self.ns.end_experiment = False
        self.ns.start_flag = False
        self.ns.flag_stop_tdc = False
        self.ns.flag_finished_tdc = False
        self.ns.flag_tdc_failure = False
        self.ns.plot_clear_flag = False
        self.ns.clear_index_save_image = False
        self.ns.hitmap_plot_size = 1.0
        self.ns.number_of_experiment_in_text_line = 0
        self.ns.index_experiment_in_text_line = 0
        self.ns.flag_cameras_take_screenshot = False
        self.ns.temperature = 0
        self.ns.set_temperature = 0
        self.ns.set_temperature_flag = None
        self.ns.vacuum_main = 0
        self.ns.vacuum_buffer = 0
        self.ns.vacuum_buffer_backing = 0
        self.ns.vacuum_load_lock = 0
        self.ns.vacuum_load_lock_backing = 0

        ### Experiment variables
        # self.lock_experiment_variables = threading.Lock()
        self.ns.main_v_dc = []
        self.ns.main_counter = []
        self.ns.main_temperature = []
        self.ns.main_chamber_vacuum = []
        self.ns.laser_degree = []

        ### Data for saving
        self.ns.x = []
        self.ns.y = []
        self.ns.t = []

        self.ns.dld_start_counter = []
        self.ns.time_stamp = []
        self.ns.laser_intensity = []
        self.ns.laser_pulse_energy = 0
        self.ns.laser_power = 0
        self.ns.laser_freq = 0
        self.ns.laser_division_factor = 0
        self.ns.laser_average_power = 0

        self.ns.main_v_dc_dld = []
        self.ns.main_v_p_dld = []
        self.ns.main_l_p_dld = []
        self.ns.main_v_dc_tdc = []
        self.ns.main_v_p_tdc = []
        self.ns.main_l_p_tdc = []
        self.ns.main_v_dc_hsd = []
        self.ns.main_v_p_hsd = []
        self.ns.main_l_p_hsd = []

        self.ns.channel = []
        self.ns.time_data = []
        self.ns.tdc_start_counter = []

        self.ns.ch0_time = []
        self.ns.ch0_wave = []
        self.ns.ch1_time = []
        self.ns.ch1_wave = []
        self.ns.ch2_time = []
        self.ns.ch2_wave = []
        self.ns.ch3_time = []
        self.ns.ch3_wave = []
        self.ns.ch4_time = []
        self.ns.ch4_wave = []
        self.ns.ch5_time = []
        self.ns.ch5_wave = []

        self.ns.ch0 = []
        self.ns.ch1 = []
        self.ns.ch2 = []
        self.ns.ch3 = []
        self.ns.ch4 = []
        self.ns.ch5 = []
        self.ns.ch6 = []
        self.ns.ch7 = []

    def extend_to(self, variable_name, value):
        # Check that variable_name is an attribute of self.ns
        if not hasattr(self.ns, variable_name):
            raise ValueError(f"{variable_name} is not an attribute of the namespace.")

        current_variable = getattr(self.ns, variable_name)

        # Check that current_variable is a list
        if not isinstance(current_variable, list):
            raise TypeError(f"{variable_name} is not a list.")

        with self.lock_lists:
            current_variable.extend(value)
            setattr(self.ns, variable_name, current_variable)

    def clear_to(self, variable_name):
        with self.lock_lists:
            setattr(self.ns, variable_name, [])

    @property
    def COM_PORT_cryo(self):
        return self.ns.COM_PORT_cryo

    @COM_PORT_cryo.setter
    def COM_PORT_cryo(self, value):
        with self.lock:
            self.ns.COM_PORT_cryo = value

    @property
    def COM_PORT_V_dc(self):
        return self.ns.COM_PORT_V_dc

    @COM_PORT_V_dc.setter
    def COM_PORT_V_dc(self, value):
        with self.lock:
            self.ns.COM_PORT_V_dc = value

    @property
    def COM_PORT_V_p(self):
        return self.ns.COM_PORT_V_p

    @COM_PORT_V_p.setter
    def COM_PORT_V_p(self, value):
        with self.lock:
            self.ns.COM_PORT_V_p = value

    @property
    def COM_PORT_gauge_mc(self):
        return self.ns.COM_PORT_gauge_mc

    @COM_PORT_gauge_mc.setter
    def COM_PORT_gauge_mc(self, value):
        with self.lock:
            self.ns.COM_PORT_gauge_mc = value

    @property
    def COM_PORT_gauge_bc(self):
        return self.ns.COM_PORT_gauge_bc

    @COM_PORT_gauge_bc.setter
    def COM_PORT_gauge_bc(self, value):
        with self.lock:
            self.ns.COM_PORT_gauge_bc = value

    @property
    def COM_PORT_gauge_ll(self):
        return self.ns.COM_PORT_gauge_ll

    @COM_PORT_gauge_ll.setter
    def COM_PORT_gauge_ll(self, value):
        with self.lock:
            self.ns.COM_PORT_gauge_ll = value

    @property
    def COM_PORT_gauge_cll(self):
        return self.ns.COM_PORT_gauge_cll

    @COM_PORT_gauge_cll.setter
    def COM_PORT_gauge_cll(self, value):
        with self.lock:
            self.ns.COM_PORT_gauge_cll = value

    @property
    def COM_PORT_signal_generator(self):
        return self.ns.COM_PORT_signal_generator

    @COM_PORT_signal_generator.setter
    def COM_PORT_signal_generator(self, value):
        with self.lock:
            self.ns.COM_PORT_signal_generator = value

    @property
    def COM_PORT_thorlab_motor(self):
        return self.ns.COM_PORT_thorlab_motor

    @COM_PORT_thorlab_motor.setter
    def COM_PORT_thorlab_motor(self, value):
        with self.lock:
            self.ns.COM_PORT_thorlab_motor = value

    @property
    def save_meta_interval_camera(self):
        return self.ns.save_meta_interval_camera

    @save_meta_interval_camera.setter
    def save_meta_interval_camera(self, value):
        with self.lock:
            self.ns.save_meta_interval_camera = value

    @property
    def save_meta_interval_visualization(self):
        return self.ns.save_meta_interval_visualization

    @save_meta_interval_visualization.setter
    def save_meta_interval_visualization(self, value):
        with self.lock:
            self.ns.save_meta_interval_visualization = value

    @property
    def counter_source(self):
        return self.ns.counter_source

    @counter_source.setter
    def counter_source(self, value):
        with self.lock:
            self.ns.counter_source = value

    @property
    def counter(self):
        return self.ns.counter

    @counter.setter
    def counter(self, value):
        with self.lock:
            self.ns.counter = value

    @property
    def ex_time(self):
        return self.ns.ex_time

    @ex_time.setter
    def ex_time(self, value):
        with self.lock:
            self.ns.ex_time = value

    @property
    def max_ions(self):
        return self.ns.max_ions

    @max_ions.setter
    def max_ions(self, value):
        with self.lock:
            self.ns.max_ions = value

    @property
    def ex_freq(self):
        return self.ns.ex_freq

    @ex_freq.setter
    def ex_freq(self, value):
        with self.lock:
            self.ns.ex_freq = value

    @property
    def user_name(self):
        return self.ns.user_name

    @user_name.setter
    def user_name(self, value):
        with self.lock:
            self.ns.user_name = value

    @property
    def vdc_min(self):
        return self.ns.vdc_min

    @vdc_min.setter
    def vdc_min(self, value):
        with self.lock:
            self.ns.vdc_min = value

    @property
    def vdc_max(self):
        return self.ns.vdc_max

    @vdc_max.setter
    def vdc_max(self, value):
        with self.lock:
            self.ns.vdc_max = value

    @property
    def vdc_step_up(self):
        return self.ns.vdc_step_up

    @vdc_step_up.setter
    def vdc_step_up(self, value):
        with self.lock:
            self.ns.vdc_step_up = value

    @property
    def vdc_step_down(self):
        return self.ns.vdc_step_down

    @vdc_step_down.setter
    def vdc_step_down(self, value):
        with self.lock:
            self.ns.vdc_step_down = value

    @property
    def v_p_min(self):
        return self.ns.v_p_min

    @v_p_min.setter
    def v_p_min(self, value):
        with self.lock:
            self.ns.v_p_min = value

    @property
    def v_p_max(self):
        return self.ns.v_p_max

    @v_p_max.setter
    def v_p_max(self, value):
        with self.lock:
            self.ns.v_p_max = value

    @property
    def pulse_fraction(self):
        return self.ns.pulse_fraction

    @pulse_fraction.setter
    def pulse_fraction(self, value):
        with self.lock:
            self.ns.pulse_fraction = value

    @property
    def pulse_frequency(self):
        return self.ns.pulse_frequency

    @pulse_frequency.setter
    def pulse_frequency(self, value):
        with self.lock:
            self.ns.pulse_frequency = value

    @property
    def pulse_amp_per_supply_voltage(self):
        return self.ns.pulse_amp_per_supply_voltage

    @pulse_amp_per_supply_voltage.setter
    def pulse_amp_per_supply_voltage(self, value):
        with self.lock:
            self.ns.pulse_amp_per_supply_voltage = value

    @property
    def hdf5_path(self):
        return self.ns.hdf5_path

    @hdf5_path.setter
    def hdf5_path(self, value):
        with self.lock:
            self.ns.hdf5_path = value

    @property
    def flag_main_gate(self):
        return self.ns.flag_main_gate

    @flag_main_gate.setter
    def flag_main_gate(self, value):
        with self.lock:
            self.ns.flag_main_gate = value

    @property
    def flag_load_gate(self):
        return self.ns.flag_load_gate

    @flag_load_gate.setter
    def flag_load_gate(self, value):
        with self.lock:
            self.ns.flag_load_gate = value

    @property
    def flag_cryo_gate(self):
        return self.ns.flag_cryo_gate

    @flag_cryo_gate.setter
    def flag_cryo_gate(self, value):
        with self.lock:
            self.ns.flag_cryo_gate = value

    @property
    def hit_display(self):
        return self.ns.hit_display

    @hit_display.setter
    def hit_display(self, value):
        with self.lock:
            self.ns.hit_display = value

    @property
    def email(self):
        return self.ns.email

    @email.setter
    def email(self, value):
        with self.lock:
            self.ns.email = value

    @property
    def light(self):
        return self.ns.light

    @light.setter
    def light(self, value):
        with self.lock:
            self.ns.light = value

    @property
    def alignment_window(self):
        return self.ns.alignment_window

    @alignment_window.setter
    def alignment_window(self, value):
        with self.lock:
            self.ns.alignment_window = value

    @property
    def light_switch(self):
        return self.ns.light_switch

    @light_switch.setter
    def light_switch(self, value):
        with self.lock:
            self.ns.light_switch = value

    @property
    def vdc_hold(self):
        return self.ns.vdc_hold

    @vdc_hold.setter
    def vdc_hold(self, value):
        with self.lock:
            self.ns.vdc_hold = value

    @property
    def reset_heatmap(self):
        return self.ns.reset_heatmap

    @reset_heatmap.setter
    def reset_heatmap(self, value):
        with self.lock:
            self.ns.reset_heatmap = value

    @property
    def camera_0_ExposureTime(self):
        return self.ns.camera_0_ExposureTime

    @camera_0_ExposureTime.setter
    def camera_0_ExposureTime(self, value):
        with self.lock:
            self.ns.camera_0_ExposureTime = value

    @property
    def camera_1_ExposureTime(self):
        return self.ns.camera_1_ExposureTime

    @camera_1_ExposureTime.setter
    def camera_1_ExposureTime(self, value):
        with self.lock:
            self.ns.camera_1_ExposureTime = value

    @property
    def path(self):
        return self.ns.path

    @path.setter
    def path(self, value):
        with self.lock:
            self.ns.path = value

    @property
    def path_meta(self):
        return self.ns.path_meta

    @path_meta.setter
    def path_meta(self, value):
        with self.lock:
            self.ns.path_meta = value

    @property
    def index_save_image(self):
        return self.ns.index_save_image

    @index_save_image.setter
    def index_save_image(self, value):
        with self.lock:
            self.ns.index_save_image = value

    @property
    def flag_pump_load_lock(self):
        return self.ns.flag_pump_load_lock

    @flag_pump_load_lock.setter
    def flag_pump_load_lock(self, value):
        with self.lock:
            self.ns.flag_pump_load_lock = value

    @property
    def flag_pump_load_lock_click(self):
        return self.ns.flag_pump_load_lock_click

    @flag_pump_load_lock_click.setter
    def flag_pump_load_lock_click(self, value):
        with self.lock:
            self.ns.flag_pump_load_lock_click = value

    @property
    def flag_pump_load_lock_led(self):
        return self.ns.flag_pump_load_lock_led

    @flag_pump_load_lock_led.setter
    def flag_pump_load_lock_led(self, value):
        with self.lock:
            self.ns.flag_pump_load_lock_led = value

    @property
    def flag_pump_cryo_load_lock(self):
        return self.ns.flag_pump_cryo_load_lock

    @flag_pump_cryo_load_lock.setter
    def flag_pump_cryo_load_lock(self, value):
        with self.lock:
            self.ns.flag_pump_cryo_load_lock = value

    @property
    def flag_pump_cryo_load_lock_click(self):
        return self.ns.flag_pump_cryo_load_lock_click

    @flag_pump_cryo_load_lock_click.setter
    def flag_pump_cryo_load_lock_click(self, value):
        with self.lock:
            self.ns.flag_pump_cryo_load_lock_click = value

    @property
    def flag_cryo_pump_load_lock_led(self):
        return self.ns.flag_cryo_pump_load_lock_led

    @flag_cryo_pump_load_lock_led.setter
    def flag_pump_cryo_load_lock_led(self, value):
        with self.lock:
            self.ns.flag_pump_cryo_load_lock_led = value

    @property
    def flag_camera_grab(self):
        return self.ns.flag_camera_grab

    @flag_camera_grab.setter
    def flag_camera_grab(self, value):
        with self.lock:
            self.ns.flag_camera_grab = value

    @property
    def flag_camera_win_show(self):
        return self.ns.flag_camera_win_show

    @flag_camera_win_show.setter
    def flag_camera_win_show(self, value):
        with self.lock:
            self.ns.flag_camera_win_show = value

    @property
    def flag_visualization_win_show(self):
        return self.ns.flag_visualization_win_show

    @flag_visualization_win_show.setter
    def flag_visualization_win_show(self, value):
        with self.lock:
            self.ns.flag_visualization_win_show = value

    @property
    def flag_end_experiment(self):
        return self.ns.flag_end_experiment

    @flag_end_experiment.setter
    def flag_end_experiment(self, value):
        with self.lock:
            self.ns.flag_end_experiment = value

    @property
    def flag_new_min_voltage(self):
        return self.ns.flag_new_min_voltage

    @flag_new_min_voltage.setter
    def flag_new_min_voltage(self, value):
        with self.lock:
            self.ns.flag_new_min_voltage = value

    @property
    def flag_visualization_start(self):
        return self.ns.flag_visualization_start

    @flag_visualization_start.setter
    def flag_visualization_start(self, value):
        with self.lock:
            self.ns.flag_visualization_start = value

    @property
    def flag_pumps_vacuum_start(self):
        return self.ns.flag_pumps_vacuum_start

    @flag_pumps_vacuum_start.setter
    def flag_pumps_vacuum_start(self, value):
        with self.lock:
            self.ns.flag_pumps_vacuum_start = value

    @property
    def criteria_time(self):
        return self.ns.criteria_time

    @criteria_time.setter
    def criteria_time(self, value):
        with self.lock:
            self.ns.criteria_time = value

    @property
    def criteria_ions(self):
        return self.ns.criteria_ions

    @criteria_ions.setter
    def criteria_ions(self, value):
        with self.lock:
            self.ns.criteria_ions = value

    @property
    def criteria_vdc(self):
        return self.ns.criteria_vdc

    @criteria_vdc.setter
    def criteria_vdc(self, value):
        with self.lock:
            self.ns.criteria_vdc = value

    @property
    def criteria_laser(self):
        return self.ns.criteria_laser

    @criteria_laser.setter
    def criteria_laser(self, value):
        with self.lock:
            self.ns.criteria_laser = value

    @property
    def exp_name(self):
        return self.ns.exp_name

    @exp_name.setter
    def exp_name(self, value):
        with self.lock:
            self.ns.exp_name = value

    @property
    def log_path(self):
        return self.ns.log_path

    @log_path.setter
    def log_path(self, value):
        with self.lock:
            self.ns.log_path = value

    @property
    def fixed_laser(self):
        return self.ns.fixed_laser

    @fixed_laser.setter
    def fixed_laser(self, value):
        with self.lock:
            self.ns.fixed_laser = value

    @property
    def laser_num_ions_per_step(self):
        return self.ns.laser_num_ions_per_step

    @laser_num_ions_per_step.setter
    def laser_num_ions_per_step(self, value):
        with self.lock:
            self.ns.laser_num_ions_per_step = value

    @property
    def laser_increase_per_step(self):
        return self.ns.laser_increase_per_step

    @laser_increase_per_step.setter
    def laser_increase_per_step(self, value):
        with self.lock:
            self.ns.laser_increase_per_step = value

    @property
    def laser_start(self):
        return self.ns.laser_start

    @laser_start.setter
    def laser_start(self, value):
        with self.lock:
            self.ns.laser_start = value

    @property
    def laser_stop(self):
        return self.ns.laser_stop

    @laser_stop.setter
    def laser_stop(self, value):
        with self.lock:
            self.ns.laser_stop = value

    @property
    def elapsed_time(self):
        return self.ns.elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, value):
        with self.lock_exp:
            self.ns.elapsed_time = value

    @property
    def start_time(self):
        return self.ns.start_time

    @start_time.setter
    def start_time(self, value):
        with self.lock:
            self.ns.start_time = value

    @property
    def end_time(self):
        return self.ns.end_time

    @end_time.setter
    def end_time(self, value):
        with self.lock:
            self.ns.end_time = value

    @property
    def total_ions(self):
        return self.ns.total_ions

    @total_ions.setter
    def total_ions(self, value):
        with self.lock_exp:
            self.ns.total_ions = value

    @property
    def specimen_voltage(self):
        return self.ns.specimen_voltage

    @specimen_voltage.setter
    def specimen_voltage(self, value):
        with self.lock_exp:
            self.ns.specimen_voltage = value

    @property
    def specimen_voltage_plot(self):
        return self.ns.specimen_voltage_plot

    @specimen_voltage_plot.setter
    def specimen_voltage_plot(self, value):
        with self.lock_data_plot:
            self.ns.specimen_voltage_plot = value

    @property
    def detection_rate(self):
        return self.ns.detection_rate

    @detection_rate.setter
    def detection_rate(self, value):
        with self.lock:
            self.ns.detection_rate = value

    @property
    def detection_rate_current(self):
        return self.ns.detection_rate_current

    @detection_rate_current.setter
    def detection_rate_current(self, value):
        with self.lock_exp:
            self.ns.detection_rate_current = value

    @property
    def detection_rate_current_plot(self):
        return self.ns.detection_rate_current_plot

    @detection_rate_current_plot.setter
    def detection_rate_current_plot(self, value):
        with self.lock_data_plot:
            self.ns.detection_rate_current_plot = value

    @property
    def pulse_voltage(self):
        return self.ns.pulse_voltage

    @pulse_voltage.setter
    def pulse_voltage(self, value):
        with self.lock_exp:
            self.ns.pulse_voltage = value

    @property
    def control_algorithm(self):
        return self.ns.control_algorithm

    @control_algorithm.setter
    def control_algorithm(self, value):
        with self.lock:
            self.ns.control_algorithm = value

    @property
    def pulse_mode(self):
        return self.ns.pulse_mode

    @pulse_mode.setter
    def pulse_mode(self, value):
        with self.lock:
            self.ns.pulse_mode = value

    @property
    def count_last(self):
        return self.ns.count_last

    @count_last.setter
    def count_last(self, value):
        with self.lock:
            self.ns.count_last = value

    @property
    def count_temp(self):
        return self.ns.count_temp

    @count_temp.setter
    def count_temp(self, value):
        with self.lock:
            self.ns.count_temp = value

    @property
    def avg_n_count(self):
        return self.ns.avg_n_count

    @avg_n_count.setter
    def avg_n_count(self, value):
        self.ns.avg_n_count = value


    @property
    def index_warning_message(self):
        return self.ns.index_warning_message

    @index_warning_message.setter
    def index_warning_message(self, value):
        with self.lock:
            self.ns.index_warning_message = value

    @property
    def index_line(self):
        return self.ns.index_line

    @index_line.setter
    def index_line(self, value):
        with self.lock:
            self.ns.index_line = value

    @property
    def stop_flag(self):
        return self.ns.stop_flag

    @stop_flag.setter
    def stop_flag(self, value):
        with self.lock:
            self.ns.stop_flag = value

    @property
    def end_experiment(self):
        return self.ns.end_experiment

    @end_experiment.setter
    def end_experiment(self, value):
        with self.lock:
            self.ns.end_experiment = value

    @property
    def start_flag(self):
        return self.ns.start_flag

    @start_flag.setter
    def start_flag(self, value):
        with self.lock:
            self.ns.start_flag = value

    @property
    def flag_stop_tdc(self):
        return self.ns.flag_stop_tdc

    @flag_stop_tdc.setter
    def flag_stop_tdc(self, value):
        with self.lock:
            self.ns.flag_stop_tdc = value

    @property
    def flag_finished_tdc(self):
        return self.ns.flag_finished_tdc

    @flag_finished_tdc.setter
    def flag_finished_tdc(self, value):
        with self.lock:
            self.ns.flag_finished_tdc = value

    @property
    def flag_tdc_failure(self):
        return self.ns.flag_tdc_failure

    @flag_tdc_failure.setter
    def flag_tdc_failure(self, value):
        with self.lock:
            self.ns.flag_tdc_failure = value

    @property
    def plot_clear_flag(self):
        return self.ns.plot_clear_flag

    @plot_clear_flag.setter
    def plot_clear_flag(self, value):
        with self.lock:
            self.ns.plot_clear_flag = value

    @property
    def clear_index_save_image(self):
        return self.ns.clear_index_save_image

    @clear_index_save_image.setter
    def clear_index_save_image(self, value):
        with self.lock:
            self.ns.clear_index_save_image = value

    @property
    def hitmap_plot_size(self):
        return self.ns.hitmap_plot_size

    @hitmap_plot_size.setter
    def hitmap_plot_size(self, value):
        with self.lock:
            self.ns.hitmap_plot_size = value

    @property
    def number_of_experiment_in_text_line(self):
        return self.ns.number_of_experiment_in_text_line

    @number_of_experiment_in_text_line.setter
    def number_of_experiment_in_text_line(self, value):
        with self.lock:
            self.ns.number_of_experiment_in_text_line = value

    @property
    def index_experiment_in_text_line(self):
        return self.ns.index_experiment_in_text_line

    @index_experiment_in_text_line.setter
    def index_experiment_in_text_line(self, value):
        with self.lock:
            self.ns.index_experiment_in_text_line = value


    @property
    def flag_cameras_take_screenshot(self):
        return self.ns.flag_cameras_take_screenshot

    @flag_cameras_take_screenshot.setter
    def flag_cameras_take_screenshot(self, value):
        with self.lock:
            self.ns.flag_cameras_take_screenshot = value

    @property
    def temperature(self):
        return self.ns.temperature

    @temperature.setter
    def temperature(self, value):
        with self.lock_vacuum_tmp:
            self.ns.temperature = value

    @property
    def set_temperature(self):
        return self.ns.set_temperature

    @set_temperature.setter
    def set_temperature(self, value):
        with self.lock_vacuum_tmp:
            self.ns.set_temperature = value

    @property
    def set_temperature_flag(self):
        return self.ns.set_temperature_flag

    @set_temperature_flag.setter
    def set_temperature_flag(self, value):
        with self.lock_vacuum_tmp:
            self.ns.set_temperature_flag = value

    @property
    def vacuum_main(self):
        return self.ns.vacuum_main

    @vacuum_main.setter
    def vacuum_main(self, value):
        with self.lock_vacuum_tmp:
            self.ns.vacuum_main = value

    @property
    def vacuum_buffer(self):
        return self.ns.vacuum_buffer

    @vacuum_buffer.setter
    def vacuum_buffer(self, value):
        with self.lock_vacuum_tmp:
            self.ns.vacuum_buffer = value

    @property
    def vacuum_buffer_backing(self):
        return self.ns.vacuum_buffer_backing

    @vacuum_buffer_backing.setter
    def vacuum_buffer_backing(self, value):
        with self.lock_vacuum_tmp:
            self.ns.vacuum_buffer_backing = value

    @property
    def vacuum_load_lock(self):
        return self.ns.vacuum_load_lock

    @vacuum_load_lock.setter
    def vacuum_load_lock(self, value):
        with self.lock_vacuum_tmp:
            self.ns.vacuum_load_lock = value

    @property
    def vacuum_load_lock_backing(self):
        return self.ns.vacuum_load_lock_backing

    @vacuum_load_lock_backing.setter
    def vacuum_load_lock_backing(self, value):
        with self.lock_vacuum_tmp:
            self.ns.vacuum_load_lock_backing = value

    @property
    def main_v_dc(self):
        with self.lock_lists:
            return self.ns.main_v_dc

    @main_v_dc.setter
    def main_v_dc(self, value):
        with self.lock_lists:
            self.ns.main_v_dc = value


    @property
    def main_counter(self):
        with self.lock_lists:
            return self.ns.main_counter

    @main_counter.setter
    def main_counter(self, value):
        with self.lock_lists:
            self.ns.main_counter = value

    @property
    def main_temperature(self):
        with self.lock_lists:
            return self.ns.main_temperature

    @main_temperature.setter
    def main_temperature(self, value):
        with self.lock_lists:
            self.ns.main_temperature = value

    @property
    def main_chamber_vacuum(self):
        with self.lock_lists:
            return self.ns.main_chamber_vacuum

    @main_chamber_vacuum.setter
    def main_chamber_vacuum(self, value):
        with self.lock_lists:
            self.ns.main_chamber_vacuum = value

    @property
    def main_v_p_hsd(self):
        with self.lock_lists:
            return self.ns.main_v_p_hsd

    @main_v_p_hsd.setter
    def main_v_p_hsd(self, value):
        with self.lock_lists:
            self.ns.main_v_p_hsd = value

    @property
    def main_l_p_hsd(self):
        with self.lock_lists:
            return self.ns.main_l_p_hsd

    @main_l_p_hsd.setter
    def main_l_p_hsd(self, value):
        with self.lock_lists:
            self.ns.main_l_p_hsd = value

    @property
    def laser_degree(self):
        with self.lock_lists:
            return self.ns.laser_degree

    @laser_degree.setter
    def laser_degree(self, value):
        with self.lock_lists:
            self.ns.laser_degree = value


    @property
    def x(self):
        with self.lock_lists:
            return self.ns.x

    @x.setter
    def x(self, value):
        with self.lock_lists:
            self.ns.x = value

    @property
    def y(self):
        with self.lock_lists:
            return self.ns.y

    @y.setter
    def y(self, value):
        with self.lock_lists:
            self.ns.y = value

    @property
    def t(self):
        with self.lock_lists:
            return self.ns.t

    @t.setter
    def t(self, value):
        with self.lock_lists:
            self.ns.t = value

    @property
    def dld_start_counter(self):
        with self.lock_lists:
            return self.ns.dld_start_counter

    @dld_start_counter.setter
    def dld_start_counter(self, value):
        with self.lock_lists:
            self.ns.dld_start_counter = value

    @property
    def time_stamp(self):
        with self.lock_lists:
            return self.ns.time_stamp

    @time_stamp.setter
    def time_stamp(self, value):
        with self.lock_lists:
            self.ns.time_stamp = value

    @property
    def laser_intensity(self):
        with self.lock_lists:
            return self.ns.laser_intensity

    @laser_intensity.setter
    def laser_intensity(self, value):
        with self.lock_lists:
            self.ns.laser_intensity = value

    @property
    def laser_pulse_energy(self):
        with self.lock_lists:
            return self.ns.laser_pulse_energy

    @laser_pulse_energy.setter
    def laser_pulse_energy(self, value):
        with self.lock_lists:
            self.ns.laser_pulse_energy = value

    @property
    def laser_power(self):
        with self.lock_lists:
            return self.ns.laser_power

    @laser_power.setter
    def laser_power(self, value):
        with self.lock_lists:
            self.ns.laser_power = value

    @property
    def laser_freq(self):
        with self.lock_lists:
            return self.ns.laser_freq

    @laser_freq.setter
    def laser_freq(self, value):
        with self.lock_lists:
            self.ns.laser_freq = value

    @property
    def laser_division_factor(self):
        with self.lock_lists:
            return self.ns.laser_division_factor

    @laser_division_factor.setter
    def laser_division_factor(self, value):
        with self.lock_lists:
            self.ns.laser_division_factor = value

    @property
    def laser_average_power(self):
        with self.lock_lists:
            return self.ns.laser_average_power

    @laser_average_power.setter
    def laser_average_power(self, value):
        with self.lock_lists:
            self.ns.laser_average_power = value

    @property
    def main_v_dc_dld(self):
        with self.lock_lists:
            return self.ns.main_v_dc_dld

    @main_v_dc_dld.setter
    def main_v_dc_dld(self, value):
        with self.lock_lists:
            self.ns.main_v_dc_dld = value

    @property
    def main_v_p_dld(self):
        with self.lock_lists:
            return self.ns.main_v_p_dld

    @main_v_p_dld.setter
    def main_v_p_dld(self, value):
        with self.lock_lists:
            self.ns.main_v_p_dld = value

    @property
    def main_l_p_dld(self):
        with self.lock_lists:
            return self.ns.main_l_p_dld

    @main_l_p_dld.setter
    def main_l_p_dld(self, value):
        with self.lock_lists:
            self.ns.main_l_p_dld = value

    @property
    def main_v_dc_tdc(self):
        with self.lock_lists:
            return self.ns.main_v_dc_tdc

    @main_v_dc_tdc.setter
    def main_v_dc_tdc(self, value):
        with self.lock_lists:
            self.ns.main_v_dc_tdc = value

    @property
    def main_v_p_tdc(self):
        with self.lock_lists:
            return self.ns.main_v_p_tdc

    @main_v_p_tdc.setter
    def main_v_p_tdc(self, value):
        with self.lock_lists:
            self.ns.main_v_p_tdc = value

    @property
    def main_l_p_tdc(self):
        with self.lock_lists:
            return self.ns.main_l_p_tdc

    @main_l_p_tdc.setter
    def main_l_p_tdc(self, value):
        with self.lock_lists:
            self.ns.main_l_p_tdc = value

    @property
    def main_v_dc_hsd(self):
        with self.lock_lists:
            return self.ns.main_v_dc_hsd

    @main_v_dc_hsd.setter
    def main_v_dc_hsd(self, value):
        with self.lock_lists:
            self.ns.main_v_dc_hsd = value


    @property
    def channel(self):
        with self.lock_lists:
            return self.ns.channel

    @channel.setter
    def channel(self, value):
        with self.lock_lists:
            self.ns.channel = value

    @property
    def time_data(self):
        with self.lock_lists:
            return self.ns.time_data

    @time_data.setter
    def time_data(self, value):
        with self.lock_lists:
            self.ns.time_data = value

    @property
    def tdc_start_counter(self):
        with self.lock_lists:
            return self.ns.tdc_start_counter

    @tdc_start_counter.setter
    def tdc_start_counter(self, value):
        with self.lock_lists:
            self.ns.tdc_start_counter = value

    @property
    def ch0_time(self):
        with self.lock_lists:
            return self.ns.ch0_time

    @ch0_time.setter
    def ch0_time(self, value):
        with self.lock_lists:
            self.ns.ch0_time = value

    @property
    def ch0_wave(self):
        with self.lock_lists:
            return self.ns.ch0_wave

    @ch0_wave.setter
    def ch0_wave(self, value):
        with self.lock_lists:
            self.ns.ch0_wave = value

    @property
    def ch1_time(self):
        with self.lock_lists:
            return self.ns.ch1_time

    @ch1_time.setter
    def ch1_time(self, value):
        with self.lock_lists:
            self.ns.ch1_time = value

    @property
    def ch1_wave(self):
        with self.lock_lists:
            return self.ns.ch1_wave

    @ch1_wave.setter
    def ch1_wave(self, value):
        with self.lock_lists:
            self.ns.ch1_wave = value

    @property
    def ch2_time(self):
        with self.lock_lists:
            return self.ns.ch2_time

    @ch2_time.setter
    def ch2_time(self, value):
        with self.lock_lists:
            self.ns.ch2_time = value

    @property
    def ch2_wave(self):
        with self.lock_lists:
            return self.ns.ch2_wave

    @ch2_wave.setter
    def ch2_wave(self, value):
        with self.lock_lists:
            self.ns.ch2_wave = value

    @property
    def ch3_time(self):
        with self.lock_lists:
            return self.ns.ch3_time

    @ch3_time.setter
    def ch3_time(self, value):
        with self.lock_lists:
            self.ns.ch3_time = value

    @property
    def ch3_wave(self):
        with self.lock_lists:
            return self.ns.ch3_wave

    @ch3_wave.setter
    def ch3_wave(self, value):
        with self.lock_lists:
            self.ns.ch3_wave = value

    @property
    def ch4_time(self):
        with self.lock_lists:
            return self.ns.ch4_time

    @ch4_time.setter
    def ch4_time(self, value):
        with self.lock_lists:
            self.ns.ch4_time = value

    @property
    def ch4_wave(self):
        with self.lock_lists:
            return self.ns.ch4_wave

    @ch4_wave.setter
    def ch4_wave(self, value):
        with self.lock_lists:
            self.ns.ch4_wave = value

    @property
    def ch5_time(self):
        with self.lock_lists:
            return self.ns.ch5_time

    @ch5_time.setter
    def ch5_time(self, value):
        with self.lock_lists:
            self.ns.ch5_time = value

    @property
    def ch5_wave(self):
        with self.lock_lists:
            return self.ns.ch5_wave

    @ch5_wave.setter
    def ch5_wave(self, value):
        with self.lock_lists:
            self.ns.ch5_wave = value

    @property
    def ch0(self):
        with self.lock_lists:
            return self.ns.ch0

    @ch0.setter
    def ch0(self, value):
        with self.lock_lists:
            self.ns.ch0 = value

    @property
    def ch1(self):
        with self.lock_lists:
            return self.ns.ch1

    @ch1.setter
    def ch1(self, value):
        with self.lock_lists:
            self.ns.ch1 = value

    @property
    def ch2(self):
        with self.lock_lists:
            return self.ns.ch2

    @ch2.setter
    def ch2(self, value):
        with self.lock_lists:
            self.ns.ch2 = value

    @property
    def ch3(self):
        with self.lock_lists:
            return self.ns.ch3

    @ch3.setter
    def ch3(self, value):
        with self.lock_lists:
            self.ns.ch3 = value

    @property
    def ch4(self):
        with self.lock_lists:
            return self.ns.ch4

    @ch4.setter
    def ch4(self, value):
        with self.lock_lists:
            self.ns.ch4 = value

    @property
    def ch5(self):
        with self.lock_lists:
            return self.ns.ch5

    @ch5.setter
    def ch5(self, value):
        with self.lock_lists:
            self.ns.ch5 = value

    @property
    def ch6(self):
        with self.lock_lists:
            return self.ns.ch6

    @ch6.setter
    def ch6(self, value):
        with self.lock_lists:
            self.ns.ch6 = value

    @property
    def ch7(self):
        with self.lock_lists:
            return self.ns.ch7

    @ch7.setter
    def ch7(self, value):
        with self.lock_lists:
            self.ns.ch7 = value
