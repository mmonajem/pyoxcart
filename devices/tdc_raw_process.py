"""
This is the main new script for reading TDC.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""

import numpy as np
import h5py

with h5py.File('D:\\oxcart\\data\\741_Aug-02-2021_15-45_test\\test_data.h5', 'a') as f:
    channel = np.array(f['tdc/channel'])
    time_data = np.array(f['tdc/time_data'])
    start_counter = np.array(f['tdc/start_counter'])
    high_voltage = np.array(f['tdc/high_voltage'])
    pulse_voltage = np.array(f['tdc/pulse_voltage'])


def idx_search():
    a = np.zeros(0)
    b = np.zeros(0)
    cat = np.zeros((1,20))
    index = np.zeros((1,20))
    for i in range(len(start_counter)):
        temp = start_counter[i]
        b = np.append(b, i)
        if i+1 < len(start_counter):
            if i==0:
                a = np.append(a, start_counter[i])
            if temp == start_counter[i+1]:
                a = np.append(a, start_counter[i+1])
            else:
                while len(a) < 20:
                    a = np.append(a, np.NaN)
                while len(b) < 20:
                    b = np.append(b, np.NaN)

                a = np.expand_dims(a, axis=0)
                b = np.expand_dims(b, axis=0)
                cat = np.concatenate((cat, a), axis=0)
                index = np.concatenate((index, b), axis=0)
                a = np.zeros(0)
                b = np.zeros(0)
    cat = cat[1:,:]
    index = index[1:,:]
    idx_sort = np.argsort(start_counter)
    sorted_records_array = start_counter[idx_sort]
    vals, idx_start, count = np.unique(sorted_records_array, return_counts=True, return_index=True)
    res = np.split(idx_sort, idx_start[1:])
    count = 0
    count_4 = 0
    count_3 = 0
    count_2 = 0
    count_1 = 0
    count_even = 0
    count_odd = 0
    count_big_even = 0
    count_big_odd = 0
    for i in range(len(res)):
        count += 1
        if len(res[i]) == 4:
            # print(res[i])
            count_4 += 1
        elif len(res[i]) == 3:
            count_3 += 1
        elif 1 < len(res[i]) == 2:
            count_2 += 1
        elif len(res[i]) == 1:
            count_1 += 1
        else:
            if (len(res[i]) % 4) == 0:
                count_big_even += 1
            else:
                count_big_odd += 1

        if (len(res[i]) % 4) == 0:
            count_even += 1
        else:
            count_odd += 1

    print('count', count)
    print('count_even', count_even)
    print('count_odd', count_odd)
    print('count_big_even', count_big_even)
    print('count_big_odd', count_big_odd)
    print('count_4', count_4)
    print('count_3', count_3)
    print('count_2', count_2)
    print('count_1', count_1)

idx_search()
a = np.array(([1,2,3], [2,3]))
print(a)
# a = np.zeros(0)
# for i in range(start_counter):
#     val = start_counter[i]
#     b = [i]
#     j = 0
#     while start_counter[i + j] == val:
#         b += [i + j]
#         j += 1
#     a = np.concatenate((a, b), 1)
#     i = i+j
