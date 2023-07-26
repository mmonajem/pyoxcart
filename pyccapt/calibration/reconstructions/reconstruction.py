import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.graph_objects as go

# Local module and scripts
from pyccapt.calibration.calibration_tools import share_variables
from pyccapt.calibration.data_tools import data_loadcrop, selectors_data


def cart2pol(x, y):
    """
    Convert Cartesian coordinates to polar coordinates.

    Args:
        x (float): x-coordinate.
        y (float): y-coordinate.

    Returns:
        float: rho, the radial distance from the origin.
        float: phi, the angle in radians.
    """
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(rho, phi):
    """
    Convert polar coordinates to Cartesian coordinates.

    Args:
        rho (float): radial distance from the origin.
        phi (float): angle in radians.

    Returns:
        float: x-coordinate.
        float: y-coordinate.
    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def atom_probe_recons_from_detector_Gault_et_al(detx, dety, hv, flight_path_length, kf, det_eff, icf, field_evap, avg_dens):
    """
    Perform atom probe reconstruction using Gault et al.'s method.

    Args:
        detx (float): Hit position on the detector (x-coordinate).
        dety (float): Hit position on the detector (y-coordinate).
        hv (float): High voltage.
        flight_path_length (float): Distance between detector and sample.
        kf (float): Field reduction factor.
        det_eff (float): Efficiency of the detector.
        icf (float): Image compression factor due to sample imperfections.
        field_evap (float): Evaporation field in V/nm.
        avg_dens (float): Atomic density in atoms/nm^3.

    Returns:
        float: x-coordinates of reconstructed atom positions in nm.
        float: y-coordinates of reconstructed atom positions in nm.
        float: z-coordinates of reconstructed atom positions in nm.
    """
    # Convert detector coordinates to polar form
    rad, ang = cart2pol(detx * 1E-2, dety * 1E-2)

    # Calculate effective detector area
    det_area = (np.max(rad) ** 2) * np.pi

    # Calculate radius evolution
    radius_evolution = hv / (kf * (field_evap / 1E-9))

    # Calculate launch angle relative to specimen axis
    theta_p = np.arctan(rad / (flight_path_length * 1E-3))

    # Calculate theta normal
    theta_a = theta_p + np.arcsin((icf - 1) * np.sin(theta_p))

    # Convert polar coordinates to Cartesian coordinates
    z_p, d = pol2cart(radius_evolution, theta_a)
    x, y = pol2cart(d, ang)

    # Calculate z coordinate
    dz_p = radius_evolution * (1 - np.cos(theta_a))
    omega = 1E-9 ** 3 / avg_dens
    # icf_2 = theta_a / theta_p
    # dz = (omega * ((flight_path_length * 1E-3) ** 2) * (kf ** 2) * ((field_evap / 1E-9) ** 2)) / (
    #         det_area * det_eff * (icf_2 ** 2) * (hv ** 2))

    dz = (omega * ((flight_path_length * 1E-3) ** 2) * (kf ** 2) * ((field_evap / 1E-9) ** 2)) / (
            det_area * det_eff * (icf ** 2) * (hv ** 2))
    cum_z = np.cumsum(dz)
    z = cum_z + dz_p

    return x * 1E9, y * 1E9, z * 1E9

def atom_probe_recons_Bas_et_al(detx, dety, hv, flight_path_length, kf, det_eff, icf, field_evap, avg_dens):
    """
    Perform atom probe reconstruction using Bas et al.'s method.

    Args:
        detx (float): Hit position on the detector (x-coordinate).
        dety (float): Hit position on the detector (y-coordinate).
        hv (float): High voltage.
        flight_path_length (float): Distance between detector and sample.
        kf (float): Field reduction factor.
        det_eff (float): Efficiency of the detector.
        icf (float): Image compression factor due to sample imperfections.
        field_evap (float): Evaporation field in V/nm.
        avg_dens (float): Atomic density in atoms/nm^3.

    Returns:
        float: x-coordinates of reconstructed atom positions in nm.
        float: y-coordinates of reconstructed atom positions in nm.
        float: z-coordinates of reconstructed atom positions in nm.
    """
    radius_evolution = hv / (icf * (field_evap / 1E-9))
    m = (flight_path_length * 1E-3) / (kf * radius_evolution)

    x = (detx * 1E-2) / m
    y = (dety * 1E-2) / m

    rad, ang = cart2pol(detx * 1E-3, dety * 1E-3)
    det_area = (np.max(rad) ** 2) * np.pi

    omega = 1E-9 ** 3 / avg_dens
    dz = (omega * ((flight_path_length * 1E-3) ** 2) * (kf ** 2) * ((field_evap / 1E-9) ** 2)) / (
            det_area * det_eff * (icf ** 2) * (hv ** 2))
    dz_p = radius_evolution * (1 - np.sqrt(1 - ((x ** 2 + y ** 2) / (radius_evolution ** 2))))
    z = np.cumsum(dz) + dz_p

    return x * 1E9, y * 1E9, z * 1E9


def reconstruction_plot(data, range_data, variables, element_percentage, rotary_fig_save, selected_area, figname):
    """
    Generate a 3D plot for atom probe reconstruction data.

    Args:
        data (DataFrame): Atom probe reconstruction data.
        range_data (DataFrame): Range data for different elements.
        variables (object): Variables object.
        element_percentage (str): Percentage of elements to display.
        rotary_fig_save (bool): Whether to save the rotary figure.
        selected_area (bool): Whether a specific area is selected.
        figname (str): Name of the figure.

    Returns:
        None
    """
    data_f = data.copy(deep=True)

    if selected_area:
        data_f = data_f[
            (data_f['x (nm)'] > variables.selected_x1) & (data_f['x (nm)'] < variables.selected_x2) &
            (data_f['y (nm)'] > variables.selected_y1) & (data_f['y (nm)'] < variables.selected_y2) &
            (data_f['z (nm)'] > variables.selected_z1) & (data_f['z (nm)'] < variables.selected_z2)
            ]
        data_f.reset_index(inplace=True, drop=True)

    element_percentage = element_percentage.replace('[', '').replace(']', '').split(',')

    fig = go.Figure()

    phases = range_data['element'].tolist()
    colors = range_data['color'].tolist()
    mc_low = range_data['mc_low'].tolist()
    mc_up = range_data['mc_up'].tolist()
    charge = range_data['charge'].tolist()
    isotope = range_data['isotope'].tolist()

    for index, elemen in enumerate(phases):
        df_s = data_f.copy(deep=True)
        df_s = df_s[(df_s['mc_c (Da)'] > mc_low[index]) & (df_s['mc_c (Da)'] < mc_up[index])]
        df_s.reset_index(inplace=True, drop=True)

        remove_n = int(len(df_s) - (len(df_s) * float(element_percentage[index])))
        drop_indices = np.random.choice(df_s.index, remove_n, replace=False)
        df_subset = df_s.drop(drop_indices)

        if phases[index] == 'unranged':
            name_element = 'unranged'
        else:
            name_element = r'${}^{%s}%s^{%s+}$' % (isotope[index], phases[index], charge[index])

        fig.add_trace(
            go.Scatter3d(
                x=df_subset['x (nm)'],
                y=df_subset['y (nm)'],
                z=df_subset['z (nm)'],
                mode='markers',
                name=name_element,
                showlegend=True,
                marker=dict(
                    size=2,
                    color=colors[index],
                    opacity=1,
                )
            )
        )

    fig.update_scenes(
        xaxis_title="x (nm)",
        yaxis_title="y (nm)",
        zaxis_title="z (nm)"
    )
    fig.update_scenes(zaxis_autorange="reversed")
    fig.update_layout(
        legend_title="",
        legend={'itemsizing': 'constant'},
        font=dict(size=8)
    )

    if rotary_fig_save:
        rotary_fig(fig, figname)

    config = dict(
        {
            'scrollZoom': True,
            'displayModeBar': True,
            'modeBarButtonsToAdd': [
                'drawline',
                'drawopenpath',
                'drawclosedpath',
                'drawcircle',
                'drawrect',
                'eraseshape'
            ]
        }
    )

    plotly.offline.plot(
        fig,
        filename=variables.result_path + '\\{fn}.html'.format(fn=figname),
        show_link=True,
        auto_open=False
    )

    fig.update_scenes(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)
    fig.write_image(variables.result_path + "\\3d_o.png", scale=0.6, format='png')
    fig.write_image(variables.result_path + "\\3d_o.svg", scale=0.4, format='svg')
    fig.update_scenes(xaxis_visible=True, yaxis_visible=True, zaxis_visible=True)
    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.99
        )
    )
    fig.write_image(variables.result_path + "\\3d.png", scale=0.6, format='png')
    fig.write_image(variables.result_path + "\\3d.svg", scale=0.4, format='svg')
    fig.show(config=config)


def rotate_z(x, y, z, theta):
    """
    Rotate coordinates around the z-axis.

    Args:
        x (float): x-coordinate.
        y (float): y-coordinate.
        z (float): z-coordinate.
        theta (float): Rotation angle.

    Returns:
        tuple: Rotated coordinates (x, y, z).
    """
    w = x + 1j * y
    return np.real(np.exp(1j * theta) * w), np.imag(np.exp(1j * theta) * w), z


def rotary_fig(fig1, variables, figname):
    """
    Generate a rotating figure using Plotly.

    Args:
        fig1 (plotly.graph_objects.Figure): The base figure.
        variables (object): The variables object.
        figname (str): The name of the figure.

    Returns:
        None
    """
    fig = go.Figure(fig1)
    x_eye = -1.25
    y_eye = 2
    z_eye = 0.5

    fig.update_scenes(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)

    fig.update_layout(
        width=600,
        height=600,
        scene_camera_eye=dict(x=x_eye, y=y_eye, z=z_eye),
        updatemenus=[
            dict(
                type='buttons',
                showactive=False,
                y=1.2,
                x=0.8,
                xanchor='left',
                yanchor='bottom',
                pad=dict(t=45, r=10),
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[
                            None,
                            dict(
                                frame=dict(duration=15, redraw=True),
                                transition=dict(duration=0),
                                fromcurrent=True,
                                mode='immediate'
                            )
                        ]
                    )
                ]
            )
        ]
    )

    frames = []
    for t in np.arange(0, 20, 0.1):
        xe, ye, ze = rotate_z(x_eye, y_eye, z_eye, -t)
        frames.append(go.Frame(layout=dict(scene_camera_eye=dict(x=xe, y=ye, z=ze))))
    fig.frames = frames
    plotly.offline.plot(
        fig,
        filename=variables.result_path + '\\rota_{fn}.html'.format(fn=figname),
        show_link=True,
        auto_open=False
    )


def scatter_plot(data, range_data, variables, element_percentage, selected_area, x_or_y, figname):
    """
    Generate a scatter plot based on the provided data.

    Args:
        data (pandas.DataFrame): The input data.
        range_data (pandas.DataFrame): Data containing range information for different elements.
        variables (object): The variables object.
        element_percentage (str): Element percentage information.
        selected_area (bool): True if a specific area is selected, False otherwise.
        x_or_y (str): Either 'x' or 'y' indicating the axis to plot.
        figname (str): The name of the figure.

    Returns:
        None
    """
    ax = plt.figure().add_subplot(111)

    phases = range_data['element'].tolist()
    colors = range_data['color'].tolist()
    mc_low = range_data['mc_low'].tolist()
    mc_up = range_data['mc_up'].tolist()
    charge = range_data['charge'].tolist()
    isotope = range_data['isotope'].tolist()
    mc = data['mc_c (Da)']

    element_percentage = element_percentage.replace('[', '')
    element_percentage = element_percentage.replace(']', '')
    element_percentage = element_percentage.split(',')

    for index, elemen in enumerate(phases):
        df_s = data.copy(deep=True)
        df_s = df_s[(df_s['mc_c (Da)'] > mc_low[index]) & (df_s['mc_c (Da)'] < mc_up[index])]
        df_s.reset_index(inplace=True, drop=True)
        remove_n = int(len(df_s) - (len(df_s) * float(element_percentage[index])))
        drop_indices = np.random.choice(df_s.index, remove_n, replace=False)
        df_subset = df_s.drop(drop_indices)
        if phases[index] == 'unranged':
            name_element = 'unranged'
        else:
            name_element = r'${}^{%s}%s^{%s+}$' % (isotope[index], phases[index], charge[index])
        if x_or_y == 'x':
            ax.scatter(df_subset['x (nm)'], df_subset['z (nm)'], s=2, label=name_element, color=colors[index])
        elif x_or_y == 'y':
            ax.scatter(df_subset['y (nm)'], df_subset['z (nm)'], s=2, label=name_element)

    if not selected_area:
        data_loadcrop.rectangle_box_selector(ax)
        plt.connect('key_press_event', selectors_data.toggle_selector)
    ax.xaxis.tick_top()
    ax.invert_yaxis()
    if x_or_y == 'x':
        ax.set_xlabel('X (nm)')
    elif x_or_y == 'y':
        ax.set_xlabel('Y (nm)')
    ax.xaxis.set_label_position('top')
    ax.set_ylabel('Z (nm)')
    plt.legend(loc='upper right')

    plt.savefig(variables.result_path + '\\projection_{fn}.png'.format(fn=figname))
    plt.show()


def heatmap(data, range_data, variables, element_percentage, save):
    """
    Generate a heatmap based on the provided data.

    Args:
        data (pandas.DataFrame): The input data.
        range_data (pandas.DataFrame): Data containing range information for different elements.
        variables (object): The variables object.
        element_percentage (str): Element percentage information.
        save (bool): True to save the plot, False to display it.

    Returns:
        None
    """
    ax = plt.figure().add_subplot(111)

    phases = range_data['element'].tolist()
    colors = range_data['color'].tolist()
    mc_low = range_data['mc_low'].tolist()
    mc_up = range_data['mc_up'].tolist()
    charge = range_data['charge'].tolist()
    isotope = range_data['isotope'].tolist()
    mc = data['mc_c (Da)']

    element_percentage = element_percentage.replace('[', '')
    element_percentage = element_percentage.replace(']', '')
    element_percentage = element_percentage.split(',')

    for index, elemen in enumerate(phases):
        df_s = data.copy(deep=True)
        df_s = df_s[(df_s['mc_c (Da)'] > mc_low[index]) & (df_s['mc_c (Da)'] < mc_up[index])]
        df_s.reset_index(inplace=True, drop=True)
        remove_n = int(len(df_s) - (len(df_s) * float(element_percentage[index])))
        drop_indices = np.random.choice(df_s.index, remove_n, replace=False)
        df_subset = df_s.drop(drop_indices)
        if phases[index] == 'unranged':
            name_element = 'unranged'
        else:
            name_element = r'${}^{%s}%s^{%s+}$' % (isotope[index], phases[index], charge[index])
        xx = df_subset['x_det (cm)'].to_numpy() * 10
        yy = df_subset['y_det (cm)'].to_numpy() * 10
        ax.scatter(xx, yy, s=2, label=name_element, color=colors[index])

    ax.set_xlabel("x [mm]", color="red", fontsize=10)
    ax.set_ylabel("y [mm]", color="red", fontsize=10)
    plt.title("Detector Heatmap")
    plt.legend(loc='upper right')

    if save:
        plt.savefig(variables.result_path + "heatmap.png", format="png", dpi=600)
        plt.savefig(variables.result_path + "heatmap.svg", format="svg", dpi=600)
    plt.show()