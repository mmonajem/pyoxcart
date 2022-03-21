import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector, EllipseSelector
from matplotlib.patches import Circle
import pandas as pd
import selector, variables, data_tools


def fetch_dataset_from_dld_grp(filename:"type: string - Path to hdf5(.h5) file")->"type:list - list of dataframes":
    try:
        hdf5Data = data_tools.read_hdf5(filename)
        dld_highVoltage = hdf5Data['dld/high_voltage']
        dld_pulseVoltage = hdf5Data['dld/pulse_voltage']
        dld_startCounter = hdf5Data['dld/start_counter']
        dld_t = hdf5Data['dld/t']
        dld_x = hdf5Data['dld/x']
        dld_y = hdf5Data['dld/y']
        dldGroupStorage = [dld_highVoltage, dld_pulseVoltage, dld_startCounter, dld_t, dld_x, dld_y]
        return dldGroupStorage
    except KeyError as error:
        print("[*]Keys missing in the dataset -> ", error)


def concatenate_dataframes_of_dld_grp(dataframeList:"type:list - list of dataframes")->"type:list - list of dataframes":
    dld_masterDataframeList = dataframeList
    dld_masterDataframe = pd.concat(dld_masterDataframeList, axis=1)
    return dld_masterDataframe


def plot_graph_for_dld_high_voltage(ax1:"type:object", dldGroupStorage:"type:list - list of dataframes"):
    # Plot tof and high voltage
    y = dldGroupStorage[3]  # dld_t
    y.loc[y['values'] > 5000, 'values'] = 0
    yaxis = y['values'].to_numpy()
    # y[y>5000] = 0
    xaxis = np.arange(len(yaxis))
    heatmap, xedges, yedges = np.histogram2d(xaxis, yaxis, bins=(1200, 800))
    heatmap[heatmap == 0] = 1  # to have zero after apply log
    heatmap = np.log(heatmap)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # set x-axis label
    ax1.set_xlabel("hit sequence number", color="red", fontsize=14)
    # set y-axis label
    ax1.set_ylabel("time of flight [ns]", color="red", fontsize=14)
    plt.title("Experiment history")
    plt.imshow(heatmap.T, extent=extent, origin='lower', aspect="auto")

    # plot high voltage curve
    ax2 = ax1.twinx()

    # dldGroupStorage[0] --> dld/high_voltage
    high_voltage = dldGroupStorage[0]['values'].to_numpy()
    xaxis = np.arange(len(high_voltage))
    ax2.plot(xaxis, high_voltage, color='r', linewidth=2)
    ax2.set_ylabel("DC voltage [V]", color="blue", fontsize=14)
    rectangle_box_selector(ax2)
    plt.connect('key_press_event', selector.toggle_selector)
    plt.show(block=True)


def rectangle_box_selector(axisObject:"type:object"):
    # drawtype is 'box' or 'line' or 'none'
    selector.toggle_selector.RS = RectangleSelector(axisObject, selector.line_select_callback,
                                                    useblit=True,
                                                    button=[1, 3],  # don't use middle button
                                                    minspanx=1, minspany=1,
                                                    spancoords='pixels',
                                                    interactive=True)


def crop_dataset(dld_masterDataframe:"type:list - list of dataframes")->"type:list  - cropped list content":
    dld_masterDataframe = dld_masterDataframe.to_numpy()
    data_crop = dld_masterDataframe[int(variables.selected_x1):int(variables.selected_x2), :]
    return data_crop


def elliptical_shape_selector(axisObject:"type:object", figureObject:"type:object"):
    # Helper
    # axisObject = ax1
    # figureObject = fig1
    selector.toggle_selector.ES = EllipseSelector(axisObject, selector.onselect, useblit=True,
                                                  button=[1, 3],  # don't use middle button
                                                  minspanx=1, minspany=1,
                                                  spancoords='pixels',
                                                  interactive=True)
    figureObject.canvas.mpl_connect('key_press_event', selector.toggle_selector)


