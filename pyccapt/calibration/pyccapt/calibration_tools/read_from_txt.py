import pandas as pd
import numpy as np
import os.path as path
import h5py

p = path.abspath(path.join("", '../../../../tests/data/2022_07_04/'))
name = ['LFIM1_DAn', 'LFIM2_cooled_DAn', 'LFIM5_Erbium_DAn', 'LFIM6_Erbium_DAn', 'LFIM7_DAn']
high_voltage = [3651, 3643, 6152, 6974, 6974]

# p = path.abspath(path.join("", '../../../../tests/data/2022_07_05/'))
# name = ['LFIM1_BJ_G_OPCPA_DAn', 'LFIM2_BJ_G_OPCPA_cooled_DAn', 'LFIM3_BJ_G_Erbium_cooled_DAn', 'LFIM4_BJ_G_Erbium_cooled_DAn',
#         'LFIM5_BJ_G_Erbium_cooled_DAn', 'LFIM6_BJ_G_Erbium_cooled_DAn', 'LFIM7_BJ_G_Erbium_cooled_DAn', 'LFIM8_BJ_G_Erbium_cooled_DAn']
# high_voltage = [3900, 4214, 5915, 5915, 5915, 5915, 5777, 6210]


for i in range(len(name)):
    data = pd.read_table(p + '/' + name[i] + '.txt', delimiter=" ", header=None, index_col=None)
    with h5py.File(p + '\\%s.h5' % name[i], "w") as f:
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
        f.create_dataset("dld/high_voltage", data=np.full((len(data[1])), high_voltage[i]), dtype='f')

        f.create_dataset("tdc/ch0", 0, dtype='i')
        f.create_dataset("tdc/ch1", 0, dtype='i')
        f.create_dataset("tdc/ch2", 0, dtype='i')
        f.create_dataset("tdc/ch3", 0, dtype='i')
        f.create_dataset("tdc/ch4", 0, dtype='i')
        f.create_dataset("tdc/ch5", 0, dtype='i')
        f.create_dataset("tdc/ch6", 0, dtype='i')
        f.create_dataset("tdc/ch7", 0, dtype='i')

print(data)
