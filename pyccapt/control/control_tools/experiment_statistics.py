import datetime


def save_statistics_apt(variables):
    """
    Save setup parameters and run statistics in a text file.

    Args:
        variables (object): An object containing experiment variables.

    Returns:
        None
    """
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Create a header with additional information
    header = f"""
    Experiment Parameters and Statistics
    -------------------------------------------
    Experiment Timestamp: {current_datetime}
    Username: {variables.user_name}
    Email: {variables.email}
    Experiment Name: {variables.ex_name}
    Maximum Experiment Time: {variables.ex_time} seconds
    Maximum Number of Ions: {variables.max_ions}
    Control Refresh Frequency: {variables.ex_freq} Hz
    Specimen DC Voltage Range (Min-Max): {variables.vdc_min} V - {variables.vdc_max} V
    K_p Upwards: {variables.vdc_step_up}
    K_p Downwards: {variables.vdc_step_down}
    Control Algorithm: {variables.control_algorithm}
    Pulse Mode: {variables.pulse_mode}
    """
    if variables.pulse_mode == 'Voltage':
        header += f"""
        Pulse Voltage Range (Min-Max): {variables.v_p_min} V - {variables.v_p_max} V
        """

    header += f"""
    Pulse Fraction: {variables.pulse_fraction}%
    Pulse Frequency: {variables.pulse_frequency} kHz
    Detection Rate: {variables.detection_rate}%
    Counter Source: {variables.counter_source}
    -----------------------------------------------------
    """

    # Save setup parameters and run statistics in a text file
    statistics = f"""
    Experiment Elapsed Time (Sec): {variables.elapsed_time:.3f}
    Experiment Total Ions: {variables.total_ions}
    Specimen Max Achieved Voltage (V): {variables.specimen_voltage:.3f}
    Specimen Max Achieved Pulse Voltage (V): {variables.pulse_voltage:.3f}
    Last detection rate: {variables.detection_rate_current_plot:.3f}%
    -----------------------------------------------------
    """
    software_info = "Created by PyCCAPT software."

    with open(variables.path + '\\parameters.txt', 'w') as f:
        f.write(header)
        f.write(statistics)
        f.write(software_info)
