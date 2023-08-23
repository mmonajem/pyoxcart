import time
from queue import Queue

import numpy as np

# local imports
from pyccapt.control.devices import initialize_devices
from pyccapt.control.tdc_surface_concept import scTDC

QUEUE_DATA = 0
QUEUE_ENDOFMEAS = 1


class BufDataCB4(scTDC.buffered_data_callbacks_pipe):
	"""
	The class inherits from python wrapper module scTDC and class: buffered_data_callbacks_pipe
	"""

	def __init__(self, lib, dev_desc, data_field_selection, dld_events,
	             max_buffered_data_len=500000):
		'''
		Initialize the base class: scTDC.buffered_data_callbacks_pipe

		Args:
			lib (scTDClib): A scTDClib object.
			dev_desc (int): Device descriptor as returned by sc_tdc_init_inifile(...).
			data_field_selection (int): A 'bitwise or' combination of SC_DATA_FIELD_xyz constants.
			dld_events (bool): True to receive DLD events, False to receive TDC events.
			max_buffered_data_len (int): Number of events buffered before invoking callbacks.
		'''
		super().__init__(lib, dev_desc, data_field_selection, max_buffered_data_len, dld_events)

		self.queue = Queue()
		self.end_of_meas = False

	def on_data(self, d):
		"""
		This class method function:
			1. Makes a deep copy of numpy arrays in d
			2. Inserts basic values by simple assignment
			3. Inserts numpy arrays using the copy method of the source array

		Args:
			d (dict): Data dictionary.

		Returns:
			None
		"""
		dcopy = {}
		for k in d.keys():
			if isinstance(d[k], np.ndarray):
				dcopy[k] = d[k].copy()
			else:
				dcopy[k] = d[k]
		self.queue.put((QUEUE_DATA, dcopy))
		if self.end_of_meas:
			self.end_of_meas = False
			self.queue.put((QUEUE_ENDOFMEAS, None))

	def on_end_of_meas(self):
		"""
		This class method sets end_of_meas to True.

		Returns:
			True (bool)
		"""
		self.end_of_meas = True
		return True


def experiment_measure(variables):
	# from line_profiler import LineProfiler
	#
	# lp1 = LineProfiler()
	#
	# lp1.add_function(experiment_measure_2)
	#
	# # Run the profiler
	# lp1(experiment_measure_2)(variables)
	# # Save the profiling result to a file
	# lp1.dump_stats('./../../experiment_measure.lprof')

	experiment_measure_2(variables)


