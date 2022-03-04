import h5py
import numpy as np
import matplotlib.pyplot as plt

f = h5py.File('D:\\oxcart\\data\\200_Jun-07-2021_10-29_test_w3\\test_w3_data.h5', 'a')
# f = h5py.File('D:\\oxcart\\data\\243_Jun-16-2021_13-47_test\\test_data.h5', 'a')

def h5printR(item, leading = ''):
    for key in item:
        if isinstance(item[key], h5py.Dataset):
            print(leading + key + ': ' + str(item[key].shape))
        else:
            print(leading + key)
            h5printR(item[key], leading + '  ')

# Print structure of a `.h5` file
def h5print(filename):
    with h5py.File(filename, 'r') as h:
        print(filename)
        h5printR(h, '  ')

# h5print('D:\\oxcart\\data\\200_Jun-07-2021_10-29_test_w3\\test_w3_data.h5')



# x = np.array(f['dld/x'])
# y = np.array(f['dld/y'])
# t = np.array(f['dld/t'])
# v = np.array(f['dld/high_voltage'])
x = np.array(f['dld/x'])
y = np.array(f['dld/y'])
t = np.array(f['dld/t'])
v = np.array(f['dld/high_voltage'])

print(x.shape, np.max(x), np.min(x))
print(y.shape, np.max(y), np.min(y))
print(t.shape, np.max(t), np.min(t))
print(v.shape, np.max(v), np.min(v))

# m/q = (2 * e * v * t**2 ) / (d**2)
d_0 = 110
e = 1.602 * (10**(-19))

pix_size_x = 0.03243
pix_size_y = 0.03257

x_n = x - 2450
y_n = y - 2450

x_n = x_n * pix_size_x
y_n = y_n * pix_size_y

t_n = t * 27.432 * (10**-12)
l = np.sqrt((d_0**2) + (x_n**2) + (y_n**2))

math_to_charge = (2 * v * e * (t_n**2)) / (l * (((10**-3))**2))

print(np.max(math_to_charge), np.min(math_to_charge))

math_to_charge = math_to_charge[math_to_charge > 10**-18]
print(np.max(math_to_charge), np.min(math_to_charge))
ax1 = plt.subplot(411)
ax1.set_title("m/n")
hist, bins, _ = plt.hist(math_to_charge, bins=128)

# logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]), 128)
logbins = np.logspace(np.log10(np.min(math_to_charge)),
                   np.log10(np.max(math_to_charge)),
                   num=128)
ax2 = plt.subplot(412)
ax2.set_title("Logarithmic m/n")
plt.hist(math_to_charge, bins=logbins)


print(max(t), min(t))
t = t[t<800000]
bins = np.logspace(np.log10(np.min(t)),
                   np.log10(np.max(t)),
                   num=128)

ax3 = plt.subplot(413)
ax3.set_title("tof")
plt.hist(t, bins=128)



ax4 = plt.subplot(414)
ax4.set_title("Logarithmic tof")
plt.hist(t, bins=bins)
plt.show()

f.close()
