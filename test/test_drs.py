"""
This is the main script for testing drs digitizer.
It contains the main control loop of experiment.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""
# import the module
import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np
import matplotlib.pyplot as plt
import time
import h5py

# load the library
drs_lib = ctypes.CDLL("../drs/drs_lib.dll")


class DRS(object):
    def __init__(self, trigger, test, delay, sample_frequency):
        # trigger=0 --> Internal trigger
        # trigger=1 --> External rigger
        # test=0 --> Test mode off
        # test=1 --> test mode - connect 100 MHz clock connected to all channels
        # Trigger delay in ns
        drs_lib.Drs_new.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float]
        drs_lib.Drs_new.restype = ctypes.c_void_p
        drs_lib.Drs_reader.argtypes = [ctypes.c_void_p]
        drs_lib.Drs_reader.restype = ndpointer(dtype=ctypes.c_float, shape=(8 * 1024,))
        drs_lib.Drs_delete_drs_ox.restype = ctypes.c_void_p
        drs_lib.Drs_delete_drs_ox.argtypes = [ctypes.c_void_p]
        self.obj = drs_lib.Drs_new(trigger, test, delay, sample_frequency)

    def reader(self, ):
        data = drs_lib.Drs_reader(self.obj)
        return data

    def delete_drs_ox(self):
        drs_lib.Drs_delete_drs_ox(self.obj)


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

# with h5py.File('data.h5', "w") as f:
#     f.create_dataset("detector_0_time", data=data_final[0, 0:1024], dtype='f')
#     f.create_dataset("detector_0_voltage", data=data_final[1, 0:1024], dtype='f')
#     f.create_dataset("detector_1_time", data=data_final[2, 0:1024], dtype='f')
#     f.create_dataset('detector_1_voltage', data=data_final[3, 0:1024], dtype='f')
#     f.create_dataset('detector_2_time', data=data_final[4, 0:1024], dtype='f')
#     f.create_dataset("detector_2_voltage", data=data_final[5, 0:1024], dtype='f')
#     f.create_dataset('detector_3_time', data=data_final[6, 0:1024], dtype='f')
#     f.create_dataset("detector_3_voltage", data=data_final[7, 0:1024], dtype='f')