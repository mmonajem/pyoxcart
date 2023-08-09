"""
This is the main script is load the GUI base on the configuration file.
"""

import os
import sys

from PyQt6 import QtWidgets

# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files
from pyccapt.control.gui import gui_main


def main():
	try:
		# load the Json file
		configFile = 'config.json'
		p = os.path.abspath(os.path.join(__file__, "../.."))
		os.chdir(p)
		conf = read_files.read_json_file(configFile)
	except Exception as e:
		print('Can not load the configuration file')
		print(e)
		sys.exit()
	# Initialize global experiment variables
	variables = share_variables.Variables(conf)
	variables.log_path = p

	app = QtWidgets.QApplication(sys.argv)
	PyCCAPT = QtWidgets.QMainWindow()
	signal_emitter = gui_main.SignalEmitter()
	ui = gui_main.Ui_PyCCAPT(variables, conf, signal_emitter)
	ui.setupUi(PyCCAPT)
	PyCCAPT.show()
	sys.exit(app.exec())


if __name__ == '__main__':
	main()
