import os

from pyccapt.calibration.calibration_tools import share_variables
from pyccapt.calibration.data_tools import data_tools
from pyccapt.calibration.mc import tof_tools


def load_data(dataset_path, max_mc, flightPathLength, pulse_mode, tdc):
	# Calculate the maximum possible time of flight (TOF)
	max_tof = int(tof_tools.mc2tof(max_mc.value, 1000, 0, 0, flightPathLength.value))
	print('The maximum possible TOF is:', max_tof, 'ns')
	print('=============================')
	# create an instance of the Variables opject
	variables = share_variables.Variables()
	variables.pulse_mode = pulse_mode.value
	dataset_main_path = os.path.dirname(dataset_path)
	dataset_name_with_extention = os.path.basename(dataset_path)
	variables.dataset_name = os.path.splitext(dataset_name_with_extention)[0]
	variables.result_data_path = dataset_main_path + '/' + variables.dataset_name + '/load_crop/'
	variables.result_data_name = variables.dataset_name
	variables.result_path = dataset_main_path + '/' + variables.dataset_name + '/load_crop/'

	if not os.path.isdir(variables.result_path):
		os.makedirs(variables.result_path, mode=0o777, exist_ok=True)

	print('The data will be saved on the path:', variables.result_data_path)
	print('=============================')
	print('The dataset name after saving is:', variables.result_data_name)
	print('=============================')
	print('The figures will be saved on the path:', variables.result_path)
	print('=============================')

	# Create data farame out of hdf5 file dataset
	dld_group_storage = data_tools.load_data(dataset_path, tdc.value, mode='raw')

	# Remove the data with tof greater thatn Max TOF or below 0 ns
	data = data_tools.remove_invalid_data(dld_group_storage, max_tof)
	print('Total number of Ions:', len(data))

	variables.data = data
	variables.data_backup = data.copy()
	variables.max_mc = max_mc.value
	variables.max_tof = max_tof
	variables.flight_path_length = flightPathLength.value
	variables.pulse_mode = pulse_mode.value

	return variables
