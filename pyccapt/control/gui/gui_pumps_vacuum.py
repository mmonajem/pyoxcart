import os
import sys
import threading
import time

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QPixmap

# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files
from pyccapt.control.devices import initialize_devices


class Ui_Pumps_Vacuum(object):

    def __init__(self, variables, conf, SignalEmitter, parent=None):
        self.variables = variables
        self.conf = conf
        self.parent = parent
        self.emitter = SignalEmitter

    def setupUi(self, Pumps_Vacuum):
        Pumps_Vacuum.setObjectName("Pumps_Vacuum")
        Pumps_Vacuum.resize(850, 164)
        self.gridLayout_3 = QtWidgets.QGridLayout(Pumps_Vacuum)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.led_pump_load_lock = QtWidgets.QLabel(parent=Pumps_Vacuum)
        self.led_pump_load_lock.setMinimumSize(QtCore.QSize(50, 50))
        self.led_pump_load_lock.setMaximumSize(QtCore.QSize(50, 50))
        self.led_pump_load_lock.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.led_pump_load_lock.setObjectName("led_pump_load_lock")
        self.gridLayout.addWidget(self.led_pump_load_lock, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_210 = QtWidgets.QLabel(parent=Pumps_Vacuum)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_210.setFont(font)
        self.label_210.setObjectName("label_210")
        self.gridLayout.addWidget(self.label_210, 0, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.vacuum_load_lock = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vacuum_load_lock.sizePolicy().hasHeightForWidth())
        self.vacuum_load_lock.setSizePolicy(sizePolicy)
        self.vacuum_load_lock.setMinimumSize(QtCore.QSize(100, 50))
        self.vacuum_load_lock.setStyleSheet("QLCDNumber{\n"
                                            "                                    border: 2px solid yellow;\n"
                                            "                                    border-radius: 10px;\n"
                                            "                                    padding: 0 8px;\n"
                                            "                                    }\n"
                                            "                                ")
        self.vacuum_load_lock.setObjectName("vacuum_load_lock")
        self.gridLayout.addWidget(self.vacuum_load_lock, 0, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_211 = QtWidgets.QLabel(parent=Pumps_Vacuum)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_211.setFont(font)
        self.label_211.setObjectName("label_211")
        self.gridLayout.addWidget(self.label_211, 0, 3, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.vacuum_buffer = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vacuum_buffer.sizePolicy().hasHeightForWidth())
        self.vacuum_buffer.setSizePolicy(sizePolicy)
        self.vacuum_buffer.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.vacuum_buffer.setFont(font)
        self.vacuum_buffer.setStyleSheet("QLCDNumber{\n"
                                         "                                    border: 2px solid blue;\n"
                                         "                                    border-radius: 10px;\n"
                                         "                                    padding: 0 8px;\n"
                                         "                                    }\n"
                                         "                                ")
        self.vacuum_buffer.setObjectName("vacuum_buffer")
        self.gridLayout.addWidget(self.vacuum_buffer, 0, 4, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_212 = QtWidgets.QLabel(parent=Pumps_Vacuum)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_212.setFont(font)
        self.label_212.setObjectName("label_212")
        self.gridLayout.addWidget(self.label_212, 0, 5, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.pump_load_lock_switch = QtWidgets.QPushButton(parent=Pumps_Vacuum)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pump_load_lock_switch.sizePolicy().hasHeightForWidth())
        self.pump_load_lock_switch.setSizePolicy(sizePolicy)
        self.pump_load_lock_switch.setMinimumSize(QtCore.QSize(0, 25))
        self.pump_load_lock_switch.setStyleSheet("QPushButton{\n"
                                                 "                                    background: rgb(193, 193, 193)\n"
                                                 "                                    }\n"
                                                 "                                ")
        self.pump_load_lock_switch.setObjectName("pump_load_lock_switch")
        self.gridLayout.addWidget(self.pump_load_lock_switch, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_213 = QtWidgets.QLabel(parent=Pumps_Vacuum)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_213.setFont(font)
        self.label_213.setObjectName("label_213")
        self.gridLayout.addWidget(self.label_213, 1, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.vacuum_load_lock_back = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vacuum_load_lock_back.sizePolicy().hasHeightForWidth())
        self.vacuum_load_lock_back.setSizePolicy(sizePolicy)
        self.vacuum_load_lock_back.setMinimumSize(QtCore.QSize(100, 50))
        self.vacuum_load_lock_back.setStyleSheet("QLCDNumber{\n"
                                                 "                                    border: 2px solid yellow;\n"
                                                 "                                    border-radius: 10px;\n"
                                                 "                                    padding: 0 8px;\n"
                                                 "                                    }\n"
                                                 "                                ")
        self.vacuum_load_lock_back.setObjectName("vacuum_load_lock_back")
        self.gridLayout.addWidget(self.vacuum_load_lock_back, 1, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_214 = QtWidgets.QLabel(parent=Pumps_Vacuum)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_214.setFont(font)
        self.label_214.setObjectName("label_214")
        self.gridLayout.addWidget(self.label_214, 1, 3, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.vacuum_buffer_back = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vacuum_buffer_back.sizePolicy().hasHeightForWidth())
        self.vacuum_buffer_back.setSizePolicy(sizePolicy)
        self.vacuum_buffer_back.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.vacuum_buffer_back.setFont(font)
        self.vacuum_buffer_back.setStyleSheet("QLCDNumber{\n"
                                              "                                    border: 2px solid blue;\n"
                                              "                                    border-radius: 10px;\n"
                                              "                                    padding: 0 8px;\n"
                                              "                                    }\n"
                                              "                                ")
        self.vacuum_buffer_back.setObjectName("vacuum_buffer_back")
        self.gridLayout.addWidget(self.vacuum_buffer_back, 1, 4, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.label_215 = QtWidgets.QLabel(parent=Pumps_Vacuum)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_215.setFont(font)
        self.label_215.setObjectName("label_215")
        self.gridLayout.addWidget(self.label_215, 1, 5, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.temp = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.temp.sizePolicy().hasHeightForWidth())
        self.temp.setSizePolicy(sizePolicy)
        self.temp.setMinimumSize(QtCore.QSize(100, 50))
        self.temp.setStyleSheet("QLCDNumber{\n"
                                "                                    border: 2px solid brown;\n"
                                "                                    border-radius: 10px;\n"
                                "                                    padding: 0 8px;\n"
                                "                                    }\n"
                                "                                ")
        self.temp.setObjectName("temp")
        self.gridLayout.addWidget(self.temp, 1, 6, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.vacuum_main = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vacuum_main.sizePolicy().hasHeightForWidth())
        self.vacuum_main.setSizePolicy(sizePolicy)
        self.vacuum_main.setMinimumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.vacuum_main.setFont(font)
        self.vacuum_main.setStyleSheet("QLCDNumber{\n"
                                       "                                    border: 2px solid green;\n"
                                       "                                    border-radius: 10px;\n"
                                       "                                    padding: 0 8px;\n"
                                       "                                    }\n"
                                       "                                ")
        self.vacuum_main.setObjectName("vacuum_main")
        self.gridLayout.addWidget(self.vacuum_main, 0, 6, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.Error = QtWidgets.QLabel(parent=Pumps_Vacuum)
        self.Error.setMinimumSize(QtCore.QSize(800, 30))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setStrikeOut(False)
        self.Error.setFont(font)
        self.Error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Error.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.Error.setObjectName("Error")
        self.gridLayout_2.addWidget(self.Error, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Pumps_Vacuum)
        QtCore.QMetaObject.connectSlotsByName(Pumps_Vacuum)

        ###
        self.led_red = QPixmap('./files/led-red-on.png')
        self.led_green = QPixmap('./files/green-led-on.png')
        self.led_pump_load_lock.setPixmap(self.led_green)
        self.pump_load_lock_switch.clicked.connect(self.pump_switch)
        # Set 8 digits for each LCD to show
        self.vacuum_main.setDigitCount(8)
        self.vacuum_buffer.setDigitCount(8)
        self.vacuum_buffer_back.setDigitCount(8)
        self.vacuum_load_lock.setDigitCount(8)
        self.vacuum_load_lock_back.setDigitCount(8)
        self.temp.setDigitCount(8)

        ###
        self.emitter.temp.connect(self.update_temperature)
        self.emitter.vacuum_main.connect(self.update_vacuum_main)
        self.emitter.vacuum_buffer.connect(self.update_vacuum_buffer)
        self.emitter.vacuum_buffer_back.connect(self.update_vacuum_buffer_back)
        self.emitter.vacuum_load_back.connect(self.update_vacuum_load_back)
        self.emitter.vacuum_load.connect(self.update_vacuum_load)
        # Connect the bool_flag_while_loop signal to a slot
        self.emitter.bool_flag_while_loop.connect(self.update_bool_flag_while_loop_gauges)
        self.emitter.bool_flag_while_loop.emit(True)

        # Thread for reading gauges
        if self.conf['gauges'] == "on":
            # Thread for reading gauges
            gauges_thread = threading.Thread(target=initialize_devices.state_update,
                                             args=(self.conf, self.variables, self.emitter,))
            gauges_thread.setDaemon(True)
            gauges_thread.start()

        # Create a QTimer to hide the warning message after 8 seconds
        self.timer = QTimer(self.parent)
        self.timer.timeout.connect(self.hideMessage)

    def retranslateUi(self, Pumps_Vacuum):
        _translate = QtCore.QCoreApplication.translate
        ###
        # Pumps_Vacuum.setWindowTitle(_translate("Pumps_Vacuum", "Form"))
        Pumps_Vacuum.setWindowTitle(_translate("Pumps_Vacuum", "PyCCAPT Pumps and Vacuum Control"))
        Pumps_Vacuum.setWindowIcon(QtGui.QIcon('./files/logo3.png'))
        ###
        self.led_pump_load_lock.setText(_translate("Pumps_Vacuum", "pump"))
        self.label_210.setText(_translate("Pumps_Vacuum", "Load lock (mBar)"))
        self.label_211.setText(_translate("Pumps_Vacuum", "Buffer Chamber (mBar)"))
        self.label_212.setText(_translate("Pumps_Vacuum", "Main Chamber (mBar)"))
        self.pump_load_lock_switch.setText(_translate("Pumps_Vacuum", "Load Lock Pump"))
        self.label_213.setText(_translate("Pumps_Vacuum", "Load Lock Pre(mBar)"))
        self.label_214.setText(_translate("Pumps_Vacuum", "Buffer Chamber Pre (mBar)"))
        self.label_215.setText(_translate("Pumps_Vacuum", "Temperature (K)"))
        self.Error.setText(_translate("Pumps_Vacuum", "<html><head/><body><p><br/></p></body></html>"))

    def update_temperature(self, value):
        self.temp.display(value)

    def update_vacuum_main(self, value):
        self.vacuum_main.display('{:.2e}'.format(value))

    def update_vacuum_buffer(self, value):
        self.vacuum_buffer.display('{:.2e}'.format(value))

    def update_vacuum_buffer_back(self, value):
        self.vacuum_buffer_back.display('{:.2e}'.format(value))

    def update_vacuum_load_back(self, value):
        self.vacuum_load_lock.display('{:.2e}'.format(value))

    def update_vacuum_load(self, value):
        self.vacuum_load_lock_back.display('{:.2e}'.format(value))

    def update_bool_flag_while_loop_gauges(self, value):
        # Connect the bool_flag_while_loop signal to a slot in this function
        with self.variables.lock_statistics:
            self.variables.bool_flag_while_loop_gages = value

    def hideMessage(self):
        # Hide the message and stop the timer
        _translate = QtCore.QCoreApplication.translate
        self.Error.setText(_translate("OXCART",
                                      "<html><head/><body><p><span style=\" "
                                      "color:#ff0000;\"></span></p></body></html>"))

        self.timer.stop()

    def pump_switch(self):
        """
			The function for Switching the Load Lock pump
		"""
        with self.variables.lock_statistics:
            try:
                if not self.variables.start_flag and not self.variables.flag_main_gate \
                        and not self.variables.flag_cryo_gate and not self.variables.flag_load_gate:
                    if self.variables.flag_pump_load_lock:
                        self.variables.flag_pump_load_lock_click = True
                        self.led_pump_load_lock.setPixmap(self.led_red)
                        self.pump_load_lock_switch.setEnabled(False)
                        time.sleep(1)
                        self.pump_load_lock_switch.setEnabled(True)
                    elif not variables.flag_pump_load_lock:
                        self.variables.flag_pump_load_lock_click = True
                        self.led_pump_load_lock.setPixmap(self.led_green)
                        self.pump_load_lock_switch.setEnabled(False)
                        time.sleep(1)
                        self.pump_load_lock_switch.setEnabled(True)
                else:  # SHow error message in the GUI
                    if not self.variables.start_flag:
                        self.error_message("!!! An experiment is running !!!")
                    else:
                        self.error_message("!!! First Close all the Gates !!!")

                    self.timer.start(8000)
            except Exception as e:
                print('Error in pump_switch function')
                print(e)
                pass

    def error_message(self, message):
        _translate = QtCore.QCoreApplication.translate
        self.Error.setText(_translate("OXCART",
                                      "<html><head/><body><p><span style=\" color:#ff0000;\">"
                                      + message + "</span></p></body></html>"))

    def stop(self):
        # Stop any background processes, timers, or threads here
        self.timer.stop()  # If you want to stop this timer when closing
        # Add any additional cleanup code here


class SignalEmitter(QObject):
    temp = pyqtSignal(float)
    vacuum_main = pyqtSignal(float)
    vacuum_buffer = pyqtSignal(float)
    vacuum_buffer_back = pyqtSignal(float)
    vacuum_load_back = pyqtSignal(float)
    vacuum_load = pyqtSignal(float)
    bool_flag_while_loop = pyqtSignal(bool)


class PumpsVacuumWindow(QtWidgets.QWidget):
    def __init__(self, gui_pumps_vacuum, signal_emitter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui_pumps_vacuum = gui_pumps_vacuum
        self.signal_emitter = signal_emitter

    def closeEvent(self, event):
        self.gui_pumps_vacuum.stop()  # Call the stop method to stop any background activity
        # Additional cleanup code here if needed
        super().closeEvent(event)
        self.signal_emitter.bool_flag_while_loop.emit(False)


if __name__ == "__main__":
    try:
        # load the Json file
        configFile = 'config.json'
        p = os.path.abspath(os.path.join(__file__, "../../.."))
        os.chdir(p)
        conf = read_files.read_json_file(configFile)
    except Exception as e:
        print('Can not load the configuration file')
        print(e)
        sys.exit()
    # Initialize global experiment class variables
    variables = share_variables.Variables(conf)
    variables.log_path = p

    app = QtWidgets.QApplication(sys.argv)
    Pumps_vacuum = QtWidgets.QWidget()
    signal_emitter = SignalEmitter()
    ui = Ui_Pumps_Vacuum(variables, conf, signal_emitter)
    ui.setupUi(Pumps_vacuum)
    Pumps_vacuum.show()
    sys.exit(app.exec())
