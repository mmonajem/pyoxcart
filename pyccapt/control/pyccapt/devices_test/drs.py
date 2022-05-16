"""
This is the script for testing DRS digitizer.
"""
# import the module
import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np
import matplotlib.pyplot as plt
import time


class DRS(object):
    def __init__(self, trigger, test, delay, sample_frequency):
        # trigger=0 --> Internal trigger
        # trigger=1 --> External rigger
        # test=0 --> Test mode off
        # test=1 --> test mode - connect 100 MHz clock connected to all channels
        # Trigger delay in ns
        # load the library
        self.drs_lib = ctypes.CDLL("../drs/drs_lib.dll")
        self.drs_lib.Drs_new.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float]
        self.drs_lib.Drs_new.restype = ctypes.c_void_p
        self.drs_lib.Drs_reader.argtypes = [ctypes.c_void_p]
        self.drs_lib.Drs_reader.restype = ndpointer(dtype=ctypes.c_float, shape=(8 * 1024,))
        self.drs_lib.Drs_delete_drs_ox.restype = ctypes.c_void_p
        self.drs_lib.Drs_delete_drs_ox.argtypes = [ctypes.c_void_p]
        self.obj = self.drs_lib.Drs_new(trigger, test, delay, sample_frequency)

    def reader(self, ):
        data = self.drs_lib.Drs_reader(self.obj)
        return data

    def delete_drs_ox(self):
        self.drs_lib.Drs_delete_drs_ox(self.obj)


if __name__ == '__main__':
    # Create drs object and initialize the drs board
    drs_ox = DRS(trigger=0, test=1, delay=0, sample_frequency=2)

    # code
    for i in range(5):
        # Read the data from drs
        start = time.time()
        returnVale = np.array(drs_ox.reader())
        print('run time:', time.time() - start)
        # Reshape the all 4 channel of time and wave arrays
        data = returnVale.reshape(8, 1024)

        if i == 0:
            data_final = data
        else:
            data_final = np.concatenate((data_final, data), axis=1)

    drs_ox.delete_drs_ox()
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    fig.tight_layout()
    ax1.plot(data[0, 0:1024], data[1, 0:1024], 'b')
    ax1.set_title('detector signal 1')
    ax2.plot(data[2, 0:1024], data[3, 0:1024], 'r')
    ax2.set_title('detector signal 2')
    ax3.plot(data[4, 0:1024], data[5, 0:1024], 'g')
    ax3.set_title('detector signal 3')
    ax4.plot(data[6, 0:1024], data[7, 0:1024], 'y')
    ax4.set_title('detector signal 4')

    fig.subplots_adjust(wspace=0.2)
    plt.show()

