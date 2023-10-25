import multiprocessing
import os
import sys
import threading
import time

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QPixmap

# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files
from pyccapt.control.devices import initialize_devices


class Ui_Pumps_Vacuum(object):
	def __init__(self, variables, conf, SignalEmitter, parent=None):
		"""
		Constructor for the Pumps and Vacuum UI class.

		Args:
			variables (object): Global experiment variables.
			conf (dict): Configuration settings.
			SignalEmitter (object): Emitter for signals.
			parent: Parent widget (optional).

		Return:
			None
		"""
		self.variables = variables
		self.conf = conf
		self.parent = parent
		self.emitter = SignalEmitter

	def setupUi(self, Pumps_Vacuum):
		"""
		Sets up the UI for the Pumps and Vacuum tab.
		Args:
			Pumps_Vacuum (object): Pumps and Vacuum tab widget.

		Return:
			None
		"""
		Pumps_Vacuum.setObjectName("Pumps_Vacuum")
		Pumps_Vacuum.resize(620, 369)
		self.gridLayout_2 = QtWidgets.QGridLayout(Pumps_Vacuum)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		self.verticalLayout_8 = QtWidgets.QVBoxLayout()
		self.verticalLayout_8.setObjectName("verticalLayout_8")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.verticalLayout_4 = QtWidgets.QVBoxLayout()
		self.verticalLayout_4.setObjectName("verticalLayout_4")
		self.label_215 = QtWidgets.QLabel(parent=Pumps_Vacuum)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_215.setFont(font)
		self.label_215.setObjectName("label_215")
		self.verticalLayout_4.addWidget(self.label_215)
		self.label_214 = QtWidgets.QLabel(parent=Pumps_Vacuum)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_214.setFont(font)
		self.label_214.setObjectName("label_214")
		self.verticalLayout_4.addWidget(self.label_214)
		self.label_217 = QtWidgets.QLabel(parent=Pumps_Vacuum)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_217.setFont(font)
		self.label_217.setObjectName("label_217")
		self.verticalLayout_4.addWidget(self.label_217)
		self.label_213 = QtWidgets.QLabel(parent=Pumps_Vacuum)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_213.setFont(font)
		self.label_213.setObjectName("label_213")
		self.verticalLayout_4.addWidget(self.label_213)
		self.horizontalLayout_2.addLayout(self.verticalLayout_4)
		self.verticalLayout_3 = QtWidgets.QVBoxLayout()
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.temp = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
		                                   QtWidgets.QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.temp.sizePolicy().hasHeightForWidth())
		self.temp.setSizePolicy(sizePolicy)
		self.temp.setMinimumSize(QtCore.QSize(100, 50))
		self.temp.setStyleSheet("QLCDNumber{\n"
		                        "border: 2px solid orange;\n"
		                        "border-radius: 10px;\n"
		                        "padding: 0 8px;\n"
		                        "}\n"
		                        "                                        ")
		self.temp.setObjectName("temp")
		self.verticalLayout_3.addWidget(self.temp)
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
		                                      "                                            border: 2px solid brown;\n"
		                                      "                                            border-radius: 10px;\n"
		                                      "                                            padding: 0 8px;\n"
		                                      "                                            }\n"
		                                      "                                        ")
		self.vacuum_buffer_back.setObjectName("vacuum_buffer_back")
		self.verticalLayout_3.addWidget(self.vacuum_buffer_back)
		self.vacuum_cryo_load_lock_back = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
		                                   QtWidgets.QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vacuum_cryo_load_lock_back.sizePolicy().hasHeightForWidth())
		self.vacuum_cryo_load_lock_back.setSizePolicy(sizePolicy)
		self.vacuum_cryo_load_lock_back.setMinimumSize(QtCore.QSize(100, 50))
		self.vacuum_cryo_load_lock_back.setStyleSheet("QLCDNumber{\n"
		                                              "border: 2px solid magenta;\n"
		                                              "border-radius: 10px;\n"
		                                              "padding: 0 8px;\n"
		                                              "}\n"
		                                              "                                        ")
		self.vacuum_cryo_load_lock_back.setObjectName("vacuum_cryo_load_lock_back")
		self.verticalLayout_3.addWidget(self.vacuum_cryo_load_lock_back)
		self.vacuum_load_lock_back = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
		                                   QtWidgets.QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vacuum_load_lock_back.sizePolicy().hasHeightForWidth())
		self.vacuum_load_lock_back.setSizePolicy(sizePolicy)
		self.vacuum_load_lock_back.setMinimumSize(QtCore.QSize(100, 50))
		self.vacuum_load_lock_back.setStyleSheet("QLCDNumber{\n"
		                                         "border: 2px solid blue;\n"
		                                         "border-radius: 10px;\n"
		                                         "padding: 0 8px;\n"
		                                         "}\n"
		                                         "                                        ")
		self.vacuum_load_lock_back.setObjectName("vacuum_load_lock_back")
		self.verticalLayout_3.addWidget(self.vacuum_load_lock_back)
		self.horizontalLayout_2.addLayout(self.verticalLayout_3)
		self.verticalLayout_8.addLayout(self.horizontalLayout_2)
		self.verticalLayout_6 = QtWidgets.QVBoxLayout()
		self.verticalLayout_6.setObjectName("verticalLayout_6")
		self.led_pump_load_lock = QtWidgets.QLabel(parent=Pumps_Vacuum)
		self.led_pump_load_lock.setMinimumSize(QtCore.QSize(50, 50))
		self.led_pump_load_lock.setMaximumSize(QtCore.QSize(50, 50))
		self.led_pump_load_lock.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.led_pump_load_lock.setObjectName("led_pump_load_lock")
		self.verticalLayout_6.addWidget(self.led_pump_load_lock, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
		self.pump_load_lock_switch = QtWidgets.QPushButton(parent=Pumps_Vacuum)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pump_load_lock_switch.sizePolicy().hasHeightForWidth())
		self.pump_load_lock_switch.setSizePolicy(sizePolicy)
		self.pump_load_lock_switch.setMinimumSize(QtCore.QSize(0, 25))
		self.pump_load_lock_switch.setStyleSheet("QPushButton{\n"
		                                         "                                            background: rgb(193, 193, 193)\n"
		                                         "                                            }\n"
		                                         "                                        ")
		self.pump_load_lock_switch.setObjectName("pump_load_lock_switch")
		self.verticalLayout_6.addWidget(self.pump_load_lock_switch, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
		self.verticalLayout_8.addLayout(self.verticalLayout_6)
		self.gridLayout.addLayout(self.verticalLayout_8, 0, 0, 1, 1)
		self.verticalLayout_7 = QtWidgets.QVBoxLayout()
		self.verticalLayout_7.setObjectName("verticalLayout_7")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.verticalLayout_2 = QtWidgets.QVBoxLayout()
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.label_212 = QtWidgets.QLabel(parent=Pumps_Vacuum)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_212.setFont(font)
		self.label_212.setObjectName("label_212")
		self.verticalLayout_2.addWidget(self.label_212)
		self.label_211 = QtWidgets.QLabel(parent=Pumps_Vacuum)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_211.setFont(font)
		self.label_211.setObjectName("label_211")
		self.verticalLayout_2.addWidget(self.label_211)
		self.label_216 = QtWidgets.QLabel(parent=Pumps_Vacuum)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_216.setFont(font)
		self.label_216.setObjectName("label_216")
		self.verticalLayout_2.addWidget(self.label_216)
		self.label_210 = QtWidgets.QLabel(parent=Pumps_Vacuum)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_210.setFont(font)
		self.label_210.setObjectName("label_210")
		self.verticalLayout_2.addWidget(self.label_210)
		self.horizontalLayout.addLayout(self.verticalLayout_2)
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")
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
		                               "                                            border: 2px solid green;\n"
		                               "                                            border-radius: 10px;\n"
		                               "                                            padding: 0 8px;\n"
		                               "                                            }\n"
		                               "                                        ")
		self.vacuum_main.setObjectName("vacuum_main")
		self.verticalLayout.addWidget(self.vacuum_main)
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
		                                 "                                            border: 2px solid brown;\n"
		                                 "                                            border-radius: 10px;\n"
		                                 "                                            padding: 0 8px;\n"
		                                 "                                            }\n"
		                                 "                                        ")
		self.vacuum_buffer.setObjectName("vacuum_buffer")
		self.verticalLayout.addWidget(self.vacuum_buffer)
		self.vacuum_cryo_load_lock = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
		                                   QtWidgets.QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vacuum_cryo_load_lock.sizePolicy().hasHeightForWidth())
		self.vacuum_cryo_load_lock.setSizePolicy(sizePolicy)
		self.vacuum_cryo_load_lock.setMinimumSize(QtCore.QSize(100, 50))
		self.vacuum_cryo_load_lock.setStyleSheet("QLCDNumber{\n"
		                                         "                                            border: 2px solid magenta;\n"
		                                         "                                            border-radius: 10px;\n"
		                                         "                                            padding: 0 8px;\n"
		                                         "                                            }\n"
		                                         "                                        ")
		self.vacuum_cryo_load_lock.setObjectName("vacuum_cryo_load_lock")
		self.verticalLayout.addWidget(self.vacuum_cryo_load_lock)
		self.vacuum_load_lock = QtWidgets.QLCDNumber(parent=Pumps_Vacuum)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
		                                   QtWidgets.QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vacuum_load_lock.sizePolicy().hasHeightForWidth())
		self.vacuum_load_lock.setSizePolicy(sizePolicy)
		self.vacuum_load_lock.setMinimumSize(QtCore.QSize(100, 50))
		self.vacuum_load_lock.setStyleSheet("QLCDNumber{\n"
		                                    "border: 2px solid blue;\n"
		                                    "border-radius: 10px;\n"
		                                    "padding: 0 8px;\n"
		                                    "}\n"
		                                    "                                        ")
		self.vacuum_load_lock.setObjectName("vacuum_load_lock")
		self.verticalLayout.addWidget(self.vacuum_load_lock)
		self.horizontalLayout.addLayout(self.verticalLayout)
		self.verticalLayout_7.addLayout(self.horizontalLayout)
		self.verticalLayout_5 = QtWidgets.QVBoxLayout()
		self.verticalLayout_5.setObjectName("verticalLayout_5")
		self.led_pump_cryo_load_lock = QtWidgets.QLabel(parent=Pumps_Vacuum)
		self.led_pump_cryo_load_lock.setMinimumSize(QtCore.QSize(50, 50))
		self.led_pump_cryo_load_lock.setMaximumSize(QtCore.QSize(50, 50))
		self.led_pump_cryo_load_lock.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.led_pump_cryo_load_lock.setObjectName("led_pump_cryo_load_lock")
		self.verticalLayout_5.addWidget(self.led_pump_cryo_load_lock, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
		self.pump_cryo_load_lock_switch = QtWidgets.QPushButton(parent=Pumps_Vacuum)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pump_cryo_load_lock_switch.sizePolicy().hasHeightForWidth())
		self.pump_cryo_load_lock_switch.setSizePolicy(sizePolicy)
		self.pump_cryo_load_lock_switch.setMinimumSize(QtCore.QSize(0, 25))
		self.pump_cryo_load_lock_switch.setStyleSheet("QPushButton{\n"
		                                              "                                            background: rgb(193, 193, 193)\n"
		                                              "                                            }\n"
		                                              "                                        ")
		self.pump_cryo_load_lock_switch.setObjectName("pump_cryo_load_lock_switch")
		self.verticalLayout_5.addWidget(self.pump_cryo_load_lock_switch, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
		self.verticalLayout_7.addLayout(self.verticalLayout_5)
		self.gridLayout.addLayout(self.verticalLayout_7, 0, 1, 1, 1)
		self.Error = QtWidgets.QLabel(parent=Pumps_Vacuum)
		self.Error.setMinimumSize(QtCore.QSize(600, 30))
		font = QtGui.QFont()
		font.setPointSize(13)
		font.setBold(True)
		font.setStrikeOut(False)
		self.Error.setFont(font)
		self.Error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		self.Error.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
		self.Error.setObjectName("Error")
		self.gridLayout.addWidget(self.Error, 1, 0, 1, 2)
		self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

		self.retranslateUi(Pumps_Vacuum)
		QtCore.QMetaObject.connectSlotsByName(Pumps_Vacuum)

		###
		self.led_red = QPixmap('./files/led-red-on.png')
		self.led_green = QPixmap('./files/green-led-on.png')
		self.led_pump_load_lock.setPixmap(self.led_green)
		self.led_pump_cryo_load_lock.setPixmap(self.led_green)
		self.pump_load_lock_switch.clicked.connect(self.pump_switch_ll)
		self.pump_cryo_load_lock_switch.clicked.connect(self.pump_switch_cryo_ll)
		# Set 8 digits for each LCD to show
		self.vacuum_main.setDigitCount(8)
		self.vacuum_buffer.setDigitCount(8)
		self.vacuum_buffer_back.setDigitCount(8)
		self.vacuum_load_lock.setDigitCount(8)
		self.vacuum_load_lock_back.setDigitCount(8)
		self.vacuum_cryo_load_lock.setDigitCount(8)
		self.vacuum_cryo_load_lock_back.setDigitCount(8)
		self.temp.setDigitCount(8)

		###
		self.emitter.temp.connect(self.update_temperature)
		self.emitter.vacuum_main.connect(self.update_vacuum_main)
		self.emitter.vacuum_buffer.connect(self.update_vacuum_buffer)
		self.emitter.vacuum_buffer_back.connect(self.update_vacuum_buffer_back)
		self.emitter.vacuum_load_lock_back.connect(self.update_vacuum_load_back)
		self.emitter.vacuum_load_lock.connect(self.update_vacuum_load)
		self.emitter.vacuum_cryo_load_lock.connect(self.update_vacuum_cryo_load_lock)
		self.emitter.vacuum_cryo_load_lock_back.connect(self.update_vacuum_cryo_load_lock_back)
		# Connect the bool_flag_while_loop signal to a slot
		self.emitter.bool_flag_while_loop.emit(True)

		# Thread for reading gauges
		if self.conf['gauges'] == "on":
			# Thread for reading gauges
			self.gauges_thread = threading.Thread(target=initialize_devices.state_update,
			                                      args=(self.conf, self.variables, self.emitter,))
			self.gauges_thread.setDaemon(True)
			self.gauges_thread.start()

		# Create a QTimer to hide the warning message after 8 seconds
		self.timer = QTimer(self.parent)
		self.timer.timeout.connect(self.hideMessage)

	def retranslateUi(self, Pumps_Vacuum):
		"""
		Set the text and title of the widgets
		Args:
			Pumps_Vacuum: the main window

		Return:
			None
		"""
		_translate = QtCore.QCoreApplication.translate
		###
		# Pumps_Vacuum.setWindowTitle(_translate("Pumps_Vacuum", "Form"))
		Pumps_Vacuum.setWindowTitle(_translate("Pumps_Vacuum", "PyCCAPT Pumps and Vacuum Control"))
		Pumps_Vacuum.setWindowIcon(QtGui.QIcon('./files/logo3.png'))
		###
		self.label_215.setText(_translate("Pumps_Vacuum", "Temperature (K)"))
		self.label_214.setText(_translate("Pumps_Vacuum", "Buffer Chamber Pre (mBar)"))
		self.label_217.setText(_translate("Pumps_Vacuum", "CryoLoad Lock Pre(mBar)"))
		self.label_213.setText(_translate("Pumps_Vacuum", "Load Lock Pre(mBar)"))
		self.led_pump_load_lock.setText(_translate("Pumps_Vacuum", "pump"))
		self.pump_load_lock_switch.setText(_translate("Pumps_Vacuum", "Vent LL "))
		self.label_212.setText(_translate("Pumps_Vacuum", "Main Chamber (mBar)"))
		self.label_211.setText(_translate("Pumps_Vacuum", "Buffer Chamber (mBar)"))
		self.label_216.setText(_translate("Pumps_Vacuum", "Cryo Load lock (mBar)"))
		self.label_210.setText(_translate("Pumps_Vacuum", "Load lock (mBar)"))
		self.led_pump_cryo_load_lock.setText(_translate("Pumps_Vacuum", "pump"))
		self.pump_cryo_load_lock_switch.setText(_translate("Pumps_Vacuum", "Vent CLL"))
		self.Error.setText(_translate("Pumps_Vacuum", "<html><head/><body><p><br/></p></body></html>"))

	def update_temperature(self, value):
		"""
		Update the temperature value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		self.temp.display(value)

	def update_vacuum_main(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		self.vacuum_main.display('{:.2e}'.format(value))

	def update_vacuum_buffer(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		self.vacuum_buffer.display('{:.2e}'.format(value))

	def update_vacuum_buffer_back(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		self.vacuum_buffer_back.display('{:.2e}'.format(value))

	def update_vacuum_load_back(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		self.vacuum_load_lock_back.display('{:.2e}'.format(value))

	def update_vacuum_load(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		self.vacuum_load_lock.display('{:.2e}'.format(value))

	def update_vacuum_cryo_load_lock(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		self.vacuum_cryo_load_lock.display('{:.2e}'.format(value))

	def update_vacuum_cryo_load_lock_back(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		self.vacuum_cryo_load_lock_back.display('{:.2e}'.format(value))

	def hideMessage(self):
		"""
		Hide the warning message
		Args:
			None

		Return:
			None
		"""
		# Hide the message and stop the timer
		_translate = QtCore.QCoreApplication.translate
		self.Error.setText(_translate("OXCART",
		                              "<html><head/><body><p><span style=\" "
		                              "color:#ff0000;\"></span></p></body></html>"))

		self.timer.stop()

	def pump_switch_ll(self):
		"""
		Switch the pump on or off
		Args:
			None

		Return:
			None
		"""
		# with self.variables.lock_statistics:
		try:
			if not self.variables.start_flag and not self.variables.flag_main_gate \
					and not self.variables.flag_cryo_gate and not self.variables.flag_load_gate:
				if self.variables.flag_pump_load_lock:
					self.variables.flag_pump_load_lock_click = True
					self.led_pump_load_lock.setPixmap(self.led_red)
					self.pump_load_lock_switch.setEnabled(False)
					time.sleep(1)
					self.pump_load_lock_switch.setEnabled(True)
				elif not self.variables.flag_pump_load_lock:
					self.variables.flag_pump_load_lock_click = True
					self.led_pump_load_lock.setPixmap(self.led_green)
					self.pump_load_lock_switch.setEnabled(False)
					time.sleep(1)
					self.pump_load_lock_switch.setEnabled(True)
			else:  # SHow error message in the GUI
				if self.variables.start_flag:
					self.error_message("!!! An experiment is running !!!")
				else:
					self.error_message("!!! First Close all the Gates !!!")

				self.timer.start(8000)
		except Exception as e:
			print('Error in pump_switch function')
			print(e)
			pass

	def pump_switch_cryo_ll(self):
		try:
			if not self.variables.start_flag and not self.variables.flag_main_gate \
					and not self.variables.flag_cryo_gate and not self.variables.flag_load_gate:
				if self.variables.flag_pump_cryo_load_lock:
					self.variables.flag_pump_cryo_load_lock_click = True
					self.led_pump_cryo_load_lock.setPixmap(self.led_red)
					self.pump_cryo_load_lock_switch.setEnabled(False)
					time.sleep(1)
					self.pump_cryo_load_lock_switch.setEnabled(True)
				elif not self.variables.flag_pump_cryo_load_lock:
					self.variables.flag_pump_cryo_load_lock_click = True
					self.led_pump_cryo_load_lock.setPixmap(self.led_green)
					self.pump_cryo_load_lock_switch.setEnabled(False)
					time.sleep(1)
					self.pump_cryo_load_lock_switch.setEnabled(True)
			else:  # SHow error message in the GUI
				if self.variables.start_flag:
					self.error_message("!!! An experiment is running !!!")
				else:
					self.error_message("!!! First Close all the Gates !!!")

				self.timer.start(8000)
		except Exception as e:
			print('Error in pump_switch function')
			print(e)
			pass

	def error_message(self, message):
		"""
		Show the warning message
		Args:
			message: the message to be shown

		Return:
			None
		"""
		_translate = QtCore.QCoreApplication.translate
		self.Error.setText(_translate("OXCART",
		                              "<html><head/><body><p><span style=\" color:#ff0000;\">"
		                              + message + "</span></p></body></html>"))

	def stop(self):
		"""
		Stop the timer
		Args:
			None

		Return:
			None
		"""
		# Stop any background processes, timers, or threads here
		self.timer.stop()  # If you want to stop this timer when closing


class SignalEmitter(QObject):
	"""
	Signal emitter class for emitting signals related to vacuum and pumps control.
	"""

	temp = pyqtSignal(float)
	vacuum_main = pyqtSignal(float)
	vacuum_buffer = pyqtSignal(float)
	vacuum_buffer_back = pyqtSignal(float)
	vacuum_load_lock_back = pyqtSignal(float)
	vacuum_load_lock = pyqtSignal(float)
	vacuum_cryo_load_lock = pyqtSignal(float)
	vacuum_cryo_load_lock_back = pyqtSignal(float)
	bool_flag_while_loop = pyqtSignal(bool)


class PumpsVacuumWindow(QtWidgets.QWidget):
	"""
	Widget for Pumps and Vacuum control window.
	"""
	closed = QtCore.pyqtSignal()  # Define a custom closed signal

	def __init__(self, gui_pumps_vacuum, signal_emitter, *args, **kwargs):
		"""
		Constructor for the PumpsVacuumWindow class.

		Args:
			gui_pumps_vacuum: Instance of the PumpsVacuum control.
			signal_emitter: SignalEmitter object for communication.
			*args: Additional positional arguments.
			**kwargs: Additional keyword arguments.
		"""
		super().__init__(*args, **kwargs)
		self.gui_pumps_vacuum = gui_pumps_vacuum
		self.signal_emitter = signal_emitter

	def closeEvent(self, event):
		"""
			Close event for the window.

			Args:
				event: Close event.
		"""
		self.gui_pumps_vacuum.stop()  # Call the stop method to stop any background activity
		self.signal_emitter.bool_flag_while_loop.emit(False)
		self.gui_pumps_vacuum.gauges_thread.join(1)
		# Additional cleanup code here if needed
		self.closed.emit()  # Emit the custom closed signal
		super().closeEvent(event)

	def setWindowStyleFusion(self):
		# Set the Fusion style
		QtWidgets.QApplication.setStyle("Fusion")


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
	manager = multiprocessing.Manager()
	ns = manager.Namespace()
	variables = share_variables.Variables(conf, ns)

	app = QtWidgets.QApplication(sys.argv)
	app.setStyle('Fusion')
	Pumps_vacuum = QtWidgets.QWidget()
	signal_emitter = SignalEmitter()
	ui = Ui_Pumps_Vacuum(variables, conf, signal_emitter)
	ui.setupUi(Pumps_vacuum)
	Pumps_vacuum.show()
	sys.exit(app.exec())
