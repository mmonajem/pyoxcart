from copy import copy
from matplotlib import cm
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams, colors
from matplotlib.patches import Circle
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar


from pyccapt.calibration.data_tools.data_loadcrop import elliptical_shape_selector



def plot_density_map(x, y, z=False, bins=(256, 256), frac=1.0, axis_mode='normal', figure_size=(5, 4), variables=None,
                  range_sequence=[], range_mc=[], range_detx=[], range_dety=[], range_x=[], range_y=[], range_z=[],
                  range_vol=[], data_crop=False, draw_circle=False, mode_selector='circle', axes=['x', 'y'],
                     save=False, figname='', cmap='plasma'):
    """
    Plot and crop the FDM with the option to select a region of interest.

    Args:
        x: x-axis data
        y: y-axis data
        z: z weight data
        bins: Number of bins for the histogram
        frac: Fraction of the data to be plotted
        axis_mode: Flag to choose whether to plot axis or scalebar: 'normal' or 'scalebar'
        variables: Variables object
        range_sequence: Range of sequence
        range_mc: Range of mc
        range_detx: Range of detx
        range_dety: Range of dety
        range_x: Range of x-axis
        range_y: Range of y-axis
        range_z: Range of z-axis
        range_vol: Range of voltage
        figure_size: Size of the plot
        draw_circle: Flag to enable circular region of interest selection
        mode_selector: Mode of selection (circle or ellipse)
        axes: Axes for the histogram
        save: Flag to choose whether to save the plot or not
        data_crop: Flag to control whether only the plot is shown or cropping functionality is enabled
        figname: Name of the figure to be saved
        cmap: Colormap for the plot

    Returns:
        None
    """
    if range_sequence or range_mc or range_detx or range_dety or range_x or range_y or range_z:
        if range_sequence:
            mask_sequence = np.zeros_like(len(x), dtype=bool)
            mask_sequence[range_sequence[0]:range_sequence[1]] = True
        else:
            mask_sequence = np.ones(len(x), dtype=bool)
        if range_detx and range_dety:
            mask_det_x = (variables.dld_x_det < range_detx[1]) & (variables.dld_x_det > range_detx[0])
            mask_det_y = (variables.dld_y_det < range_dety[1]) & (variables.dld_y_det > range_dety[0])
            mask_det = mask_det_x & mask_det_y
        else:
            mask_det = np.ones(len(variables.dld_x_det), dtype=bool)
        if range_mc:
            mask_mc = (variables.mc <= range_mc[1]) & (variables.mc >= range_mc[0])
        else:
            mask_mc = np.ones(len(variables.mc), dtype=bool)
        if range_x and range_y and range_z:
            mask_x = (variables.x < range_x[1]) & (variables.x > range_x[0])
            mask_y = (variables.y < range_y[1]) & (variables.y > range_y[0])
            mask_z = (variables.z < range_z[1]) & (variables.z > range_z[0])
            mask_3d = mask_x & mask_y & mask_z
        else:
            mask_3d = np.ones(len(variables.x), dtype=bool)
        if range_vol:
            mask_vol = (variables.dld_high_voltage < range_vol[1]) & (variables.dld_high_voltage > range_vol[0])
        else:
            mask_vol = np.ones(len(variables.dld_high_voltage), dtype=bool)
        mask = mask_sequence & mask_det & mask_mc & mask_3d & mask_vol
        variables.mask = mask
        print('The number of data mc:', len(mask_mc[mask_mc == True]))
        print('The number of data det:', len(mask_det[mask_det == True]))
        print('The number of data 3d:', len(mask_3d[mask_3d == True]))
        print('The number of data after cropping:', len(mask[mask == True]))
    else:
        mask = np.ones(len(x), dtype=bool)

    x = x[mask]
    y = y[mask]

    if frac < 1:
        # set axis limits based on fraction of x and y data baded on fraction
        mask_fraq = np.random.choice(len(x), int(len(x) * frac), replace=False)
        x_t = np.copy(x)
        y_t = np.copy(y)
        x = x[mask_fraq]
        y = y[mask_fraq]


    fig1, ax1 = plt.subplots(figsize=figure_size, constrained_layout=True)


    # Check if the bin is a tuple
    if isinstance(bins, tuple):
        pass
    else:
        x_edges = np.arange(x.min(), x.max() + bins, bins)
        y_edges = np.arange(y.min(), y.max() + bins, bins)
        bins = [x_edges, y_edges]

    if z is False:
        FDM, xedges, yedges = np.histogram2d(x, y, bins=bins)
    else:
        FDM, xedges, yedges = np.histogram2d(x, y, bins=bins, weights=z)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    cmap_instance = copy(cm.get_cmap(cmap))
    cmap_instance.set_bad(cmap_instance(0))
    pcm = ax1.pcolormesh(xedges, yedges, FDM.T, cmap=cmap_instance, norm=colors.LogNorm(), rasterized=True)
    cbar = fig1.colorbar(pcm, ax=ax1, pad=0)
    cbar.set_label('Event Counts', fontsize=10)

    if frac < 1:
        # extract tof
        x_lim = x_t
        y_lim = y_t

        ax1.set_xlim([min(x_lim), max(x_lim)])
        ax1.set_ylim([min(y_lim), max(y_lim)])

    if variables is not None:
        if data_crop:
            elliptical_shape_selector(ax1, fig1, variables, mode=mode_selector)
        if draw_circle:
            print('x:', variables.selected_x_fdm, 'y:', variables.selected_y_fdm, 'roi:', variables.roi_fdm)
            circ = Circle((variables.selected_x_fdm, variables.selected_y_fdm), variables.roi_fdm, fill=True,
                          alpha=0.3, color='green', linewidth=5)
            ax1.add_patch(circ)
    if axis_mode == 'scalebar':
        fontprops = fm.FontProperties(size=10)
        scalebar = AnchoredSizeBar(ax1.transData,
                                   1, '1 cm', 'lower left',
                                   pad=0.1,
                                   color='white',
                                   frameon=False,
                                   size_vertical=0.1,
                                   fontproperties=fontprops)

        ax1.add_artist(scalebar)
        plt.axis('off')  # Turn off both x and y axes
    elif axis_mode == 'normal':
        if 'x' in axes and 'y' in axes:
            ax1.set_xlabel(r"$x (nm)$", fontsize=10)
            ax1.set_ylabel(r"$y (nm)$", fontsize=10)
        elif 'y' in axes and 'z' in axes:
            ax1.set_xlabel(r"$y (nm)$", fontsize=10)
            ax1.set_ylabel(r"$z (nm)$", fontsize=10)
        elif 'x' in axes and 'z' in axes:
            ax1.set_xlabel(r"$x (nm)$", fontsize=10)
            ax1.set_ylabel(r"$z (nm)$", fontsize=10)

    if save and variables is not None:
        # Enable rendering for text elements
        rcParams['svg.fonttype'] = 'none'
        plt.savefig("%s.png" % (variables.result_path + figname), format="png", dpi=600)
        plt.savefig("%s.svg" % (variables.result_path + figname), format="svg", dpi=600)
    plt.show()