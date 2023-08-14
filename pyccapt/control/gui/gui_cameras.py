import os
import sys
import threading

import numpy as np
import pyqtgraph as pg
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QPixmap
from pypylon import pylon

# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files
from pyccapt.control.devices.camera import Camera


class Ui_Cameras_Alignment(object):
	def __init__(self, variables, conf, SignalEmitter):
		"""
		Initialize the UiCamerasAlignment class.

		Args:
		    variables: Global experiment variables.
		    conf: Configuration data.
		    SignalEmitter: Signal emitter for communication.
		"""
		self.conf = conf
		self.emitter = SignalEmitter
		self.variables = variables

	def setupUi(self, Cameras_Alignment):
		"""
        Set up the GUI for the Cameras Alignment window.

        Args:
            Cameras_Alignment:

        Returns:
            None
        """
		Cameras_Alignment.setObjectName("Cameras_Alignment")

		Cameras_Alignment.resize(1049, 616)
		self.gridLayout_4 = QtWidgets.QGridLayout(Cameras_Alignment)
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.gridLayout_3 = QtWidgets.QGridLayout()
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		self.label_202 = QtWidgets.QLabel(parent=Cameras_Alignment)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_202.setFont(font)
		self.label_202.setObjectName("label_202")
		self.gridLayout.addWidget(self.label_202, 0, 1, 1, 1)
		self.label_203 = QtWidgets.QLabel(parent=Cameras_Alignment)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_203.setFont(font)
		self.label_203.setObjectName("label_203")
		self.gridLayout.addWidget(self.label_203, 1, 0, 1, 1)
		###
		# self.cam_s_o = QtWidgets.QLabel(parent=Cameras_alignment)
		self.cam_s_o = pg.ImageView(parent=Cameras_Alignment)
		self.cam_s_o.adjustSize()
		self.cam_s_o.ui.histogram.hide()
		self.cam_s_o.ui.roiBtn.hide()
		self.cam_s_o.ui.menuBtn.hide()
		self.cam_s_o.setObjectName("cam_s_o")
		###
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
		                                   QtWidgets.QSizePolicy.Policy.Expanding)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.cam_s_o.sizePolicy().hasHeightForWidth())
		self.cam_s_o.setSizePolicy(sizePolicy)
		self.cam_s_o.setMinimumSize(QtCore.QSize(250, 250))
		self.cam_s_o.setStyleSheet("QWidget{\n"
		                           "border: 2px solid gray;\n"
		                           "}")
		# self.cam_s_o.setText("")
		self.cam_s_o.setObjectName("cam_s_o")
		self.gridLayout.addWidget(self.cam_s_o, 2, 0, 1, 4)
		###
		# self.cam_s_d = QtWidgets.QLabel(parent=Cameras_alignment)
		self.cam_s_d = pg.ImageView(parent=Cameras_Alignment)
		self.cam_s_d.adjustSize()
		self.cam_s_d.ui.histogram.hide()
		self.cam_s_d.ui.roiBtn.hide()
		self.cam_s_d.ui.menuBtn.hide()
		###
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
		                                   QtWidgets.QSizePolicy.Policy.Expanding)
		sizePolicy.setHorizontalStretch(2)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.cam_s_d.sizePolicy().hasHeightForWidth())
		self.cam_s_d.setSizePolicy(sizePolicy)
		self.cam_s_d.setMinimumSize(QtCore.QSize(600, 250))
		self.cam_s_d.setMaximumSize(QtCore.QSize(16777215, 16777215))
		self.cam_s_d.setStyleSheet("QWidget{\n"
		                           "border: 2px solid gray;\n"
		                           "}")
		# self.cam_s_d.setText("")
		self.cam_s_d.setObjectName("cam_s_d")
		self.gridLayout.addWidget(self.cam_s_d, 2, 4, 1, 1)
		self.label_205 = QtWidgets.QLabel(parent=Cameras_Alignment)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_205.setFont(font)
		self.label_205.setObjectName("label_205")
		self.gridLayout.addWidget(self.label_205, 3, 1, 1, 2)
		self.label_208 = QtWidgets.QLabel(parent=Cameras_Alignment)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_208.setFont(font)
		self.label_208.setObjectName("label_208")
		self.gridLayout.addWidget(self.label_208, 4, 0, 1, 1)
		###
		# self.cam_b_o = QtWidgets.QLabel(parent=Cameras_alignment)
		self.cam_b_o = pg.ImageView(parent=Cameras_Alignment)
		self.cam_b_o.adjustSize()
		self.cam_b_o.ui.histogram.hide()
		self.cam_b_o.ui.roiBtn.hide()
		self.cam_b_o.ui.menuBtn.hide()
		###
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
		                                   QtWidgets.QSizePolicy.Policy.Expanding)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.cam_b_o.sizePolicy().hasHeightForWidth())
		self.cam_b_o.setSizePolicy(sizePolicy)
		self.cam_b_o.setMinimumSize(QtCore.QSize(250, 250))
		self.cam_b_o.setMaximumSize(QtCore.QSize(16777215, 16777215))
		self.cam_b_o.setStyleSheet("QWidget{\n"
		                           "border: 2px solid gray;\n"
		                           "}")
		# self.cam_b_o.setText("")
		self.cam_b_o.setObjectName("cam_b_o")
		self.gridLayout.addWidget(self.cam_b_o, 5, 0, 1, 4)
		###
		# self.cam_b_d = QtWidgets.QLabel(parent=Cameras_alignment)
		self.cam_b_d = pg.ImageView(parent=Cameras_Alignment)
		self.cam_b_d.adjustSize()
		self.cam_b_d.ui.histogram.hide()
		self.cam_b_d.ui.roiBtn.hide()
		self.cam_b_d.ui.menuBtn.hide()
		###
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
		                                   QtWidgets.QSizePolicy.Policy.Expanding)
		sizePolicy.setHorizontalStretch(2)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.cam_b_d.sizePolicy().hasHeightForWidth())
		self.cam_b_d.setSizePolicy(sizePolicy)
		self.cam_b_d.setMinimumSize(QtCore.QSize(600, 250))
		self.cam_b_d.setMaximumSize(QtCore.QSize(16777215, 16777215))
		self.cam_b_d.setStyleSheet("QWidget{\n"
		                           "border: 2px solid gray;\n"
		                           "}")
		# self.cam_b_d.setText("")
		self.cam_b_d.setObjectName("cam_b_d")
		self.gridLayout.addWidget(self.cam_b_d, 5, 4, 1, 1)
		self.label_204 = QtWidgets.QLabel(parent=Cameras_Alignment)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_204.setFont(font)
		self.label_204.setObjectName("label_204")
		self.gridLayout.addWidget(self.label_204, 1, 4, 1, 1)
		self.label_209 = QtWidgets.QLabel(parent=Cameras_Alignment)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_209.setFont(font)
		self.label_209.setObjectName("label_209")
		self.gridLayout.addWidget(self.label_209, 4, 4, 1, 1)
		self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
		self.gridLayout_2 = QtWidgets.QGridLayout()
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.light = QtWidgets.QPushButton(parent=Cameras_Alignment)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.light.sizePolicy().hasHeightForWidth())
		self.light.setSizePolicy(sizePolicy)
		self.light.setMinimumSize(QtCore.QSize(0, 25))
		self.light.setStyleSheet("QPushButton{\n"
		                         "background: rgb(193, 193, 193)\n"
		                         "}")
		self.light.setObjectName("light")
		self.gridLayout_2.addWidget(self.light, 0, 0, 1, 1)
		self.led_light = QtWidgets.QLabel(parent=Cameras_Alignment)
		self.led_light.setMaximumSize(QtCore.QSize(50, 50))
		self.led_light.setObjectName("led_light")
		self.gridLayout_2.addWidget(self.led_light, 0, 1, 1, 1)
		self.win_alignment = QtWidgets.QPushButton(parent=Cameras_Alignment)
		self.win_alignment.setMinimumSize(QtCore.QSize(0, 25))
		self.win_alignment.setStyleSheet("QPushButton{\n"
		                                 "background: rgb(193, 193, 193)\n"
		                                 "}")
		self.win_alignment.setObjectName("win_alignment")
		self.gridLayout_2.addWidget(self.win_alignment, 1, 0, 1, 1)
		spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
		                                   QtWidgets.QSizePolicy.Policy.Expanding)
		self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
		self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)
		self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

		self.retranslateUi(Cameras_Alignment)
		QtCore.QMetaObject.connectSlotsByName(Cameras_Alignment)
		Cameras_Alignment.setTabOrder(self.light, self.win_alignment)

		###
		# Diagram and LEDs ##############
		self.led_red = QPixmap('./files/led-red-on.png')
		self.led_green = QPixmap('./files/green-led-on.png')
		self.led_light.setPixmap(self.led_red)

		# bottom camera (x, y)
		arrow1 = pg.ArrowItem(pos=(940, 770), angle=0)
		self.cam_b_o.addItem(arrow1)
		# Side camera (x, y)
		arrow1 = pg.ArrowItem(pos=(450, 550), angle=-90)
		arrow2 = pg.ArrowItem(pos=(450, 1500), angle=90)
		arrow3 = pg.ArrowItem(pos=(890, 1100), angle=0)
		self.cam_s_o.addItem(arrow1)
		self.cam_s_o.addItem(arrow2)
		self.cam_s_o.addItem(arrow3)
		# side camera zoom (x, y)
		arrow1 = pg.ArrowItem(pos=(265, 57), angle=90, brush='r')
		self.cam_s_d.addItem(arrow1)
		# bottom camera zoom (x, y)
		arrow1 = pg.ArrowItem(pos=(260, 50), angle=90, brush='r')
		self.cam_b_d.addItem(arrow1)
		###
		self.light.clicked.connect(self.light_switch)
		self.win_alignment.clicked.connect(self.win_alignment_switch)

		self.emitter.img0_orig.connect(self.update_cam_s_o)
		self.emitter.img0_zoom.connect(self.update_cam_s_d)
		self.emitter.img1_orig.connect(self.update_cam_b_o)
		self.emitter.img1_zoom.connect(self.update_cam_b_d)
		self.initialize_camera_thread()

	def retranslateUi(self, Cameras_alignment):
		"""

		Args:
			Cameras_alignment:

		Returns:
			None
		"""
		_translate = QtCore.QCoreApplication.translate
		###
		# Cameras_alignment.setWindowTitle(_translate("Cameras_alignment", "Form"))
		Cameras_alignment.setWindowTitle(_translate("Cameras_alignment", "PyCCAPT Cameras"))
		Cameras_alignment.setWindowIcon(QtGui.QIcon('./files/logo3.png'))
		###
		self.label_202.setText(_translate("Cameras_alignment", "Camera Side"))
		font = QtGui.QFont()

		font.setPointSize(12)
		font.setBold(True)
		self.label_202.setFont(font)
		self.label_203.setText(_translate("Cameras_alignment", "Overview"))
		self.label_205.setText(_translate("Cameras_alignment", "Camera Bottom"))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		self.label_205.setFont(font)
		self.label_208.setText(_translate("Cameras_alignment", "Overview"))
		self.label_204.setText(_translate("Cameras_alignment", "Detail"))
		self.label_209.setText(_translate("Cameras_alignment", "Detail"))
		self.light.setText(_translate("Cameras_alignment", "Light"))
		self.led_light.setText(_translate("Cameras_alignment", "TextLabel"))
		self.win_alignment.setText(_translate("Cameras_alignment", "Alignment window"))

	def update_cam_s_o(self, img):
		self.cam_s_o.setImage(img, autoRange=False)

	def update_cam_s_d(self, img):
		self.cam_s_d.setImage(img, autoRange=False)

	def update_cam_b_o(self, img):
		self.cam_b_o.setImage(img, autoRange=False)

	def update_cam_b_d(self, img):
		self.cam_b_d.setImage(img, autoRange=False)

	def light_switch(self):
		"""
		light switch function

		Args:
			None

		Return:
			None
		"""
		if not self.variables.light:
			self.led_light.setPixmap(self.led_green)
			self.camera.light_switch()
			# with self.variables.lock_setup_parameters:
			self.variables.light = True

			self.variables.light_switch = True

		elif self.variables.light:
			self.led_light.setPixmap(self.led_red)
			self.camera.light_switch()
			# with self.variables.lock_setup_parameters:
			self.variables.light = False
			self.variables.light_switch = False

	def win_alignment_switch(self):
		"""
		Alignment window switch function

		Args:
			None

		Return:
			None
		"""
		if not self.variables.alignment_window:
			# with self.variables.lock_setup_parameters:
			self.variables.alignment_window = True
			self.win_alignment.setStyleSheet("QPushButton{\n"
			                                 "background: rgb(0, 255, 26)\n"
			                                 "}")
		elif self.variables.alignment_window:
			# with self.variables.lock_setup_parameters:
			self.variables.alignment_window = False
			self.win_alignment.setStyleSheet("QPushButton{\n"
			                                 "background: rgb(193, 193, 193)\n"
			                                 "}")

	def initialize_camera_thread(self):
		"""
		Initialize camera thread

		Args:
			None

		Return:
			None
		"""
		if self.conf['camera'] == "off":
			print('The cameras is off')
		else:
			# Create cameras thread
			try:
				# Limits the amount of cameras used for grabbing.
				# The bandwidth used by a FireWire camera device can be limited by adjusting the packet size.
				maxCamerasToUse = 2
				# The exit code of the sample application.
				exitCode = 0
				# Get the transport layer factory.
				tlFactory = pylon.TlFactory.GetInstance()
				# Get all attached devices and exit application if no device is found.
				devices = tlFactory.EnumerateDevices()

				if len(devices) == 0:
					raise pylon.RuntimeException("No camera present.")

				# Create an array of instant cameras for the found devices and avoid exceeding a maximum number of
				# devices.
				cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse))

				# Create and attach all Pylon Devices.
				for i, cam in enumerate(cameras):
					cam.Attach(tlFactory.CreateDevice(devices[i]))
				converter = pylon.ImageFormatConverter()

				# converting to opencv bgr format
				converter.OutputPixelFormat = pylon.PixelType_BGR8packed
				converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

				self.camera = Camera(devices, tlFactory, cameras, converter, self.variables, self.emitter)

				# Thread for reading cameras
				self.camera_thread = threading.Thread(target=self.camera.update_cameras)
				self.camera_thread.setDaemon(True)
				# with self.variables.lock_setup_parameters:
				self.variables.flag_camera_grab = True
				self.camera_thread.start()

			except Exception as e:
				print('Can not initialize the Cameras')
				print(e)

	def stop(self):
		"""
		Stop the timer and any other background processes, timers, or threads here

		Args:
			None

		Return:
			None
		"""
		# Add any additional cleanup code here
		# with self.variables.lock_setup_parameters:
		self.variables.flag_camera_grab = False
		self.camera_thread.join()