def plot_crop_FDM(data_crop:"type:list  - cropped list content"):
    # Plot and crop FDM

    fig1, ax1 = plt.subplots(figsize=(4, 4))
    FDM, xedges, yedges = np.histogram2d(data_crop[:, 4], data_crop[:, 5], bins=(256, 256))

    FDM[FDM == 0] = 1  # to have zero after apply log
    FDM = np.log(FDM)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # set x-axis label
    ax1.set_xlabel("x [mm]", color="red", fontsize=14)
    # set y-axis label
    ax1.set_ylabel("y [mm]", color="red", fontsize=14)
    plt.title("FDM")
    plt.imshow(FDM.T, extent=extent, origin='lower', aspect="auto")
    elliptical_shape_selector(ax1, fig1)
    plt.show(block=True)


def plot_FDM_after_selection(data_crop:"type:list  - cropped list content"):
    # Plot FDM with selected part
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    FDM, xedges, yedges = np.histogram2d(data_crop[:, 4], data_crop[:, 5], bins=(256, 256))
    FDM[FDM == 0] = 1  # to have zero after apply log
    FDM = np.log(FDM)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # set x-axis label
    ax1.set_xlabel("x [mm]", color="red", fontsize=14)
    # set y-axis label
    ax1.set_ylabel("y [mm]", color="red", fontsize=14)
    plt.title("FDM")
    plt.imshow(FDM.T, extent=extent, origin='lower', aspect="auto")
    print('x:', variables.selected_x_fdm, 'y:', variables.selected_y_fdm, 'roi:', variables.roi_fdm)
    circ = Circle((variables.selected_x_fdm, variables.selected_y_fdm), variables.roi_fdm, color='b', fill=False)
    ax1.add_patch(circ)
    plt.show(block=True)


def crop_data_after_selection(data_crop:"type:list  - cropped list content")->list:
    # crop the data based on selected are of FDM
    detectorDist = np.sqrt(
        (data_crop[:, 4] - variables.selected_x_fdm) ** 2 + (data_crop[:, 5] - variables.selected_y_fdm) ** 2)
    mask_fdm = (detectorDist < variables.roi_fdm)
    return data_crop[np.array(mask_fdm)]


def plot_FDM(data_crop:"type:list  - cropped list content"):
    # Plot FDM
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    FDM, xedges, yedges = np.histogram2d(data_crop[:, 4], data_crop[:, 5], bins=(256, 256))
    FDM[FDM == 0] = 1  # to have zero after apply log
    FDM = np.log(FDM)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    # set x-axis label
    ax1.set_xlabel("x [mm]", color="red", fontsize=14)
    # set y-axis label
    ax1.set_ylabel("y [mm]", color="red", fontsize=14)
    plt.title("FDM")
    plt.imshow(FDM.T, extent=extent, origin='lower', aspect="auto")
    plt.show(block=True)


def save_croppped_data_to_hdf5(data_crop:"type:list  - cropped list content",
                               dld_masterDataframe:"type:list - list of dataframes", 
                               name:"type:string - name of h5 file"):
    # save the croped data

    filename = '%s_cropped.h5' % name
    hierarchyName = 'df'
    print('tofCropLossPct', (1 - len(data_crop) / len(dld_masterDataframe)) * 100)
    hdf5Dataframe = pd.DataFrame(data=data_crop,
                                 columns=['dld/high_voltage', 'dld/pulse_voltage', 'dld/start_counter', 'dld/t',
                                          'dld/x', 'dld/y'])
    data_tools.store_df_to_hdf(filename, hdf5Dataframe, hierarchyName)

# def main():
#     dldGroupStorage = fetch_dataset_from_dld_grp()
#     dld_masterDataframe = concatenate_dataframes_of_dld_grp(dldGroupStorage)
#     fig1, ax1 = plt.subplots(figsize=(6, 3))
#     plot_graph_for_dld_high_voltage(ax1, dldGroupStorage)
#     print('Min Idx:', variables.selected_x1, 'Max Idx:', variables.selected_x2)
#     data_crop = crop_dataset(dld_masterDataframe)
#     plot_crop_FDM(data_crop)
#     plot_FDM_after_selection(data_crop)
#     data_crop_FDM = crop_data_after_selection(data_crop)
#     plot_FDM(data_crop_FDM)
#     save_croppped_data_to_hdf5(data_crop_FDM, dld_masterDataframe)
#
#
# if __name__ == "__main__":
#     main()
