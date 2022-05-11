"""
This is the main script for reading TDC Roentec.
"""

# import the module
import os
import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np

from pyccapt.control.module_dir import MODULE_DIR

buf_size = 30000
time_out = 300


class tdc_dec(object):
    """
    This class setups the parameters for the tdc and allow users to read experiment
    tdc values.
    """

    def __init__(self, tdc_lib, buf_size, time_out):
        """
        Constructor function which initializes function parameters.

        Attributes:

        """
        tdc_lib.Warraper_tdc_new.restype = ctypes.c_void_p
        tdc_lib.Warraper_tdc_new.argtypes = [ctypes.c_int, ctypes.c_int]
        tdc_lib.init_tdc.argtypes = [ctypes.c_void_p]
        tdc_lib.init_tdc.restype = ctypes.c_int
        tdc_lib.run_tdc.restype = ctypes.c_int
        tdc_lib.run_tdc.argtypes =[ctypes.c_void_p]
        tdc_lib.stop_tdc.restype = ctypes.c_int
        tdc_lib.stop_tdc.argtypes = [ctypes.c_void_p]
        tdc_lib.get_data_tdc_buf.restype = ndpointer(dtype=ctypes.c_double, shape=(12 * buf_size+1,))
        tdc_lib.get_data_tdc_buf.argtypes =[ctypes.c_void_p]
        self.obj = tdc_lib.Warraper_tdc_new(buf_size, time_out)
        self.tdc_lib = tdc_lib

    def stop_tdc(self, ):
        """
        This class method reads and returns the DRS value utilizing the TDC.

        Attributes:
            Does not accept any arguments

        Returns:
            data: Return the read DRS value.
        """

        return self.tdc_lib.stop_tdc(self.obj)

    def init_tdc(self, ):
        """
        This class method reads and returns the DRS value utilizing the TDC.

        Attributes:
            Does not accept any arguments

        Returns:
            data: Return the read DRS value.
        """
        self.tdc_lib.init_tdc(self.obj)

    def run_tdc(self,):
        """
        This class method destroys the object

        Attributes:
            Does not accept any arguments

        Returns:
            Does not return anything
        """

        self.tdc_lib.run_tdc(self.obj)


    def get_data_tdc_buf(self,):
        """
        This class method destroys the object

        Attributes:
            Does not accept any arguments

        Returns:
            Does not return anything
        """
        data = self.tdc_lib.get_data_tdc_buf(self.obj)
        return data


def experiment_measure(queue_x, queue_y, queue_t, queue_AbsoluteTimeStamp,
                       queue_ch0, queue_ch1, queue_ch2, queue_ch3,
                       queue_ch4, queue_ch5, queue_ch6, queue_ch7,
                       queue_stop_measurement):
    """
    measurement function: This function is called in a process by
                          apt_voltage.py tp read data from the queue.
    Attributes:
        DLD Queues: Queues that contains DLD data
            queue_y: Queue for grp: DLD and parameter: y
            queue_t: Queue for grp: DLD and parameter: t
            queue_dld_start_counter: Queue for grp: DLD and parameter: start_counter

        TDC Queues: Queues that contains TDC raw data
            queue_time_data: Queue for grp: TDC and parameter: time_data
            queue_tdc_start_counter: Queue for grp: TDC and parameter: start_counter

        Stop measurement flag: queue
            Queue for stop the measurement. This queue is set to True from apt_voltage.py

    Returns
        Does not return anything
    """

    try:
        # load the library
        os.chdir(os.path.split(MODULE_DIR)[0] + '\\control\\tdc_roentdec\\')
        tdc_lib = ctypes.CDLL("./wrapper_read_TDC8HP_x64.dll")
    except:
        print("TDC DLL was not found")

    tdc = tdc_dec(tdc_lib, buf_size=buf_size, time_out=time_out)

    ret_code = tdc.init_tdc()

    # if ret_code < 0:
    #     print("error during init:", ret_code)
    #     print(
    #         f"{initialize_devices.bcolors.FAIL}Error: TDC cannot be initialized{initialize_devices.bcolors.ENDC}")
    #     return -1
    # else:
    #     print("TDC is successfully initialized")
    tdc.run_tdc()

    while True:
        returnVale = tdc.get_data_tdc_buf()
        buffer_lenght = int(returnVale[0])

        returnVale_tmp = np.copy(returnVale[1:buffer_lenght * 12 + 1].reshape(buffer_lenght, 12))

        queue_ch0.put(returnVale_tmp[:, 0])
        queue_ch1.put(returnVale_tmp[:, 1])
        queue_ch2.put(returnVale_tmp[:, 2])
        queue_ch3.put(returnVale_tmp[:, 3])
        queue_ch4.put(returnVale_tmp[:, 4])
        queue_ch5.put(returnVale_tmp[:, 5])
        queue_ch6.put(returnVale_tmp[:, 6])
        queue_ch7.put(returnVale_tmp[:, 7])
        queue_x.put(returnVale_tmp[:, 8])
        queue_y.put(returnVale_tmp[:, 9])
        queue_t.put(returnVale_tmp[:, 10])
        queue_AbsoluteTimeStamp.put(returnVale_tmp[:, 11])

        if not queue_stop_measurement.empty():
            break

    tdc.stop_tdc()

    return 0
