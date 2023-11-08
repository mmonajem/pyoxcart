import h5py
import numpy as np


def copy_xy_from_cobold_txt_to_hdf5(txt_path, save_path):
	"""
	Copy x and y data from Cobold text file to an existing HDF5 file.

	Args:
		txt_path (str): Path to the Cobold text file.
		save_path (str): Path to the save file.

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


def cobold_txt_to_hdf5(txt_path, save_path):
	"""
	Convert Cobold text data to an HDF5 file.

	Args:
		txt_path (str): Path to the Cobold text file.
		save_path (str): Path to the save file.
	Returns:
		None
	"""
	with open(txt_path, 'r') as f:
		data = np.loadtxt(f)

	xx = data[:, 6] / 10
	yy = data[:, 7] / 10
	tof = data[:, 8]

	with h5py.File(save_path, "w") as f:
		f.create_dataset("dld/x", data=xx, dtype='f')
		f.create_dataset("dld/y", data=yy, dtype='f')
		f.create_dataset("dld/t", data=tof, dtype='f')
		f.create_dataset("dld/start_counter", data=np.zeros(len(xx)), dtype='i')
		f.create_dataset("dld/high_voltage", data=np.full(len(xx), 5300), dtype='f')
		f.create_dataset("dld/pulse", data=np.zeros(len(xx)), dtype='f')

	print('finish')


def convert_ND_angle_to_laser_intensity(file_path, ref_laser_intensity, ref_angle):
	with h5py.File(file_path, 'r+') as data:
		laser_intensity = data['dld/pulse'][:]
		OD = (laser_intensity - ref_angle) / 270
		scale = 10 ** OD
		dld_pulse = ref_laser_intensity * scale
		del data['dld/pulse']
		data.create_dataset("dld/pulse", data=dld_pulse, dtype='f')

if __name__ == "__main__":
	# txt_path = '../../../tests/data/physics_experiment/data_130_Sep-19-2023_14-58_W_12fs.txt'
	# save_path = '../../../tests/data/physics_experiment/data_130_Sep-19-2023_14-58_W_12fs.h5'
	# copy_xy_from_cobold_txt_to_hdf5(txt_path, save_path)
	file_path = '../../../tests/data/physics_experiment/data_124_Apr-18-2023_18-46_LFIM1.h5'
	# (at 242°) corresponds to an intensity of 1.4e13 W/cm^2.
	# 170 fs the highest intensity is at 3.4e13 W/cm^2
	# Energy (J) = Power Density (W/cm^2) * Area (cm^2) * Pulse Duration (s)
	ref_angle = 242
	ref_laser_intensity = 3.4e13 * 12e-15 * 4e-4 * 4e-4 * np.pi / 1e-12
	# ref_laser_intensity = 1.4 * 12 * 4 * 4 * np.pi
	print(ref_laser_intensity)
	convert_ND_angle_to_laser_intensity(file_path, ref_laser_intensity, ref_angle)
	print('Done')
