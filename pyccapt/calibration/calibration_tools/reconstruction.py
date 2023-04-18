import numpy as np
import plotly.graph_objects as go
import plotly.express as plot_x
import matplotlib.pyplot as plt
import plotly

# Local module and scripts
from pyccapt.calibration.calibration_tools import variables, data_loadcrop, selectors_data
def cart2pol(x, y):
    """
    x, y are the detector hit coordinates in mm
    :param x:
    :param y:
    :return rho, phi:
    """
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(rho, phi):
    """
    :param rho:
    :param phi:
    :return x, y:
    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def atom_probe_recons_from_detector_Gault_et_al(detx, dety, hv, flight_path_length, kf, det_eff, icf, field_evap, avg_dens):
    """
    # atom probe reconstruction after: Gault et al., Ultramicroscopy 111(2011) 448 - 457
    x, y are the detector hit coordinates in mm
    kf is the field factor and ICF is the image compression factor
    :param detx:
    :param dety:
    :param hv:
    :param kf:
    :param icf:
    :param flight_path_length:
    :param ion_volume:
    :param det_eff:
    :param radius_evolution:
    :return:
    """

    ## constants and variable setup
    # specimen parameters
    # avgDens # atomic density in atoms / nm3
    # Fevap  # evaporation field in V / nm

    # detector coordinates in polar form
    rad, ang = cart2pol(detx * 1E-2, dety * 1E-2)
    # calculating effective detector area:
    det_area = (np.max(rad) ** 2) * np.pi
    # f_evap   evaporation field in V / nm
    radius_evolution = hv / (kf * (field_evap / 1E-9))

    # m = (flight_path_length * 1E-3) / (kf * radius_evolution)

    # launch angle relative to specimen axis - a/flight_path_length - a is based on detector hit position
    # theta detector
    theta_p = np.arctan(rad / (flight_path_length * 1E-3))  # mm / mm

    # theta normal
    # m = icf - 1
    theta_a = theta_p + np.arcsin((icf - 1) * np.sin(theta_p))

    icf_2 = theta_a / theta_p

    # distance from axis and z shift of each hit
    z_p, d = pol2cart(radius_evolution, theta_a)  # nm

    # x and y coordinates from the angle on the detector and the distance to
    # the specimen axis.
    x, y = pol2cart(d, ang)  # nm

    ## calculate z coordinate
    # the z shift with respect to the top of the cap is Rspec - zP
    #     z_p = radius_evolution - z_p
    dz_p = radius_evolution * (1 - np.cos(theta_a))
    # accumulative part of z
    omega = 1E-9 ** 3 / avg_dens  # atomic volume in nm ^ 3

    # nm ^ 3 * mm ^ 2 * V ^ 2 / nm ^ 2 / (mm ^ 2 * V ^ 2)
    #     dz = omega * ((flight_path_length * 1E-3) ** 2) * (kf ** 2)  / (det_eff * det_area * (icf ** 2)) * (
    #                 hv ** 2)
    dz = (omega * ((flight_path_length * 1E-3) ** 2) * (kf ** 2) * ((field_evap / 1E-9) ** 2)) / (
                det_area * det_eff * (icf_2 ** 2) * (hv ** 2))
    # wide angle correction
    cum_z = np.cumsum(dz)
    z = cum_z + dz_p

    return x * 1E9, y * 1E9, z * 1E9


def atom_probe_recons_Bas_et_al(detx, dety, hv, flight_path_length, kf, det_eff, icf, field_evap, avg_dens):
    """
    :param detx: Hit position on the detector
    :param dety: Hit position on the detector
    :param hv: High voltage
    :param kf: Field reduction factor
    :param icf: Image compression factor Because sample is not a perfect sphere
    :param flight_path_length: distance between detector and sample
    :param ion_volume: atomic volume in atoms/nm ^ 3
    :param det_eff: Efficiency of the detector
    :return:
    """
    # f_evap   evaporation field in V / nm
    radius_evolution = hv / (icf * (field_evap / 1E-9))

    m = (flight_path_length * 1E-3) / (kf * radius_evolution)

    x = (detx * 1E-2) / m
    y = (dety * 1E-2) / m

    # detector coordinates in polar form
    rad, ang = cart2pol(detx * 1E-3, dety * 1E-3)
    # calculating effective detector area:
    det_area = (np.max(rad) ** 2) * np.pi

    # accumulative part of z
    omega = 1E-9 ** 3 / avg_dens  # atomic volume in nm ^ 3

    #     dz = ((omega * (110 * 1E-3)**2) / (det_area * det_eff * (icf ** 2) * (radius_evolution ** 2))

    dz = (omega * ((flight_path_length * 1E-3) ** 2) * (kf ** 2) * ((field_evap / 1E-9) ** 2)) / (
                det_area * det_eff * (icf ** 2) * (hv ** 2))

    #     dz_p = radius_evolution * (1 - np.sqrt((x**2 + y**2) / (radius_evolution**2)))
    dz_p = radius_evolution * (1 - np.sqrt(1 - ((x ** 2 + y ** 2) / (radius_evolution ** 2))))

    z = np.cumsum(dz) + dz_p

    return x * 1E9, y * 1E9, z * 1E9


def reconstruction_plot(data, range_data, element_percentage, rotary_fig_save, selected_area, figname):
    data_f = data.copy(deep=True)
    if selected_area:
        data_f = data_f[(data_f['x (nm)'] > variables.selected_x1) & (data_f['x (nm)'] < variables.selected_x2) &
                        (data_f['y (nm)'] > variables.selected_y1) & (data_f['y (nm)'] < variables.selected_y2) &
                        (data_f['z (nm)'] > variables.selected_z1) & (data_f['z (nm)'] < variables.selected_z2)]

        data_f.reset_index(inplace=True, drop=True)

    element_percentage = element_percentage.replace('[', '')
    element_percentage = element_percentage.replace(']', '')
    element_percentage = element_percentage.split(',')

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
        #         print(len(df_s))
        drop_indices = np.random.choice(df_s.index, remove_n, replace=False)
        df_subset = df_s.drop(drop_indices)
        #         print(len(df_subset))
        if phases[index] == 'unranged':
            name_element = 'unranged'
        else:
            name_element = r'${}^{%s}%s^{%s+}$' % (isotope[index], phases[index], charge[index])
        fig.add_trace(
            go.Scatter3d(x=df_subset['x (nm)'], y=df_subset['y (nm)'], z=df_subset['z (nm)'], mode='markers',
                         name=name_element,
                         showlegend=True,
                         marker=dict(
                             size=2,
                             color=colors[index],
                             opacity=1,
                         )
                         ))

    #         print(elemen)
    fig.update_scenes(
        xaxis_title="x (nm)",
        yaxis_title="y (nm)",
        zaxis_title="z (nm)")
    fig.update_scenes(zaxis_autorange="reversed")
    fig.update_layout(legend_title="", title="PyCCAPT", legend={'itemsizing': 'constant'}, font=dict(
        size=8,
    ))



    if rotary_fig_save:
        rotary_fig(fig, figname)
    config = dict(
        {'scrollZoom': True, 'displayModeBar': True, 'modeBarButtonsToAdd': ['drawline',
                                        'drawopenpath',
                                        'drawclosedpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                       ]})
    plotly.offline.plot(fig, filename=variables.result_path + '\\{fn}.html'.format(fn=figname), show_link=True,
                        auto_open=False)
    fig.update_layout(height=500, width=500)
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)
    fig.write_image(variables.result_path + "\\3d.png")
    fig.update_scenes(xaxis_visible=True, yaxis_visible=True,zaxis_visible=True)
    fig.show(config=config)

def rotary_fig(fig1, figname):
    fig = go.Figure(fig1)
    x_eye = -1.25
    y_eye = 2
    z_eye = 0.5

    fig.update_scenes(xaxis_visible=False, yaxis_visible=False,zaxis_visible=False)

    fig.update_layout(
             width=600,
             height=600,
             scene_camera_eye=dict(x=x_eye, y=y_eye, z=z_eye),
             updatemenus=[dict(type='buttons',
                      showactive=False,
                      y=1.2,
                      x=0.8,
                      xanchor='left',
                      yanchor='bottom',
                      pad=dict(t=45, r=10),
                      buttons=[dict(label='Play',
                                     method='animate',
                                     args=[None, dict(frame=dict(duration=15, redraw=True),
                                                                 transition=dict(duration=0),
                                                                 fromcurrent=True,
                                                                 mode='immediate'
                                                                )]
                                                )
                                          ]
                                  )
                            ]
    )


    def rotate_z(x, y, z, theta):
        w = x+1j*y
        return np.real(np.exp(1j*theta)*w), np.imag(np.exp(1j*theta)*w), z

    frames = []
    for t in np.arange(0, 20, 0.1):
        xe, ye, ze = rotate_z(x_eye, y_eye, z_eye, -t)
        frames.append(go.Frame(layout=dict(scene_camera_eye=dict(x=xe, y=ye, z=ze))))
    fig.frames = frames
    plotly.offline.plot(fig, filename=variables.result_path + '\\{fn}.html'.format(fn='rota_'+figname), show_link=True, auto_open=False)
#     fig.show()

def projection(data, range_data, element_percentage, selected_area, x_or_y, figname):

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
        # print(len(df_s))
        drop_indices = np.random.choice(df_s.index, remove_n, replace=False)
        df_subset = df_s.drop(drop_indices)
        # print(len(df_subset))
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


def heatmap(data, range_data, selected_area, element_percentage, save):
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
        # print(len(df_s))
        drop_indices = np.random.choice(df_s.index, remove_n, replace=False)
        df_subset = df_s.drop(drop_indices)
        # print(len(df_subset))
        if phases[index] == 'unranged':
            name_element = 'unranged'
        else:
            name_element = r'${}^{%s}%s^{%s+}$' % (isotope[index], phases[index], charge[index])
        # Plot heat map and convert from cm to mm
        xx = df_subset['x_det (cm)'].to_numpy() * 10
        yy = df_subset['y_det (cm)'].to_numpy() * 10
        ax.scatter(xx, yy, s=2, label=name_element, color=colors[index])

    # set x-axis label
    ax.set_xlabel("x [mm]", color="red", fontsize=10)
    # set y-axis label
    ax.set_ylabel("y [mm]", color="red", fontsize=10)
    plt.title("Detector Heatmap")
    plt.legend(loc='upper right')

    if save:
        plt.savefig(variables.result_path + "heatmap.png", format="png", dpi=600)
        plt.savefig(variables.result_path + "heatmap.svg", format="svg", dpi=600)
    plt.show()
