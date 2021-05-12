
import numpy as np


def init():

    global counter
    global ex_time
    global ex_freq
    global vdc_min
    global vdc_max
    global vdc_step_up
    global vdc_step_down
    global v_p_min
    global v_p_max
    global pulse_fraction
    global stop_flag
    global start_flag
    global pulse_frequency
    global pulse_amp_per_supply_voltage
    global cycle_avg
    global flag_main_gate
    global flag_load_gate
    global flag_cryo_gate
    global email
    global tweet
    global camera_0_ExposureTime
    global camera_1_ExposureTime
    global path
    global index_save_image

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
    global light
    global img0_orig
    global img0_zoom
    global img1_orig
    global img1_zoom
    global temperature

    # Setup parameters
    counter = 0
    ex_time = 0
    ex_freq =0
    vdc_min = 0.0
    vdc_max = 0.0
    vdc_step_up = 0.0
    vdc_step_down = 0.0
    v_p_min = 0.0
    v_p_max = 0.0
    pulse_fraction = 0
    pulse_frequency = 0
    pulse_amp_per_supply_voltage = 3500/160
    cycle_avg = 0
    hdf5_path = ''
    flag_main_gate = False
    flag_load_gate = False
    flag_cryo_gate = False
    email = ''
    tweet = False
    light = False
    camera_0_ExposureTime = 10000000
    camera_1_ExposureTime = 1000000
    img0_orig = np.ones((500,500,3), dtype=np.uint8)
    img0_zoom = np.ones((1200,500,3), dtype=np.uint8)
    img1_orig = np.ones((500,500,3), dtype=np.uint8)
    img1_zoom = np.ones((1200,500,3), dtype=np.uint8)
    path = ''
    index_save_image = 0

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
    stop_flag = False
    start_flag = False
    temperature = 0

