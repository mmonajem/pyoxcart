"""
This is the main script of main GUI of the OXCART Atom Probe.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""

import sys
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
# Serial ports and Camera libraries
import serial.tools.list_ports
from pypylon import pylon
# Local project scripts
import oxcart
import variables
from devices.camera import Camera
from devices import initialize_devices


class Ui_OXCART(Camera, object):
    """
    The GUI class of the Oxcart
    """
    def __init__(self, devices, tlFactory, cameras, converter, lock):
        super().__init__(devices, tlFactory, cameras, converter) # Cameras variables and converter
        self.lock = lock # Lock for thread ...

    def setupUi(self, OXCART):
        OXCART.setObjectName("OXCART")
        OXCART.resize(3400, 1800)
        self.centralwidget = QtWidgets.QWidget(OXCART)
        self.centralwidget.setObjectName("centralwidget")
        # self.vdc_time = QtWidgets.QWidget(self.centralwidget)
        self.vdc_time = pg.PlotWidget(self.centralwidget)
        self.vdc_time.setGeometry(QtCore.QRect(530, 260, 500, 500))
        self.vdc_time.setObjectName("vdc_time")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(730, 210, 80, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(3030, 1520, 314, 106))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.start_button = QtWidgets.QPushButton(self.layoutWidget)
        self.start_button.setObjectName("start_button")
        self.gridLayout_2.addWidget(self.start_button, 1, 0, 1, 1)
        self.stop_button = QtWidgets.QPushButton(self.layoutWidget)
        self.stop_button.setObjectName("stop_button")
        self.gridLayout_2.addWidget(self.stop_button, 2, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(1230, 210, 156, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        # self.detection_rate_viz = QtWidgets.QWidget(self.centralwidget)
        self.detection_rate_viz = pg.PlotWidget(self.centralwidget)
        self.detection_rate_viz.setGeometry(QtCore.QRect(1080, 260, 500, 500))
        self.detection_rate_viz.setObjectName("detection_rate_viz")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(710, 830, 134, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        # self.visualization = QtWidgets.QWidget(self.centralwidget)
        self.visualization = pg.PlotWidget(self.centralwidget)
        self.visualization.setGeometry(QtCore.QRect(530, 870, 500, 500))
        self.visualization.setObjectName("visualization")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(1280, 820, 51, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        # self.temperature = QtWidgets.QWidget(self.centralwidget)
        self.temperature = pg.PlotWidget(self.centralwidget)
        self.temperature.setGeometry(QtCore.QRect(2530, 1400, 411, 311))
        self.temperature.setObjectName("temperature")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(10, 1130, 101, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.Error = QtWidgets.QLabel(self.centralwidget)
        self.Error.setGeometry(QtCore.QRect(530, 1400, 1241, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.Error.setFont(font)
        self.Error.setAlignment(QtCore.Qt.AlignCenter)
        self.Error.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.Error.setObjectName("Error")
        self.diagram = QtWidgets.QLabel(self.centralwidget)
        self.diagram.setGeometry(QtCore.QRect(10, 1170, 491, 391))
        self.diagram.setText("")
        self.diagram.setObjectName("diagram")
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        self.label_29.setGeometry(QtCore.QRect(1810, 830, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.centralwidget)
        self.label_30.setGeometry(QtCore.QRect(1810, 230, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.centralwidget)
        self.label_31.setGeometry(QtCore.QRect(2700, 840, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.centralwidget)
        self.label_32.setGeometry(QtCore.QRect(2700, 220, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.centralwidget)
        self.label_33.setGeometry(QtCore.QRect(2220, 800, 171, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.label_34 = QtWidgets.QLabel(self.centralwidget)
        self.label_34.setGeometry(QtCore.QRect(2200, 190, 171, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")
        self.light = QtWidgets.QPushButton(self.centralwidget)
        self.light.setGeometry(QtCore.QRect(3120, 50, 101, 46))
        self.light.setObjectName("light")
        self.led_light = QtWidgets.QLabel(self.centralwidget)
        self.led_light.setGeometry(QtCore.QRect(3240, 40, 111, 61))
        self.led_light.setAlignment(QtCore.Qt.AlignCenter)
        self.led_light.setObjectName("led_light")
        self.vacuum_main = QtWidgets.QLCDNumber(self.centralwidget)
        self.vacuum_main.setGeometry(QtCore.QRect(2270, 1510, 231, 91))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.vacuum_main.setFont(font)
        self.vacuum_main.setObjectName("vacuum_main")
        self.vacuum_buffer = QtWidgets.QLCDNumber(self.centralwidget)
        self.vacuum_buffer.setGeometry(QtCore.QRect(1780, 1500, 231, 91))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.vacuum_buffer.setFont(font)
        self.vacuum_buffer.setObjectName("vacuum_buffer")
        self.vacuum_load_lock = QtWidgets.QLCDNumber(self.centralwidget)
        self.vacuum_load_lock.setGeometry(QtCore.QRect(1190, 1500, 231, 91))
        self.vacuum_load_lock.setObjectName("vacuum_load_lock")
        self.label_35 = QtWidgets.QLabel(self.centralwidget)
        self.label_35.setGeometry(QtCore.QRect(2020, 1540, 241, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_35.setFont(font)
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.centralwidget)
        self.label_36.setGeometry(QtCore.QRect(1490, 1540, 251, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.centralwidget)
        self.label_37.setGeometry(QtCore.QRect(980, 1540, 181, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.centralwidget)
        self.label_38.setGeometry(QtCore.QRect(2050, 1650, 191, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.temp = QtWidgets.QLCDNumber(self.centralwidget)
        self.temp.setGeometry(QtCore.QRect(2270, 1620, 231, 91))
        self.temp.setObjectName("temp")
        ####
        # self.cam_s_o = QtWidgets.QLabel(self.centralwidget)
        self.cam_s_o = pg.ImageView(self.centralwidget)
        self.cam_s_o.adjustSize()
        self.cam_s_o.ui.histogram.hide()
        self.cam_s_o.ui.roiBtn.hide()
        self.cam_s_o.ui.menuBtn.hide()
        self.cam_s_o.setGeometry(QtCore.QRect(1630, 260, 500, 500))
        # self.cam_s_o.setText("")
        self.cam_s_o.setObjectName("cam_s_o")
        # self.cam_b_o = QtWidgets.QLabel(self.centralwidget)
        self.cam_b_o = pg.ImageView(self.centralwidget)
        self.cam_b_o.adjustSize()
        self.cam_b_o.ui.histogram.hide()
        self.cam_b_o.ui.roiBtn.hide()
        self.cam_b_o.ui.menuBtn.hide()
        self.cam_b_o.setGeometry(QtCore.QRect(1630, 870, 500, 500))
        # self.cam_b_o.setText("")
        ####
        self.cam_b_o.setObjectName("cam_b_o")
        self.cam_s_d = QtWidgets.QLabel(self.centralwidget)
        self.cam_s_d.setGeometry(QtCore.QRect(2150, 260, 1200, 500))
        self.cam_s_d.setText("")
        self.cam_s_d.setObjectName("cam_s_d")
        self.cam_b_d = QtWidgets.QLabel(self.centralwidget)
        self.cam_b_d.setGeometry(QtCore.QRect(2150, 870, 1200, 500))
        self.cam_b_d.setText("")
        self.cam_b_d.setObjectName("cam_b_d")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(650, 1580, 235, 131))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.led_pump_load_lock = QtWidgets.QLabel(self.layoutWidget1)
        self.led_pump_load_lock.setAlignment(QtCore.Qt.AlignCenter)
        self.led_pump_load_lock.setObjectName("led_pump_load_lock")
        self.gridLayout_6.addWidget(self.led_pump_load_lock, 0, 0, 2, 1)
        self.pump_load_lock_switch = QtWidgets.QPushButton(self.layoutWidget1)
        self.pump_load_lock_switch.setObjectName("pump_load_lock_switch")
        self.gridLayout_6.addWidget(self.pump_load_lock_switch, 2, 0, 1, 1)
        # self.histogram = QtWidgets.QWidget(self.centralwidget)
        self.histogram = pg.PlotWidget(self.centralwidget)
        self.histogram.setGeometry(QtCore.QRect(1080, 870, 500, 500))
        self.histogram.setObjectName("histogram")
        self.label_40 = QtWidgets.QLabel(self.centralwidget)
        self.label_40.setGeometry(QtCore.QRect(1480, 1640, 291, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_40.setFont(font)
        self.label_40.setObjectName("label_40")
        self.vacuum_buffer_back = QtWidgets.QLCDNumber(self.centralwidget)
        self.vacuum_buffer_back.setGeometry(QtCore.QRect(1780, 1610, 231, 91))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.vacuum_buffer_back.setFont(font)
        self.vacuum_buffer_back.setObjectName("vacuum_buffer_back")
        self.vacuum_load_lock_back = QtWidgets.QLCDNumber(self.centralwidget)
        self.vacuum_load_lock_back.setGeometry(QtCore.QRect(1190, 1610, 231, 91))
        self.vacuum_load_lock_back.setObjectName("vacuum_load_lock_back")
        self.label_39 = QtWidgets.QLabel(self.centralwidget)
        self.label_39.setGeometry(QtCore.QRect(950, 1640, 231, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_39.setFont(font)
        self.label_39.setObjectName("label_39")
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 1580, 476, 131))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.led_main_chamber = QtWidgets.QLabel(self.layoutWidget2)
        self.led_main_chamber.setAlignment(QtCore.Qt.AlignCenter)
        self.led_main_chamber.setObjectName("led_main_chamber")
        self.gridLayout.addWidget(self.led_main_chamber, 0, 0, 1, 1)
        self.led_load_lock = QtWidgets.QLabel(self.layoutWidget2)
        self.led_load_lock.setAlignment(QtCore.Qt.AlignCenter)
        self.led_load_lock.setObjectName("led_load_lock")
        self.gridLayout.addWidget(self.led_load_lock, 0, 1, 1, 1)
        self.led_cryo = QtWidgets.QLabel(self.layoutWidget2)
        self.led_cryo.setAlignment(QtCore.Qt.AlignCenter)
        self.led_cryo.setObjectName("led_cryo")
        self.gridLayout.addWidget(self.led_cryo, 0, 2, 1, 1)
        self.main_chamber_switch = QtWidgets.QPushButton(self.layoutWidget2)
        self.main_chamber_switch.setObjectName("main_chamber_switch")
        self.gridLayout.addWidget(self.main_chamber_switch, 1, 0, 1, 1)
        self.load_lock_switch = QtWidgets.QPushButton(self.layoutWidget2)
        self.load_lock_switch.setObjectName("load_lock_switch")
        self.gridLayout.addWidget(self.load_lock_switch, 1, 1, 1, 1)
        self.cryo_switch = QtWidgets.QPushButton(self.layoutWidget2)
        self.cryo_switch.setObjectName("cryo_switch")
        self.gridLayout.addWidget(self.cryo_switch, 1, 2, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(530, 30, 2581, 140))
        self.textEdit.setObjectName("textEdit")
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 880, 436, 242))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_11 = QtWidgets.QLabel(self.layoutWidget3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_4.addWidget(self.label_11, 0, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)
        self.elapsed_time = QtWidgets.QLineEdit(self.layoutWidget3)
        self.elapsed_time.setText("")
        self.elapsed_time.setObjectName("elapsed_time")
        self.gridLayout_4.addWidget(self.elapsed_time, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 2, 0, 1, 1)
        self.total_ions = QtWidgets.QLineEdit(self.layoutWidget3)
        self.total_ions.setText("")
        self.total_ions.setObjectName("total_ions")
        self.gridLayout_4.addWidget(self.total_ions, 2, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 3, 0, 1, 1)
        self.speciemen_voltage = QtWidgets.QLineEdit(self.layoutWidget3)
        self.speciemen_voltage.setText("")
        self.speciemen_voltage.setObjectName("speciemen_voltage")
        self.gridLayout_4.addWidget(self.speciemen_voltage, 3, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_16.setObjectName("label_16")
        self.gridLayout_4.addWidget(self.label_16, 4, 0, 1, 1)
        self.pulse_voltage = QtWidgets.QLineEdit(self.layoutWidget3)
        self.pulse_voltage.setText("")
        self.pulse_voltage.setObjectName("pulse_voltage")
        self.gridLayout_4.addWidget(self.pulse_voltage, 4, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 5, 0, 1, 1)
        self.detection_rate = QtWidgets.QLineEdit(self.layoutWidget3)
        self.detection_rate.setText("")
        self.detection_rate.setObjectName("detection_rate")
        self.gridLayout_4.addWidget(self.detection_rate, 5, 1, 1, 1)
        self.layoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(10, 13, 488, 850))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget4)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.layoutWidget4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.parameters_source = QtWidgets.QComboBox(self.layoutWidget4)
        self.parameters_source.setObjectName("parameters_source")
        self.parameters_source.addItem("")
        self.parameters_source.addItem("")
        self.gridLayout_3.addWidget(self.parameters_source, 0, 1, 1, 1)
        self.label_43 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_43.setObjectName("label_43")
        self.gridLayout_3.addWidget(self.label_43, 1, 0, 1, 1)
        self.ex_user = QtWidgets.QLineEdit(self.layoutWidget4)
        self.ex_user.setObjectName("ex_user")
        self.gridLayout_3.addWidget(self.ex_user, 1, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_21.setObjectName("label_21")
        self.gridLayout_3.addWidget(self.label_21, 2, 0, 1, 1)
        self.ex_name = QtWidgets.QLineEdit(self.layoutWidget4)
        self.ex_name.setObjectName("ex_name")
        self.gridLayout_3.addWidget(self.ex_name, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 3, 0, 1, 1)
        self.ex_time = QtWidgets.QLineEdit(self.layoutWidget4)
        self.ex_time.setObjectName("ex_time")
        self.gridLayout_3.addWidget(self.ex_time, 3, 1, 1, 1)
        self.label_41 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_41.setObjectName("label_41")
        self.gridLayout_3.addWidget(self.label_41, 4, 0, 1, 1)
        self.max_ions = QtWidgets.QLineEdit(self.layoutWidget4)
        self.max_ions.setObjectName("max_ions")
        self.gridLayout_3.addWidget(self.max_ions, 4, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 5, 0, 1, 1)
        self.ex_freq = QtWidgets.QLineEdit(self.layoutWidget4)
        self.ex_freq.setObjectName("ex_freq")
        self.gridLayout_3.addWidget(self.ex_freq, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 6, 0, 1, 1)
        self.vdc_min = QtWidgets.QLineEdit(self.layoutWidget4)
        self.vdc_min.setObjectName("vdc_min")
        self.gridLayout_3.addWidget(self.vdc_min, 6, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 7, 0, 1, 1)
        self.vdc_max = QtWidgets.QLineEdit(self.layoutWidget4)
        self.vdc_max.setObjectName("vdc_max")
        self.gridLayout_3.addWidget(self.vdc_max, 7, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 8, 0, 1, 1)
        self.vdc_steps_up = QtWidgets.QLineEdit(self.layoutWidget4)
        self.vdc_steps_up.setObjectName("vdc_steps_up")
        self.gridLayout_3.addWidget(self.vdc_steps_up, 8, 1, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_28.setObjectName("label_28")
        self.gridLayout_3.addWidget(self.label_28, 9, 0, 1, 1)
        self.vdc_steps_down = QtWidgets.QLineEdit(self.layoutWidget4)
        self.vdc_steps_down.setObjectName("vdc_steps_down")
        self.gridLayout_3.addWidget(self.vdc_steps_down, 9, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 10, 0, 1, 1)
        self.cycle_avg = QtWidgets.QLineEdit(self.layoutWidget4)
        self.cycle_avg.setObjectName("cycle_avg")
        self.gridLayout_3.addWidget(self.cycle_avg, 10, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 11, 0, 1, 1)
        self.vp_min = QtWidgets.QLineEdit(self.layoutWidget4)
        self.vp_min.setObjectName("vp_min")
        self.gridLayout_3.addWidget(self.vp_min, 11, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 12, 0, 1, 1)
        self.vp_max = QtWidgets.QLineEdit(self.layoutWidget4)
        self.vp_max.setObjectName("vp_max")
        self.gridLayout_3.addWidget(self.vp_max, 12, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_25.setObjectName("label_25")
        self.gridLayout_3.addWidget(self.label_25, 13, 0, 1, 1)
        self.pulse_fraction = QtWidgets.QLineEdit(self.layoutWidget4)
        self.pulse_fraction.setObjectName("pulse_fraction")
        self.gridLayout_3.addWidget(self.pulse_fraction, 13, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_23.setObjectName("label_23")
        self.gridLayout_3.addWidget(self.label_23, 14, 0, 1, 1)
        self.pulse_frequency = QtWidgets.QLineEdit(self.layoutWidget4)
        self.pulse_frequency.setObjectName("pulse_frequency")
        self.gridLayout_3.addWidget(self.pulse_frequency, 14, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 15, 0, 1, 1)
        self.detection_rate_init = QtWidgets.QLineEdit(self.layoutWidget4)
        self.detection_rate_init.setObjectName("detection_rate_init")
        self.gridLayout_3.addWidget(self.detection_rate_init, 15, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 16, 0, 1, 1)
        self.hit_displayed = QtWidgets.QLineEdit(self.layoutWidget4)
        self.hit_displayed.setObjectName("hit_displayed")
        self.gridLayout_3.addWidget(self.hit_displayed, 16, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_26.setObjectName("label_26")
        self.gridLayout_3.addWidget(self.label_26, 17, 0, 1, 1)
        self.email = QtWidgets.QLineEdit(self.layoutWidget4)
        self.email.setText("")
        self.email.setObjectName("email")
        self.gridLayout_3.addWidget(self.email, 17, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_27.setObjectName("label_27")
        self.gridLayout_3.addWidget(self.label_27, 18, 0, 1, 1)
        self.tweet = QtWidgets.QComboBox(self.layoutWidget4)
        self.tweet.setObjectName("tweet")
        self.tweet.addItem("")
        self.tweet.addItem("")
        self.gridLayout_3.addWidget(self.tweet, 18, 1, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_42.setObjectName("label_42")
        self.gridLayout_3.addWidget(self.label_42, 19, 0, 1, 1)
        self.counter_source = QtWidgets.QComboBox(self.layoutWidget4)
        self.counter_source.setObjectName("counter_source")
        self.counter_source.addItem("")
        self.counter_source.addItem("")
        self.gridLayout_3.addWidget(self.counter_source, 19, 1, 1, 1)
        OXCART.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(OXCART)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 3400, 38))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        OXCART.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(OXCART)
        self.statusbar.setObjectName("statusbar")
        OXCART.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(OXCART)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(OXCART)
        QtCore.QMetaObject.connectSlotsByName(OXCART)

        #### Set 8 digits for each LCD to show
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
        ####

    def retranslateUi(self, OXCART):
        _translate = QtCore.QCoreApplication.translate
        OXCART.setWindowTitle(_translate("OXCART", "OXCART"))
        self.label_7.setText(_translate("OXCART", "Voltage"))
        self.start_button.setText(_translate("OXCART", "Start"))
        ###
        self._translate = QtCore.QCoreApplication.translate
        self.start_button.clicked.connect(self.thread_main)
        self.thread = MainThread()
        self.thread.signal.connect(self.finished_thread_main)
        self.stop_button.setText(_translate("OXCART", "Stop"))
        self.stop_button.clicked.connect(self.stop_ex)
        ###
        self.label_10.setText(_translate("OXCART", "Detection Rate"))
        self.label_19.setText(_translate("OXCART", "Visualization"))
        self.label_24.setText(_translate("OXCART", "TOF"))
        self.label_18.setText(_translate("OXCART", "Diagram"))
        self.Error.setText(_translate("OXCART", "<html><head/><body><p><br/></p></body></html>"))
        self.label_29.setText(_translate("OXCART", "Overview"))
        self.label_30.setText(_translate("OXCART", "Overview"))
        self.label_31.setText(_translate("OXCART", "Detail"))
        self.label_32.setText(_translate("OXCART", "Detail"))
        self.label_33.setText(_translate("OXCART", "Camera Bottom"))
        self.label_34.setText(_translate("OXCART", "Camera Side"))
        self.light.setText(_translate("OXCART", "Light"))
        self.led_light.setText(_translate("OXCART", "light"))
        self.label_35.setText(_translate("OXCART", "Main Chamber (mBar)"))
        self.label_36.setText(_translate("OXCART", "Buffer Chamber (mBar)"))
        self.label_37.setText(_translate("OXCART", "Load lock (mBar)"))
        ###
        self.main_chamber_switch.clicked.connect(lambda: self.gates(1))
        self.load_lock_switch.clicked.connect(lambda: self.gates(2))
        self.cryo_switch.clicked.connect(lambda: self.gates(3))
        self.light.clicked.connect(lambda: self.light_switch())
        self.pump_load_lock_switch.clicked.connect(lambda: self.pump_switch())
        ###
        self.label_38.setText(_translate("OXCART", "Temperature (K)"))
        self.led_pump_load_lock.setText(_translate("OXCART", "pump"))
        self.pump_load_lock_switch.setText(_translate("OXCART", "Load Lock Pump"))
        self.label_40.setText(_translate("OXCART", "Buffer Chamber Pre (mBar)"))
        self.label_39.setText(_translate("OXCART", "Load Lock Pre(mBar)"))
        self.led_main_chamber.setText(_translate("OXCART", "Main"))
        self.led_load_lock.setText(_translate("OXCART", "Load"))
        self.led_cryo.setText(_translate("OXCART", "Cryo"))
        self.main_chamber_switch.setText(_translate("OXCART", "Main Chamber"))
        self.load_lock_switch.setText(_translate("OXCART", "Load Lock"))
        self.cryo_switch.setText(_translate("OXCART", "Cryo"))
        self.textEdit.setHtml(_translate("OXCART", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ex_user=user1;ex_name=test1;ex_time=90;max_ions=2000;ex_freq=10;vdc_min=500;vdc_max=4000;vdc_steps_up=100;vdc_steps_down=100;vp_min=328;vp_max=3281;pulse_fraction=20;pulse_frequency=200;detection_rate_init=1;hit_displayed=20000;email=;tweet=No;counter_source=TDC</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ex_user=user2;ex_name=test2;ex_time=100;max_ions=3000;ex_freq=5;vdc_min=1000;vdc_max=3000;vdc_steps_up=50;vdc_steps_down=50;vp_min=400;vp_max=2000;pulse_fraction=15;pulse_frequency=200;detection_rate_init=2;hit_displayed=40000;email=;tweet=No;counter_source=Pulse Counter</p></body></html>"))
        self.label_11.setText(_translate("OXCART", "Run Statistics"))
        self.label_12.setText(_translate("OXCART", "Elapsed Time (S):"))
        self.label_13.setText(_translate("OXCART", "Total Ions"))
        self.label_14.setText(_translate("OXCART", "Specimen Voltage (V)"))
        self.label_16.setText(_translate("OXCART", "Pulse Voltage (V)"))
        self.label_15.setText(_translate("OXCART", "Detection Rate (%)"))
        self.label.setText(_translate("OXCART", "Setup Parameters"))
        self.parameters_source.setItemText(0, _translate("OXCART", "TextBox"))
        self.parameters_source.setItemText(1, _translate("OXCART", "TextLine"))
        self.label_43.setText(_translate("OXCART", "Experiment User"))
        self.ex_user.setText(_translate("OXCART", "user"))
        self.label_21.setText(_translate("OXCART", "Experiment Name"))
        self.ex_name.setText(_translate("OXCART", "test"))
        self.label_2.setText(_translate("OXCART", "Max. Experiment Time (S)"))
        self.ex_time.setText(_translate("OXCART", "90"))
        self.label_41.setText(_translate("OXCART", "Max. Number of Ions"))
        self.max_ions.setText(_translate("OXCART", "2000"))
        self.label_3.setText(_translate("OXCART", "Control refresh Freq.(Hz)"))
        self.ex_freq.setText(_translate("OXCART", "10"))
        self.label_4.setText(_translate("OXCART", "Specimen Start Voltage (V)"))
        self.vdc_min.setText(_translate("OXCART", "500"))
        self.label_5.setText(_translate("OXCART", "Specimen Stop Voltage (V)"))
        self.vdc_max.setText(_translate("OXCART", "4000"))
        self.label_6.setText(_translate("OXCART", "K_p Upwards"))
        self.vdc_steps_up.setText(_translate("OXCART", "100"))
        self.label_28.setText(_translate("OXCART", "K_p Downwards"))
        self.vdc_steps_down.setText(_translate("OXCART", "100"))
        self.label_20.setText(_translate("OXCART", "Cycle for Avg. (Hz)"))
        self.cycle_avg.setText(_translate("OXCART", "10"))
        self.label_8.setText(_translate("OXCART", "Pulse Min. Voltage (V)"))
        self.vp_min.setText(_translate("OXCART", "328"))
        self.label_9.setText(_translate("OXCART", "Pulse Max. Voltage (V)"))
        self.vp_max.setText(_translate("OXCART", "3281"))
        self.label_25.setText(_translate("OXCART", "Pulse Fraction (%)"))
        self.pulse_fraction.setText(_translate("OXCART", "20"))
        self.label_23.setText(_translate("OXCART", "Pulse Frequency (KHz)"))
        self.pulse_frequency.setText(_translate("OXCART", "200"))
        self.label_17.setText(_translate("OXCART", "Detection Rate (%)"))
        self.detection_rate_init.setText(_translate("OXCART", "1"))
        self.label_22.setText(_translate("OXCART", "# Hits Displayed"))
        self.hit_displayed.setText(_translate("OXCART", "20000"))
        self.label_26.setText(_translate("OXCART", "Email"))
        self.label_27.setText(_translate("OXCART", "Twitter"))
        self.tweet.setItemText(0, _translate("OXCART", "No"))
        self.tweet.setItemText(1, _translate("OXCART", "Yes"))
        self.label_42.setText(_translate("OXCART", "Counter Source"))
        self.counter_source.setItemText(0, _translate("OXCART", "TDC"))
        self.counter_source.setItemText(1, _translate("OXCART", "Pulse Counter"))
        self.menuFile.setTitle(_translate("OXCART", "File"))
        self.actionExit.setText(_translate("OXCART", "Exit"))

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

        # Temperature #########################
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
            size=1, brush=pg.mkBrush(255, 255, 255, 120))
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
        self.diagram_close_all = QPixmap('.\png\close_all.png')
        self.diagram_main_open = QPixmap('.\png\main_open.png')
        self.diagram_load_open = QPixmap('.\png\load_open.png')
        self.diagram_cryo_open = QPixmap('.\png\cryo_open.png')
        self.led_red = QPixmap('.\png\led-red-on.png')
        self.led_green = QPixmap('.\png\green-led-on.png')

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
                if text_line_b[i][0] == 'tweet':
                    if text_line_b[i][1] == 'NO':
                        self.tweet.setCurrentIndex(0)
                    if text_line_b[i][1] == 'Yes':
                        self.tweet.setCurrentIndex(1)

        # check if the gates are closed
        if not variables.flag_main_gate:
            if self.parameters_source.currentText() == 'TextLine' and variables.index_line == 0:
                lines = self.textEdit.toPlainText() # Copy all the lines in TextLine
                self.text_line = lines.splitlines() # Seperate the lines in TextLine
                self.num_line = len(self.text_line) # count number of line in TextLine (Number of experiments that have to be done)
            elif self.parameters_source.currentText() != 'TextLine' and variables.index_line == 0:
                self.num_line = 0
            self.start_button.setEnabled(False) # Disable the start button in the GUI
            variables.plot_clear_flag = True # Change the flag to clear the plots in GUI

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
            variables.pulse_frequency = int(float(self.pulse_frequency.text()))
            variables.hdf5_path = self.ex_name.text()
            variables.email = self.email.text()
            variables.cycle_avg = int(float(self.cycle_avg.text()))
            variables.vdc_step_up = int(float(self.vdc_steps_up.text()))
            variables.vdc_step_down = int(float(self.vdc_steps_down.text()))
            variables.v_p_min = int(float(self.vp_min.text()))
            variables.v_p_max = int(float(self.vp_max.text()))
            variables.counter_source = str(self.counter_source.currentText())
            if variables.counter_source == 'TDC_Raw':
                variables.raw_mode = True

            if self.tweet.currentText() == 'Yes':
                variables.tweet = True

            # Read the experiment counter
            with open('./png/counter.txt') as f:
                variables.counter = int(f.readlines()[0])
            # Current time and date
            now = datetime.datetime.now()
            exp_name = "%s_" % variables.counter + \
                       now.strftime("%b-%d-%Y_%H-%M") + "_%s" % variables.hdf5_path
            variables.path = 'D:\\oxcart\\data\\%s' % exp_name
            # Create folder to save the data
            if not os.path.isdir(variables.path):
                os.makedirs(variables.path, mode=0o777, exist_ok=True)
            # start the run methos of MainThread Class, which is main function of oxcart.py
            self.thread.start()
            if self.parameters_source.currentText() == 'TextLine':
                variables.index_line += 1 # increase the index line of TextLine to read the second line in next step
        else:
            _translate = QtCore.QCoreApplication.translate
            self.Error.setText(_translate("OXCART",
                                          "<html><head/><body><p><span style=\" color:#ff0000;\">!!! First Close Main "
                                          "Gate !!!</span></p></body></html>"))
    def finished_thread_main(self):
        """
        The function that is run after end of experiment(MainThread)
        """
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        QScreen.grabWindow(app.primaryScreen(),
                           QApplication.desktop().winId()).save(variables.path + '\\screenshot.png')
        if variables.index_line < self.num_line: # Do next experiment in case of TextLine
            self.thread_main()
        else:
            variables.index_line = 0

    def stop_ex(self):
        """
        The function that is run if STOP button is pressed
        """
        if variables.start_flag == True:
            variables.stop_flag = True # Set the STOP flag
            self.stop_button.setEnabled(False) # Disable the stop button
            print('STOP Flag is set:', variables.stop_flag)

    def gates(self, gate_num):
        """
        The function for closing or opening gates
        """
        def switch_gate(num):
            """
            The function for applying the command of closing or opening gate
            """
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan('Dev2/port0/line%s' % num)
                task.start()
                task.write([True])
                time.sleep(.5)
                task.write([False])
        # Main gate
        if gate_num == 1 and not variables.flag_load_gate and not variables.flag_cryo_gate and variables.flag_pump_load_lock:
            if not variables.flag_main_gate: # Open the main gate
                switch_gate(0)
                self.led_main_chamber.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_main_open)
                variables.flag_main_gate = True
            elif variables.flag_main_gate: # Close the main gate
                switch_gate(1)
                self.led_main_chamber.setPixmap(self.led_red)
                self.diagram.setPixmap(self.diagram_close_all)
                variables.flag_main_gate = False
        # Buffer gate
        elif gate_num == 2 and not variables.flag_main_gate and not variables.flag_cryo_gate and variables.flag_pump_load_lock:
            if not variables.flag_load_gate: # Open the main gate
                switch_gate(2)
                self.led_load_lock.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_load_open)
                variables.flag_load_gate = True
            elif variables.flag_load_gate: # Close the main gate
                switch_gate(3)
                self.led_load_lock.setPixmap(self.led_red)
                self.diagram.setPixmap(self.diagram_close_all)
                variables.flag_load_gate = False
        # Cryo gate
        elif gate_num == 3 and not variables.flag_main_gate and not variables.flag_load_gate and variables.flag_pump_load_lock:
            if not variables.flag_cryo_gate: # Open the main gate
                switch_gate(4)
                self.led_cryo.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_cryo_open)
                variables.flag_cryo_gate = True
            elif variables.flag_cryo_gate: # Close the main gate
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
        if not variables.flag_main_gate and not variables.flag_cryo_gate \
                and not variables.flag_load_gate:
            if variables.flag_pump_load_lock:
                variables.flag_pump_load_lock_click = True
                self.pump_load_lock_switch.setEnabled(False)
            elif not variables.flag_pump_load_lock:
                variables.flag_pump_load_lock_click = True
                self.pump_load_lock_switch.setEnabled(False)
        else: # SHow error message in the GUI
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
        # Temperature
        self.x_tem = self.x_tem[1:]  # Remove the first element.
        self.x_tem = np.append(self.x_tem, self.x_tem[-1] + 1)  # Add a new value 1 higher than the last.
        self.y_tem = self.y_tem[1:]  # Remove the first element.
        self.y_tem = np.append(self.y_tem, int(variables.temperature))

        self.data_line_tem.setData(self.x_tem, self.y_tem)
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
            variables.plot_clear_flag = False

        if variables.start_flag:
            if variables.index_wait_on_plot_start <= 16:
                variables.index_wait_on_plot_start += 1

            if variables.index_wait_on_plot_start >= 8:
                # V_dc and V_p
                if variables.index_plot <= 999:
                    self.y_vdc[variables.index_plot] = int(variables.specimen_voltage)  # Add a new value.
                    self.y_vps[variables.index_plot] = int(variables.pulse_voltage)  # Add a new value.
                else:
                    self.x_vdc = np.append(self.x_vdc,
                                           self.x_vdc[-1] + 1)  # Add a new value 1 higher than the last.
                    self.y_vdc = np.append(self.y_vdc, int(variables.specimen_voltage))  # Add a new value.
                    self.y_vps = np.append(self.y_vps, int(variables.pulse_voltage))  # Add a new value.

                self.data_line_vdc.setData(self.x_vdc, self.y_vdc)
                self.data_line_vps.setData(self.x_vdc, self.y_vps)

                # Detection Rate Visualization
                if variables.index_plot <= 999:
                    self.y_dtec[variables.index_plot] = int(variables.avg_n_count)  # Add a new value.
                else:
                    self.x_dtec = self.x_dtec[1:]  # Remove the first element.
                    self.x_dtec = np.append(self.x_dtec,
                                            self.x_dtec[-1] + 1)  # Add a new value 1 higher than the last.
                    self.y_dtec = self.y_dtec[1:]
                    self.y_dtec = np.append(self.y_dtec, int(variables.avg_n_count))

                self.data_line_dtec.setData(self.x_dtec, self.y_dtec)
                # Increase the index
                variables.index_plot += 1
            # Time of Flight
            if variables.counter_source == 'TDC' and variables.total_ions > 0 and variables.index_wait_on_plot_start > 16 \
                    and variables.index_wait_on_plot_start > 16 and not variables.raw_mode:
                if variables.index_wait_on_plot_start > 16:

                    # max_lenght = max(len(variables.x), len(variables.y),
                    #                  len(variables.t), len(variables.main_v_dc_dld))
                    # d_0 = 110
                    # e = 1.602 * 10**(-19)
                    # dtec_dim = 78
                    # pix_size_x = 0.03243
                    # pix_size_y = 0.03257
                    try:
                        # x_n = np.array(variables.x[:max_lenght]) - 2450
                        # y_n = np.array(variables.y[:max_lenght]) - 2450

                        # x_n = x_n * pix_size_x
                        # y_n = y_n * pix_size_y

                        #
                        # t_n = np.array(variables.t[:max_lenght]) * 27.432 * 10**(-12)
                        #
                        # l = np.sqrt(d_0 ** 2 + x_n ** 2 + y_n ** 2)

                        # math_to_charge = (2 * np.array(variables.main_v_dc_dld[:max_lenght]) * e * t_n**2) / ((l * 10 ** -3)**2)
                        def replaceZeroes(data):
                            min_nonzero = np.min(data[np.nonzero(data)])
                            data[data == 0] = min_nonzero
                            return data
                        math_to_charge = variables.t[variables.t < 800000]
                        math_to_charge = math_to_charge * 27.432 * 0.001 # Time in ns
                        self.y_tof, self.x_tof = np.histogram(math_to_charge, bins=512)
                        self.histogram.clear()
                        self.y_tof = replaceZeroes(self.y_tof)
                        self.histogram.addItem(
                            pg.BarGraphItem(x=self.x_tof[:-1], height=np.log(self.y_tof), width=0.1, brush='r'))

                    except:
                        print(
                            f"{initialize_devices.bcolors.FAIL}Error: Cannot plot Histogram correctly{initialize_devices.bcolors.ENDC}")

                    # Visualization
                    try:
                        # adding points to the scatter plot
                        self.scatter.clear()
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
                    except:
                        print(
                            f"{initialize_devices.FAIL}Error: Cannot plot Ions correctly{initialize_devices.bcolors.ENDC}")

            # save plots to the file
            if variables.index_plot_save % 100 == 0:
                exporter = pg.exporters.ImageExporter(self.vdc_time.plotItem)
                exporter.export(variables.path + '\\v_dc_p_%s.png' % variables.index_plot_save)
                exporter = pg.exporters.ImageExporter(self.detection_rate_viz.plotItem)
                exporter.export(variables.path + '\\detection_rate_%s.png' % variables.index_plot_save)
                exporter = pg.exporters.ImageExporter(self.visualization.plotItem)
                exporter.export(variables.path + '\\visualization_%s.png' % variables.index_plot_save)
                exporter = pg.exporters.ImageExporter(self.histogram.plotItem)
                exporter.export(variables.path + '\\tof_%s.png' % variables.index_plot_save)

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
        self.vacuum_buffer.display(variables.vacuum_buffer)
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
            variables.ex_freq = int(float(self.ex_freq.text()))
            variables.max_ions = int(float(self.max_ions.text()))
            variables.vdc_min = int(float(self.vdc_min.text()))
            variables.detection_rate = float(self.detection_rate_init.text())
            variables.pulse_fraction = int(float(self.pulse_fraction.text()))
            variables.hit_display = int(float(self.hit_displayed.text()))
            variables.pulse_fraction = int(float(self.pulse_fraction.text())) / 100
            variables.pulse_frequency = int(float(self.pulse_frequency.text()))
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

        except:
            print(
                f"{initialize_devices.bcolors.FAIL}Error: Cannot update setup parameters{initialize_devices.bcolors.ENDC}")

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
    def __init__(self, ):
        QThread.__init__(self, )
        # run method gets called when we start the thread

    def run(self):
        main_thread = oxcart.main()
        self.signal.emit(main_thread)


if __name__ == "__main__":

    # Initialize global experiment variables
    variables.init()
    # Cryovac initialized
    try:
        com_port_cryovac = serial.Serial(
            port=initialize_devices.com_ports[variables.com_port_idx_cryovac].device,  # chosen COM port
            baudrate=9600,  # 115200
            bytesize=serial.EIGHTBITS,  # 8
            parity=serial.PARITY_NONE,  # N
            stopbits=serial.STOPBITS_ONE  # 1
        )
        initialize_devices.initialize_cryovac(com_port_cryovac)
    except Exception as e:
        print('Can not initialize the Cryovac')
        print(e)
    # Main and Buffer vacuum gauges
    try:
        initialize_devices.initialize_pfeiffer_gauges()
    except Exception as e:
        print('Can not initialize the Pfeiffer gauges')
        print(e)
    # Buffer Backing vacuum gauges
    try:
        initialize_devices.initialize_edwards_tic_buffer_chamber()
    except Exception as e:
        print('Can not initialize the buffer vacuum gauges')
        print(e)
    # Load Lock vacuum gauges
    try:
        initialize_devices.initialize_edwards_tic_load_lock()
    except Exception as e:
        print('Can not initialize the Edwards gauges')
        print(e)

    # Cameras thread
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

        # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
        cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse))

        # Create and attach all Pylon Devices.
        for i, cam in enumerate(cameras):
            cam.Attach(tlFactory.CreateDevice(devices[i]))
        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        camera = Camera(devices, tlFactory, cameras, converter)

    except:
        print('Can not initialize the Cameras')
    # Thread for reading cameras
    lock2 = threading.Lock()
    camera_thread = threading.Thread(target=camera.update_cameras, args=(lock2,))
    camera_thread.setDaemon(True)
    camera_thread.start()
    lock1 = threading.Lock()
    # Thread for reading gauges
    gauges_thread = threading.Thread(target=initialize_devices.gauges_update, args=(lock1, com_port_cryovac))
    gauges_thread.setDaemon(True)
    gauges_thread.start()

    app = QtWidgets.QApplication(sys.argv)
    # get display resolution
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    print('Screen size is:(%s,%s)' % (width, height))
    OXCART = QtWidgets.QMainWindow()
    lock = threading.Lock()
    ui = Ui_OXCART(camera.devices, camera.tlFactory, camera.cameras, camera.converter, lock)
    ui.setupUi(OXCART)
    OXCART.show()
    sys.exit(app.exec_())

