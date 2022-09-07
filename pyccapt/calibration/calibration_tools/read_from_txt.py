import pandas as pd
import os.path as path
import h5py

# Local module and scripts
from pyccapt.calibration.calibration_tools import data_loadcrop

p = path.abspath(path.join("", '../../../tests/data/'))
name = ['data_97_Jul-22-2022_15-25_With_laser_2']

# high_voltage = [3651]


dataset_name = "data_115_Jul-27-2022_17-44_Powersweep3"
filename = p + '//' + dataset_name + '.h5'
dldGroupStorage = data_loadcrop.fetch_dataset_from_dld_grp(filename, tdc='roentdec')

for i in range(len(name)):
    data = pd.read_table(p + '/' + name[i] + '.txt', delimiter=" ", header=None, index_col=None)
    with h5py.File(p + '\\%s_2.h5' % name[i], "w") as f:
        f.create_dataset("apt/high_voltage", 0, dtype='f')
        f.create_dataset("apt/num_events", 0, dtype='i')
        f.create_dataset("apt/time_counter", 0, dtype='i')

        f.create_dataset("time/time_s", 0, dtype='i')
        f.create_dataset("time/time_m", 0, dtype='i')
        f.create_dataset("time/time_h", 0, dtype='i')

        f.create_dataset("dld/x", data=data[6], dtype='i')
        f.create_dataset("dld/y", data=data[7], dtype='i')
        f.create_dataset("dld/t", data=data[8], dtype='i')
        f.create_dataset("dld/AbsoluteTimeStamp", data=data[3], dtype='i')

        # f.create_dataset("dld/high_voltage", data=np.full((len(data[1])), high_voltage[i]), dtype='f')
        f.create_dataset("dld/high_voltage", data=dldGroupStorage[0], dtype='f')

        # f.create_dataset("dld/laser_intensity", data=np.full((len(data[1])), high_voltage[i]), dtype='f')
        f.create_dataset("dld/laser_intensity", data=dldGroupStorage[1], dtype='f')

        f.create_dataset("tdc/ch0", 0, dtype='i')
        f.create_dataset("tdc/ch1", 0, dtype='i')
        f.create_dataset("tdc/ch2", 0, dtype='i')
        f.create_dataset("tdc/ch3", 0, dtype='i')
        f.create_dataset("tdc/ch4", 0, dtype='i')
        f.create_dataset("tdc/ch5", 0, dtype='i')
        f.create_dataset("tdc/ch6", 0, dtype='i')
        f.create_dataset("tdc/ch7", 0, dtype='i')

print(data)
