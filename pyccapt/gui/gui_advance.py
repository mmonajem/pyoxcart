"""
This is the main script of main GUI of the OXCART Atom Probe.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""

import numpy as np
import nidaqmx
import time
import threading
import datetime
import os
# PyQt and PyQtgraph libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QScreen, QPixmap, QImage
import pyqtgraph as pg
import pyqtgraph.exporters

# Local module and scripts
from pyccapt.apt import apt_tdc_surface_consept
from pyccapt.tools import variables
from pyccapt.tools import tof2mc_simple
from pyccapt.devices.camera import Camera
from pyccapt.devices import initialize_devices
from pyccapt.tools.module_dir import MODULE_DIR


class UI_APT_A(Camera, object):
    """
    The GUI class of voltage mode (oxcart)
    """

    def __init__(self, devices, tlFactory, cameras, converter, lock, app, conf):
        if conf['camera'] == "on":
            super().__init__(devices, tlFactory, cameras, converter)  # Cameras variables and converter
        self.lock = lock  # Lock for thread ...
        self.app = app
        self.conf = conf

    def setupUi(self, UI_APT_A):
        UI_APT_A.setObjectName("UI_APT_A")
        UI_APT_A.resize(3462, 1869)
        self.centralwidget = QtWidgets.QWidget(UI_APT_A)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_9.setObjectName("gridLayout_9")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem, 2, 0, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_17 = QtWidgets.QGridLayout()
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.led_pump_load_lock = QtWidgets.QLabel(self.centralwidget)
        self.led_pump_load_lock.setAlignment(QtCore.Qt.AlignCenter)
        self.led_pump_load_lock.setObjectName("led_pump_load_lock")
        self.gridLayout_6.addWidget(self.led_pump_load_lock, 1, 0, 2, 1)
        self.pump_load_lock_switch = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pump_load_lock_switch.sizePolicy().hasHeightForWidth())
        self.pump_load_lock_switch.setSizePolicy(sizePolicy)
        self.pump_load_lock_switch.setStyleSheet("QPushButton{\n"
                                                 "background: rgb(193, 193, 193)\n"
                                                 "}")
        self.pump_load_lock_switch.setObjectName("pump_load_lock_switch")
        self.gridLayout_6.addWidget(self.pump_load_lock_switch, 3, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                            QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem1, 0, 0, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_6, 0, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.label_35 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_35.setFont(font)
        self.label_35.setObjectName("label_35")
        self.gridLayout_16.addWidget(self.label_35, 0, 4, 1, 1)
        self.label_39 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_39.setFont(font)
        self.label_39.setObjectName("label_39")
        self.gridLayout_16.addWidget(self.label_39, 1, 0, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_40.setFont(font)
        self.label_40.setObjectName("label_40")
        self.gridLayout_16.addWidget(self.label_40, 1, 2, 1, 1)
        self.vacuum_buffer_back = QtWidgets.QLCDNumber(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vacuum_buffer_back.sizePolicy().hasHeightForWidth())
        self.vacuum_buffer_back.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.vacuum_buffer_back.setFont(font)
        self.vacuum_buffer_back.setStyleSheet("QLCDNumber{\n"
"border: 2px solid blue;\n"
"border-radius: 10px;\n"
"padding: 0 8px;\n"
"}")
        self.vacuum_buffer_back.setObjectName("vacuum_buffer_back")
        self.gridLayout_16.addWidget(self.vacuum_buffer_back, 1, 3, 1, 1)
        self.label_38 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.gridLayout_16.addWidget(self.label_38, 1, 4, 1, 1)
        self.vacuum_buffer = QtWidgets.QLCDNumber(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vacuum_buffer.sizePolicy().hasHeightForWidth())
        self.vacuum_buffer.setSizePolicy(sizePolicy)
        self.vacuum_buffer.setMinimumSize(QtCore.QSize(230, 100))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.vacuum_buffer.setFont(font)
        self.vacuum_buffer.setStyleSheet("QLCDNumber{\n"
"border: 2px solid blue;\n"
"border-radius: 10px;\n"
"padding: 0 8px;\n"
"}")
        self.vacuum_buffer.setObjectName("vacuum_buffer")
        self.gridLayout_16.addWidget(self.vacuum_buffer, 0, 3, 1, 1)
        self.vacuum_main = QtWidgets.QLCDNumber(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vacuum_main.sizePolicy().hasHeightForWidth())
        self.vacuum_main.setSizePolicy(sizePolicy)
        self.vacuum_main.setMinimumSize(QtCore.QSize(230, 100))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.vacuum_main.setFont(font)
        self.vacuum_main.setStyleSheet("QLCDNumber{\n"
"border: 2px solid green;\n"
"border-radius: 10px;\n"
"padding: 0 8px;\n"
"}")
        self.vacuum_main.setObjectName("vacuum_main")
        self.gridLayout_16.addWidget(self.vacuum_main, 0, 5, 1, 1)
        self.vacuum_load_lock = QtWidgets.QLCDNumber(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vacuum_load_lock.sizePolicy().hasHeightForWidth())
        self.vacuum_load_lock.setSizePolicy(sizePolicy)
        self.vacuum_load_lock.setMinimumSize(QtCore.QSize(230, 100))
        self.vacuum_load_lock.setStyleSheet("QLCDNumber{\n"
"border: 2px solid yellow;\n"
"border-radius: 10px;\n"
"padding: 0 8px;\n"
"}")
        self.vacuum_load_lock.setObjectName("vacuum_load_lock")
        self.gridLayout_16.addWidget(self.vacuum_load_lock, 0, 1, 1, 1)
        self.vacuum_load_lock_back = QtWidgets.QLCDNumber(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vacuum_load_lock_back.sizePolicy().hasHeightForWidth())
        self.vacuum_load_lock_back.setSizePolicy(sizePolicy)
        self.vacuum_load_lock_back.setStyleSheet("QLCDNumber{\n"
"border: 2px solid yellow;\n"
"border-radius: 10px;\n"
"padding: 0 8px;\n"
"}")
        self.vacuum_load_lock_back.setObjectName("vacuum_load_lock_back")
        self.gridLayout_16.addWidget(self.vacuum_load_lock_back, 1, 1, 1, 1)
        self.label_36 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.gridLayout_16.addWidget(self.label_36, 0, 2, 1, 1)
        self.label_37 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setObjectName("label_37")
        self.gridLayout_16.addWidget(self.label_37, 0, 0, 1, 1)
        self.temp = QtWidgets.QLCDNumber(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.temp.sizePolicy().hasHeightForWidth())
        self.temp.setSizePolicy(sizePolicy)
        self.temp.setMinimumSize(QtCore.QSize(230, 100))
        self.temp.setStyleSheet("QLCDNumber{\n"
"border: 2px solid brown;\n"
"border-radius: 10px;\n"
"padding: 0 8px;\n"
"}")
        self.temp.setObjectName("temp")
        self.gridLayout_16.addWidget(self.temp, 1, 5, 1, 1)
        self.horizontalLayout_8.addLayout(self.gridLayout_16)
        # self.temperature = QtWidgets.QGraphicsView(self.centralwidget)
        self.temperature = pg.PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.temperature.sizePolicy().hasHeightForWidth())
        self.temperature.setSizePolicy(sizePolicy)
        self.temperature.setMinimumSize(QtCore.QSize(400, 400))
        self.temperature.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 4 4px;\n"
"}")
        self.temperature.setObjectName("temperature")
        self.horizontalLayout_8.addWidget(self.temperature)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy)
        self.start_button.setStyleSheet("QPushButton{\n"
"background: rgb(193, 193, 193)\n"
"}")
        self.start_button.setObjectName("start_button")
        self.gridLayout_2.addWidget(self.start_button, 0, 0, 1, 1)
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy)
        self.stop_button.setStyleSheet("QPushButton{\n"
"background: rgb(193, 193, 193)\n"
"}")
        self.stop_button.setObjectName("stop_button")
        self.gridLayout_2.addWidget(self.stop_button, 1, 0, 1, 1)
        self.horizontalLayout_7.addLayout(self.gridLayout_2)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_7)
        self.gridLayout_17.addLayout(self.horizontalLayout_8, 0, 1, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_17, 2, 1, 1, 2)
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.led_main_chamber = QtWidgets.QLabel(self.centralwidget)
        self.led_main_chamber.setAlignment(QtCore.Qt.AlignCenter)
        self.led_main_chamber.setObjectName("led_main_chamber")
        self.gridLayout.addWidget(self.led_main_chamber, 0, 0, 1, 1)
        self.led_load_lock = QtWidgets.QLabel(self.centralwidget)
        self.led_load_lock.setAlignment(QtCore.Qt.AlignCenter)
        self.led_load_lock.setObjectName("led_load_lock")
        self.gridLayout.addWidget(self.led_load_lock, 0, 1, 1, 1)
        self.led_cryo = QtWidgets.QLabel(self.centralwidget)
        self.led_cryo.setAlignment(QtCore.Qt.AlignCenter)
        self.led_cryo.setObjectName("led_cryo")
        self.gridLayout.addWidget(self.led_cryo, 0, 2, 1, 1)
        self.main_chamber_switch = QtWidgets.QPushButton(self.centralwidget)
        self.main_chamber_switch.setStyleSheet("QPushButton{\n"
"background: rgb(193, 193, 193)\n"
"}")
        self.main_chamber_switch.setObjectName("main_chamber_switch")
        self.gridLayout.addWidget(self.main_chamber_switch, 1, 0, 1, 1)
        self.load_lock_switch = QtWidgets.QPushButton(self.centralwidget)
        self.load_lock_switch.setStyleSheet("QPushButton{\n"
"background: rgb(193, 193, 193)\n"
"}")
        self.load_lock_switch.setObjectName("load_lock_switch")
        self.gridLayout.addWidget(self.load_lock_switch, 1, 1, 1, 1)
        self.cryo_switch = QtWidgets.QPushButton(self.centralwidget)
        self.cryo_switch.setStyleSheet("QPushButton{\n"
"background: rgb(193, 193, 193)\n"
"}")
        self.cryo_switch.setObjectName("cryo_switch")
        self.gridLayout.addWidget(self.cryo_switch, 1, 2, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)
        self.speciemen_voltage = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speciemen_voltage.sizePolicy().hasHeightForWidth())
        self.speciemen_voltage.setSizePolicy(sizePolicy)
        self.speciemen_voltage.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.speciemen_voltage.setText("")
        self.speciemen_voltage.setObjectName("speciemen_voltage")
        self.gridLayout_4.addWidget(self.speciemen_voltage, 3, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 4, 0, 1, 1)
        self.pulse_voltage = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pulse_voltage.sizePolicy().hasHeightForWidth())
        self.pulse_voltage.setSizePolicy(sizePolicy)
        self.pulse_voltage.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.pulse_voltage.setText("")
        self.pulse_voltage.setObjectName("pulse_voltage")
        self.gridLayout_4.addWidget(self.pulse_voltage, 4, 1, 1, 1)
        self.total_ions = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.total_ions.sizePolicy().hasHeightForWidth())
        self.total_ions.setSizePolicy(sizePolicy)
        self.total_ions.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.total_ions.setText("")
        self.total_ions.setObjectName("total_ions")
        self.gridLayout_4.addWidget(self.total_ions, 2, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 3, 0, 1, 1)
        self.detection_rate = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detection_rate.sizePolicy().hasHeightForWidth())
        self.detection_rate.setSizePolicy(sizePolicy)
        self.detection_rate.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.detection_rate.setText("")
        self.detection_rate.setObjectName("detection_rate")
        self.gridLayout_4.addWidget(self.detection_rate, 5, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 5, 0, 1, 1)
        self.elapsed_time = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.elapsed_time.sizePolicy().hasHeightForWidth())
        self.elapsed_time.setSizePolicy(sizePolicy)
        self.elapsed_time.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.elapsed_time.setText("")
        self.elapsed_time.setObjectName("elapsed_time")
        self.gridLayout_4.addWidget(self.elapsed_time, 1, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName("label_23")
        self.gridLayout_3.addWidget(self.label_23, 14, 0, 1, 2)
        self.vdc_steps_down = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vdc_steps_down.sizePolicy().hasHeightForWidth())
        self.vdc_steps_down.setSizePolicy(sizePolicy)
        self.vdc_steps_down.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.vdc_steps_down.setObjectName("vdc_steps_down")
        self.gridLayout_3.addWidget(self.vdc_steps_down, 9, 2, 1, 1)
        self.pulse_frequency = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pulse_frequency.sizePolicy().hasHeightForWidth())
        self.pulse_frequency.setSizePolicy(sizePolicy)
        self.pulse_frequency.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.pulse_frequency.setObjectName("pulse_frequency")
        self.gridLayout_3.addWidget(self.pulse_frequency, 14, 2, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 15, 0, 1, 2)
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 10, 0, 1, 2)
        self.pulse_fraction = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pulse_fraction.sizePolicy().hasHeightForWidth())
        self.pulse_fraction.setSizePolicy(sizePolicy)
        self.pulse_fraction.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.pulse_fraction.setObjectName("pulse_fraction")
        self.gridLayout_3.addWidget(self.pulse_fraction, 13, 2, 1, 1)
        self.detection_rate_init = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detection_rate_init.sizePolicy().hasHeightForWidth())
        self.detection_rate_init.setSizePolicy(sizePolicy)
        self.detection_rate_init.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.detection_rate_init.setObjectName("detection_rate_init")
        self.gridLayout_3.addWidget(self.detection_rate_init, 15, 2, 1, 1)
        self.cycle_avg = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cycle_avg.sizePolicy().hasHeightForWidth())
        self.cycle_avg.setSizePolicy(sizePolicy)
        self.cycle_avg.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.cycle_avg.setObjectName("cycle_avg")
        self.gridLayout_3.addWidget(self.cycle_avg, 10, 2, 1, 1)
        self.vp_max = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vp_max.sizePolicy().hasHeightForWidth())
        self.vp_max.setSizePolicy(sizePolicy)
        self.vp_max.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.vp_max.setObjectName("vp_max")
        self.gridLayout_3.addWidget(self.vp_max, 12, 2, 1, 1)
        self.vdc_steps_up = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vdc_steps_up.sizePolicy().hasHeightForWidth())
        self.vdc_steps_up.setSizePolicy(sizePolicy)
        self.vdc_steps_up.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.vdc_steps_up.setObjectName("vdc_steps_up")
        self.gridLayout_3.addWidget(self.vdc_steps_up, 8, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 11, 0, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 12, 0, 1, 2)
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setObjectName("label_25")
        self.gridLayout_3.addWidget(self.label_25, 13, 0, 1, 2)
        self.label_28 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setObjectName("label_28")
        self.gridLayout_3.addWidget(self.label_28, 9, 0, 1, 1)
        self.vp_min = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vp_min.sizePolicy().hasHeightForWidth())
        self.vp_min.setSizePolicy(sizePolicy)
        self.vp_min.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.vp_min.setObjectName("vp_min")
        self.gridLayout_3.addWidget(self.vp_min, 11, 2, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy)
        self.label_42.setObjectName("label_42")
        self.gridLayout_3.addWidget(self.label_42, 19, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 16, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy)
        self.doubleSpinBox.setStyleSheet("QDoubleSpinBox{\n"
"background: rgb(223,223,233)\n"
"}")
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout_3.addWidget(self.doubleSpinBox, 16, 1, 1, 1)
        self.email = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email.sizePolicy().hasHeightForWidth())
        self.email.setSizePolicy(sizePolicy)
        self.email.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.email.setText("")
        self.email.setObjectName("email")
        self.gridLayout_3.addWidget(self.email, 17, 2, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setObjectName("label_27")
        self.gridLayout_3.addWidget(self.label_27, 18, 0, 1, 1)
        self.hit_displayed = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hit_displayed.sizePolicy().hasHeightForWidth())
        self.hit_displayed.setSizePolicy(sizePolicy)
        self.hit_displayed.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.hit_displayed.setObjectName("hit_displayed")
        self.gridLayout_3.addWidget(self.hit_displayed, 16, 2, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setObjectName("label_26")
        self.gridLayout_3.addWidget(self.label_26, 17, 0, 1, 1)
        self.tweet = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tweet.sizePolicy().hasHeightForWidth())
        self.tweet.setSizePolicy(sizePolicy)
        self.tweet.setStyleSheet("QComboBox{\n"
"background: rgb(223,223,233)\n"
"}")
        self.tweet.setObjectName("tweet")
        self.tweet.addItem("")
        self.tweet.addItem("")
        self.gridLayout_3.addWidget(self.tweet, 18, 2, 1, 1)
        self.counter_source = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.counter_source.sizePolicy().hasHeightForWidth())
        self.counter_source.setSizePolicy(sizePolicy)
        self.counter_source.setStyleSheet("QComboBox{\n"
"background: rgb(223,223,233)\n"
"}")
        self.counter_source.setObjectName("counter_source")
        self.counter_source.addItem("")
        self.counter_source.addItem("")
        self.counter_source.addItem("")
        self.counter_source.addItem("")
        self.gridLayout_3.addWidget(self.counter_source, 19, 2, 1, 1)
        self.parameters_source = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameters_source.sizePolicy().hasHeightForWidth())
        self.parameters_source.setSizePolicy(sizePolicy)
        self.parameters_source.setStyleSheet("QComboBox{\n"
"background: rgb(223,223,233)\n"
"}")
        self.parameters_source.setObjectName("parameters_source")
        self.parameters_source.addItem("")
        self.parameters_source.addItem("")
        self.gridLayout_3.addWidget(self.parameters_source, 0, 2, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 2, 0, 1, 1)
        self.ex_user = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ex_user.sizePolicy().hasHeightForWidth())
        self.ex_user.setSizePolicy(sizePolicy)
        self.ex_user.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.ex_user.setObjectName("ex_user")
        self.gridLayout_3.addWidget(self.ex_user, 1, 2, 1, 1)
        self.label_43 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy)
        self.label_43.setObjectName("label_43")
        self.gridLayout_3.addWidget(self.label_43, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 2)
        self.ex_name = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ex_name.sizePolicy().hasHeightForWidth())
        self.ex_name.setSizePolicy(sizePolicy)
        self.ex_name.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.ex_name.setObjectName("ex_name")
        self.gridLayout_3.addWidget(self.ex_name, 2, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 5, 0, 1, 2)
        self.ex_freq = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ex_freq.sizePolicy().hasHeightForWidth())
        self.ex_freq.setSizePolicy(sizePolicy)
        self.ex_freq.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.ex_freq.setObjectName("ex_freq")
        self.gridLayout_3.addWidget(self.ex_freq, 5, 2, 1, 1)
        self.max_ions = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_ions.sizePolicy().hasHeightForWidth())
        self.max_ions.setSizePolicy(sizePolicy)
        self.max_ions.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.max_ions.setObjectName("max_ions")
        self.gridLayout_3.addWidget(self.max_ions, 4, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 6, 0, 1, 2)
        self.ex_time = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ex_time.sizePolicy().hasHeightForWidth())
        self.ex_time.setSizePolicy(sizePolicy)
        self.ex_time.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.ex_time.setObjectName("ex_time")
        self.gridLayout_3.addWidget(self.ex_time, 3, 2, 1, 1)
        self.vdc_min = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vdc_min.sizePolicy().hasHeightForWidth())
        self.vdc_min.setSizePolicy(sizePolicy)
        self.vdc_min.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.vdc_min.setObjectName("vdc_min")
        self.gridLayout_3.addWidget(self.vdc_min, 6, 2, 1, 1)
        self.vdc_max = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vdc_max.sizePolicy().hasHeightForWidth())
        self.vdc_max.setSizePolicy(sizePolicy)
        self.vdc_max.setStyleSheet("QLineEdit{\n"
"background: rgb(223,223,233)\n"
"}")
        self.vdc_max.setObjectName("vdc_max")
        self.gridLayout_3.addWidget(self.vdc_max, 7, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 8, 0, 1, 1)
        self.label_41 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy)
        self.label_41.setObjectName("label_41")
        self.gridLayout_3.addWidget(self.label_41, 4, 0, 1, 1)
        self.criteria_ions = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.criteria_ions.sizePolicy().hasHeightForWidth())
        self.criteria_ions.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(False)
        self.criteria_ions.setFont(font)
        self.criteria_ions.setMouseTracking(True)
        self.criteria_ions.setStyleSheet("QCheckBox{\n"
"background: rgb(223,223,233)\n"
"}")
        self.criteria_ions.setText("")
        self.criteria_ions.setChecked(True)
        self.criteria_ions.setObjectName("criteria_ions")
        self.gridLayout_3.addWidget(self.criteria_ions, 4, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 3, 0, 1, 1)
        self.criteria_time = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.criteria_time.sizePolicy().hasHeightForWidth())
        self.criteria_time.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(False)
        self.criteria_time.setFont(font)
        self.criteria_time.setMouseTracking(True)
        self.criteria_time.setStyleSheet("QCheckBox{\n"
"background: rgb(223,223,233)\n"
"}")
        self.criteria_time.setText("")
        self.criteria_time.setChecked(True)
        self.criteria_time.setObjectName("criteria_time")
        self.gridLayout_3.addWidget(self.criteria_time, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 7, 0, 1, 1)
        self.criteria_vdc = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.criteria_vdc.sizePolicy().hasHeightForWidth())
        self.criteria_vdc.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setItalic(False)
        self.criteria_vdc.setFont(font)
        self.criteria_vdc.setMouseTracking(True)
        self.criteria_vdc.setStyleSheet("QCheckBox{\n"
"background: rgb(223,223,233)\n"
"}")
        self.criteria_vdc.setText("")
        self.criteria_vdc.setChecked(True)
        self.criteria_vdc.setObjectName("criteria_vdc")
        self.gridLayout_3.addWidget(self.criteria_vdc, 7, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_5.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("")
        self.label_18.setObjectName("label_18")
        self.verticalLayout_2.addWidget(self.label_18)
        self.diagram = QtWidgets.QLabel(self.centralwidget)
        ####
        self.diagram.setAlignment(QtCore.Qt.AlignCenter)
        ####
        self.diagram.setMinimumSize(QtCore.QSize(350, 350))
        self.diagram.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 4 4px;\n"
"background: rgb(255, 255, 255)\n"
"}")
        self.diagram.setText("")
        self.diagram.setObjectName("diagram")
        self.verticalLayout_2.addWidget(self.diagram)
        self.gridLayout_13.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_13, 0, 0, 3, 1)
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_34 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")
        self.gridLayout_11.addWidget(self.label_34, 0, 3, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.gridLayout_11.addWidget(self.label_30, 1, 1, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.gridLayout_11.addWidget(self.label_32, 1, 4, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_11, 0, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        ####
        # self.cam_b_o = QtWidgets.QLabel(self.centralwidget)
        self.cam_b_o = pg.ImageView(self.centralwidget)
        self.cam_b_o.adjustSize()
        self.cam_b_o.ui.histogram.hide()
        self.cam_b_o.ui.roiBtn.hide()
        self.cam_b_o.ui.menuBtn.hide()
        ####
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.cam_b_o.sizePolicy().hasHeightForWidth())
        self.cam_b_o.setSizePolicy(sizePolicy)
        self.cam_b_o.setMinimumSize(QtCore.QSize(500, 500))
        self.cam_b_o.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cam_b_o.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 4 4px;\n"
"}")
        # self.cam_b_o.setText("")
        self.cam_b_o.setObjectName("cam_b_o")
        self.horizontalLayout_6.addWidget(self.cam_b_o)
        self.cam_b_d = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.cam_b_d.sizePolicy().hasHeightForWidth())
        self.cam_b_d.setSizePolicy(sizePolicy)
        self.cam_b_d.setMinimumSize(QtCore.QSize(1200, 500))
        self.cam_b_d.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cam_b_d.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 4 4px;\n"
"}")
        self.cam_b_d.setText("")
        self.cam_b_d.setObjectName("cam_b_d")
        self.horizontalLayout_6.addWidget(self.cam_b_d)
        self.gridLayout_14.addLayout(self.horizontalLayout_6, 3, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        ###
        # self.cam_s_o = QtWidgets.QLabel(self.centralwidget)
        self.cam_s_o = pg.ImageView(self.centralwidget)
        self.cam_s_o.adjustSize()
        self.cam_s_o.ui.histogram.hide()
        self.cam_s_o.ui.roiBtn.hide()
        self.cam_s_o.ui.menuBtn.hide()
        self.cam_s_o.setObjectName("cam_s_o")
        ###
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.cam_s_o.sizePolicy().hasHeightForWidth())
        self.cam_s_o.setSizePolicy(sizePolicy)
        self.cam_s_o.setMinimumSize(QtCore.QSize(500, 500))
        self.cam_s_o.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 4 4px;\n"
"}")
        # self.cam_s_o.setText("")
        self.cam_s_o.setObjectName("cam_s_o")
        self.horizontalLayout_5.addWidget(self.cam_s_o)
        self.cam_s_d = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.cam_s_d.sizePolicy().hasHeightForWidth())
        self.cam_s_d.setSizePolicy(sizePolicy)
        self.cam_s_d.setMinimumSize(QtCore.QSize(1200, 500))
        self.cam_s_d.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cam_s_d.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 4 4px;\n"
"}")
        self.cam_s_d.setText("")
        self.cam_s_d.setObjectName("cam_s_d")
        self.horizontalLayout_5.addWidget(self.cam_s_d)
        self.gridLayout_14.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.gridLayout_12.addWidget(self.label_29, 1, 0, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.gridLayout_12.addWidget(self.label_33, 0, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.gridLayout_12.addWidget(self.label_31, 1, 2, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_12, 2, 0, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_14, 1, 2, 1, 1)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.Error = QtWidgets.QLabel(self.centralwidget)
        self.Error.setMinimumSize(QtCore.QSize(800, 50))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.Error.setFont(font)
        self.Error.setAlignment(QtCore.Qt.AlignCenter)
        self.Error.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.Error.setObjectName("Error")
        self.horizontalLayout_10.addWidget(self.Error)
        self.gridLayout_8.addLayout(self.horizontalLayout_10, 3, 0, 1, 3)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.vdc_time = QtWidgets.QWidget(self.centralwidget)
        self.vdc_time = pg.PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.vdc_time.sizePolicy().hasHeightForWidth())
        self.vdc_time.setSizePolicy(sizePolicy)
        self.vdc_time.setMinimumSize(QtCore.QSize(500, 500))
        self.vdc_time.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 4 4px;\n"
"}")
        self.vdc_time.setObjectName("vdc_time")
        self.horizontalLayout.addWidget(self.vdc_time)
        # self.detection_rate_viz = QtWidgets.QWidget(self.centralwidget)
        self.detection_rate_viz = pg.PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.detection_rate_viz.sizePolicy().hasHeightForWidth())
        self.detection_rate_viz.setSizePolicy(sizePolicy)
        self.detection_rate_viz.setMinimumSize(QtCore.QSize(500, 500))
        self.detection_rate_viz.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 4 4px;\n"
"}")
        self.detection_rate_viz.setObjectName("detection_rate_viz")
        self.horizontalLayout.addWidget(self.detection_rate_viz)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_3.addWidget(self.label_19)
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_3.addWidget(self.label_24)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        ###
        # self.visualization = QtWidgets.QWidget(self.centralwidget)
        self.visualization = pg.PlotWidget(self.centralwidget)
        self.visualization.setObjectName("visualization")
        self.detector_circle = pg.QtGui.QGraphicsEllipseItem(0, 0, 2400, 2400)  # x, y, width, height
        self.detector_circle.setPen(pg.mkPen(color=(255, 0, 0), width=1))
        self.visualization.addItem(self.detector_circle)
        ###
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.visualization.sizePolicy().hasHeightForWidth())
        self.visualization.setSizePolicy(sizePolicy)
        self.visualization.setMinimumSize(QtCore.QSize(500, 500))
        self.visualization.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 4 4px;\n"
"}")
        self.visualization.setObjectName("visualization")
        self.horizontalLayout_4.addWidget(self.visualization)
        # self.histogram = QtWidgets.QWidget(self.centralwidget)
        self.histogram = pg.PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.histogram.sizePolicy().hasHeightForWidth())
        self.histogram.setSizePolicy(sizePolicy)
        self.histogram.setMinimumSize(QtCore.QSize(500, 500))
        self.histogram.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 4 4px;\n"
"}")
        self.histogram.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.histogram.setObjectName("histogram")
        self.horizontalLayout_4.addWidget(self.histogram)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.gridLayout_8.addLayout(self.verticalLayout_3, 1, 1, 1, 1)
        self.gridLayout_18 = QtWidgets.QGridLayout()
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(2508, 80))
        self.textEdit.setStyleSheet("QWidget{\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"padding: 0 8px;\n"
"background: rgb(223,223,233)\n"
"}")
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_18.addWidget(self.textEdit, 0, 0, 1, 1)
        self.light = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.light.sizePolicy().hasHeightForWidth())
        self.light.setSizePolicy(sizePolicy)
        self.light.setStyleSheet("QPushButton{\n"
"background: rgb(193, 193, 193)\n"
"}")
        self.light.setObjectName("light")
        self.gridLayout_18.addWidget(self.light, 0, 1, 1, 1)
        self.led_light = QtWidgets.QLabel(self.centralwidget)
        self.led_light.setMinimumSize(QtCore.QSize(90, 30))
        self.led_light.setAlignment(QtCore.Qt.AlignCenter)
        self.led_light.setObjectName("led_light")
        self.gridLayout_18.addWidget(self.led_light, 0, 2, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_18, 0, 1, 1, 2)
        self.gridLayout_9.addLayout(self.gridLayout_8, 1, 0, 1, 1)
        UI_APT_A.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(UI_APT_A)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 3462, 38))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        UI_APT_A.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(UI_APT_A)
        self.statusbar.setObjectName("statusbar")
        UI_APT_A.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(UI_APT_A)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(UI_APT_A)
        QtCore.QMetaObject.connectSlotsByName(UI_APT_A)

        #### Set 8 digits for each LCD to show
        self.doubleSpinBox.setValue(1.0)
        self.vacuum_main.setDigitCount(8)
        self.vacuum_buffer.setDigitCount(8)
        self.vacuum_buffer_back.setDigitCount(8)
        self.vacuum_load_lock.setDigitCount(8)
        self.vacuum_load_lock_back.setDigitCount(8)
        self.temp.setDigitCount(8)

        arrow1 = pg.ArrowItem(pos=(100, 1700), angle=-90)
        # arrow2 = pg.ArrowItem(pos=(100, 2100), angle=90)
        arrow3 = pg.ArrowItem(pos=(130, 1800), angle=0)
        self.cam_b_o.addItem(arrow1)
        # self.cam_b_o.addItem(arrow2)
        self.cam_b_o.addItem(arrow3)

        arrow1 = pg.ArrowItem(pos=(590, 620), angle=-90)
        arrow2 = pg.ArrowItem(pos=(570, 1120), angle=90)
        # arrow3 = pg.ArrowItem(pos=(890, 1100), angle=0)
        self.cam_s_o.addItem(arrow1)
        self.cam_s_o.addItem(arrow2)
        # self.cam_s_o.addItem(arrow3)

    def retranslateUi(self, UI_APT_A):
        _translate = QtCore.QCoreApplication.translate
        UI_APT_A.setWindowTitle(_translate("UI_APT_A", "OXCART"))
        ###
        UI_APT_A.setWindowTitle(_translate("OXCART", "APT Control Software"))
        UI_APT_A.setWindowIcon(QtGui.QIcon('./files/logo3.png'))
        ###
        self.pump_load_lock_switch.setText(_translate("UI_APT_A", "Load Lock Pump"))
        self.led_pump_load_lock.setText(_translate("UI_APT_A", "pump"))
        self.label_35.setText(_translate("UI_APT_A", "Main Chamber (mBar)"))
        self.label_39.setText(_translate("UI_APT_A", "Load Lock Pre(mBar)"))
        self.label_40.setText(_translate("UI_APT_A", "Buffer Chamber Pre (mBar)"))
        self.label_38.setText(_translate("UI_APT_A", "Temperature (K)"))
        self.label_36.setText(_translate("UI_APT_A", "Buffer Chamber (mBar)"))
        self.label_37.setText(_translate("UI_APT_A", "Load lock (mBar)"))
        self.start_button.setText(_translate("UI_APT_A", "Start"))
        ###
        self._translate = QtCore.QCoreApplication.translate
        self.start_button.clicked.connect(self.thread_main)
        self.thread = MainThread(self.conf)
        self.thread.signal.connect(self.finished_thread_main)
        self.stop_button.setText(_translate("OXCART", "Stop"))
        self.stop_button.clicked.connect(self.stop_ex)
        ###
        self.led_main_chamber.setText(_translate("UI_APT_A", "Main"))
        self.led_load_lock.setText(_translate("UI_APT_A", "Load"))
        self.led_cryo.setText(_translate("UI_APT_A", "Cryo"))
        self.main_chamber_switch.setText(_translate("UI_APT_A", "Main Chamber"))
        self.load_lock_switch.setText(_translate("UI_APT_A", "Load Lock"))
        self.cryo_switch.setText(_translate("UI_APT_A", "Cryo"))
        self.label_12.setText(_translate("UI_APT_A", "Elapsed Time (S):"))
        self.label_16.setText(_translate("UI_APT_A", "Pulse Voltage (V)"))
        self.label_11.setText(_translate("UI_APT_A", "Run Statistics"))
        self.label_14.setText(_translate("UI_APT_A", "Specimen Voltage (V)"))
        self.label_13.setText(_translate("UI_APT_A", "Total Ions"))
        self.label_15.setText(_translate("UI_APT_A", "Detection Rate (%)"))
        self.label_23.setText(_translate("UI_APT_A", "Pulse Frequency (KHz)"))
        self.vdc_steps_down.setText(_translate("UI_APT_A", "100"))
        self.pulse_frequency.setText(_translate("UI_APT_A", "200"))
        self.label_17.setText(_translate("UI_APT_A", "Detection Rate (%)"))
        self.label_20.setText(_translate("UI_APT_A", "Cycle for Avg. (Hz)"))
        self.pulse_fraction.setText(_translate("UI_APT_A", "20"))
        self.detection_rate_init.setText(_translate("UI_APT_A", "1"))
        self.cycle_avg.setText(_translate("UI_APT_A", "10"))
        self.vp_max.setText(_translate("UI_APT_A", "3281"))
        self.vdc_steps_up.setText(_translate("UI_APT_A", "100"))
        self.label_8.setText(_translate("UI_APT_A", "Pulse Min. Voltage (V)"))
        self.label_9.setText(_translate("UI_APT_A", "Pulse Max. Voltage (V)"))
        self.label_25.setText(_translate("UI_APT_A", "Pulse Fraction (%)"))
        self.label_28.setText(_translate("UI_APT_A", "K_p Downwards"))
        self.vp_min.setText(_translate("UI_APT_A", "328"))
        self.label_42.setText(_translate("UI_APT_A", "Counter Source"))
        self.label_22.setText(_translate("UI_APT_A", "# Hits Displayed"))
        self.label_27.setText(_translate("UI_APT_A", "Twitter"))
        self.hit_displayed.setText(_translate("UI_APT_A", "20000"))
        self.label_26.setText(_translate("UI_APT_A", "Email"))
        self.tweet.setItemText(0, _translate("UI_APT_A", "No"))
        self.tweet.setItemText(1, _translate("UI_APT_A", "Yes"))
        self.counter_source.setItemText(0, _translate("UI_APT_A", "TDC"))
        self.counter_source.setItemText(1, _translate("UI_APT_A", "TDC_Raw"))
        self.counter_source.setItemText(2, _translate("UI_APT_A", "DRS"))
        self.counter_source.setItemText(3, _translate("UI_APT_A", "Pulse Counter"))
        self.parameters_source.setItemText(0, _translate("UI_APT_A", "TextBox"))
        self.parameters_source.setItemText(1, _translate("UI_APT_A", "TextLine"))
        self.label_21.setText(_translate("UI_APT_A", "Experiment Name"))
        self.ex_user.setText(_translate("UI_APT_A", "user"))
        self.label_43.setText(_translate("UI_APT_A", "Experiment User"))
        self.label.setText(_translate("UI_APT_A", "Setup Parameters"))
        self.ex_name.setText(_translate("UI_APT_A", "test"))
        self.label_3.setText(_translate("UI_APT_A", "Control refresh Freq.(Hz)"))
        self.ex_freq.setText(_translate("UI_APT_A", "10"))
        self.max_ions.setText(_translate("UI_APT_A", "2000"))
        self.label_4.setText(_translate("UI_APT_A", "Specimen Start Voltage (V)"))
        self.ex_time.setText(_translate("UI_APT_A", "90"))
        self.vdc_min.setText(_translate("UI_APT_A", "500"))
        self.vdc_max.setText(_translate("UI_APT_A", "4000"))
        self.label_6.setText(_translate("UI_APT_A", "K_p Upwards"))
        self.label_41.setText(_translate("UI_APT_A", "Max. Number of Ions"))
        self.label_2.setText(_translate("UI_APT_A", "Max. Experiment Time (S)"))
        self.label_5.setText(_translate("UI_APT_A", "Specimen Stop Voltage (V)"))
        self.label_18.setText(_translate("UI_APT_A", "Diagram"))
        self.label_34.setText(_translate("UI_APT_A", "Camera Side"))
        self.label_30.setText(_translate("UI_APT_A", "Overview"))
        self.label_32.setText(_translate("UI_APT_A", "Detail"))
        self.label_29.setText(_translate("UI_APT_A", "Overview"))
        self.label_33.setText(_translate("UI_APT_A", "Camera Bottom"))
        self.label_31.setText(_translate("UI_APT_A", "Detail"))
        self.Error.setText(_translate("UI_APT_A", "<html><head/><body><p><br/></p></body></html>"))
        self.label_7.setText(_translate("UI_APT_A", "Voltage"))
        self.label_10.setText(_translate("UI_APT_A", "Detection Rate"))
        self.label_19.setText(_translate("UI_APT_A", "Visualization"))
        self.label_24.setText(_translate("UI_APT_A", "TOF"))
        self.textEdit.setHtml(_translate("UI_APT_A", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">ex_user=user1;</span>ex_name=test1;ex_time=90;max_ions=2000;ex_freq=10;vdc_min=500;vdc_max=4000;vdc_steps_up=100;vdc_steps_down=100;vp_min=328;vp_max=3281;pulse_fraction=20;pulse_frequency=200;detection_rate_init=1;hit_displayed=20000;email=;tweet=No;counter_source=TDC<span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">;criteria_time=True;criteria_ions=False;criteria_vdc=False</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">ex_user=user2;ex_name=test2;ex_time=100;max_ions=3000;ex_freq=5;vdc_min=1000;vdc_max=3000;vdc_steps_up=50;vdc_steps_down=50;vp_min=400;vp_max=2000;pulse_fraction=15;pulse_frequency=200;detection_rate_init=2;hit_displayed=40000;email=;tweet=No;counter_source=Pulse Counter;criteria_time=False;criteria_ions=False;criteria_vdc=True</span></p></body></html>"))
        self.light.setText(_translate("UI_APT_A", "Light"))
        self.led_light.setText(_translate("UI_APT_A", "light"))
        self.menuFile.setTitle(_translate("UI_APT_A", "File"))
        self.actionExit.setText(_translate("UI_APT_A", "Exit"))

        ###
        self.main_chamber_switch.clicked.connect(lambda: self.gates(1))
        self.load_lock_switch.clicked.connect(lambda: self.gates(2))
        self.cryo_switch.clicked.connect(lambda: self.gates(3))
        self.light.clicked.connect(lambda: self.light_switch())
        self.pump_load_lock_switch.clicked.connect(lambda: self.pump_switch())

        # High Voltage visualization ################
        self.x_vdc = np.arange(1000)  # 1000 time points
        self.y_vdc = np.zeros(1000)  # 1000 data points
        self.y_vdc[:] = np.nan
        self.y_vps = np.zeros(1000)  # 1000 data points
        self.y_vps[:] = np.nan
        # Add legend
        self.vdc_time.addLegend()
        pen_vdc = pg.mkPen(color=(255, 0, 0), width=6)
        pen_vps = pg.mkPen(color=(0, 0, 255), width=3)
        self.data_line_vdc = self.vdc_time.plot(self.x_vdc, self.y_vdc, name="High Vol.", pen=pen_vdc)
        self.data_line_vps = self.vdc_time.plot(self.x_vdc, self.y_vps, name="Pulse Vol.", pen=pen_vps)
        self.vdc_time.setBackground('w')
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.vdc_time.setLabel("left", "High Voltage (v)", **styles)
        self.vdc_time.setLabel("bottom", "Time (s)", **styles)
        # Add grid
        self.vdc_time.showGrid(x=True, y=True)
        # Add Range
        self.vdc_time.setXRange(0, 1000, padding=0.05)
        self.vdc_time.setYRange(0, 15000, padding=0.05)

        # Detection Visualization #########################
        self.x_dtec = np.arange(1000)  # 1000 time points
        self.y_dtec = np.zeros(1000)  # 1000 data points
        self.y_dtec[:] = np.nan
        pen_dtec = pg.mkPen(color=(255, 0, 0), width=6)
        self.data_line_dtec = self.detection_rate_viz.plot(self.x_dtec, self.y_dtec, pen=pen_dtec)
        self.detection_rate_viz.setBackground('w')
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.detection_rate_viz.setLabel("left", "Counts", **styles)
        self.detection_rate_viz.setLabel("bottom", "Time (s)", **styles)
        # Add grid
        self.detection_rate_viz.showGrid(x=True, y=True)
        # Add Range
        self.detection_rate_viz.setXRange(0, 1000, padding=0.05)
        self.detection_rate_viz.setYRange(0, 4000, padding=0.05)

        # Histogram #########################
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.histogram.setLabel("left", "Frequency (counts)", **styles)
        self.histogram.setLabel("bottom", "Time (ns)", **styles)

        # Temperature #########################
        self.x_tem = np.arange(100)  # 1000 time points
        self.y_tem = np.zeros(100)  # 1000 data points
        self.y_tem[:] = np.nan
        pen_dtec = pg.mkPen(color=(255, 0, 0), width=6)
        self.data_line_tem = self.temperature.plot(self.x_tem, self.y_tem, pen=pen_dtec)
        self.temperature.setBackground('b')
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.temperature.setLabel("left", "Temperature (K)", **styles)
        self.temperature.setLabel("bottom", "Time (s)", **styles)
        # Add grid
        self.temperature.showGrid(x=True, y=True)
        # Add Range
        self.temperature.setYRange(0, 100, padding=0.1)

        # Visualization #####################
        self.scatter = pg.ScatterPlotItem(
                size=self.doubleSpinBox.value(), brush=pg.mkBrush(255, 255, 255, 120))
        self.visualization.getPlotItem().hideAxis('bottom')
        self.visualization.getPlotItem().hideAxis('left')

        # timer plot, variables, and cameras
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(1000)
        self.timer1.timeout.connect(self.update_cameras)
        self.timer1.start()
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(1000)
        self.timer2.timeout.connect(self.update_plot_data)
        self.timer2.start()
        self.timer3 = QtCore.QTimer()
        self.timer3.setInterval(2000)
        self.timer3.timeout.connect(self.statistics)
        self.timer3.start()

        # Diagram and LEDs ##############
        self.diagram_close_all = QPixmap('./files/close_all.png')
        self.diagram_main_open = QPixmap('./files/main_open.png')
        self.diagram_load_open = QPixmap('./files/load_open.png')
        self.diagram_cryo_open = QPixmap('./files/cryo_open.png')
        self.led_red = QPixmap('./files/led-red-on.png')
        self.led_green = QPixmap('./files/green-led-on.png')

        self.diagram.setPixmap(self.diagram_close_all)
        self.led_main_chamber.setPixmap(self.led_red)
        self.led_load_lock.setPixmap(self.led_red)
        self.led_cryo.setPixmap(self.led_red)
        self.led_light.setPixmap(self.led_red)
        self.led_pump_load_lock.setPixmap(self.led_green)

    def thread_main(self):
            """
                Main thread for running experiment
                """

            def read_update(text_line, index_line):
                    """
                            Function for reading the Textline box
                            This function is only run if Textline is selected in the GUI
                            The function read the the text line and put it in the Qboxes
                            """
                    _translate = QtCore.QCoreApplication.translate
                    text_line = text_line[index_line].split(';')
                    text_line_b = []
                    for i in range(len(text_line)):
                            text_line_b.append(text_line[i].split('='))
                    for i in range(len(text_line_b)):
                            if text_line_b[i][0] == 'ex_user':
                                    self.ex_user.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'ex_name':
                                    self.ex_name.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'ex_time':
                                    self.ex_time.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'ex_freq':
                                    self.ex_freq.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'max_ions':
                                    self.max_ions.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'vdc_min':
                                    self.vdc_min.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'vdc_max':
                                    self.vdc_max.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'detection_rate_init':
                                    self.detection_rate_init.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'pulse_fraction':
                                    self.pulse_fraction.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'pulse_frequency':
                                    self.pulse_frequency.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'hit_displayed':
                                    self.hit_displayed.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'hdf5_path':
                                    self.ex_name.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'email':
                                    self.email.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'cycle_avg':
                                    self.cycle_avg.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'vdc_steps_up':
                                    self.vdc_steps_up.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'vdc_steps_down':
                                    self.vdc_steps_down.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'vp_min':
                                    self.vp_min.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'vp_max':
                                    self.vp_max.setText(_translate("OXCART", text_line_b[i][1]))
                            if text_line_b[i][0] == 'counter_source':
                                    if text_line_b[i][1] == 'TDC':
                                            self.counter_source.setCurrentIndex(0)
                                    if text_line_b[i][1] == 'TDC_Raw':
                                            self.counter_source.setCurrentIndex(1)
                                    if text_line_b[i][1] == 'Pulse Counter':
                                            self.counter_source.setCurrentIndex(2)
                                    if text_line_b[i][1] == 'DRS':
                                            self.counter_source.setCurrentIndex(3)
                            if text_line_b[i][0] == 'tweet':
                                    if text_line_b[i][1] == 'NO':
                                            self.tweet.setCurrentIndex(0)
                                    if text_line_b[i][1] == 'Yes':
                                            self.tweet.setCurrentIndex(1)
                            if text_line_b[i][0] == 'criteria_time':
                                    if text_line_b[i][1] == 'True':
                                            self.criteria_time.setChecked(True)
                                    elif text_line_b[i][1] == 'False':
                                            self.criteria_time.setChecked(False)
                            if text_line_b[i][0] == 'criteria_ions':
                                    if text_line_b[i][1] == 'True':
                                            self.criteria_ions.setChecked(True)
                                    elif text_line_b[i][1] == 'False':
                                            self.criteria_ions.setChecked(False)
                            if text_line_b[i][0] == 'criteria_vdc':
                                    if text_line_b[i][1] == 'True':
                                            self.criteria_vdc.setChecked(True)
                                    elif text_line_b[i][1] == 'False':
                                            self.criteria_vdc.setChecked(False)

            # check if the gates are closed
            if not variables.flag_main_gate and not variables.flag_load_gate and not variables.flag_cryo_gate:
                    if self.parameters_source.currentText() == 'TextLine' and variables.index_line == 0:
                            lines = self.textEdit.toPlainText()  # Copy all the lines in TextLine
                            self.text_line = lines.splitlines()  # Seperate the lines in TextLine
                            self.num_line = len(
                                    self.text_line)  # count number of line in TextLine (Number of experiments that have to be done)
                    elif self.parameters_source.currentText() != 'TextLine' and variables.index_line == 0:
                            self.num_line = 0
                    self.start_button.setEnabled(False)  # Disable the start button in the GUI
                    variables.plot_clear_flag = True  # Change the flag to clear the plots in GUI

                    # If the TextLine is selected the read_update function is run
                    if self.parameters_source.currentText() == 'TextLine':
                            read_update(self.text_line, variables.index_line)
                    # Update global variables to do the experiments
                    variables.user_name = self.ex_user.text()
                    variables.ex_time = int(float(self.ex_time.text()))
                    variables.ex_freq = int(float(self.ex_freq.text()))
                    variables.max_ions = int(float(self.max_ions.text()))
                    variables.vdc_min = int(float(self.vdc_min.text()))
                    variables.detection_rate = float(self.detection_rate_init.text())
                    variables.hit_display = int(float(self.hit_displayed.text()))
                    variables.pulse_fraction = int(float(self.pulse_fraction.text())) / 100
                    variables.pulse_frequency = float(self.pulse_frequency.text())
                    variables.hdf5_path = self.ex_name.text()
                    variables.email = self.email.text()
                    variables.cycle_avg = int(float(self.cycle_avg.text()))
                    variables.vdc_step_up = int(float(self.vdc_steps_up.text()))
                    variables.vdc_step_down = int(float(self.vdc_steps_down.text()))
                    variables.v_p_min = int(float(self.vp_min.text()))
                    variables.v_p_max = int(float(self.vp_max.text()))
                    variables.counter_source = str(self.counter_source.currentText())
                    if self.criteria_time.isChecked():
                            variables.criteria_time = True
                    elif not self.criteria_time.isChecked():
                            variables.criteria_time = False
                    if self.criteria_ions.isChecked():
                            variables.criteria_ions = True
                    elif not self.criteria_ions.isChecked():
                            variables.criteria_ions = False
                    if self.criteria_vdc.isChecked():
                            variables.criteria_vdc = True
                    elif not self.criteria_vdc.isChecked():
                            variables.criteria_vdc = False
                    if variables.counter_source == 'TDC_Raw':
                            variables.raw_mode = True

                    if self.tweet.currentText() == 'Yes':
                            variables.tweet = True

                    # Read the experiment counter
                    with open('./files/counter_oxcart.txt') as f:
                            variables.counter = int(f.readlines()[0])
                    # Current time and date
                    now = datetime.datetime.now()
                    variables.exp_name = "%s_" % variables.counter + \
                                         now.strftime("%b-%d-%Y_%H-%M") + "_%s" % variables.hdf5_path

                    variables.path = os.path.join(os.path.split(MODULE_DIR)[0],
                                                  'data_voltage_pulse_mode\\%s' % variables.exp_name)
                    # Create folder to save the data
                    if not os.path.isdir(variables.path):
                            os.makedirs(variables.path, mode=0o777, exist_ok=True)
                    # start the run methos of MainThread Class, which is main function of apt_voltage.py
                    self.thread.start()
                    if self.parameters_source.currentText() == 'TextLine':
                            variables.index_line += 1  # increase the index line of TextLine to read the second line in next step
            else:
                    _translate = QtCore.QCoreApplication.translate
                    self.Error.setText(_translate("OXCART",
                                                  "<html><head/><body><p><span style=\" color:#ff0000;\">!!! First Close all "
                                                  "Gates !!!</span></p></body></html>"))

    def finished_thread_main(self, ):
            """
                The function that is run after end of experiment(MainThread)
                """
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            QScreen.grabWindow(self.app.primaryScreen(),
                               QApplication.desktop().winId()).save(variables.path + '\screenshot.png')
            if variables.index_line < self.num_line:  # Do next experiment in case of TextLine
                    self.thread_main()
            else:
                    variables.index_line = 0

    def stop_ex(self):
            """
                The function that is run if STOP button is pressed
                """
            if variables.start_flag == True:
                    variables.stop_flag = True  # Set the STOP flag
                    self.stop_button.setEnabled(False)  # Disable the stop button

    def gates(self, gate_num):
            """
                The function for closing or opening gates
                """

            def switch_gate(num):
                    """
                            The function for applying the command of closing or opening gate
                            """
                    with nidaqmx.Task() as task:
                            if self.conf['gates'] != "off":
                                    task.do_channels.add_do_chan(self.conf['COM_PORT_gates'] + 'line%s' % num)
                                    task.start()
                                    task.write([True])
                                    time.sleep(.5)
                                    task.write([False])
                            else:
                                    print('The gates control is off')

            # Main gate
            if not variables.start_flag and gate_num == 1 and not variables.flag_load_gate and not variables.flag_cryo_gate and variables.flag_pump_load_lock:
                    if not variables.flag_main_gate:  # Open the main gate
                            switch_gate(0)
                            self.led_main_chamber.setPixmap(self.led_green)
                            self.diagram.setPixmap(self.diagram_main_open)
                            variables.flag_main_gate = True
                    elif variables.flag_main_gate:  # Close the main gate
                            switch_gate(1)
                            self.led_main_chamber.setPixmap(self.led_red)
                            self.diagram.setPixmap(self.diagram_close_all)
                            variables.flag_main_gate = False
            # Buffer gate
            elif not variables.start_flag and gate_num == 2 and not variables.flag_main_gate and not variables.flag_cryo_gate and variables.flag_pump_load_lock:
                    if not variables.flag_load_gate:  # Open the main gate
                            switch_gate(2)
                            self.led_load_lock.setPixmap(self.led_green)
                            self.diagram.setPixmap(self.diagram_load_open)
                            variables.flag_load_gate = True
                    elif variables.flag_load_gate:  # Close the main gate
                            switch_gate(3)
                            self.led_load_lock.setPixmap(self.led_red)
                            self.diagram.setPixmap(self.diagram_close_all)
                            variables.flag_load_gate = False
            # Cryo gate
            elif not variables.start_flag and gate_num == 3 and not variables.flag_main_gate and not variables.flag_load_gate and variables.flag_pump_load_lock:
                    if not variables.flag_cryo_gate:  # Open the main gate
                            switch_gate(4)
                            self.led_cryo.setPixmap(self.led_green)
                            self.diagram.setPixmap(self.diagram_cryo_open)
                            variables.flag_cryo_gate = True
                    elif variables.flag_cryo_gate:  # Close the main gate
                            switch_gate(5)
                            self.led_cryo.setPixmap(self.led_red)
                            self.diagram.setPixmap(self.diagram_close_all)
                            variables.flag_cryo_gate = False
            # Show the error message in the GUI
            else:
                    _translate = QtCore.QCoreApplication.translate
                    self.Error.setText(_translate("OXCART",
                                                  "<html><head/><body><p><span style=\" color:#ff0000;\">!!! First Close all "
                                                  "the Gates and switch on the pump !!!</span></p></body></html>"))

    def pump_switch(self):
            """
                The function for Switching the Load Lock pump
                """
            if not variables.start_flag and not variables.flag_main_gate and not variables.flag_cryo_gate \
                    and not variables.flag_load_gate:
                    if variables.flag_pump_load_lock:
                            variables.flag_pump_load_lock_click = True
                            self.pump_load_lock_switch.setEnabled(False)
                    elif not variables.flag_pump_load_lock:
                            variables.flag_pump_load_lock_click = True
                            self.pump_load_lock_switch.setEnabled(False)
            else:  # SHow error message in the GUI
                    _translate = QtCore.QCoreApplication.translate
                    self.Error.setText(_translate("OXCART",
                                                  "<html><head/><body><p><span style=\" color:#ff0000;\">!!! First Close all "
                                                  "the Gates !!!</span></p></body></html>"))

    def light_switch(self):
            """
                The function for switching the exposure time of cameras in case of swithching the light
                """
            if not variables.light:
                    self.led_light.setPixmap(self.led_green)
                    Camera.light_switch(self)
                    self.timer1.setInterval(500)
                    variables.light = True
                    variables.sample_adjust = True
                    variables.light_swich = True
            elif variables.light:
                    self.led_light.setPixmap(self.led_red)
                    Camera.light_switch(self)
                    self.timer1.setInterval(500)
                    variables.light = False
                    variables.sample_adjust = False
                    variables.light_swich = False

    def thread_worker(self, target):
            """
                The function for creating workers
                """
            return threading.Thread(target=target)

    def update_plot_data(self):
            """
                The function for updating plots
            """
            if self.conf['pump'] == "off":
                    self.pump_load_lock_switch.setEnabled(False)
            if self.conf['gates'] == "off":
                    self.main_chamber_switch.setEnabled(False)
                    self.load_lock_switch.setEnabled(False)
                    self.cryo_switch.setEnabled(False)
            # Temperature
            self.x_tem = self.x_tem[1:]  # Remove the first element.
            self.x_tem = np.append(self.x_tem, self.x_tem[-1] + 1)  # Add a new value 1 higher than the last.
            self.y_tem = self.y_tem[1:]  # Remove the first element.
            try:
                    self.y_tem = np.append(self.y_tem, int(variables.temperature))
                    self.data_line_tem.setData(self.x_tem, self.y_tem)
            except Exception as e:
                    print(
                            f"{initialize_devices.bcolors.FAIL}Error: Cannot read the temperature{initialize_devices.bcolors.ENDC}")
                    print(e)
            if variables.index_auto_scale_graph == 30:
                    self.temperature.enableAutoRange(axis='x')
                    self.vdc_time.enableAutoRange(axis='x')
                    self.detection_rate_viz.enableAutoRange(axis='x')
                    variables.index_auto_scale_graph = 0

            self.temperature.disableAutoRange()
            self.vdc_time.disableAutoRange()
            self.detection_rate_viz.disableAutoRange()

            variables.index_auto_scale_graph += 1

            if variables.plot_clear_flag:
                    self.x_vdc = np.arange(1000)  # 1000 time points
                    self.y_vdc = np.zeros(1000)  # 1000 data points
                    self.y_vdc[:] = np.nan
                    self.y_vps = np.zeros(1000)  # 1000 data points
                    self.y_vps[:] = np.nan

                    self.data_line_vdc.setData(self.x_vdc, self.y_vdc)
                    self.data_line_vps.setData(self.x_vdc, self.y_vps)

                    self.x_dtec = np.arange(1000)
                    self.y_dtec = np.zeros(1000)
                    self.y_dtec[:] = np.nan

                    self.data_line_dtec.setData(self.x_dtec, self.y_dtec)

                    self.histogram.clear()

                    self.scatter.clear()
                    self.visualization.clear()
                    self.visualization.addItem(self.detector_circle)
                    variables.plot_clear_flag = False

                    variables.specimen_voltage = 0
                    variables.pulse_voltage = 0
                    variables.elapsed_time = 0
                    variables.total_ions = 0
                    variables.avg_n_count = 0

            if variables.start_flag:
                    if variables.index_wait_on_plot_start <= 16:
                            variables.index_wait_on_plot_start += 1

                    if variables.index_wait_on_plot_start >= 8:
                            # V_dc and V_p
                            if variables.index_plot <= 999:
                                    self.y_vdc[variables.index_plot] = int(
                                            variables.specimen_voltage)  # Add a new value.
                                    self.y_vps[variables.index_plot] = int(variables.pulse_voltage)  # Add a new value.
                            else:
                                    self.x_vdc = np.append(self.x_vdc,
                                                           self.x_vdc[
                                                                   -1] + 1)  # Add a new value 1 higher than the last.
                                    self.y_vdc = np.append(self.y_vdc,
                                                           int(variables.specimen_voltage))  # Add a new value.
                                    self.y_vps = np.append(self.y_vps, int(variables.pulse_voltage))  # Add a new value.

                            self.data_line_vdc.setData(self.x_vdc, self.y_vdc)
                            self.data_line_vps.setData(self.x_vdc, self.y_vps)

                            # Detection Rate Visualization
                            if variables.index_plot <= 999:
                                    self.y_dtec[variables.index_plot] = int(variables.avg_n_count)  # Add a new value.
                            else:
                                    self.x_dtec = self.x_dtec[1:]  # Remove the first element.
                                    self.x_dtec = np.append(self.x_dtec,
                                                            self.x_dtec[
                                                                    -1] + 1)  # Add a new value 1 higher than the last.
                                    self.y_dtec = self.y_dtec[1:]
                                    self.y_dtec = np.append(self.y_dtec, int(variables.avg_n_count))

                            self.data_line_dtec.setData(self.x_dtec, self.y_dtec)
                            # Increase the index
                            variables.index_plot += 1
                    # Time of Flight
                    if variables.counter_source == 'TDC' and variables.total_ions > 0 and variables.index_wait_on_plot_start > 16 \
                            and variables.index_wait_on_plot_start > 16 and not variables.raw_mode:
                            if variables.index_wait_on_plot_start > 16:

                                    try:
                                            def replaceZeroes(data):
                                                    min_nonzero = np.min(data[np.nonzero(data)])
                                                    data[data == 0] = min_nonzero
                                                    return data

                                            if self.conf["visualization"] == 'tof':
                                                    tof = variables.t * 27.432 / (1000 * 4)  # Time in ns
                                                    viz = tof[tof < 5000]
                                            elif self.conf["visualization"] == 'mc':
                                                    max_lenght = max(len(variables.x), len(variables.y),
                                                                     len(variables.t), len(variables.main_v_dc_dld))
                                                    viz = tof2mc_simple.tof_bin2mc(variables.t[:max_lenght], 0,
                                                                                   variables.main_v_dc_dld[
                                                                                   :max_lenght],
                                                                                   variables.x[:max_lenght],
                                                                                   variables.x[:max_lenght],
                                                                                   flightPathLength=110)
                                                    viz = viz[viz < 200]

                                            self.y_tof, self.x_tof = np.histogram(viz, bins=512)
                                            self.histogram.clear()
                                            self.y_tof = replaceZeroes(self.y_tof)
                                            self.histogram.addItem(
                                                    pg.BarGraphItem(x=self.x_tof[:-1], height=np.log(self.y_tof),
                                                                    width=0.1, brush='r'))

                                    except Exception as e:
                                            print(
                                                    f"{initialize_devices.bcolors.FAIL}Error: Cannot plot Histogram correctly{initialize_devices.bcolors.ENDC}")
                                            print(e)
                                    # Visualization
                                    try:
                                            # adding points to the scatter plot
                                            self.scatter.clear()
                                            self.scatter.setSize(self.doubleSpinBox.value())
                                            x = variables.x
                                            y = variables.y
                                            min_length = min(len(x), len(y))
                                            x = variables.x[-min_length:]
                                            y = variables.y[-min_length:]
                                            self.scatter.setData(x=x[-variables.hit_display:],
                                                                 y=y[-variables.hit_display:])
                                            # add item to plot window
                                            # adding scatter plot item to the plot window
                                            self.visualization.clear()
                                            self.visualization.addItem(self.scatter)
                                            self.visualization.addItem(self.detector_circle)
                                    except Exception as e:
                                            print(
                                                    f"{initialize_devices.FAIL}Error: Cannot plot Ions correctly{initialize_devices.bcolors.ENDC}")
                                            print(e)
                    # save plots to the file
                    if variables.index_plot_save % 100 == 0:
                            exporter = pg.exporters.ImageExporter(self.vdc_time.plotItem)
                            exporter.export(variables.path + '/v_dc_p_%s.png' % variables.index_plot_save)
                            exporter = pg.exporters.ImageExporter(self.detection_rate_viz.plotItem)
                            exporter.export(variables.path + '/detection_rate_%s.png' % variables.index_plot_save)
                            exporter = pg.exporters.ImageExporter(self.visualization.plotItem)
                            exporter.export(variables.path + '/visualization_%s.png' % variables.index_plot_save)
                            exporter = pg.exporters.ImageExporter(self.histogram.plotItem)
                            exporter.export(variables.path + '/tof_%s.png' % variables.index_plot_save)

                    # Increase the index
                    variables.index_plot_save += 1

            # Statistics Update
            self.speciemen_voltage.setText(str(float("{:.3f}".format(variables.specimen_voltage))))
            self.pulse_voltage.setText(str(float("{:.3f}".format(variables.pulse_voltage))))
            self.elapsed_time.setText(str(float("{:.3f}".format(variables.elapsed_time))))
            self.total_ions.setText((str(variables.total_ions)))
            self.detection_rate.setText(str
                    (float("{:.3f}".format(
                    (variables.avg_n_count * 100) / (1 + variables.pulse_frequency * 1000)))))

    def statistics(self):
            """
                The function for updating statistics in the GUI
                """
            # update temperature and vacuum gages
            self.temp.display(variables.temperature)
            self.vacuum_main.display(variables.vacuum_main)
            self.vacuum_buffer.display('{:.2e}'.format(float(variables.vacuum_buffer)))
            self.vacuum_buffer_back.display('{:.2e}'.format(variables.vacuum_buffer_backing))
            self.vacuum_load_lock.display('{:.2e}'.format(variables.vacuum_load_lock))
            self.vacuum_load_lock_back.display('{:.2e}'.format(variables.vacuum_load_lock_backing))
            if variables.flag_pump_load_lock_led == False:
                    self.led_pump_load_lock.setPixmap(self.led_red)
                    self.pump_load_lock_switch.setEnabled(True)
                    variables.flag_pump_load_lock_led = None
            elif variables.flag_pump_load_lock_led == True:
                    self.led_pump_load_lock.setPixmap(self.led_green)
                    self.pump_load_lock_switch.setEnabled(True)
                    variables.flag_pump_load_lock_led = None

            # Clean up the error message
            if variables.index_warning_message == 15:
                    _translate = QtCore.QCoreApplication.translate
                    self.Error.setText(_translate("OXCART",
                                                  "<html><head/><body><p><span style=\" "
                                                  "color:#ff0000;\"></span></p></body></html>"))
                    variables.index_warning_message = 0

            variables.index_warning_message += 1

            try:
                    # Update the setup parameters
                    variables.ex_time = int(float(self.ex_time.text()))
                    variables.user_name = self.ex_user.text()
                    variables.ex_freq = int(float(self.ex_freq.text()))
                    variables.max_ions = int(float(self.max_ions.text()))
                    variables.vdc_min = int(float(self.vdc_min.text()))
                    variables.detection_rate = float(self.detection_rate_init.text())
                    variables.hit_display = int(float(self.hit_displayed.text()))
                    variables.pulse_fraction = int(float(self.pulse_fraction.text())) / 100
                    variables.pulse_frequency = float(self.pulse_frequency.text())
                    variables.hdf5_path = self.ex_name.text()
                    variables.email = self.email.text()
                    variables.cycle_avg = int(float(self.cycle_avg.text()))
                    variables.vdc_step_up = int(float(self.vdc_steps_up.text()))
                    variables.vdc_step_down = int(float(self.vdc_steps_down.text()))
                    variables.v_p_min = int(float(self.vp_min.text()))
                    variables.v_p_max = int(float(self.vp_max.text()))
                    variables.counter_source = str(self.counter_source.currentText())

                    if variables.counter_source == 'Pulse Counter':
                            variables.counter_source = 'pulse_counter'

                    if self.tweet.currentText() == 'Yes':
                            variables.tweet = True
                    elif self.tweet.currentText() == 'No':
                            variables.tweet = False

                    if self.criteria_time.isChecked():
                            variables.criteria_time = True
                    elif not self.criteria_time.isChecked():
                            variables.criteria_time = False
                    if self.criteria_ions.isChecked():
                            variables.criteria_ions = True
                    elif not self.criteria_ions.isChecked():
                            variables.criteria_ions = False
                    if self.criteria_vdc.isChecked():
                            variables.criteria_vdc = True
                    elif not self.criteria_vdc.isChecked():
                            variables.criteria_vdc = False

                    # Show error message for V_dc higher than 20Kv
                    if int(float(self.vdc_max.text())) > 20000:
                            _translate = QtCore.QCoreApplication.translate
                            self.Error.setText(_translate("OXCART",
                                                          "<html><head/><body><p><span style=\" color:#ff0000;\">Maximum possible "
                                                          "number is 20KV</span></p></body></html>"))
                            self.vdc_max.setText(_translate("OXCART", str(variables.vdc_max)))
                    else:
                            variables.vdc_max = int(float(self.vdc_max.text()))
                    # Show error message for V_p higher than 3281
                    if float(self.vp_max.text()) > 3281:
                            _translate = QtCore.QCoreApplication.translate
                            self.Error.setText(_translate("OXCART",
                                                          "<html><head/><body><p><span style=\" color:#ff0000;\">Maximum possible "
                                                          "number is 3281 V</span></p></body></html>"))
                            self.vp_max.setText(_translate("OXCART", str(variables.v_p_max)))
                    else:
                            variables.v_p_max = int(float(self.vp_max.text()))

            except Exception as e:
                    print(
                            f"{initialize_devices.bcolors.FAIL}Error: Cannot update setup parameters{initialize_devices.bcolors.ENDC}")
                    print(e)

    def update_cameras(self, ):
            """
                The function for updating cameras in the GUI
                """
            self.cam_s_o.setImage(variables.img0_orig, autoRange=False)
            self.cam_b_o.setImage(variables.img1_orig, autoRange=False)

            self.camera0_zoom = QImage(variables.img0_zoom, 1200, 500, QImage.Format_RGB888)
            self.camera1_zoom = QImage(variables.img1_zoom, 1200, 500, QImage.Format_RGB888)

            self.camera0_zoom = QtGui.QPixmap(self.camera0_zoom)
            self.camera1_zoom = QtGui.QPixmap(self.camera1_zoom)

            self.cam_s_d.setPixmap(self.camera0_zoom)
            self.cam_b_d.setPixmap(self.camera1_zoom)

class MainThread(QThread):
    """
    A class for creating main_thread
    The run method create thread of main function in the OXCART script
    """
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, conf):
            QThread.__init__(self, )
            self.conf = conf

    def run(self):
            main_thread = apt_tdc_surface_consept.main(self.conf)
            self.signal.emit(main_thread)


