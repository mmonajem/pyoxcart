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
import os

from apt_pycontrol.tools.module_dir import MODULE_DIR

# load the library

os.chdir(os.path.split(MODULE_DIR)[0] + '\\tdc_roentdec\\') # directory has to be changed to be changed to the directory of dlls
tdc_lib = ctypes.CDLL("../tdc_roentdec/simple_read_TDC8HP_x64.dll")


class tdc_roentec(object):
    """
    This class setups the parameters for the tdc and allow users to read experiment
    tdc values.
    """

    def __init__(self, buf_size, time_out):
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
        tdc_lib.get_data_tdc.restype = ndpointer(dtype=ctypes.c_double, shape=(12,))
        tdc_lib.get_data_tdc.argtypes =[ctypes.c_void_p]
        tdc_lib.get_data_tdc_buf.restype = ndpointer(dtype=ctypes.c_double, shape=(12 * buf_size,))
        tdc_lib.get_data_tdc_buf.argtypes =[ctypes.c_void_p]
        self.obj = tdc_lib.Warraper_tdc_new(buf_size, time_out)

    def stop_tdc(self, ):
        """
        This class method reads and returns the DRS value utilizing the TDC.

        Attributes:
            Does not accept any arguments
        Returns:
            data: Return the read DRS value.
        """
        return tdc_lib.stop_tdc(self.obj)

    def init_tdc(self, ):
        """
        This class method reads and returns the DRS value utilizing the TDC.

        Attributes:
            Does not accept any arguments
        Returns:
            data: Return the read DRS value.
        """
        tdc_lib.init_tdc(self.obj)

    def run_tdc(self,):
        """
        This class method destroys the object

        Attributes:
            Does not accept any arguments
        Returns:
            Does not return anything

        """
        tdc_lib.run_tdc(self.obj)

    def get_data_tdc(self,):
        """
        This class method destroys the object

        Attributes:
            Does not accept any arguments
        Returns:
            Does not return anything

        """
        data = tdc_lib.get_data_tdc(self.obj)
        return data

    def get_data_tdc_buf(self,):
        """
        This class method destroys the object

        Attributes:
            Does not accept any arguments
        Returns:
            Does not return anything

        """
        data = tdc_lib.get_data_tdc_buf(self.obj)
        return data


def experiment_measure(iteration, buf_size=1, time_out=1):
    """
    This function

    Attributes:

        Parameters:

    Return :
        Does not return anything
    """

    tdc = tdc_roentec(buf_size=buf_size, time_out=time_out)

    tdc.init_tdc()

    tdc.run_tdc()

    i = 0
    start = time.time()
    while True:
        returnVale = tdc.get_data_tdc()

        if 'data' in locals():
            data = np.append(data, np.expand_dims(returnVale[1:], axis=1), 1)
        else:
            data = np.expand_dims(returnVale[1:], axis=1)

        if i == iteration:
            break
        i = i + 1
    print('Experiment time:', time.time() - start)

    print(data.shape)

    np.savetxt("data.csv", np.round(data, decimals = 2), delimiter=",")
    #time.sleep(5)

    tdc.stop_tdc()

    os.system('"lmf2txt.exe output.lmf -f"')

def experiment_measure_buf(buffer_size, time_out):
    """
    This function

    Attributes:

        Parameters:

    Return :
        Does not return anything
    """

    tdc = tdc_roentec(buf_size=buffer_size, time_out=time_out)

    tdc.init_tdc()

    tdc.run_tdc()

    i = 0
    start = time.time()

    while True:
        returnVale = tdc.get_data_tdc_buf()
        buffer_lenght = returnVale[0]
        returnVale = returnVale[1:].reshape(12, buffer_lenght)
        if 'data' in locals():
            data = np.append(data, returnVale, 1)
        else:
            data = returnVale

        print('%s events recorded in (s):' %buffer_lenght, time.time() - start)
        if i == 2:
            break
        i = i + 1

    print('Experiment time:', time.time() - start)

    print(data.shape)

    np.savetxt("data.csv", np.round(data, decimals = 2), delimiter=",")
    #time.sleep(5)

    tdc.stop_tdc()

    os.system('"lmf2txt.exe output.lmf -f"')


if __name__ == '__main__':
    # experiment_measure(5)
    experiment_measure_buf(1000, 100)