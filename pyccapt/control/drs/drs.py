"""
This is the main new script for reading DRS digitizer.
"""

# import the module
import ctypes
import os

import numpy as np
from numpy.ctypeslib import ndpointer


class DRS(object):
    """
    This class setups the parameters for the DRS group and allow users to read experiment
    DRS values.
    """

    def __init__(self, trigger, test, delay, sample_frequency, log, log_path):
        """
        Constructor function which initializes function parameters.

        Attributes:
            trigger:  trigger=0 --> Internal trigger
                      trigger=1 --> External rigger
            test:  test=1 --> test mode -
                   connect 100 MHz clock connected to all channels
            delay: Trigger delay in nanosecond
            sample_frequency: sample frequency at which the data is being captured
        """

        # load the library

        try:
            # load the library
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

    def reader(self, ):
        """
        This class method reads and returns the DRS value utilizing the drs.

        Attributes:
            Does not accept any arguments

        Returns:
            data: Return the read DRS value.
        """

        data = self.drs_lib.Drs_reader(self.obj)
        if self.log:
            self.log_drs.info("Function - reader | response - > {} | type -> {}".format(data, type(data)))

        return data

    def delete_drs_ox(self):
        """
        This class method destroys the object

        Attributes:
            Does not accept any arguments

        Returns:
            Does not return anything
        """

        self.drs_lib.Drs_delete_drs_ox(self.obj)


# Create drs object and initialize the drs board

def experiment_measure(queue_ch0_time, queue_ch0_wave,
                       queue_ch1_time, queue_ch1_wave,
                       queue_ch2_time, queue_ch2_wave,
                       queue_ch3_time, queue_ch3_wave,
                       queue_stop_measurement, log, log_path):
    """
    This function continosly reads the DRS data and put the data into
    the queue. Exits when reads queue_stop_measurement is empty.

    Attributes:
        Accepts different queues objects of different channels and parameters
        Channels:
            Channel 1
            Channel 1
            Channel 2
            Channel 3
        Parameters:
            time
            wave

    Return :
        Does not return anything
    """
    # trigger = 1 means use external trigger
    # delay is in ns
    # test = 1 means run drs in test mode with sinusoidal signal
    drs_ox = DRS(trigger=0, test=1, delay=0, sample_frequency=2, log=log, log_path=log_path)

    while True:

        if queue_stop_measurement.empty():
            # Read the data from drs
            returnVale = np.array(drs_ox.reader())
            # Reshape the all 4 channel of time and wave arrays
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
