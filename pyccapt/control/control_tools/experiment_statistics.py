def save_statistics_apt(variables):
	"""
	Save setup parameters and run statistics in a text file.

	Args:
		variables (object): An object containing experiment variables.

	Returns:
		None
	"""
	# Save setup parameters and run statistics in a text file
	# with variables.lock_setup_parameters and variables.lock_statistics:
	with open(variables.path + '\\parameters.txt', 'w') as f:
		f.write('Username: ' + variables.user_name + '\n')
		f.write('Experiment Name: ' + variables.hdf5_path + '\n')
		f.write('Detection Rate (%s): %s\n' % ('%', variables.detection_rate))
		f.write('Maximum Number of Ions: %s\n' % variables.max_ions)
		f.write('Counter source: %s\n' % variables.counter_source)
		f.write('Experiment Control Refresh freq. (Hz): %s\n' % variables.ex_freq)
		f.write('K_p Upwards: %s\n' % variables.vdc_step_up)
		f.write('K_p Downwards: %s\n' % variables.vdc_step_down)
		f.write('Email: ' + variables.email + '\n')
		f.write('Specimen start Voltage (V): %s\n' % variables.vdc_min)
		f.write('Specimen Stop Voltage (V): %s\n' % variables.vdc_max)
		f.write('Specimen Max Achieved Voltage (V): %s\n' % "{:.3f}".format(variables.specimen_voltage))
		if variables.pulse_mode == 'Voltage':
			f.write('Pulse start Voltage (V): %s\n' % variables.v_p_min)
			f.write('Pulse Stop Voltage (V): %s\n' % variables.v_p_max)
		f.write('Pulse Fraction (%s): %s\n' % ('%', variables.pulse_fraction))
		f.write('Specimen Max Achieved Pulse Voltage (V): %s\n' % "{:.3f}".format(variables.pulse_voltage))
		f.write('Experiment Elapsed Time (Sec): %s\n' % "{:.3f}".format(variables.elapsed_time))
		f.write('Experiment Total Ions: %s\n' % variables.total_ions)
