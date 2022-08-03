
from unittest.mock import patch, Mock, MagicMock
import matplotlib.pyplot as plt
import os


from pyccapt.calibration_tools import data_loadcrop, data_tools


<<<<<<< HEAD
p = os.path.abspath(os.path.join("", "."))
=======
p = os.path.abspath(os.path.join("",
                                 "../../../Downloads/Compressed/pyccapt-/pyccapt-fa5750ba9a4d60be3b1d4216313cb4907cefc50f/tests"))
>>>>>>> 82136ce (add unit tests)
path = p + '//data//data_tests//'
test_file_name = 'OLO_Al_6_data.h5'


def return_master_df_list():

    filename = path + test_file_name
    list_of_dataframes = data_loadcrop.fetch_dataset_from_dld_grp(filename, 'surface_concept')
    response = data_loadcrop.concatenate_dataframes_of_dld_grp(list_of_dataframes)
    return response


def test_fetch_dataset_from_dld_grp_check_returnType():
    filename = path + test_file_name
    response = data_loadcrop.fetch_dataset_from_dld_grp(filename, 'surface_concept')
    assert isinstance(response, list)


@patch.object(data_loadcrop.logger, "critical")
def test_fetch_dataset_from_dld_grp_check_key_missing(mock):
    filename = path + test_file_name
    data = data_tools.read_hdf5(filename, 'surface_concept')
    data.pop('dld/high_voltage')
    data_loadcrop.data_tools.read_hdf5 = Mock(return_value=data)
    response = data_loadcrop.fetch_dataset_from_dld_grp(filename, 'surface_concept')
    mock.assert_called_with("[*]Keys missing in the dataset")


@patch.object(data_loadcrop.logger, "critical")
def test_fetch_dataset_from_dld_grp_file_not_found(mock):
    file_name = 'not.h5'
    data_response = data_tools.read_hdf5(file_name)
    data_loadcrop.data_tools.read_hdf5 = Mock(return_value=data_response)
    response = data_loadcrop.fetch_dataset_from_dld_grp(file_name, 'surface_concept')
    mock.assert_called_with("[*] HDF5 file not found")


def test_concatenate_dataframes_of_dld_grp_functionality():
    filename = path + test_file_name
    data_response = data_tools.read_hdf5(filename)
    data_loadcrop.data_tools.read_hdf5 = Mock(return_value = data_response)
    list_of_dataframes = data_loadcrop.fetch_dataset_from_dld_grp(filename, 'surface_concept')
    df1_column_len = int(len(list_of_dataframes[0].columns))
    df2_column_len = int(len(list_of_dataframes[1].columns))
    df3_column_len = int(len(list_of_dataframes[2].columns))
    df4_column_len = int(len(list_of_dataframes[3].columns))
    df5_column_len = int(len(list_of_dataframes[4].columns))
    df6_column_len = int(len(list_of_dataframes[5].columns))
    response = data_loadcrop.concatenate_dataframes_of_dld_grp(list_of_dataframes)
    assert len(response.columns) == (df1_column_len + df2_column_len + df3_column_len + df4_column_len + df5_column_len+df6_column_len)


@patch.object(data_loadcrop, "rectangle_box_selector")
def test_plot_graph_for_dld_high_voltage_rect_equal_none_func(mock):
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    filename = path + test_file_name
    response = data_loadcrop.fetch_dataset_from_dld_grp(filename, 'surface_concept')
    data_loadcrop.plot_graph_for_dld_high_voltage(ax1, response)
    mock.assert_called()


@patch.object(data_loadcrop.plt, "savefig")
def test_plot_graph_for_dld_high_voltage_plt_save_func(mock):
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    filename = path + test_file_name
    response = data_loadcrop.fetch_dataset_from_dld_grp(filename, 'surface_concept')
    data_loadcrop.plot_graph_for_dld_high_voltage(ax1, response, save_name="test_plot")
    mock.assert_called()


