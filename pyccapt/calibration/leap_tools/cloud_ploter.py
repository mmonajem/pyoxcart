import os
import matplotlib.pyplot as plt
import plotly

from pyccapt.calibration.leap_tools import apt_importers


def pre_data(pos_file, rrng_file, input_type):
    if input_type == 'pos':
        pos = apt_importers.read_pos(pos_file)
        ions, rrngs = apt_importers.read_rrng(rrng_file)
        pos_comp = apt_importers.label_ions(pos, rrngs)
        elements = apt_importers.deconvolve(pos_comp)

    elif input_type == 'epos':
        epos = apt_importers.read_epos(pos_file)
        ions, rrngs = apt_importers.read_rrng(rrng_file)
        epos_comp = apt_importers.label_ions(epos, rrngs)
        elements = apt_importers.deconvolve(epos_comp)

    return elements


def decompose(data, element):
    initial = data.loc[element]
    pos = initial[['x (nm)', 'y (nm)', 'z (nm)']].values
    # a bug existed, when only one line contained in pos.
    color = initial['colour'].values[0]
    px, py, pz = (pos[:,0], pos[:,1], pos[:,2])
    return px, py, pz, color


def cloud_plotter(data, phases, result_path, filename, plot_type='cloud'):
    if plot_type == 'projection':
        # plot static images with matplotlib.
        ax = plt.figure().add_subplot(111)
        for element in phases:
            px, py, pz, color = decompose(data, element)
            ax.scatter(py, pz, s=2, label=element)
        ax.xaxis.tick_top()
        ax.invert_yaxis()
        ax.set_xlabel('Y')
        ax.xaxis.set_label_position('top')
        ax.set_ylabel('Z')
        plt.legend()
        plt.savefig(result_path + 'output_{fn}.png'.format(fn=filename))

    elif plot_type == 'cloud':
        # Adjust fig parameters in def_function.py
        plotly_data = list()
        for element in phases:
            px, py, pz, color = decompose(data, element)
            scatter = dict(
                mode="markers",
                name=element,
                type="scatter3d",
                x=px, y=py, z=pz,
                opacity = 0.2,
                marker = dict(size=2, color=color)
            )
            plotly_data.append(scatter)

        layout = dict(
            title='APT 3D Point Cloud',
            scene=dict(xaxis=dict(zeroline=False, title='x (nm)'),
                       yaxis=dict(zeroline=False, title='y (nm)'),
                       zaxis=dict(zeroline=False, title='z (nm)', autorange='reversed'))
        )
        fig = dict(data=plotly_data, layout=layout)
        plotly.offline.plot(fig, filename=result_path + '{fn}.html'.format(fn=filename), show_link=False)
        return fig
    else:
        print("Plot type error!")


if __name__ == "__main__":
    p = os.path.abspath(os.path.join("", "../../.."))
    path = p + '\\tests\\data\\data_leap_test\\'
    result_path = p + '\\tests\\results\\leap_test\\'

    if not os.path.isdir(result_path):
            os.makedirs(result_path, mode=0o777, exist_ok=True)

    pos_elements = pre_data(path + 'voldata.pos', path + 'rangefile.rrng', input_type='pos')
    # epos_elements = pre_data(path + 'voldata.epos', path + 'rangefile.rrng', input_type='epos')

    ions, rrngs = apt_importers.read_rrng(path + 'rangefile.rrng')

    pos_elements_l = pos_elements[['x (nm)', 'y (nm)', 'z (nm)', 'element', 'colour']].set_index("element")

    print(ions)
    phases = ['H', 'C', 'O', 'Ca', 'Ga', 'Na', 'N']
    filename = '_'.join(phases)
    cloud_plotter(pos_elements_l, phases, result_path, filename, plot_type='cloud')