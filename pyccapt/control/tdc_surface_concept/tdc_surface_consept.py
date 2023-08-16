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


def experiment_measure(queue_x,
                       queue_y, queue_t,
                       queue_dld_start_counter,
                       queue_channel,
                       queue_time_data,
                       queue_tdc_start_counter,
                       queue_stop_measurement):
	"""
	Measurement function: This function is called in a process to read data from the queue.

	Args:
		queue_x (multiprocessing.Queue): Queue for x data.
		queue_y (multiprocessing.Queue): Queue for y data.
		queue_t (multiprocessing.Queue): Queue for t data.
		queue_dld_start_counter (multiprocessing.Queue): Queue for DLD start counter data.
		queue_channel (multiprocessing.Queue): Queue for channel data.
		queue_time_data (multiprocessing.Queue): Queue for time data.
		queue_tdc_start_counter (multiprocessing.Queue): Queue for TDC start counter data.
		queue_stop_measurement (multiprocessing.Queue): Queue to stop measurement.

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

	retcode = bufdatacb.start_measurement(300)
	if errorcheck(retcode) < 0:
		return -1

	while True:
		eventtype, data = bufdatacb.queue.get()
		eventtype_raw, data_raw = bufdatacb_raw.queue.get()

		if eventtype == QUEUE_DATA:
			queue_x.put(data["dif1"])
			queue_y.put(data["dif2"])
			queue_t.put(data["time"])
			queue_dld_start_counter.put(data["start_counter"])
			queue_channel.put(data_raw["channel"])
			queue_time_data.put(data_raw["time"])
			queue_tdc_start_counter.put(data_raw["start_counter"])
		elif eventtype == QUEUE_ENDOFMEAS:
			if queue_stop_measurement.empty():
				retcode = bufdatacb.start_measurement(300)
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
