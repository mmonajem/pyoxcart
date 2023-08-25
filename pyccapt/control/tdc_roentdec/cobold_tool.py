import h5py
import numpy as np


def copy_xy_from_cobold_txt_to_hdf5(txt_path, save_path):
	"""
	Copy x and y data from Cobold text file to an existing HDF5 file.

	Args:
		txt_path (str): Path to the Cobold text file.

	Returns:
		None
	"""
	# Read data from text file
	with open(txt_path, 'r') as f:
		data = np.loadtxt(f)

	xx = data[:, 6] / 10
	yy = data[:, 7] / 10

	with h5py.File(save_path, 'r+') as file:
		del file['dld/x']
		del file['dld/y']

		file.create_dataset('dld/x', data=xx)
		file.create_dataset('dld/y', data=yy)

	print('finish')


def cobold_txt_to_hdf5(txt_path):
	"""
	Convert Cobold text data to an HDF5 file.

	Args:
		txt_path (str): Path to the Cobold text file.

	Returns:
		None
	"""
	with open(txt_path, 'r') as f:
		data = np.loadtxt(f)

	xx = data[:, 6] / 10
	yy = data[:, 7] / 10
	tof = data[:, 8]

	with h5py.File('data_TiO2.h5', "w") as f:
		f.create_dataset("dld/x", data=xx, dtype='f')
		f.create_dataset("dld/y", data=yy, dtype='f')
		f.create_dataset("dld/t", data=tof, dtype='f')
		f.create_dataset("dld/start_counter", data=np.zeros(len(xx)), dtype='i')
		f.create_dataset("dld/high_voltage", data=np.full(len(xx), 5300), dtype='f')
		f.create_dataset("dld/pulse", data=np.zeros(len(xx)), dtype='f')

	print('finish')


if __name__ == "__main__":
	txt_path = 'LFIM14_DAn.txt'
	cobold_txt_to_hdf5(txt_path)