@patch.object(data_loadcrop, "RectangleSelector")
def test_rectangle_box_selector_func(mock):
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    data_loadcrop.rectangle_box_selector(ax1)
    mock.assert_called()




'''
@patch('data_loadcrop.variables.selected_x1',0)
#@patch('data_loadcrop.variables.selected_x2',0)
def test_crop_dataset_check_functionality():
    import pandas as pd
    d = {'col1': [1, 2], 'col2': [3, 4],'col3': [4, 5],'col4': [6, 4]}
    df = pd.DataFrame(data=d)
    #data_loadcrop.variables.selected_x1 = MagicMock(return_value = 0)
    #data_loadcrop.variables.selected_x2 = MagicMock(return_value = 0)
    response = data_loadcrop.crop_dataset(df)
    print("response",response)
    #assert len(response) == 1
'''


@patch.object(data_loadcrop, "elliptical_shape_selector")
def test_plot_crop_FDM_functionality(mock):
    import matplotlib.pyplot as plt
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    master_df = return_master_df_list()
    master_df = master_df.to_numpy()
    cropped_df = master_df[0:20:]
    plt.imshow = MagicMock()
    data_loadcrop.plot_crop_FDM(ax1,fig1,cropped_df)
    mock.assert_called()


@patch.object(data_loadcrop.logger, "info")
def test_plot_crop_FDM_save_fig_func(mock):
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    master_df = return_master_df_list()
    master_df = master_df.to_numpy()
    cropped_df = master_df[0:20:]
    plt.imshow = MagicMock()
    plt.savefig = MagicMock()
    data_loadcrop.plot_crop_FDM(ax1, fig1, cropped_df, "test_plot")
    mock.assert_called_with("Plot saved by the name test_plot")


'''
@patch.object(data_loadcrop.logger, "info")   
def test_plot_FDM_after_selection_functionality(mock):
    import variables
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    master_df = return_master_df_list()
    master_df = master_df.to_numpy()
    cropped_df = master_df[0:20:]
    plt.imshow = MagicMock()
    variables.selected_x_fdm = MagicMock()
    variables.selected_y_fdm = MagicMock()
    data_loadcrop.plot_FDM_after_selection(ax1,fig1,cropped_df)
    mock.assert_called_with("Circle selector Called")
'''
'''
@patch.object(data_loadcrop.logger, "info") 
def test_plot_FDM_after_selection_save_fig_func(mock):
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    master_df = return_master_df_list()
    master_df = master_df.to_numpy()
    cropped_df = master_df[0:20:]
    plt.imshow = MagicMock()
    plt.savefig = MagicMock()
    data_loadcrop.plot_crop_FDM(ax1,fig1,cropped_df,"test_plot")
    mock.assert_called_with("Plot saved by the name test_plot") 
'''
'''
'''
@patch.object(data_loadcrop.plt, "imshow")
def test_plot_FDM_functionality(mock):
    import matplotlib.pyplot as plt
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    master_df = return_master_df_list()
    master_df = master_df.to_numpy()
    cropped_df = master_df[0:20:]
    data_loadcrop.plot_FDM(ax1,fig1,cropped_df)
    mock.assert_called()

@patch.object(data_loadcrop.logger, "info")
def test_plot_FDM_save_fig_func(mock):
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    master_df = return_master_df_list()
    master_df = master_df.to_numpy()
    cropped_df = master_df[0:20:]
    plt.imshow = MagicMock()
    plt.savefig = MagicMock()
    data_loadcrop.plot_FDM(ax1,fig1,cropped_df,"test_plot")
    mock.assert_called_with("Plot saved by the name test_plot")

@patch.object(data_loadcrop.data_tools, "store_df_to_hdf")
def test_save_croppped_data_to_hdf5_func(mock):
    master_df =  return_master_df_list()
    master_df =  master_df.to_numpy()
    cropped = master_df[:20:]
    data_tools.store_df_to_hdf = MagicMock()
    data_loadcrop.save_croppped_data_to_hdf5(cropped,master_df,"../files/unittests_dummy_test.h5")
    mock.assert_called()