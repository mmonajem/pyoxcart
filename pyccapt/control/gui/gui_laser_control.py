import multiprocessing
import os
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap

# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files


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
        Laser_Control.resize(936, 345)
        self.gridLayout_5 = QtWidgets.QGridLayout(Laser_Control)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtWidgets.QLabel(Laser_Control)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.laser_wavelegnth = QtWidgets.QComboBox(Laser_Control)
        self.laser_wavelegnth.setStyleSheet("QComboBox{background: rgb(223,223,233)}")
        self.laser_wavelegnth.setObjectName("laser_wavelegnth")
        self.laser_wavelegnth.addItem("")
        self.laser_wavelegnth.addItem("")
        self.laser_wavelegnth.addItem("")
        self.gridLayout_3.addWidget(self.laser_wavelegnth, 0, 1, 1, 1)
        self.laser_enable = QtWidgets.QPushButton(Laser_Control)
        self.laser_enable.setMinimumSize(QtCore.QSize(90, 25))
        self.laser_enable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.laser_enable.setStyleSheet("")
        self.laser_enable.setObjectName("laser_enable")
        self.gridLayout_3.addWidget(self.laser_enable, 0, 2, 1, 1)
        self.led_laser_enable = QtWidgets.QLabel(Laser_Control)
        self.led_laser_enable.setObjectName("led_laser_enable")
        self.gridLayout_3.addWidget(self.led_laser_enable, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(Laser_Control)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.laser_power = QtWidgets.QComboBox(Laser_Control)
        self.laser_power.setStyleSheet("QComboBox{background: rgb(223,223,233)}")
        self.laser_power.setObjectName("laser_power")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.laser_power.addItem("")
        self.gridLayout_3.addWidget(self.laser_power, 1, 1, 1, 1)
        self.laser_on = QtWidgets.QPushButton(Laser_Control)
        self.laser_on.setMinimumSize(QtCore.QSize(90, 25))
        self.laser_on.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.laser_on.setStyleSheet("")
        self.laser_on.setObjectName("laser_on")
        self.gridLayout_3.addWidget(self.laser_on, 1, 2, 1, 1)
        self.led_laser_on = QtWidgets.QLabel(Laser_Control)
        self.led_laser_on.setObjectName("led_laser_on")
        self.gridLayout_3.addWidget(self.led_laser_on, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(Laser_Control)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 2, 0, 1, 1)
        self.laser_rate = QtWidgets.QComboBox(Laser_Control)
        self.laser_rate.setStyleSheet("QComboBox{background: rgb(223,223,233)}")
        self.laser_rate.setObjectName("laser_rate")
        self.laser_rate.addItem("")
        self.laser_rate.addItem("")
        self.laser_rate.addItem("")
        self.laser_rate.addItem("")
        self.laser_rate.addItem("")
        self.laser_rate.addItem("")
        self.laser_rate.addItem("")
        self.gridLayout_3.addWidget(self.laser_rate, 2, 1, 1, 1)
        self.laser_standby = QtWidgets.QPushButton(Laser_Control)
        self.laser_standby.setMinimumSize(QtCore.QSize(90, 25))
        self.laser_standby.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.laser_standby.setStyleSheet("")
        self.laser_standby.setObjectName("laser_standby")
        self.gridLayout_3.addWidget(self.laser_standby, 2, 2, 1, 1)
        self.led_laser_laser_standby = QtWidgets.QLabel(Laser_Control)
        self.led_laser_laser_standby.setObjectName("led_laser_laser_standby")
        self.gridLayout_3.addWidget(self.led_laser_laser_standby, 2, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(Laser_Control)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 3, 0, 1, 1)
        self.laser_divition_factor = QtWidgets.QComboBox(Laser_Control)
        self.laser_divition_factor.setStyleSheet("QComboBox{background: rgb(223,223,233)}")
        self.laser_divition_factor.setObjectName("laser_divition_factor")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.laser_divition_factor.addItem("")
        self.gridLayout_3.addWidget(self.laser_divition_factor, 3, 1, 1, 1)
        self.laser_listen = QtWidgets.QPushButton(Laser_Control)
        self.laser_listen.setMinimumSize(QtCore.QSize(90, 25))
        self.laser_listen.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.laser_listen.setStyleSheet("")
        self.laser_listen.setObjectName("laser_listen")
        self.gridLayout_3.addWidget(self.laser_listen, 3, 2, 1, 1)
        self.led_laser_listen = QtWidgets.QLabel(Laser_Control)
        self.led_laser_listen.setObjectName("led_laser_listen")
        self.gridLayout_3.addWidget(self.led_laser_listen, 3, 3, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 2, 3)
        self.label_12 = QtWidgets.QLabel(Laser_Control)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 0, 4, 1, 1)
        self.laser_scan_mode5 = QtWidgets.QComboBox(Laser_Control)
        self.laser_scan_mode5.setStyleSheet("QComboBox{background: rgb(223,223,233)}")
        self.laser_scan_mode5.setObjectName("laser_scan_mode5")
        self.laser_scan_mode5.addItem("")
        self.gridLayout_4.addWidget(self.laser_scan_mode5, 0, 5, 1, 1)
        self.scanning_disp = QtWidgets.QGraphicsView(Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.scanning_disp.sizePolicy().hasHeightForWidth())
        self.scanning_disp.setSizePolicy(sizePolicy)
        self.scanning_disp.setMinimumSize(QtCore.QSize(250, 250))
        self.scanning_disp.setStyleSheet("QWidget{\n"
                                         "                                            border: 0.5px solid gray;\n"
                                         "                                            }\n"
                                         "                                        ")
        self.scanning_disp.setObjectName("scanning_disp")
        self.gridLayout_4.addWidget(self.scanning_disp, 0, 6, 4, 1)
        self.label_13 = QtWidgets.QLabel(Laser_Control)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 1, 4, 1, 1)
        self.laser_focus_mode = QtWidgets.QComboBox(Laser_Control)
        self.laser_focus_mode.setStyleSheet("QComboBox{background: rgb(223,223,233)}")
        self.laser_focus_mode.setObjectName("laser_focus_mode")
        self.laser_focus_mode.addItem("")
        self.gridLayout_4.addWidget(self.laser_focus_mode, 1, 5, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_9 = QtWidgets.QLabel(Laser_Control)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        self.laser_power_disp = QtWidgets.QLCDNumber(Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_power_disp.sizePolicy().hasHeightForWidth())
        self.laser_power_disp.setSizePolicy(sizePolicy)
        self.laser_power_disp.setMinimumSize(QtCore.QSize(100, 50))
        self.laser_power_disp.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.laser_power_disp.setFont(font)
        self.laser_power_disp.setStyleSheet("QLCDNumber{\n"
                                            "                                                            border: 2px solid green;\n"
                                            "                                            border-radius: 10px;\n"
                                            "                                            padding: 0 8px;\n"
                                            "                                            }\n"
                                            "                                        ")
        self.laser_power_disp.setObjectName("laser_power_disp")
        self.horizontalLayout.addWidget(self.laser_power_disp)
        self.label_10 = QtWidgets.QLabel(Laser_Control)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout.addWidget(self.label_10)
        self.laser_pulse_energy_disp = QtWidgets.QLCDNumber(Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_pulse_energy_disp.sizePolicy().hasHeightForWidth())
        self.laser_pulse_energy_disp.setSizePolicy(sizePolicy)
        self.laser_pulse_energy_disp.setMinimumSize(QtCore.QSize(100, 50))
        self.laser_pulse_energy_disp.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.laser_pulse_energy_disp.setFont(font)
        self.laser_pulse_energy_disp.setStyleSheet("QLCDNumber{\n"
                                                   "                                                            border: 2px solid green;\n"
                                                   "                                            border-radius: 10px;\n"
                                                   "                                            padding: 0 8px;\n"
                                                   "                                            }\n"
                                                   "                                        ")
        self.laser_pulse_energy_disp.setObjectName("laser_pulse_energy_disp")
        self.horizontalLayout.addWidget(self.laser_pulse_energy_disp)
        self.label_11 = QtWidgets.QLabel(Laser_Control)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout.addWidget(self.label_11)
        self.laser_repetion_rate_disp = QtWidgets.QLCDNumber(Laser_Control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_repetion_rate_disp.sizePolicy().hasHeightForWidth())
        self.laser_repetion_rate_disp.setSizePolicy(sizePolicy)
        self.laser_repetion_rate_disp.setMinimumSize(QtCore.QSize(100, 50))
        self.laser_repetion_rate_disp.setMaximumSize(QtCore.QSize(100, 50))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.laser_repetion_rate_disp.setFont(font)
        self.laser_repetion_rate_disp.setStyleSheet("QLCDNumber{\n"
                                                    "                                                            border: 2px solid green;\n"
                                                    "                                            border-radius: 10px;\n"
                                                    "                                            padding: 0 8px;\n"
                                                    "                                            }\n"
                                                    "                                        ")
        self.laser_repetion_rate_disp.setObjectName("laser_repetion_rate_disp")
        self.horizontalLayout.addWidget(self.laser_repetion_rate_disp)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_4.addLayout(self.horizontalLayout, 2, 0, 1, 6)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_14 = QtWidgets.QLabel(Laser_Control)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 0, 0, 1, 1)
        self.laser_speed_lr = QtWidgets.QDoubleSpinBox(Laser_Control)
        self.laser_speed_lr.setStyleSheet("QDoubleSpinBox{\n"
                                          "                                                background: rgb(223,223,233)\n"
                                          "                                                }\n"
                                          "                                            ")
        self.laser_speed_lr.setObjectName("laser_speed_lr")
        self.gridLayout_2.addWidget(self.laser_speed_lr, 0, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(Laser_Control)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 1, 0, 1, 1)
        self.laser_speed_ud = QtWidgets.QDoubleSpinBox(Laser_Control)
        self.laser_speed_ud.setStyleSheet("QDoubleSpinBox{\n"
                                          "                                                background: rgb(223,223,233)\n"
                                          "                                                }\n"
                                          "                                            ")
        self.laser_speed_ud.setObjectName("laser_speed_ud")
        self.gridLayout_2.addWidget(self.laser_speed_ud, 1, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(Laser_Control)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 2, 0, 1, 1)
        self.laser_speed_fb = QtWidgets.QDoubleSpinBox(Laser_Control)
        self.laser_speed_fb.setStyleSheet("QDoubleSpinBox{\n"
                                          "                                                background: rgb(223,223,233)\n"
                                          "                                                }\n"
                                          "                                            ")
        self.laser_speed_fb.setObjectName("laser_speed_fb")
        self.gridLayout_2.addWidget(self.laser_speed_fb, 2, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 1)
        self.laser_up = QtWidgets.QPushButton(Laser_Control)
        self.laser_up.setMinimumSize(QtCore.QSize(50, 25))
        self.laser_up.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.laser_up.setStyleSheet("")
        self.laser_up.setObjectName("laser_up")
        self.gridLayout.addWidget(self.laser_up, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 2, 1, 1)
        self.laser_left = QtWidgets.QPushButton(Laser_Control)
        self.laser_left.setMinimumSize(QtCore.QSize(50, 25))
        self.laser_left.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.laser_left.setStyleSheet("")
        self.laser_left.setObjectName("laser_left")
        self.gridLayout.addWidget(self.laser_left, 1, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem4, 1, 1, 1, 1)
        self.leser_right = QtWidgets.QPushButton(Laser_Control)
        self.leser_right.setMinimumSize(QtCore.QSize(50, 25))
        self.leser_right.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.leser_right.setStyleSheet("")
        self.leser_right.setObjectName("leser_right")
        self.gridLayout.addWidget(self.leser_right, 1, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem5, 2, 0, 1, 1)
        self.laser_down = QtWidgets.QPushButton(Laser_Control)
        self.laser_down.setMinimumSize(QtCore.QSize(50, 25))
        self.laser_down.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.laser_down.setStyleSheet("")
        self.laser_down.setObjectName("laser_down")
        self.gridLayout.addWidget(self.laser_down, 2, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem6, 2, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 3, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.laser_forward = QtWidgets.QPushButton(Laser_Control)
        self.laser_forward.setStyleSheet("")
        self.laser_forward.setObjectName("laser_forward")
        self.verticalLayout.addWidget(self.laser_forward)
        spacerItem7 = QtWidgets.QSpacerItem(17, 24, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem7)
        self.laser_backward = QtWidgets.QPushButton(Laser_Control)
        self.laser_backward.setStyleSheet("")
        self.laser_backward.setObjectName("laser_backward")
        self.verticalLayout.addWidget(self.laser_backward)
        self.gridLayout_4.addLayout(self.verticalLayout, 3, 2, 1, 1)
        self.laser_home = QtWidgets.QPushButton(Laser_Control)
        self.laser_home.setStyleSheet("")
        self.laser_home.setObjectName("laser_home")
        self.gridLayout_4.addWidget(self.laser_home, 3, 3, 1, 1)
        self.Error = QtWidgets.QLabel(Laser_Control)
        self.Error.setMinimumSize(QtCore.QSize(500, 30))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setStrikeOut(False)
        self.Error.setFont(font)
        self.Error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Error.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.Error.setObjectName("Error")
        self.gridLayout_4.addWidget(self.Error, 4, 0, 1, 4)
        self.start_scanning = QtWidgets.QPushButton(Laser_Control)
        self.start_scanning.setStyleSheet("QPushButton{background: rgb(193, 193, 193)}\n"
                                          "                                            ")
        self.start_scanning.setObjectName("start_scanning")
        self.gridLayout_4.addWidget(self.start_scanning, 4, 6, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)

        self.retranslateUi(Laser_Control)
        QtCore.QMetaObject.connectSlotsByName(Laser_Control)
        Laser_Control.setTabOrder(self.laser_wavelegnth, self.laser_power)
        Laser_Control.setTabOrder(self.laser_power, self.laser_rate)
        Laser_Control.setTabOrder(self.laser_rate, self.laser_divition_factor)
        Laser_Control.setTabOrder(self.laser_divition_factor, self.laser_enable)
        Laser_Control.setTabOrder(self.laser_enable, self.laser_on)
        Laser_Control.setTabOrder(self.laser_on, self.laser_standby)
        Laser_Control.setTabOrder(self.laser_standby, self.laser_listen)
        Laser_Control.setTabOrder(self.laser_listen, self.laser_scan_mode5)
        Laser_Control.setTabOrder(self.laser_scan_mode5, self.laser_focus_mode)
        Laser_Control.setTabOrder(self.laser_focus_mode, self.laser_speed_lr)
        Laser_Control.setTabOrder(self.laser_speed_lr, self.laser_speed_ud)
        Laser_Control.setTabOrder(self.laser_speed_ud, self.laser_speed_fb)
        Laser_Control.setTabOrder(self.laser_speed_fb, self.laser_left)
        Laser_Control.setTabOrder(self.laser_left, self.laser_up)
        Laser_Control.setTabOrder(self.laser_up, self.leser_right)
        Laser_Control.setTabOrder(self.leser_right, self.laser_down)
        Laser_Control.setTabOrder(self.laser_down, self.laser_forward)
        Laser_Control.setTabOrder(self.laser_forward, self.laser_backward)
        Laser_Control.setTabOrder(self.laser_backward, self.laser_home)
        Laser_Control.setTabOrder(self.laser_home, self.start_scanning)
        Laser_Control.setTabOrder(self.start_scanning, self.scanning_disp)

        self.led_red = QPixmap('./files/led-red-on.png')
        self.led_green = QPixmap('./files/green-led-on.png')
        self.led_laser_laser_standby.setPixmap(self.led_red)
        self.led_laser_on.setPixmap(self.led_red)
        self.led_laser_enable.setPixmap(self.led_red)
        self.led_laser_listen.setPixmap(self.led_red)

    def retranslateUi(self, Laser_Control):
        _translate = QtCore.QCoreApplication.translate
        ###
        # Laser_Control.setWindowTitle(_translate("Laser_Control", "Form"))
        Laser_Control.setWindowTitle(_translate("Laser_Control", "PyCCAPT Laser Control"))
        Laser_Control.setWindowIcon(QtGui.QIcon('./files/logo.png'))
        ###
        Laser_Control.setToolTip(_translate("Laser_Control", "<html><head/><body><p>1</p></body></html>"))
        self.label_4.setText(_translate("Laser_Control", "Wavelength"))
        self.laser_wavelegnth.setItemText(0, _translate("Laser_Control", "IR"))
        self.laser_wavelegnth.setItemText(1, _translate("Laser_Control", "Green"))
        self.laser_wavelegnth.setItemText(2, _translate("Laser_Control", "DUV"))
        self.laser_enable.setText(_translate("Laser_Control", "Output Enable"))
        self.led_laser_enable.setText(_translate("Laser_Control", "Output enable"))
        self.label.setText(_translate("Laser_Control", "Power control"))
        self.laser_power.setItemText(0, _translate("Laser_Control", "0.00"))
        self.laser_power.setItemText(1, _translate("Laser_Control", "0.25"))
        self.laser_power.setItemText(2, _translate("Laser_Control", "0.50"))
        self.laser_power.setItemText(3, _translate("Laser_Control", "0.74"))
        self.laser_power.setItemText(4, _translate("Laser_Control", "0.99"))
        self.laser_power.setItemText(5, _translate("Laser_Control", "1.24"))
        self.laser_power.setItemText(6, _translate("Laser_Control", "1.49"))
        self.laser_power.setItemText(7, _translate("Laser_Control", "1.73"))
        self.laser_power.setItemText(8, _translate("Laser_Control", "1.98"))
        self.laser_power.setItemText(9, _translate("Laser_Control", "2.23"))
        self.laser_power.setItemText(10, _translate("Laser_Control", "2.48"))
        self.laser_power.setItemText(11, _translate("Laser_Control", "2.72"))
        self.laser_power.setItemText(12, _translate("Laser_Control", "2.97"))
        self.laser_power.setItemText(13, _translate("Laser_Control", "3.22"))
        self.laser_power.setItemText(14, _translate("Laser_Control", "3.47"))
        self.laser_power.setItemText(15, _translate("Laser_Control", "3.71"))
        self.laser_power.setItemText(16, _translate("Laser_Control", "3.96"))
        self.laser_power.setItemText(17, _translate("Laser_Control", "4.21"))
        self.laser_power.setItemText(18, _translate("Laser_Control", "4.46"))
        self.laser_power.setItemText(19, _translate("Laser_Control", "4.70"))
        self.laser_power.setItemText(20, _translate("Laser_Control", "4.95"))
        self.laser_power.setItemText(21, _translate("Laser_Control", "5.20"))
        self.laser_on.setText(_translate("Laser_Control", "Laser on"))
        self.led_laser_on.setText(_translate("Laser_Control", "Laser on"))
        self.label_2.setText(_translate("Laser_Control", "Repetion rate"))
        self.laser_rate.setItemText(0, _translate("Laser_Control", "400"))
        self.laser_rate.setItemText(1, _translate("Laser_Control", "500"))
        self.laser_rate.setItemText(2, _translate("Laser_Control", "580"))
        self.laser_rate.setItemText(3, _translate("Laser_Control", "721"))
        self.laser_rate.setItemText(4, _translate("Laser_Control", "800"))
        self.laser_rate.setItemText(5, _translate("Laser_Control", "899"))
        self.laser_rate.setItemText(6, _translate("Laser_Control", "1000"))
        self.laser_standby.setText(_translate("Laser_Control", "Standby"))
        self.led_laser_laser_standby.setText(_translate("Laser_Control", "Standby"))
        self.label_3.setText(_translate("Laser_Control", "Divition Factor"))
        self.laser_divition_factor.setItemText(0, _translate("Laser_Control", "1.0"))
        self.laser_divition_factor.setItemText(1, _translate("Laser_Control", "1.8"))
        self.laser_divition_factor.setItemText(2, _translate("Laser_Control", "3.2"))
        self.laser_divition_factor.setItemText(3, _translate("Laser_Control", "5.6"))
        self.laser_divition_factor.setItemText(4, _translate("Laser_Control", "10"))
        self.laser_divition_factor.setItemText(5, _translate("Laser_Control", "18"))
        self.laser_divition_factor.setItemText(6, _translate("Laser_Control", "32"))
        self.laser_divition_factor.setItemText(7, _translate("Laser_Control", "56"))
        self.laser_divition_factor.setItemText(8, _translate("Laser_Control", "100"))
        self.laser_divition_factor.setItemText(9, _translate("Laser_Control", "180"))
        self.laser_divition_factor.setItemText(10, _translate("Laser_Control", "320"))
        self.laser_divition_factor.setItemText(11, _translate("Laser_Control", "560"))
        self.laser_divition_factor.setItemText(12, _translate("Laser_Control", "1000"))
        self.laser_divition_factor.setItemText(13, _translate("Laser_Control", "1800"))
        self.laser_divition_factor.setItemText(14, _translate("Laser_Control", "3200"))
        self.laser_divition_factor.setItemText(15, _translate("Laser_Control", "5600"))
        self.laser_divition_factor.setItemText(16, _translate("Laser_Control", "10000"))
        self.laser_divition_factor.setItemText(17, _translate("Laser_Control", "18000"))
        self.laser_divition_factor.setItemText(18, _translate("Laser_Control", "32000"))
        self.laser_divition_factor.setItemText(19, _translate("Laser_Control", "56000"))
        self.laser_divition_factor.setItemText(20, _translate("Laser_Control", "100000"))
        self.laser_divition_factor.setItemText(21, _translate("Laser_Control", "180000"))
        self.laser_divition_factor.setItemText(22, _translate("Laser_Control", "320000"))
        self.laser_divition_factor.setItemText(23, _translate("Laser_Control", "560000"))
        self.laser_divition_factor.setItemText(24, _translate("Laser_Control", "1000000"))
        self.laser_listen.setText(_translate("Laser_Control", "Listen"))
        self.led_laser_listen.setText(_translate("Laser_Control", "Listen"))
        self.label_12.setText(_translate("Laser_Control", "Scan mode"))
        self.laser_scan_mode5.setItemText(0, _translate("Laser_Control", "Standard"))
        self.label_13.setText(_translate("Laser_Control", "Focus mode"))
        self.laser_focus_mode.setItemText(0, _translate("Laser_Control", "Standard"))
        self.label_9.setText(_translate("Laser_Control", "Laser power"))
        self.label_10.setText(_translate("Laser_Control", "Pulse energy"))
        self.label_11.setText(_translate("Laser_Control", "Repetirion rate"))
        self.label_14.setText(_translate("Laser_Control", "Speed L/R"))
        self.label_15.setText(_translate("Laser_Control", "Speed  U/D"))
        self.label_16.setText(_translate("Laser_Control", "Speed  F/B"))
        self.laser_up.setText(_translate("Laser_Control", "up"))
        self.laser_left.setText(_translate("Laser_Control", "Left"))
        self.leser_right.setText(_translate("Laser_Control", "Right"))
        self.laser_down.setText(_translate("Laser_Control", "Down"))
        self.laser_forward.setText(_translate("Laser_Control", "Forward"))
        self.laser_backward.setText(_translate("Laser_Control", "Backward"))
        self.laser_home.setText(_translate("Laser_Control", "Home"))
        self.Error.setText(_translate("Laser_Control", "<html><head/><body><p><br/></p></body></html>"))
        self.start_scanning.setText(_translate("Laser_Control", "Start scaning"))

    def disable_button_for_10_seconds(self):
        """
        Handle the close event of the GatesWindow.

        Args:
            None

        Return:
            None
        """
        pass

    def stop(self):
        """
        Handle the close event of the GatesWindow.

        Args:
            None

        Return:
            None
        """
        # Stop any background processes, timers, or threads here
        pass

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
    ns = manager.Namespace()
    variables = share_variables.Variables(conf, ns)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    Laser_Control = QtWidgets.QWidget()
    ui = Ui_Laser_Control(variables, conf)
    ui.setupUi(Laser_Control)
    Laser_Control.show()
    sys.exit(app.exec())

