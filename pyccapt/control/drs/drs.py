import ctypes
import os
import numpy as np
from numpy.ctypeslib import ndpointer

# local imports
from pyccapt.control.control_tools import loggi


class DRS:
    """
    This class sets up the parameters for the DRS group and allows users to read experiment DRS values.
    """

    def __init__(self, trigger, test, delay, sample_frequency, log, log_path):
        """
        Constructor function which initializes function parameters.

        Args:
            trigger (int): Trigger type. 0 for internal trigger, 1 for external trigger.
            test (int): Test mode. 0 for normal mode, 1 for test mode (connect 100 MHz clock to all channels).
            delay (int): Trigger delay in nanoseconds.
            sample_frequency (float): Sample frequency at which the data is being captured.
            log (bool): Enable logging.
            log_path (str): Path for logging.

        """
        try:
            p = os.path.abspath(os.path.join(__file__, "../../drs"))
            os.chdir(p)
            self.drs_lib = ctypes.CDLL("./drs_lib.dll")
        except Exception as e:
            print("DRS DLL was not found")
            print(e)

        self.drs_lib.Drs_new.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float]
        self.drs_lib.Drs_new.restype = ctypes.c_void_p
        self.drs_lib.Drs_reader.argtypes = [ctypes.c_void_p]
        self.drs_lib.Drs_reader.restype = ndpointer(dtype=ctypes.c_float, shape=(8 * 1024,))
        self.drs_lib.Drs_delete_drs_ox.restype = ctypes.c_void_p
        self.drs_lib.Drs_delete_drs_ox.argtypes = [ctypes.c_void_p]
        self.obj = self.drs_lib.Drs_new(trigger, test, delay, sample_frequency)
        self.log = log
        self.log_path = log_path
        if self.log:
            self.log_drs = loggi.logger_creator('drs', 'dsr.log', path=self.log_path)

    def reader(self):
        """
        Read and return the DRS values.

        Returns:
            data: Read DRS values.
        """
        data = self.drs_lib.Drs_reader(self.obj)
        if self.log:
            self.log_drs.info("Function - reader | response - > {} | type -> {}".format(data, type(data)))
        return data

    def delete_drs_ox(self):
        """
        Destroy the object.
        """
        self.drs_lib.Drs_delete_drs_ox(self.obj)

def experiment_measure(queue_ch0_time, queue_ch0_wave,
                       queue_ch1_time, queue_ch1_wave,
                       queue_ch2_time, queue_ch2_wave,
                       queue_ch3_time, queue_ch3_wave,
                       queue_stop_measurement, log, log_path):
    """
    Continuously reads the DRS data and puts it into the queues.

    Args:
        queue_ch0_time (Queue): Queue for channel 0 time data.
        queue_ch0_wave (Queue): Queue for channel 0 wave data.
        queue_ch1_time (Queue): Queue for channel 1 time data.
        queue_ch1_wave (Queue): Queue for channel 1 wave data.
        queue_ch2_time (Queue): Queue for channel 2 time data.
        queue_ch2_wave (Queue): Queue for channel 2 wave data.
        queue_ch3_time (Queue): Queue for channel 3 time data.
        queue_ch3_wave (Queue): Queue for channel 3 wave data.
        queue_stop_measurement (Queue): Queue to stop measurement.
        log (bool): Enable logging.
        log_path (str): Path for logging.
    """
    drs_ox = DRS(trigger=0, test=1, delay=0, sample_frequency=2, log=log, log_path=log_path)

    while True:
        if queue_stop_measurement.empty():
            returnVale = np.array(drs_ox.reader())
            data = returnVale.reshape(8, 1024)
            queue_ch0_time.put(data[0, :])
            queue_ch0_wave.put(data[1, :])
            queue_ch1_time.put(data[2, :])
            queue_ch1_wave.put(data[3, :])
            queue_ch2_time.put(data[4, :])
            queue_ch2_wave.put(data[5, :])
            queue_ch3_time.put(data[6, :])
            queue_ch3_wave.put(data[7, :])
        else:
            print('DRS loop is break in child process')
            break

    drs_ox.delete_drs_ox()

