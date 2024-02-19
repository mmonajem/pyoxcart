import multiprocessing
import os
import sys

from PyQt6 import QtWidgets

from pyccapt.control.control import share_variables, read_files
from pyccapt.control.gui import gui_main


def main():
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

	x_plot = multiprocessing.Queue()
	y_plot = multiprocessing.Queue()
	t_plot = multiprocessing.Queue()
	main_v_dc_plot = multiprocessing.Queue()

	app = QtWidgets.QApplication(sys.argv)
	app.setStyle('Fusion')
	pyccapt_window = QtWidgets.QMainWindow()
	ui = gui_main.Ui_PyCCAPT(variables, conf, x_plot, y_plot, t_plot, main_v_dc_plot)
	ui.setupUi(pyccapt_window)
	pyccapt_window.show()
	sys.exit(app.exec())


if __name__ == '__main__':
	main()
