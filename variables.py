

def init():

    global ex_time
    global ex_freq
    global vdc_min
    global vdc_max
    global vdc_step
    global v_p_min
    global v_p_max
    global pulse_fraction
    global stop_flag
    global start_flag
    global pulse_frequency
    global pulse_amp_per_supply_voltage
    global cycle_avg

    global elapsed_time
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

    # Setup parameters
    ex_time = 0
    ex_freq =0
    vdc_min = 0.0
    vdc_max = 0.0
    vdc_step = 0.0
    v_p_min = 0.0
    v_p_max = 0.0
    pulse_fraction = 0
    pulse_frequency = 0
    pulse_amp_per_supply_voltage = 3500/160
    cycle_avg = 0
    hdf5_path = ''

    # Run statistics=
    elapsed_time = 0.0
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
    stop_flag = False
    start_flag = False

