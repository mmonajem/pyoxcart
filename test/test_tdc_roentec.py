"""
This is the main new script for reading TDC Roentec.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""

# import the module
import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np
import threading
import time

# load the library
tdc_lib = ctypes.CDLL("../tdc_roentdec/simple_read_TDC8HP_x64.dll")


class tdc_roentec(object):
    """
    This class setups the parameters for the tdc and allow users to read experiment
    tdc values.
    """

    def __init__(self,):
        """
        Constructor function which initializes function parameters.

        Attributes:

        """

        # tdc_lib.Drs_new.argtypes = [ctypes.c_void_p]
        tdc_lib.Warraper_tdc_new.restype = ctypes.c_void_p
        tdc_lib.reader_tdc.argtypes = [ctypes.c_void_p]
        tdc_lib.reader_tdc.restype = ndpointer(dtype=ctypes.c_double, shape=(4 * 10000,))
        tdc_lib.run_tdc.restype = ctypes.c_int
        tdc_lib.run_tdc.argtypes = [ctypes.c_void_p]
        self.obj = tdc_lib.Warraper_tdc_new()

    def reader_tdc(self, ):
        """
        This class method reads and returns the DRS value utilizing the TDC.

        Attributes:
            Does not accept any arguments
        Returns:
            data: Return the read DRS value.
        """
        data = tdc_lib.reader_tdc(self.obj)
        return data

    def run_tdc(self):
        """
        This class method destroys the object

        Attributes:
            Does not accept any arguments
        Returns:
            Does not return anything

        """
        tdc_lib.run_tdc(self.obj)


def reader(tdc, queue_x, queue_y,
                       queue_tof, queue_time_stamp):

    while True:
        returnVale = np.array(tdc.reader_tdc())
        returnVale = returnVale.reshape(4, 10000)
        for i in range(4):
            tem_arr = returnVale[i,:]
            if(len(tem_arr[tem_arr >= -10]) > 1 and i == 0):
                queue_x.put(tem_arr)
            elif (len(tem_arr[tem_arr >= -10]) > 1 and i == 1):
                queue_y.put(tem_arr)
            elif (len(tem_arr[tem_arr >= -10]) > 1 and i == 2):
                queue_tof.put(tem_arr)
            elif (len(tem_arr[tem_arr >= -10]) > 1 and i == 3):
                queue_time_stamp.put(tem_arr)

        time.sleep(0.01)


def experiment_measure(queue_x, queue_y,
                       queue_tof, queue_time_stamp, queue_stop_measurement):
    """
    This function

    Attributes:

        Parameters:

    Return :
        Does not return anything
    """

    tdc = tdc_roentec()

    thread = threading.Thread(target=reader, args=(tdc,queue_x, queue_y,
                       queue_tof, queue_time_stamp))
    thread.setDaemon(True)
    thread.start()

    tdc.run_tdc()


queue_x = np.zeros(0)
queue_y = np.zeros(0)
queue_tof = np.zeros(0)
queue_time_stamp = np.zeros(0)
experiment_measure(queue_x, queue_y,
                       queue_tof, queue_time_stamp, queue_stop_measurement=True)