class SignalEmitter(QObject):
	img0_orig = pyqtSignal(np.ndarray)
	img0_zoom = pyqtSignal(np.ndarray)
	img1_orig = pyqtSignal(np.ndarray)
	img1_zoom = pyqtSignal(np.ndarray)


class CamerasAlignmentWindow(QtWidgets.QWidget):
	closed = QtCore.pyqtSignal()  # Define a custom closed signal
	def __init__(self, gui_cameras_alignment, *args, **kwargs):
		"""
		Initialize the CamerasAlignmentWindow class.

		Args:
		    gui_cameras_alignment: An instance of the GUI cameras alignment class.
		    *args: Variable length argument list.
		    **kwargs: Arbitrary keyword arguments.
		"""
		super().__init__(*args, **kwargs)
		self.gui_cameras_alignment = gui_cameras_alignment

	def closeEvent(self, event):
		"""
		Override the close event to stop any background activity and perform additional cleanup if needed.

		Args:
		    event: The close event.
		"""
		self.gui_cameras_alignment.stop()  # Call the stop method to stop any background activity
		self.closed.emit()  # Emit the custom closed signal
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
	Cameras_Alignment = QtWidgets.QWidget()
	signal_emitter = SignalEmitter()
	ui = Ui_Cameras_Alignment(variables, conf, signal_emitter)
	ui.setupUi(Cameras_Alignment)
	Cameras_Alignment.show()
	sys.exit(app.exec())
