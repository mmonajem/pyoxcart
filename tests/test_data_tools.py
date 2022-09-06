from unittest.mock import patch, MagicMock
import os
import pandas as pd
import scipy
from deepdiff import DeepDiff

from calibration_tools import data_tools

p = os.path.abspath(os.path.join("", "."))
path = p + '//data//data_tests//'
test_file_name = 'OLO_AL_6_data.h5'


@patch.object(data_tools.logger, "critical")
def test_read_hdf5_file_not_found(mock):
    file_name = path + 'not_existing_file.h5'
    response = data_tools.read_hdf5(file_name, 'surface_concept')
    mock.assert_called_with("[*] HDF5 File could not be found")


def test_read_hdf5_no_grp_keys():
    filename = path + test_file_name
    response = data_tools.read_hdf5(filename, 'surface_concept')
    assert isinstance(response, dict)


def test_read_hdf5_through_pandas_check_returnType():

    file_name = path + 'isotopeTable.h5'
    response = data_tools.read_hdf5_through_pandas(file_name)
    assert isinstance(response, pd.core.frame.DataFrame)


@patch.object(data_tools.logger, "critical")
def test_read_hdf5_through_pandas_file_not_found(mock):
    file_name = path + 'not_existing_file.h5'
    response = data_tools.read_hdf5_through_pandas(file_name)
    mock.assert_called_with("[*] HDF5 File could not be found")


def test_read_hdf5_through_pandas_check_response():
    filename = path + 'isotopeTable.h5'
    test_response = pd.read_hdf(filename, mode='r')
    response = data_tools.read_hdf5_through_pandas(filename)
    assert test_response.equals(response)


@patch.object(data_tools.logger, "critical")
def test_read_mat_files_file_not_found(mock):
    filename = path + 'not_existing_file.mat'
    response = data_tools.read_mat_files(filename)
    mock.assert_called_with("[*] Mat File could not be found")


def test_read_mat_files_check_response():
    filename = path + 'isotopeTable.mat'
    test_response = scipy.io.loadmat(filename)
    response = data_tools.read_mat_files(filename)
    diff = DeepDiff(test_response, response)
    assert len(diff) == 0


def test_read_mat_files_check_returnType():
    filename = path + 'isotopeTable.mat'
    response = data_tools.read_mat_files(filename)
    assert isinstance(response, dict)


def test_convert_mat_to_df_check_returnType():
    filename = path + 'isotopeTable.mat'
    data = data_tools.read_mat_files(filename)
    data_tools.store_df_to_hdf = MagicMock()
    response = data_tools.convert_mat_to_df(data)
    assert isinstance(response, pd.core.frame.DataFrame)


def test_store_df_to_hdf_check_response():
    filename = path + 'isotopeTable.mat'
    matFileResponse = data_tools.read_mat_files(filename)
    pdDataframe = pd.DataFrame(matFileResponse['None'])
    filename = path + 'unittests_dummy.h5'
    data_tools.store_df_to_hdf(filename, pdDataframe, 'data')
    response = data_tools.read_hdf5_through_pandas(filename)
    assert pdDataframe.equals(response)