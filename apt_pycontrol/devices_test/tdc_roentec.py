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

end_ex = False

buffer_size = 1
class tdc_roentec(object):
    """
    This class setups the parameters for the tdc and allow users to read experiment
    tdc values.
    """

    def __init__(self, ):
        """
        Constructor function which initializes function parameters.

        Attributes:

        """

        # tdc_lib.Drs_new.argtypes = [ctypes.c_void_p]
        tdc_lib.Warraper_tdc_new.restype = ctypes.c_void_p
        tdc_lib.init_tdc.argtypes = [ctypes.c_void_p]
        tdc_lib.init_tdc.restype = ctypes.c_int
        tdc_lib.run_tdc.restype = ctypes.c_int
        tdc_lib.run_tdc.argtypes =[ctypes.c_void_p]
        tdc_lib.stop_tdc.restype = ctypes.c_int
        tdc_lib.stop_tdc.argtypes = [ctypes.c_void_p]
        tdc_lib.get_data_tdc.restype = ndpointer(dtype=ctypes.c_float, shape=(9 * buffer_size,))
        tdc_lib.get_data_tdc.argtypes =[ctypes.c_void_p]
        self.obj = tdc_lib.Warraper_tdc_new()

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


def reader(tdc):
    while True:
        returnVale = np.array(tdc.reader_tdc())
        returnVale = returnVale.reshape(5, buffer_size)
        if 'data' in locals():
            data = np.append(data, returnVale[returnVale >= -10])
        else:
            data = returnVale[returnVale >= -10]

        time.sleep(0.01)

        if end_ex:
            break

    np.savetxt("foo.csv", data, delimiter=",")

    for row in range(10):
        selected_row = returnVale[row]
        selected_row = selected_row[selected_row >= -10]
        print(np.expand_dims(selected_row, axis=0).shape)
        if row == 0:
            data_tmp = np.expand_dims(selected_row, axis=0)
        else:
            data_tmp = np.append(data_tmp, np.expand_dims(selected_row, axis=0), 0)
    # print(data_tmp.shape)
    if 'data' in locals():
        data = np.append(data, data_tmp, 0)
    else:
        data = data_tmp

    #####################
    i = 0
    while True:
        time.sleep(1)
        returnVale = np.array(tdc.reader_tdc())
        returnVale = returnVale.reshape(10, buffer_size)
        for row in range(4):
            selected_row = returnVale[row]
            #selected_row = selected_row[selected_row > -90]

            print(len(selected_row[selected_row > -90]))
            #print(selected_row.shape)
            if row == 0:
                lenght = len(selected_row)
                data_tmp = np.expand_dims(selected_row, axis=0)
            else:
                data_tmp = np.append(data_tmp, np.expand_dims(selected_row[:lenght], axis=0), 0)
        print('--------------------------')
        # print(data_tmp.shape)
        print(data_tmp.shape)
        if 'data' in locals():
            data = np.append(data, data_tmp, 1)
        else:
            data = data_tmp

        if i == 10:
            break
        i = i + 1

    print(data.shape)

    np.savetxt("data.csv", data, delimiter=",")

def experiment_measure():
    """
    This function

    Attributes:

        Parameters:

    Return :
        Does not return anything
    """

    tdc = tdc_roentec()

    tdc.init_tdc()

    #thread = threading.Thread(target=tdc.run_tdc)
    #thread.Daemon = True
    #thread.start()

    tdc.run_tdc()

    i = 0
    start = time.time()
    while True:
        returnVale = tdc.get_data_tdc()
        #returnVale = returnVale.reshape(9, buffer_size)
        #print(returnVale[0][:10])
        #print('--------------------------')
        # print(data_tmp.shape)
        #print(returnVale.shape)
        if 'data' in locals():
            data = np.append(data, np.expand_dims(returnVale, axis=1), 1)
        else:
            data = np.expand_dims(returnVale, axis=1)

        if i == 200:
            break
        i = i + 1
    print('Experiment time:', time.time() - start)

    print(data.shape)

    np.savetxt("data.csv", np.round(data, decimals = 2), delimiter=",")
    #time.sleep(5)

    tdc.stop_tdc()

    os.chdir(os.path.split(MODULE_DIR)[0] + '\\devices_test\\')
    os.system('"lmf2txt.exe output.lmf -f"')


if __name__ == '__main__':
    experiment_measure()