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

	retcode = bufdatacb.start_measurement(100)
	if errorcheck(retcode) < 0:
		return -1

	while True:
		eventtype, data = bufdatacb.queue.get()
		eventtype_raw, data_raw = bufdatacb_raw.queue.get()

		if eventtype == QUEUE_DATA:
			# correct for binning of surface concept
			xx = (((data["dif1"] - XYBINSHIFT) * XYFACTOR) / 10).tolist()  # from mm to in cm by dividing by 10
			yy = (((data["dif2"] - XYBINSHIFT) * XYFACTOR) / 10).tolist()  # from mm to in cm by dividing by 10
			tt = (data["time"] * TOFFACTOR).tolist()  # in ns
			variables.extend_to('x', xx)
			variables.extend_to('y', yy)
			variables.extend_to('t', tt)
			variables.extend_to('dld_start_counter', data["start_counter"].tolist())

			voltage_data = np.tile(variables.specimen_voltage, len(xx))
			pulse_data = np.tile(variables.pulse_voltage, len(xx))
			variables.extend_to('main_v_dc_dld_surface_concept', voltage_data.tolist())
			variables.extend_to('main_p_dld_surface_concept', pulse_data.tolist())
			# with self.variables.lock_data_plot:
			variables.extend_to('main_v_dc_plot', voltage_data.tolist())
			variables.extend_to('x_plot', xx)
			variables.extend_to('y_plot', yy)
			variables.extend_to('t_plot', tt)
			variables.main_p_dld_surface_concept.extend(
				np.tile(variables.pulse_voltage, len(xx)).tolist())

			channel_data = data_raw["channel"].tolist()
			variables.extend_to('channel', channel_data)
			variables.extend_to('time_data', data_raw["time"].tolist())
			variables.extend_to('tdc_start_counter', data_raw["start_counter"].tolist())
			voltage_data = np.tile(variables.specimen_voltage, len(channel_data))
			variables.extend_to('main_v_dc_tdc_surface_concept', voltage_data.tolist())
			variables.extend_to('main_p_tdc_surface_concept',
			                    np.tile(variables.pulse_voltage, len(channel_data)).tolist())
		elif eventtype == QUEUE_ENDOFMEAS:
			if not variables.flag_stop_tdc:
				retcode = bufdatacb.start_measurement(100)
				if errorcheck(retcode) < 0:
					return -1
			else:
				break
		else:  # unknown event
			break

	time.sleep(0.1)
	bufdatacb.close()
	device.deinitialize()

	return 0
