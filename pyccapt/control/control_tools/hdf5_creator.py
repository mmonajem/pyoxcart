import h5py


def hdf_creator(variables, conf, time_counter, time_ex_s, time_ex_m, time_ex_h):
	"""
	Save experiment data to an HDF5 file.

	Args:
		variables (object): An object containing experiment variables.
		conf (dict): A dictionary containing configuration settings.
		time_counter (list): A list of time counter data.
		time_ex_s (list): A list of seconds for experiment time.
		time_ex_m (list): A list of minutes for experiment time.
		time_ex_h (list): A list of hours for experiment time.

	Returns:
		None
	"""

	path = variables.path + '\\data_%s.h5' % variables.exp_name
	# Save HDF5 file
	with h5py.File(path, "w") as f:
		f.create_dataset("apt/high_voltage", data=variables.main_v_dc, dtype='f')
		f.create_dataset("apt/pulse", data=variables.main_v_p, dtype='f')
		f.create_dataset("apt/num_events", data=variables.main_counter, dtype='i')
		f.create_dataset('apt/temperature', data=variables.main_temperature, dtype='f')
		f.create_dataset('apt/main_chamber_vacuum', data=variables.main_chamber_vacuum, dtype='f')
		f.create_dataset("apt/time_counter", data=time_counter, dtype='i')

		f.create_dataset("time/time_s", data=time_ex_s, dtype='i')
		f.create_dataset("time/time_m", data=time_ex_m, dtype='i')
		f.create_dataset("time/time_h", data=time_ex_h, dtype='i')

		if conf['tdc'] == "on" and conf['tdc_model'] == 'Surface_Consept' \
				and variables.counter_source == 'TDC':
			f.create_dataset("dld/x", data=variables.x, dtype='f')
			f.create_dataset("dld/y", data=variables.y, dtype='f')
			f.create_dataset("dld/t", data=variables.t, dtype='f')
			f.create_dataset("dld/start_counter", data=variables.dld_start_counter, dtype='i')
			f.create_dataset("dld/high_voltage", data=variables.main_v_dc_dld_surface_concept, dtype='f')
			f.create_dataset("dld/pulse", data=variables.main_p_dld_surface_concept, dtype='f')
			# raw data
			f.create_dataset("tdc/start_counter", data=variables.tdc_start_counter, dtype='i')
			f.create_dataset("tdc/channel", data=variables.channel, dtype='i')
			f.create_dataset("tdc/time_data", data=variables.time_data, dtype='i')
			f.create_dataset("tdc/high_voltage", data=variables.main_v_dc_tdc_surface_concept, dtype='f')
			f.create_dataset("tdc/pulse", data=variables.main_p_tdc_surface_concept, dtype='f')
		elif conf['tdc'] == "on" and conf[
			'tdc_model'] == 'RoentDek' and variables.counter_source == 'TDC':
			f.create_dataset("dld/x", data=variables.x, dtype='f')
			f.create_dataset("dld/y", data=variables.y, dtype='f')
			f.create_dataset("dld/t", data=variables.t, dtype='f')
			f.create_dataset("dld/start_counter", data=variables.time_stamp, dtype='f')
			f.create_dataset("dld/high_voltage", data=variables.main_v_dc_tdc_roentdek, dtype='f')
			f.create_dataset("dld/pulse", data=variables.main_p_tdc_roentdek, dtype='f')
			# raw data
			f.create_dataset("tdc/ch0", data=variables.ch0, dtype='i')
			f.create_dataset("tdc/ch1", data=variables.ch1, dtype='i')
			f.create_dataset("tdc/ch2", data=variables.ch2, dtype='i')
			f.create_dataset("tdc/ch3", data=variables.ch3, dtype='i')
			f.create_dataset("tdc/ch4", data=variables.ch4, dtype='i')
			f.create_dataset("tdc/ch5", data=variables.ch5, dtype='i')
			f.create_dataset("tdc/ch6", data=variables.ch6, dtype='i')
			f.create_dataset("tdc/ch7", data=variables.ch6, dtype='i')
		elif conf['tdc'] == "on" and conf['tdc_model'] == 'HSD' and variables.counter_source == 'HSD':
			f.create_dataset("hsd/ch0_time", data=variables.ch0_time, dtype='f')
			f.create_dataset("hsd/ch0_wave", data=variables.ch0_wave, dtype='f')
			f.create_dataset("hsd/ch1_time", data=variables.ch1_time, dtype='f')
			f.create_dataset("hsd/ch1_wave", data=variables.ch1_wave, dtype='f')
			f.create_dataset("hsd/ch2_time", data=variables.ch2_time, dtype='f')
			f.create_dataset("hsd/ch2_wave", data=variables.ch2_wave, dtype='f')
			f.create_dataset("hsd/ch3_time", data=variables.ch3_time, dtype='f')
			f.create_dataset("hsd/ch3_wave", data=variables.ch3_wave, dtype='f')
			f.create_dataset("hsd/ch4_time", data=variables.ch4_time, dtype='f')
			f.create_dataset("hsd/ch4_wave", data=variables.ch4_wave, dtype='f')
			f.create_dataset("hsd/ch5_time", data=variables.ch5_time, dtype='f')
			f.create_dataset("hsd/ch5_wave", data=variables.ch5_wave, dtype='f')
			f.create_dataset("hsd/high_voltage", data=variables.main_v_dc_drs, dtype='f')
			f.create_dataset("hsd/pulse", data=variables.main_v_p_drs, dtype='f')
