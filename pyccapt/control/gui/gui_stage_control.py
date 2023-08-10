import os
import sys

from PyQt6 import QtCore, QtGui, QtWidgets

# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files


class Ui_Stage_Control(object):

	def __init__(self, variables, conf):
		"""
		Constructor for the Stage Control UI class.

		Args:
			variables (object): Global experiment variables.
			conf (dict): Configuration settings.

		Attributes:
			variables: Global experiment variables.
			conf: Configuration settings.
		"""
		self.variables = variables
		self.conf = conf

	def setupUi(self, Stage_Control):
		"""
		Set up the Stage Control UI.
		Args:
			Stage_Control (object): The Stage Control UI object.

		Return:
			None
		"""
		Stage_Control.setObjectName("Stage_Control")
		Stage_Control.resize(226, 166)
		self.gridLayout_4 = QtWidgets.QGridLayout(Stage_Control)
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.gridLayout_3 = QtWidgets.QGridLayout()
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.gridLayout_2 = QtWidgets.QGridLayout()
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.forward = QtWidgets.QPushButton(parent=Stage_Control)
		self.forward.setStyleSheet("QPushButton {\n"
		                           "                border: none;\n"
		                           "                background-image: url(\'arrow.png\');\n"
		                           "                background-repeat: no-repeat;\n"
		                           "                background-position: center;\n"
		                           "                background-color: transparent;\n"
		                           "                width: 40px;\n"
		                           "                height: 40px;\n"
		                           "            }")
		self.forward.setObjectName("forward")
		self.gridLayout_2.addWidget(self.forward, 0, 0, 1, 1)
		self.left = QtWidgets.QPushButton(parent=Stage_Control)
		self.left.setStyleSheet("QPushButton {\n"
		                        "                border: none;\n"
		                        "                background-image: url(\'arrow.png\');\n"
		                        "                background-repeat: no-repeat;\n"
		                        "                background-position: center;\n"
		                        "                background-color: transparent;\n"
		                        "                width: 40px;\n"
		                        "                height: 40px;\n"
		                        "            }")
		self.left.setObjectName("left")
		self.gridLayout_2.addWidget(self.left, 0, 1, 1, 1)
		self.up = QtWidgets.QPushButton(parent=Stage_Control)
		self.up.setStyleSheet("QPushButton {\n"
		                      "                border: none;\n"
		                      "                background-image: url(\'arrow.png\');\n"
		                      "                background-repeat: no-repeat;\n"
		                      "                background-position: center;\n"
		                      "                background-color: transparent;\n"
		                      "                width: 40px;\n"
		                      "                height: 40px;\n"
		                      "            }")
		self.up.setObjectName("up")
		self.gridLayout_2.addWidget(self.up, 0, 2, 1, 1)
		self.back = QtWidgets.QPushButton(parent=Stage_Control)
		self.back.setStyleSheet("QPushButton {\n"
		                        "                border: none;\n"
		                        "                background-image: url(\'arrow.png\');\n"
		                        "                background-repeat: no-repeat;\n"
		                        "                background-position: center;\n"
		                        "                background-color: transparent;\n"
		                        "                width: 40px;\n"
		                        "                height: 40px;\n"
		                        "            }")
		self.back.setObjectName("back")
		self.gridLayout_2.addWidget(self.back, 1, 0, 1, 1)
		self.right = QtWidgets.QPushButton(parent=Stage_Control)
		self.right.setStyleSheet("QPushButton {\n"
		                         "                border: none;\n"
		                         "                background-image: url(\'arrow.png\');\n"
		                         "                background-repeat: no-repeat;\n"
		                         "                background-position: center;\n"
		                         "                background-color: transparent;\n"
		                         "                width: 40px;\n"
		                         "                height: 40px;\n"
		                         "            }")
		self.right.setObjectName("right")
		self.gridLayout_2.addWidget(self.right, 1, 1, 1, 1)
		self.down = QtWidgets.QPushButton(parent=Stage_Control)
		self.down.setStyleSheet("QPushButton {\n"
		                        "                border: none;\n"
		                        "                background-image: url(\'arrow.png\');\n"
		                        "                background-repeat: no-repeat;\n"
		                        "                background-position: center;\n"
		                        "                background-color: transparent;\n"
		                        "                width: 40px;\n"
		                        "                height: 40px;\n"
		                        "            }")
		self.down.setObjectName("down")
		self.gridLayout_2.addWidget(self.down, 1, 2, 1, 1)
		self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		self.x_cord = QtWidgets.QLCDNumber(parent=Stage_Control)
		self.x_cord.setObjectName("x_cord")
		self.gridLayout.addWidget(self.x_cord, 0, 0, 1, 1)
		self.y_cord = QtWidgets.QLCDNumber(parent=Stage_Control)
		self.y_cord.setObjectName("y_cord")
		self.gridLayout.addWidget(self.y_cord, 0, 1, 1, 1)
		self.z_cord = QtWidgets.QLCDNumber(parent=Stage_Control)
		self.z_cord.setObjectName("z_cord")
		self.gridLayout.addWidget(self.z_cord, 0, 2, 1, 1)
		self.x_speed = QtWidgets.QSpinBox(parent=Stage_Control)
		self.x_speed.setObjectName("x_speed")
		self.gridLayout.addWidget(self.x_speed, 1, 0, 1, 1)
		self.y_speed = QtWidgets.QSpinBox(parent=Stage_Control)
		self.y_speed.setObjectName("y_speed")
		self.gridLayout.addWidget(self.y_speed, 1, 1, 1, 1)
		self.z_speed = QtWidgets.QSpinBox(parent=Stage_Control)
		self.z_speed.setObjectName("z_speed")
		self.gridLayout.addWidget(self.z_speed, 1, 2, 1, 1)
		self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)
		self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

		self.retranslateUi(Stage_Control)
		QtCore.QMetaObject.connectSlotsByName(Stage_Control)

	def retranslateUi(self, Stage_Control):
		"""
		Set the text and titles of the UI elements
		Args:
			None

		Return:
			None
		"""
		_translate = QtCore.QCoreApplication.translate
		###
		# Stage_Control.setWindowTitle(_translate("Stage_Control", "Form"))
		Stage_Control.setWindowTitle(_translate("Stage_Control", "PyCCAPT Stage Control"))
		Stage_Control.setWindowIcon(QtGui.QIcon('./files/logo3.png'))
		###
		self.forward.setText(_translate("Stage_Control", "Forward"))
		self.left.setText(_translate("Stage_Control", "Left"))
		self.up.setText(_translate("Stage_Control", "Up"))
		self.back.setText(_translate("Stage_Control", "Back"))
		self.right.setText(_translate("Stage_Control", "Right"))
		self.down.setText(_translate("Stage_Control", "Down"))

	def stop(self):
		"""
		Stop any background processes, timers, or threads here
		Args:
			None

		Return:
			None
		"""
		# Add any additional cleanup code here
		pass


class StageControlWindow(QtWidgets.QWidget):
	"""
	Widget for the Stage Control window.
	"""

	def __init__(self, gui_stage_control, *args, **kwargs):
		"""
		Constructor for the StageControlWindow class.

		Args:
			gui_stage_control: Instance of the StageControl.
			*args: Additional positional arguments.
			**kwargs: Additional keyword arguments.
		"""
		super().__init__(*args, **kwargs)
		self.gui_stage_control = gui_stage_control

	def closeEvent(self, event):
		"""
		Close event for the window.

		Args:
			event: Close event.
		"""
		self.gui_stage_control.stop()  # Call the stop method to stop any background activity
		# Additional cleanup code here if needed
		super().closeEvent(event)


if __name__ == "__main__":
	try:
		# Load the JSON file
		configFile = 'config.json'
		p = os.path.abspath(os.path.join(__file__, "../../.."))
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
	stage_control = QtWidgets.QWidget()
	ui = Ui_Stage_Control(variables, conf)
	ui.setupUi(stage_control)
	stage_control.show()
	sys.exit(app.exec())
