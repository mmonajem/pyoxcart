def save_statistics_apt(variables):
	"""
	Save setup parameters and run statistics in a text file.

	Args:
		variables (object): An object containing experiment variables.

	Returns:
		None
	"""
	# Save setup parameters and run statistics in a text file
	with open(variables.path + '\\parameters.txt', 'w') as f:
		f.write('Username: ' + variables.user_name + '\n')
		f.write('Experiment Name: ' + variables.ex_name + '\n')
		f.write('Maximum Experiment Time: ' + variables.ex_time + '\n')
		f.write('Maximum Number of Ions: %s\n' % variables.max_ions)
		f.write('Control Refresh Frequency: %s\n' % variables.ex_freq)
		f.write('Specimen DC Min Voltage (V): %s\n' % variables.vdc_min)
		f.write('Specimen DC Max Voltage (V): %s\n' % variables.vdc_max)
		f.write('K_p Upwards: %s\n' % variables.vdc_step_up)
		f.write('K_p Downwards: %s\n' % variables.vdc_step_down)
		f.write('Control Algorithm: %s\n' % variables.control_algorithm)
		f.write('Pulse Mode: %s\n' % variables.pulse_mode)
		f.write('Pulse Min Voltage (V): %s\n' % variables.v_p_min)
		f.write('Pulse Max Voltage (V): %s\n' % variables.v_p_max)
		f.write('Pulse Fraction (%s): %s\n' % ('%', variables.pulse_fraction))
		f.write('Pulse Frequency (Khz): %s\n' % variables.pulse_frequency)
		f.write('Detection Rate (%s): %s\n' % ('%', variables.detection_rate))
		f.write('Counter source: %s\n' % variables.counter_source)
		f.write('Email: ' + variables.email + '\n')

		if variables.pulse_mode == 'Voltage':
			f.write('Pulse start Voltage (V): %s\n' % variables.v_p_min)
			f.write('Pulse Stop Voltage (V): %s\n' % variables.v_p_max)

		f.write('Experiment Elapsed Time (Sec): %s\n' % "{:.3f}".format(variables.elapsed_time))
		f.write('Experiment Total Ions: %s\n' % variables.total_ions)
		f.write('Specimen Max Achieved Voltage (V): %s\n' % "{:.3f}".format(variables.specimen_voltage))
		f.write('Specimen Max Achieved Pulse Voltage (V): %s\n' % "{:.3f}".format(variables.pulse_voltage))
		f.write('Last detection rate: %s\n' % ('%', "{:.3f}".format(variables.detection_rate_current_plot)))
