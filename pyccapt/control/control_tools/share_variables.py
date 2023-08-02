"""
This is the main script of all global variables.
"""

import numpy as np


class Variables:
    def __init__(self, conf):
        """
        Initializing of global variables function
        """
        # Device Ports
        self.COM_PORT_cryo = conf['COM_PORT_cryo']
        self.COM_PORT_V_dc = conf['COM_PORT_V_dc']
        self.COM_PORT_V_p = conf['COM_PORT_V_p']
        self.COM_PORT_gauge_mc = conf['COM_PORT_gauge_mc']
        self.COM_PORT_gauge_bc = conf['COM_PORT_gauge_bc']
        self.COM_PORT_gauge_ll = conf['COM_PORT_gauge_ll']
        self.COM_PORT_signal_generator = conf["COM_PORT_signal_generator"]
        self.COM_PORT_thorlab_motor = conf["COM_PORT_thorlab_motor"]

        # Setup parameters
        self.counter_source = 'pulse_counter'
        self.counter = 0
        self.ex_time = 0
        self.max_ions = 0
        self.ex_freq = 0
        self.user_name = ''
        self.vdc_min = 0
        self.vdc_max = 0
        self.vdc_step_up = 0
        self.vdc_step_down = 0
        self.v_p_min = 0
        self.v_p_max = 0
        self.pulse_fraction = 0
        self.pulse_frequency = 0
        self.pulse_amp_per_supply_voltage = 3500 / 160
        self.cycle_avg = 0
        self.hdf5_path = ''
        self.flag_main_gate = False
        self.flag_load_gate = False
        self.flag_cryo_gate = False
        self.hit_display = 0
        self.email = ''
        self.tweet = False
        self.light = False
        self.alignment_window = False
        self.light_swich = False
        self.vol_fix = False
        self.camera_0_ExposureTime = 2000
        self.camera_1_ExposureTime = 2000
        self.img0_orig = np.ones((500, 500, 3), dtype=np.uint8)
        self.img0_zoom = np.ones((1200, 500, 3), dtype=np.uint8)
        self.img1_orig = np.ones((500, 500, 3), dtype=np.uint8)
        self.img1_zoom = np.ones((1200, 500, 3), dtype=np.uint8)
        self.path = ''
        self.index_save_image = 0
        self.flag_pump_load_lock = True
        self.flag_pump_load_lock_click = False
        self.flag_pump_load_lock_led = None
        self.sample_adjust = False
        self.criteria_time = True
        self.criteria_ions = True
        self.criteria_vdc = True
        self.criteria_laser = True
        self.point_size_detec_map = 1
        self.exp_name = ''
        self.log_path = ''
        self.log = False
        self.fixed_laser = 0
        self.laser_num_ions_per_step = 0
        self.laser_increase_per_step = 0
        self.laser_start = 0
        self.laser_stop = 0

        # Run statistics
        self.elapsed_time = 0.0
        self.start_time = ''
        self.end_time = ''
        self.total_ions = 0
        self.specimen_voltage = 0.0
        self.detection_rate = 0.0
        self.detection_rate_elapsed = 0.0
        self.pulse_voltage = 0.0
        self.pulse_voltage_min = 0.0
        self.pulse_voltage_max = 0.0
        self.count_last = 0
        self.count_temp = 0
        self.avg_n_count = 0
        self.index_plot = 0
        self.index_plot_save = 0
        self.index_wait_on_plot_start = 0
        self.index_plot_temp = 0
        self.index_warning_message = 0
        self.index_auto_scale_graph = 0
        self.index_line = 0
        self.stop_flag = False
        self.end_experiment = False
        self.start_flag = False
        self.plot_clear_flag = False
        self.temperature = 0
        self.vacuum_main = 0
        self.vacuum_buffer = 0
        self.vacuum_buffer_backing = 0
        self.vacuum_load_lock = 0
        self.vacuum_load_lock_backing = 0

        self.laser_degree = 0

        self.x = []
        self.y = []
        self.t = []
        self.dld_start_counter = []
        self.time_stamp = []

        self.laser_intensity = []

        self.channel = []
        self.time_data = []
        self.tdc_start_counter = []

        self.ch0_time = []
        self.ch0_wave = []
        self.ch1_time = []
        self.ch1_wave = []
        self.ch2_time = []
        self.ch2_wave = []
        self.ch3_time = []
        self.ch3_wave = []

        self.ch0 = []
        self.ch1 = []
        self.ch2 = []
        self.ch3 = []
        self.ch4 = []
        self.ch5 = []
        self.ch6 = []
        self.ch7 = []
