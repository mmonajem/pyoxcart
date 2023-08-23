import multiprocessing
import os
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer

# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files
from pyccapt.control.thorlabs_apt import thorlab_motor


class Ui_Laser_Control(object):
    def __init__(self, variables, conf):
        """
        Initialize the Ui_Laser_Control class.

        Args:
            variables: Global experiment variables.
            conf: Configuration settings.
        """
        self.variables = variables
        self.conf = conf

    def setupUi(self, Laser_Control):
        """
        Setup the GUI for the laser control.
        Args:
            Laser_Control: The GUI window

        Return:
            None
        """
        Laser_Control.setObjectName("Laser_Control")
        Laser_Control.resize(333, 171)
        self.gridLayout_2 = QtWidgets.QGridLayout(Laser_Control)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_29 = QtWidgets.QLabel(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.gridLayout.addWidget(self.label_29, 0, 0, 1, 1)
        self.home_motor = QtWidgets.QPushButton(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.home_motor.sizePolicy().hasHeightForWidth())
        self.home_motor.setSizePolicy(sizePolicy)
        self.home_motor.setMinimumSize(QtCore.QSize(0, 25))
        self.home_motor.setStyleSheet("QPushButton{\n"
                                      "background: rgb(193, 193, 193)\n"
                                      "}")
        self.home_motor.setObjectName("home_motor")
        self.gridLayout.addWidget(self.home_motor, 0, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        self.label_31.setObjectName("label_31")
        self.gridLayout.addWidget(self.label_31, 1, 0, 1, 1)
        self.criteria_laser = QtWidgets.QCheckBox(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.criteria_laser.sizePolicy().hasHeightForWidth())
        self.criteria_laser.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(False)
        self.criteria_laser.setFont(font)
        self.criteria_laser.setMouseTracking(True)
        self.criteria_laser.setStyleSheet("QCheckBox{\n"
                                          "background: rgb(223,223,233)\n"
                                          "}")
        self.criteria_laser.setText("")
        self.criteria_laser.setChecked(True)
        self.criteria_laser.setObjectName("criteria_laser")
        self.gridLayout.addWidget(self.criteria_laser, 1, 1, 1, 1)
        self.fixed_laser = QtWidgets.QLineEdit(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fixed_laser.sizePolicy().hasHeightForWidth())
        self.fixed_laser.setSizePolicy(sizePolicy)
        self.fixed_laser.setMinimumSize(QtCore.QSize(0, 20))
        self.fixed_laser.setStyleSheet("QLineEdit{\n"
                                       "background: rgb(223,223,233)\n"
                                       "}")
        self.fixed_laser.setObjectName("fixed_laser")
        self.gridLayout.addWidget(self.fixed_laser, 1, 2, 1, 1)
        self.label_18 = QtWidgets.QLabel(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 2, 0, 1, 1)
        self.laser_num_ions_per_step = QtWidgets.QLineEdit(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_num_ions_per_step.sizePolicy().hasHeightForWidth())
        self.laser_num_ions_per_step.setSizePolicy(sizePolicy)
        self.laser_num_ions_per_step.setMinimumSize(QtCore.QSize(0, 20))
        self.laser_num_ions_per_step.setStyleSheet("QLineEdit{\n"
                                                   "background: rgb(223,223,233)\n"
                                                   "}")
        self.laser_num_ions_per_step.setObjectName("laser_num_ions_per_step")
        self.gridLayout.addWidget(self.laser_num_ions_per_step, 2, 2, 1, 1)
        self.label_30 = QtWidgets.QLabel(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)
        self.label_30.setObjectName("label_30")
        self.gridLayout.addWidget(self.label_30, 3, 0, 1, 1)
        self.laser_increase_per_step = QtWidgets.QLineEdit(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_increase_per_step.sizePolicy().hasHeightForWidth())
        self.laser_increase_per_step.setSizePolicy(sizePolicy)
        self.laser_increase_per_step.setMinimumSize(QtCore.QSize(0, 10))
        self.laser_increase_per_step.setStyleSheet("QLineEdit{\n"
                                                   "background: rgb(223,223,233)\n"
                                                   "}")
        self.laser_increase_per_step.setObjectName("laser_increase_per_step")
        self.gridLayout.addWidget(self.laser_increase_per_step, 3, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 4, 0, 1, 1)
        self.laser_start = QtWidgets.QLineEdit(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_start.sizePolicy().hasHeightForWidth())
        self.laser_start.setSizePolicy(sizePolicy)
        self.laser_start.setMinimumSize(QtCore.QSize(0, 20))
        self.laser_start.setStyleSheet("QLineEdit{\n"
                                       "background: rgb(223,223,233)\n"
                                       "}")
        self.laser_start.setObjectName("laser_start")
        self.gridLayout.addWidget(self.laser_start, 4, 2, 1, 1)
        self.label_27 = QtWidgets.QLabel(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 5, 0, 1, 1)
        self.laser_stop = QtWidgets.QLineEdit(parent=Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_stop.sizePolicy().hasHeightForWidth())
        self.laser_stop.setSizePolicy(sizePolicy)
        self.laser_stop.setMinimumSize(QtCore.QSize(0, 20))
        self.laser_stop.setStyleSheet("QLineEdit{\n"
                                      "background: rgb(223,223,233)\n"
                                      "}")
        self.laser_stop.setObjectName("laser_stop")
        self.gridLayout.addWidget(self.laser_stop, 5, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Laser_Control)
        QtCore.QMetaObject.connectSlotsByName(Laser_Control)

        ###
        self.home_motor.clicked.connect(self.make_motor_home)
        # Create QTimer instance
        self.button_disable_timer = QTimer()
        self.button_disable_timer.timeout.connect(self.enable_button)
        # Trigger initial value change detection
        self.setup_parameters_changes()
        self.criteria_laser.stateChanged.connect(self.setup_parameters_changes)
        self.fixed_laser.editingFinished.connect(self.setup_parameters_changes)
        self.laser_num_ions_per_step.editingFinished.connect(self.setup_parameters_changes)
        self.laser_increase_per_step.editingFinished.connect(self.setup_parameters_changes)
        self.laser_start.editingFinished.connect(self.setup_parameters_changes)
        self.laser_stop.editingFinished.connect(self.setup_parameters_changes)
        ###

    def retranslateUi(self, Laser_Control):
        """

        Args:
            Laser_Control:

        Return:
            None
        """
        _translate = QtCore.QCoreApplication.translate
        ###
        # Laser_Control.setWindowTitle(_translate("Laser_Control", "Form"))
        Laser_Control.setWindowTitle(_translate("Laser_Control", "PyCCAPT Laser Control"))
        Laser_Control.setWindowIcon(QtGui.QIcon('./files/logo3.png'))
        ###
        self.label_29.setText(_translate("Laser_Control", "Laser Control"))
        self.home_motor.setText(_translate("Laser_Control", "Home"))
        self.label_31.setText(_translate("Laser_Control", "Fix"))
        self.fixed_laser.setText(_translate("Laser_Control", "0"))
        self.label_18.setText(_translate("Laser_Control", "# Ions per step"))
        self.laser_num_ions_per_step.setText(_translate("Laser_Control", "2000"))
        self.label_30.setText(_translate("Laser_Control", "Increase per Step "))
        self.laser_increase_per_step.setText(_translate("Laser_Control", "2"))
        self.label_16.setText(_translate("Laser_Control", "Start"))
        self.laser_start.setText(_translate("Laser_Control", "10"))
        self.label_27.setText(_translate("Laser_Control", "Stop"))
        self.laser_stop.setText(_translate("Laser_Control", "40"))

    def setup_parameters_changes(self):
        """
        the function that is run if any of the setup parameters are changed
        Args:
            None

        Return:
            None
        """
        # with self.variables.lock_setup_parameters:
        if self.criteria_laser.isChecked():
            self.variables.criteria_laser = True
        elif not self.criteria_laser.isChecked():
            self.variables.criteria_laser = False
        self.variables.fixed_laser = int(float(self.fixed_laser.text()))
        self.variables.laser_num_ions_per_step = int(float(self.laser_num_ions_per_step.text()))
        self.variables.laser_increase_per_step = int(float(self.laser_increase_per_step.text()))
        self.variables.laser_start = int(float(self.laser_start.text()))
        self.variables.laser_stop = int(float(self.laser_stop.text()))

    def make_motor_home(self):
        """
        the function that is run if home button for laser is pressed
        Args:
            None

        Return:
            None
        """
        try:
            self.disable_button_for_10_seconds()  # Disable the home button for 10 seconds

            thorlab_process = multiprocessing.Process(target=thorlab_motor.thorlab,
                                                      args=(self.conf, 0, False, True))
            thorlab_process.daemon = True
            thorlab_process.start()
        except Exception as e:
            print("Error below in homing motor")
            self.home_motor.setEnabled(True)
            print(e)

    def disable_button_for_10_seconds(self):
        """
        Handle the close event of the GatesWindow.

        Args:
            None

        Return:
            None
        """
        self.home_motor.setEnabled(False)
        self.button_disable_timer.start(10000)  # 10 seconds in milliseconds

    def enable_button(self):
        """
        Handle the close event of the GatesWindow.

        Args:
            None

        Return:
            None
        """
        self.home_motor.setEnabled(True)
        self.button_disable_timer.stop()

    def stop(self):
        """
        Handle the close event of the GatesWindow.

        Args:
            None

        Return:
            None
        """
        # Stop any background processes, timers, or threads here
        self.button_disable_timer.stop()  # If you want to stop this timer when closing
        # Add any additional cleanup code here


class LaserControlWindow(QtWidgets.QWidget):
    closed = QtCore.pyqtSignal()  # Define a custom closed signal
    def __init__(self, gui_laser_control, *args, **kwargs):
        """
        Initialize the LaserControlWindow class.

        Args:
            gui_laser_control: GUI for laser control.
            *args, **kwargs: Additional arguments for QWidget initialization.
        """
        super().__init__(*args, **kwargs)
        self.gui_laser_control = gui_laser_control

    def closeEvent(self, event):
        """
        Handle the close event of the LaserControlWindow.

        Args:
            event: Close event.
        """
        self.gui_laser_control.stop()  # Call the stop method to stop any background activity
        self.closed.emit()  # Emit the custom closed signal
        # Additional cleanup code here if needed
        super().closeEvent(event)

    def setWindowStyleFusion(self):
	    # Set the Fusion style
	    QtWidgets.QApplication.setStyle("Fusion")


if __name__ == "__main__":
	try:
		# Load the Json file
		configFile = 'config.json'
		p = os.path.abspath(os.path.join(__file__, "../../.."))
		os.chdir(p)
		conf = read_files.read_json_file(configFile)
	except Exception as e:
        print('Can not load the configuration file')
        print(e)
        sys.exit()
    # Initialize global experiment variables
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    lock_lists = manager.Lock()
    ns = manager.Namespace()
    variables = share_variables.Variables(conf, ns, lock, lock_lists)

    app = QtWidgets.QApplication(sys.argv)
	app.setStyle('Fusion')
    Laser_Control = QtWidgets.QWidget()
    ui = Ui_Laser_Control(variables, conf)
    ui.setupUi(Laser_Control)
    Laser_Control.show()
    sys.exit(app.exec())