def experiment_measure_2(variables):
	"""
	Measurement function: This function is called in a process to read data from the queue.

	Args:
		variables:

	Returns:
		int: Return code.
	"""

	# surface concept tdc specific binning and factors
	TOFFACTOR = 27.432 / (1000 * 4)  # 27.432 ps/bin, tof in ns, data is TDC time sum
	DETBINS = 4900
	BINNINGFAC = 2
	XYFACTOR = 80 / DETBINS * BINNINGFAC  # XXX mm/bin
	XYBINSHIFT = DETBINS / BINNINGFAC / 2  # to center detector

	device = scTDC.Device(autoinit=False)
	retcode, errmsg = device.initialize()

	if retcode < 0:
		print("Error during init:", retcode, errmsg)
		print(f"{initialize_devices.bcolors.FAIL}Error: Restart the TDC manually "
		      f"(Turn it On and Off){initialize_devices.bcolors.ENDC}")
		return -1
	else:
		print("TDC is successfully initialized")

	DATA_FIELD_SEL = (scTDC.SC_DATA_FIELD_DIF1 |
	                  scTDC.SC_DATA_FIELD_DIF2 |
	                  scTDC.SC_DATA_FIELD_TIME |
	                  scTDC.SC_DATA_FIELD_START_COUNTER)
	DATA_FIELD_SEL_raw = (scTDC.SC_DATA_FIELD_TIME |
	                      scTDC.SC_DATA_FIELD_CHANNEL |
	                      scTDC.SC_DATA_FIELD_START_COUNTER)

	bufdatacb = BufDataCB4(device.lib, device.dev_desc, DATA_FIELD_SEL, dld_events=True)
	bufdatacb_raw = BufDataCB4(device.lib, device.dev_desc, DATA_FIELD_SEL_raw, dld_events=False)

	def errorcheck(retcode):
		"""
		This function checks return codes for errors and does cleanup.

		Args:
			retcode (int): Return code.

		Returns:
			int: 0 if success return code or return code > 0, -1 if return code is error code or less than 0.
		"""
		if retcode < 0:
			print(device.lib.sc_get_err_msg(retcode))
			bufdatacb.close()
			device.deinitialize()
			return -1
		else:
			return 0

	xx_list = []
	yy_list = []
	tt_list = []
	xx = []
	yy = []
	tt = []
	voltage_data = []
	pulse_data = []
	start_counter = []

	channel_data = []
	time_data = []
	tdc_start_counter = []
	voltage_data_tdc = []
	pulse_data_tdc = []

	retcode = bufdatacb.start_measurement(100)
	if errorcheck(retcode) < 0:
		return -1
	save_data_plot = 0
	events_detected = 0
	start_time = time.time()
	pulse_frequency = variables.pulse_frequency
	while not variables.flag_stop_tdc:
		eventtype, data = bufdatacb.queue.get()
		eventtype_raw, data_raw = bufdatacb_raw.queue.get()
		specimen_voltage = variables.specimen_voltage
		pulse_voltage = variables.pulse_voltage
		if eventtype == QUEUE_DATA:
			# correct for binning of surface concept
			xx_dif = data["dif1"]
			yy_dif = data["dif2"]
			tt_dif = data["time"]
			start_counter.extend(data["start_counter"].tolist())
			xx_tmp = (((xx_dif - XYBINSHIFT) * XYFACTOR) * 0.1).tolist()  # from mm to in cm by dividing by 10
			yy_tmp = (((yy_dif - XYBINSHIFT) * XYFACTOR) * 0.1).tolist()  # from mm to in cm by dividing by 10
			tt_tmp = (tt_dif * TOFFACTOR).tolist()  # in ns
			xx_list.extend(xx_dif)
			yy_list.extend(yy_dif)
			tt_list.extend(tt_dif)
			xx.extend(xx_tmp)
			yy.extend(yy_tmp)
			tt.extend(tt_tmp)
			dc_voltage = np.tile(specimen_voltage, len(xx)).tolist()
			voltage_data.extend(dc_voltage)
			pulse_data.extend((np.tile(pulse_voltage, len(xx))).tolist())
			if save_data_plot == 3:
				variables.extend_to('main_v_dc_plot', dc_voltage)
				variables.extend_to('x_plot', xx_tmp)
				variables.extend_to('y_plot', yy_tmp)
				variables.extend_to('t_plot', tt_tmp)
				save_data_plot = 0
			save_data_plot += 1

		if eventtype_raw == QUEUE_DATA:
			channel_data_tmp = data_raw["channel"].tolist()
			tdc_start_counter.extend(data_raw["start_counter"].tolist())
			time_data.extend(data_raw["time"].tolist())
			# raw data
			channel_data.extend(channel_data_tmp)
			voltage_data_tdc.extend((np.tile(specimen_voltage, len(channel_data_tmp))).tolist())
			pulse_data_tdc.extend((np.tile(pulse_voltage, len(channel_data_tmp))).tolist())

		elif eventtype == QUEUE_ENDOFMEAS:
			retcode = bufdatacb.start_measurement(100)
			if errorcheck(retcode) < 0:
				return -1
		else:  # unknown event
			break
		# Update the counter
		events_detected += len(xx_dif)
		# Calculate the detection rate
		# Check if the detection rate interval has passed
		current_time = time.time()
		if current_time - start_time >= 1.0:
			elapsed_time = current_time - start_time
			detection_rate = events_detected / pulse_frequency
			print("Detection Rate:", detection_rate, "events per second", '---loop_iteration_time', elapsed_time,
			      '---events_detected', events_detected)
			# Reset the counter and timer
			events_detected = 0
			start_time = current_time

	print("TDC Measurement stopped")
	np.save(variables.path + "/x_data.npy", np.array(xx_list))
	np.save(variables.path + "/y_data.npy", np.array(yy_list))
	np.save(variables.path + "/t_data.npy", np.array(tt_list))
	np.save(variables.path + "/voltage_data.npy", np.array(voltage_data))
	np.save(variables.path + "/pulse_data.npy", np.array(pulse_data))

	variables.extend_to('x', xx)
	variables.extend_to('y', yy)
	variables.extend_to('t', tt)
	variables.extend_to('dld_start_counter', start_counter)
	variables.extend_to('main_v_dc_dld_surface_concept', voltage_data)
	variables.extend_to('main_p_dld_surface_concept', pulse_data)

	variables.extend_to('channel', channel_data)
	variables.extend_to('time_data', time_data)
	variables.extend_to('tdc_start_counter', tdc_start_counter)
	variables.extend_to('main_v_dc_tdc_surface_concept', voltage_data_tdc)
	variables.extend_to('main_p_tdc_surface_concept', pulse_data_tdc)
	print("data save in share variables")
	time.sleep(0.1)
	bufdatacb.close()
	device.deinitialize()

	variables.flag_finished_tdc = True

	return 0
