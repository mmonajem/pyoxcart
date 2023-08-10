import os
import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np


class TDC:
	"""
	This class sets up the parameters for the TDC and allows users to read experiment TDC values.
	"""

	def __init__(self, tdc_lib, buf_size=30000, time_out=300):
		"""
		Constructor function which initializes function parameters.

		Args:
			tdc_lib (ctypes.CDLL): The TDC library.
			buf_size (int): Buffer size.
			time_out (int): Timeout value.
		"""
		self.tdc_lib = tdc_lib
		self.buf_size = buf_size
		self.time_out = time_out
		tdc_lib.Warraper_tdc_new.restype = ctypes.c_void_p
		tdc_lib.Warraper_tdc_new.argtypes = [ctypes.c_int, ctypes.c_int]
		tdc_lib.init_tdc.argtypes = [ctypes.c_void_p]
		tdc_lib.init_tdc.restype = ctypes.c_int
		tdc_lib.run_tdc.restype = ctypes.c_int
		tdc_lib.run_tdc.argtypes = [ctypes.c_void_p]
		tdc_lib.stop_tdc.restype = ctypes.c_int
		tdc_lib.stop_tdc.argtypes = [ctypes.c_void_p]
		tdc_lib.get_data_tdc_buf.restype = ndpointer(dtype=ctypes.c_double, shape=(12 * self.buf_size + 1,))
		tdc_lib.get_data_tdc_buf.argtypes = [ctypes.c_void_p]

		self.obj = tdc_lib.Warraper_tdc_new(self.buf_size, self.time_out)

	def stop_tdc(self):
		"""
		Stop the TDC.

		Returns:
			int: Return code.
		"""
		return self.tdc_lib.stop_tdc(self.obj)

	def init_tdc(self):
		"""
		Initialize the TDC.

		Returns:
			int: Return code.
		"""
		return self.tdc_lib.init_tdc(self.obj)

	def run_tdc(self):
		"""
		Run the TDC.
		"""
		self.tdc_lib.run_tdc(self.obj)

	def get_data_tdc_buf(self):
		"""
		Get data from the TDC buffer.

		Returns:
			np.ndarray: Data from the TDC buffer.
		"""
		data = self.tdc_lib.get_data_tdc_buf(self.obj)
		return data

def experiment_measure(queue_x, queue_y, queue_t, queue_AbsoluteTimeStamp,
                       queue_ch0, queue_ch1, queue_ch2, queue_ch3,
                       queue_ch4, queue_ch5, queue_ch6, queue_ch7,
                       queue_stop_measurement):
	"""
	Measurement function: This function is called in a process to read data from the queue.

	Args:
		queue_x (multiprocessing.Queue): Queue for x data.
		queue_y (multiprocessing.Queue): Queue for y data.
		queue_t (multiprocessing.Queue): Queue for t data.
		queue_AbsoluteTimeStamp (multiprocessing.Queue): Queue for AbsoluteTimeStamp data.
		queue_ch0 (multiprocessing.Queue): Queue for ch0 data.
		queue_ch1 (multiprocessing.Queue): Queue for ch1 data.
		queue_ch2 (multiprocessing.Queue): Queue for ch2 data.
		queue_ch3 (multiprocessing.Queue): Queue for ch3 data.
		queue_ch4 (multiprocessing.Queue): Queue for ch4 data.
		queue_ch5 (multiprocessing.Queue): Queue for ch5 data.
		queue_ch6 (multiprocessing.Queue): Queue for ch6 data.
		queue_ch7 (multiprocessing.Queue): Queue for ch7 data.
		queue_stop_measurement (multiprocessing.Queue): Queue to stop measurement.

	Returns:
		int: Return code.
	"""
	try:
		# Load the library
		p = os.path.abspath(os.path.join(__file__, "../../..", "control", "tdc_roentdec"))
		os.chdir(p)
		tdc_lib = ctypes.CDLL("./wrapper_read_TDC8HP_x64.dll")
	except Exception as e:
		print("TDC DLL was not found")
		print(e)

	tdc = TDC(tdc_lib, buf_size=30000, time_out=300)

    ret_code = tdc.init_tdc()

    tdc.run_tdc()

    while True:
	    returnVale = tdc.get_data_tdc_buf()
	    buffer_length = int(returnVale[0])
	    returnVale_tmp = np.copy(returnVale[1:buffer_length * 12 + 1].reshape(buffer_length, 12))

	    for i in range(8):
		    queue_ch = globals()[f'queue_ch{i}']
		    queue_ch.put(returnVale_tmp[:, i])

	    queue_x.put(returnVale_tmp[:, 8])
	    queue_y.put(returnVale_tmp[:, 9])
	    queue_t.put(returnVale_tmp[:, 10])
	    queue_AbsoluteTimeStamp.put(returnVale_tmp[:, 11])

	    if not queue_stop_measurement.empty():
		    break

    tdc.stop_tdc()

    return 0
