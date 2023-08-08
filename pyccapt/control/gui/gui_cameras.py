import os
import sys
import threading

import pyqtgraph as pg
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap, QImage
from pypylon import pylon

# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files
from pyccapt.control.devices.camera import Camera


class Ui_Cameras_Alignment(object):

    def __init__(self, variables, conf, camera):
        self.camera = camera
        self.conf = conf
        self.variables = variables

    def setupUi(self, Cameras_Alignment):
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
        self.cam_s_d = QtWidgets.QLabel(parent=Cameras_Alignment)
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
        self.cam_s_d.setText("")
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
        self.cam_b_d = QtWidgets.QLabel(parent=Cameras_Alignment)
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
        self.cam_b_d.setText("")
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
        # timer cameras
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(200)
        self.timer1.timeout.connect(self.update_cameras)
        self.timer1.start()
        # Diagram and LEDs ##############
        self.led_red = QPixmap('./files/led-red-on.png')
        self.led_green = QPixmap('./files/green-led-on.png')
        self.led_light.setPixmap(self.led_red)

        # bottom camera (x, y)
        arrow1 = pg.ArrowItem(pos=(650, 670), angle=-90)
        # arrow2 = pg.ArrowItem(pos=(100, 2100), angle=90)
        arrow3 = pg.ArrowItem(pos=(940, 770), angle=0)
        self.cam_b_o.addItem(arrow1)
        # self.cam_b_o.addItem(arrow2)
        self.cam_b_o.addItem(arrow3)
        # Side camera (x, y)
        arrow1 = pg.ArrowItem(pos=(450, 550), angle=-90)
        arrow2 = pg.ArrowItem(pos=(450, 1500), angle=90)
        # arrow3 = pg.ArrowItem(pos=(890, 1100), angle=0)
        self.cam_s_o.addItem(arrow1)
        self.cam_s_o.addItem(arrow2)
        # self.cam_s_o.addItem(arrow3)
        ###
        self.light.clicked.connect(self.light_switch)
        self.win_alignment.clicked.connect(self.win_alignment_switch)

    def retranslateUi(self, Cameras_alignment):
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

    def light_switch(self):
        """
        The function for switching the exposure time of cameras in case of swithching the light
        """
        if not self.variables.light:
            self.led_light.setPixmap(self.led_green)
            self.camera.light_switch()
            self.timer1.setInterval(200)
            self.variables.light = True

            self.variables.light_swich = True
        elif self.variables.light:
            self.led_light.setPixmap(self.led_red)
            self.camera.light_switch()
            self.timer1.setInterval(200)
            self.variables.light = False
            self.variables.light_swich = False

    def win_alignment_switch(self):
        if not self.variables.alignment_window:
            self.variables.alignment_window = True
            self.win_alignment.setStyleSheet("QPushButton{\n"
                                             "background: rgb(0, 255, 26)\n"
                                             "}")
        elif self.variables.alignment_window:
            self.variables.alignment_window = False
            self.win_alignment.setStyleSheet("QPushButton{\n"
                                             "background: rgb(193, 193, 193)\n"
                                             "}")

    def update_cameras(self, ):
        """
                The function for updating cameras in the GUI
                """
        self.cam_s_o.setImage(self.variables.img0_orig, autoRange=False)
        self.cam_b_o.setImage(self.variables.img1_orig, autoRange=False)

        self.camera0_zoom = QImage(self.variables.img0_zoom, 1200, 500, QImage.Format.Format_RGB888)
        self.camera1_zoom = QImage(self.variables.img1_zoom, 1200, 500, QImage.Format.Format_RGB888)

        self.camera0_zoom = QtGui.QPixmap(self.camera0_zoom)
        self.camera1_zoom = QtGui.QPixmap(self.camera1_zoom)

        self.cam_s_d.setPixmap(self.camera0_zoom)
        self.cam_b_d.setPixmap(self.camera1_zoom)

    def stop(self):
        # Stop the timer and any other background processes, timers, or threads here
        self.timer1.stop()
        # Add any additional cleanup code here


class CamerasAlignmentWindow(QtWidgets.QWidget):
    def __init__(self, gui_cameras_alignment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui_cameras_alignment = gui_cameras_alignment

    def closeEvent(self, event):
        self.gui_cameras_alignment.stop()  # Call the stop method to stop any background activity
        # Additional cleanup code here if needed
        super().closeEvent(event)


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
    # Initialize global experiment variables
    variables = share_variables.Variables(conf)
    variables.log_path = p
    if conf['log'] == 'on':
        variables.log = True

    if conf['camera'] == "off":
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

            camera = Camera(devices, tlFactory, cameras, converter, variables)

            # Thread for reading cameras
            camera_thread = threading.Thread(target=camera.update_cameras)
            camera_thread.setDaemon(True)
            camera_thread.start()

        except Exception as e:
            print('Can not initialize the Cameras')
            print(e)
            camera = None

    app = QtWidgets.QApplication(sys.argv)
    Cameras_Alignment = QtWidgets.QWidget()
    ui = Ui_Cameras_Alignment(variables, conf, camera)
    ui.setupUi(Cameras_Alignment)
    Cameras_Alignment.show()
    sys.exit(app.exec())
