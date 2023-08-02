"""
This is the script for saving the statistics of experiment in a txt file.
"""

# Local module and scripts


def save_statistics_apt_oxcart():
    # save setup parameters and run statistics in a txt file
    with open(variables.path + '\\parameters.txt', 'w') as f:
        f.write('Username: ' + variables.user_name + '\r\n')
        f.write('Experiment Name: ' + variables.hdf5_path + '\r\n')
        f.write('Detection Rate (' + chr(37) + ') : %s\r\n' % variables.detection_rate)
        f.write('Maximum Number of Ions: %s\r\n' % variables.max_ions)
        f.write('Counter source: %s\r\n' % variables.counter_source)
        f.write('Control Refresh freq. (Hz): %s\r\n' % variables.ex_freq)
        f.write('Time bins (Sec): %s\r\n' % (1 / variables.ex_freq))
        f.write('Cycle for Avg.: %s\r\n' % variables.cycle_avg)
        f.write('K_p Upwards: %s\r\n' % variables.vdc_step_up)
        f.write('K_p Downwards: %s\r\n' % variables.vdc_step_down)
        f.write('Experiment Elapsed Time (Sec): %s\r\n' % "{:.3f}".format(variables.elapsed_time))
        f.write('Experiment Total Ions: %s\r\n' % variables.total_ions)
        f.write('Email: ' + variables.email + '\r\n')
        f.write('Twitter: %s\r\n' % variables.tweet)
        f.write('Specimen start Voltage (V): %s\r\n' % variables.vdc_min)
        f.write('Specimen Stop Voltage (V): %s\r\n' % variables.vdc_max)
        f.write('Specimen Max Achieved Voltage (V): %s\r\n' % "{:.3f}".format(variables.specimen_voltage))
        f.write('Pulse start Voltage (V): %s\r\n' % variables.v_p_min)
        f.write('Pulse Stop Voltage (V): %s\r\n' % variables.v_p_max)
        f.write('Pulse Fraction (' + chr(37) + '): %s\r\n' % variables.pulse_fraction)
        f.write('Specimen Max Achieved Pulse Voltage (V): %s\r\n' % "{:.3f}".format(variables.pulse_voltage))


def save_statistics_apt_physic():
    # save setup parameters and run statistics in a txt file
    with open(variables.path + '\\parameters.txt', 'w') as f:
        f.write('Username: ' + variables.user_name + '\r\n')
        f.write('Experiment Name: ' + variables.hdf5_path + '\r\n')
        f.write('Detection Rate (' + chr(37) + ') : %s\r\n' % variables.detection_rate)
        f.write('Maximum Number of Ions: %s\r\n' % variables.max_ions)
        f.write('Counter source: %s\r\n' % variables.counter_source)
        f.write('Control Refresh freq. (Hz): %s\r\n' % variables.ex_freq)
        f.write('Time bins (Sec): %s\r\n' % (1 / variables.ex_freq))
        f.write('Cycle for Avg.: %s\r\n' % variables.cycle_avg)
        f.write('K_p Upwards: %s\r\n' % variables.vdc_step_up)
        f.write('K_p Downwards: %s\r\n' % variables.vdc_step_down)
        f.write('Experiment Elapsed Time (Sec): %s\r\n' % "{:.3f}".format(variables.elapsed_time))
        f.write('Experiment Total Ions: %s\r\n' % variables.total_ions)
        f.write('Email: ' + variables.email + '\r\n')
        f.write('Twitter: %s\r\n' % variables.tweet)
        f.write('Specimen start Voltage (V): %s\r\n' % variables.vdc_min)
        f.write('Specimen Stop Voltage (V): %s\r\n' % variables.vdc_max)
        f.write('Specimen Max Achieved Voltage (V): %s\r\n' % "{:.3f}".format(variables.specimen_voltage))
        f.write('Pulse Fraction (' + chr(37) + '): %s\r\n' % variables.pulse_fraction)
