import multiprocessing
import os
import sys

from PyQt6 import QtWidgets

from pyccapt.control.control_tools import share_variables, read_files
from pyccapt.control.gui import gui_main


def load_gui():
    """
    Load the GUI based on the configuration file.

    This function reads the configuration file, initializes global experiment variables, and
    shows the GUI window.

    Args:
        None

    Returns:
        None
    """
    try:
        # Load the JSON file
        config_file = 'config.json'
        p = os.path.abspath(os.path.join(__file__, "../.."))
        os.chdir(p)
        conf = read_files.read_json_file(config_file)
    except Exception as e:
        print('Cannot load the configuration file')
        print(e)
        sys.exit()

    # Initialize global experiment variables
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    variables = share_variables.Variables(conf, ns)

    array_size = conf['maximum_size_plot_arrays']
    x_plot = multiprocessing.Array('d', array_size)
    y_plot = multiprocessing.Array('d', array_size)
    t_plot = multiprocessing.Array('d', array_size)
    main_v_dc_plot = multiprocessing.Array('d', array_size)
    counter_plot = multiprocessing.Value('i', 0)
    lock = multiprocessing.Lock()  # Lock for synchronization

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    pyccapt_window = QtWidgets.QMainWindow()
    ui = gui_main.Ui_PyCCAPT(variables, conf, x_plot, y_plot, t_plot, main_v_dc_plot, counter_plot, lock)
    ui.setupUi(pyccapt_window)
    pyccapt_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    load_gui()
