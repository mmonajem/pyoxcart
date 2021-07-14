"""
This is the main script of all global variables.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""
import numpy as np

com_port_idx_cryovac = 3
COM_PORT_pfeiffer = 'COM5'
COM_PORT_edwards_bc = 'COM2'
COM_PORT_edwards_ll = 'COM1'
com_port_idx_V_dc = 4
com_port_idx_V_p = 0


def init():
    """
    Initializing of global variables function
    """
    # Setup parameters
    global counter_source
    global counter
    global ex_time
    global max_ions
    global ex_freq
    global vdc_min
    global vdc_max
    global vdc_step_up
    global vdc_step_down
    global v_p_min
    global v_p_max
    global pulse_fraction
    global stop_flag
    global end_experiment
    global start_flag
    global plot_clear_flag
    global pulse_frequency
    global pulse_amp_per_supply_voltage
    global cycle_avg
    global flag_main_gate
    global flag_load_gate
    global flag_cryo_gate
    global hit_display
    global email
    global tweet
    global camera_0_ExposureTime
    global camera_1_ExposureTime
    global path
    global index_save_image
    global flag_pump_load_lock
    global flag_pump_load_lock_click
    global flag_pump_load_lock_led
    global sample_adjust

    # Statistics parameters
    global elapsed_time
    global start_time
    global end_time
    global total_ions
    global specimen_voltage
    global detection_rate
    global detection_rate_elapsed
    global pulse_voltage
    global pulse_voltage_min
    global pulse_voltage_max
    global hdf5_path
    global count_last
    global count_temp
    global avg_n_count
    global index_plot
    global index_plot_save
    global index_wait_on_plot_start
    global index_plot_temp
    global index_warning_message
    global index_auto_scale_graph
    global index_line
    global light
    global light_swich
    global img0_orig
    global img0_zoom
    global img1_orig
    global img1_zoom
    global temperature
    global vacuum_main
    global vacuum_buffer
    global vacuum_buffer_backing
    global vacuum_load_lock
    global vacuum_load_lock_backing

    # DLD parameters
    global x
    global y
    global t
    global dld_start_counter
    # TDC parameters
    global channel
    global time_data
    global tdc_start_counter

    # Experiment variables
    global main_v_dc
    global main_v_p
    global main_counter
    global main_temperature
    global main_chamber_vacuum
    global main_v_dc_dld
    global main_v_p_dld
    global main_v_dc_tdc
    global main_v_p_tdc

    counter = 0
    ex_time = 0
    max_ions = 0
    ex_freq = 0
    vdc_min = 0
    vdc_max = 0
    vdc_step_up = 0
    vdc_step_down = 0
    v_p_min = 0
    v_p_max = 0
    pulse_fraction = 0
    pulse_frequency = 0
    pulse_amp_per_supply_voltage = 3500 / 160
    cycle_avg = 0
    hdf5_path = ''
    flag_main_gate = False
    flag_load_gate = False
    flag_cryo_gate = False
    hit_display = 0
    email = ''
    tweet = False
    light = False
    light_swich = False
    camera_0_ExposureTime = 2000
    camera_1_ExposureTime = 2000
    img0_orig = np.ones((500, 500, 3), dtype=np.uint8)
    img0_zoom = np.ones((1200, 500, 3), dtype=np.uint8)
    img1_orig = np.ones((500, 500, 3), dtype=np.uint8)
    img1_zoom = np.ones((1200, 500, 3), dtype=np.uint8)
    path = ''
    index_save_image = 0
    flag_pump_load_lock = True
    flag_pump_load_lock_click = False
    flag_pump_load_lock_led = None
    sample_adjust = False

    # Run statistics=
    elapsed_time = 0.0
    start_time = ''
    end_time = ''
    total_ions = 0
    specimen_voltage = 0.0
    detection_rate = 0.0
    detection_rate_elapsed = 0.0
    pulse_voltage = 0.0
    pulse_voltage_min = 0.0
    pulse_voltage_max = 0.0
    count_last = 0
    count_temp = 0
    avg_n_count = 0
    index_plot = 0
    index_plot_save = 0
    index_wait_on_plot_start = 0
    index_plot_temp = 0
    index_warning_message = 0
    index_auto_scale_graph = 0
    index_line = 0
    stop_flag = False
    end_experiment = False
    start_flag = False
    plot_clear_flag = False
    temperature = 0
    vacuum_main = 0
    vacuum_buffer = 0
    vacuum_buffer_backing = 0
    vacuum_load_lock = 0
    vacuum_load_lock_backing = 0

    x = np.zeros(0)
    y = np.zeros(0)
    t = np.zeros(0)
    dld_start_counter = np.zeros(0)

    channel = np.zeros(0)
    time_data = np.zeros(0)
    tdc_start_counter = np.zeros(0)

    # Source of calculating the detected events pulse_counter or TDC
    counter_source = 'pulse_counter'

    main_v_dc = np.zeros(0)
    main_v_p = np.zeros(0)
    main_counter = np.zeros(0)
    main_temperature = np.zeros(0)
    main_chamber_vacuum = np.zeros(0)
    main_v_dc_dld = np.zeros(0)
    main_v_p_dld = np.zeros(0)
    main_v_dc_tdc = np.zeros(0)
    main_v_p_tdc = np.zeros(0)
