from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
import pyqtgraph as pg
import sys
import numpy as np
import nidaqmx
import time
import threading
import datetime
import os
import scipy.misc, PIL.ImageQt

import oxcart
import variables
import camera


class Ui_OXCART(object):
    def __init__(self, cameras, converter):
        self.cameras = cameras   # Initialize cameras
        self.converter = converter
    def setupUi(self, OXCART):
        OXCART.setObjectName("OXCART")
        OXCART.resize(3400, 1800)
        self.centralwidget = QtWidgets.QWidget(OXCART)
        self.centralwidget.setObjectName("centralwidget")
        # self.vdc_time = QtWidgets.QWidget(self.centralwidget)
        self.vdc_time = pg.PlotWidget(self.centralwidget)
        self.vdc_time.setGeometry(QtCore.QRect(550, 120, 500, 500))
        self.vdc_time.setObjectName("vdc_time")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(730, 50, 80, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(2860, 1520, 314, 106))
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
        self.label_10.setGeometry(QtCore.QRect(1240, 60, 156, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        # self.detection_rate_viz = QtWidgets.QWidget(self.centralwidget)
        self.detection_rate_viz = pg.PlotWidget(self.centralwidget)
        self.detection_rate_viz.setGeometry(QtCore.QRect(1100, 120, 500, 500))
        self.detection_rate_viz.setObjectName("detection_rate_viz")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(680, 750, 134, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        # self.visualization = QtWidgets.QWidget(self.centralwidget)
        self.visualization = pg.PlotWidget(self.centralwidget)
        self.visualization.setGeometry(QtCore.QRect(550, 800, 500, 500))
        self.visualization.setObjectName("visualization")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(1270, 740, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        # self.histogram = QtWidgets.QWidget(self.centralwidget)
        self.histogram = pg.PlotWidget(self.centralwidget)
        self.histogram.setGeometry(QtCore.QRect(1100, 800, 500, 500))
        self.histogram.setObjectName("histogram")
        # self.temperature = QtWidgets.QWidget(self.centralwidget)
        self.temperature = pg.PlotWidget(self.centralwidget)
        self.temperature.setGeometry(QtCore.QRect(2130, 1330, 441, 361))
        self.temperature.setObjectName("temperature")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(20, 1020, 101, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.Error = QtWidgets.QLabel(self.centralwidget)
        self.Error.setGeometry(QtCore.QRect(520, 0, 791, 51))
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
        self.diagram.setGeometry(QtCore.QRect(30, 1080, 491, 421))
        self.diagram.setText("")
        self.diagram.setObjectName("diagram")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 1530, 621, 61))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.led_load_lock = QtWidgets.QLabel(self.layoutWidget1)
        self.led_load_lock.setAlignment(QtCore.Qt.AlignCenter)
        self.led_load_lock.setObjectName("led_load_lock")
        self.gridLayout_4.addWidget(self.led_load_lock, 0, 1, 1, 1)
        self.led_main_chamber = QtWidgets.QLabel(self.layoutWidget1)
        self.led_main_chamber.setAlignment(QtCore.Qt.AlignCenter)
        self.led_main_chamber.setObjectName("led_main_chamber")
        self.gridLayout_4.addWidget(self.led_main_chamber, 0, 0, 1, 1)
        self.led_cryo = QtWidgets.QLabel(self.layoutWidget1)
        self.led_cryo.setAlignment(QtCore.Qt.AlignCenter)
        self.led_cryo.setObjectName("led_cryo")
        self.gridLayout_4.addWidget(self.led_cryo, 0, 2, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 1610, 621, 81))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.cryo_switch = QtWidgets.QPushButton(self.layoutWidget2)
        self.cryo_switch.setObjectName("cryo_switch")
        self.gridLayout.addWidget(self.cryo_switch, 0, 2, 1, 1)
        self.main_chamber_switch = QtWidgets.QPushButton(self.layoutWidget2)
        self.main_chamber_switch.setObjectName("main_chamber_switch")
        self.gridLayout.addWidget(self.main_chamber_switch, 0, 0, 1, 1)
        self.load_lock_switch = QtWidgets.QPushButton(self.layoutWidget2)
        self.load_lock_switch.setObjectName("load_lock_switch")
        self.gridLayout.addWidget(self.load_lock_switch, 0, 1, 1, 1)
        self.cam_s_o = QtWidgets.QLabel(self.centralwidget)
        self.cam_s_o.setGeometry(QtCore.QRect(1650, 120, 500, 500))
        self.cam_s_o.setObjectName("cam_s_o")
        self.vdc_time_3 = QtWidgets.QWidget(self.centralwidget)
        self.vdc_time_3.setGeometry(QtCore.QRect(1650, 790, 500, 500))
        self.vdc_time_3.setObjectName("vdc_time_3")
        self.cam_b_o = QtWidgets.QLabel(self.vdc_time_3)
        self.cam_b_o.setGeometry(QtCore.QRect(0, 10, 500, 500))
        self.cam_b_o.setObjectName("cam_b_o")
        self.cam_b_d = QtWidgets.QLabel(self.centralwidget)
        self.cam_b_d.setGeometry(QtCore.QRect(2160, 790, 1200, 500))
        self.cam_b_d.setObjectName("cam_b_d")
        self.cam_s_d = QtWidgets.QLabel(self.centralwidget)
        self.cam_s_d.setGeometry(QtCore.QRect(2160, 120, 1200, 500))
        self.cam_s_d.setObjectName("cam_s_d")
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        self.label_29.setGeometry(QtCore.QRect(1830, 760, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.centralwidget)
        self.label_30.setGeometry(QtCore.QRect(1830, 90, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.centralwidget)
        self.label_31.setGeometry(QtCore.QRect(2740, 750, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.centralwidget)
        self.label_32.setGeometry(QtCore.QRect(2710, 90, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.centralwidget)
        self.label_33.setGeometry(QtCore.QRect(2240, 730, 171, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.label_34 = QtWidgets.QLabel(self.centralwidget)
        self.label_34.setGeometry(QtCore.QRect(2220, 50, 171, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")
        self.light = QtWidgets.QPushButton(self.centralwidget)
        self.light.setGeometry(QtCore.QRect(2940, 20, 101, 46))
        self.light.setObjectName("light")
        self.led_light = QtWidgets.QLabel(self.centralwidget)
        self.led_light.setGeometry(QtCore.QRect(3060, 10, 111, 61))
        self.led_light.setAlignment(QtCore.Qt.AlignCenter)
        self.led_light.setObjectName("led_light")
        self.vacume_main = QtWidgets.QLCDNumber(self.centralwidget)
        self.vacume_main.setGeometry(QtCore.QRect(1340, 1370, 231, 91))
        self.vacume_main.setObjectName("vacume_main")
        self.vacume_buffer = QtWidgets.QLCDNumber(self.centralwidget)
        self.vacume_buffer.setGeometry(QtCore.QRect(1340, 1480, 231, 91))
        self.vacume_buffer.setObjectName("vacume_buffer")
        self.vacume_load_lock = QtWidgets.QLCDNumber(self.centralwidget)
        self.vacume_load_lock.setGeometry(QtCore.QRect(1340, 1600, 231, 91))
        self.vacume_load_lock.setObjectName("vacume_load_lock")
        self.label_35 = QtWidgets.QLabel(self.centralwidget)
        self.label_35.setGeometry(QtCore.QRect(1130, 1410, 171, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_35.setFont(font)
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.centralwidget)
        self.label_36.setGeometry(QtCore.QRect(1130, 1510, 171, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.centralwidget)
        self.label_37.setGeometry(QtCore.QRect(1140, 1630, 171, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setObjectName("label_37")
        self.pump_load_loack = QtWidgets.QPushButton(self.centralwidget)
        self.pump_load_loack.setGeometry(QtCore.QRect(860, 1620, 198, 46))
        self.pump_load_loack.setObjectName("pump_load_loack")
        self.label_38 = QtWidgets.QLabel(self.centralwidget)
        self.label_38.setGeometry(QtCore.QRect(1660, 1510, 191, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.vacume_load_lock_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.vacume_load_lock_2.setGeometry(QtCore.QRect(1860, 1480, 231, 91))
        self.vacume_load_lock_2.setObjectName("vacume_load_lock_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 753, 436, 242))
        self.widget.setObjectName("widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_11 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 0, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.widget)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 1, 0, 1, 1)
        self.elapsed_time = QtWidgets.QLineEdit(self.widget)
        self.elapsed_time.setText("")
        self.elapsed_time.setObjectName("elapsed_time")
        self.gridLayout_3.addWidget(self.elapsed_time, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 2, 0, 1, 1)
        self.total_ions = QtWidgets.QLineEdit(self.widget)
        self.total_ions.setText("")
        self.total_ions.setObjectName("total_ions")
        self.gridLayout_3.addWidget(self.total_ions, 2, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.widget)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 3, 0, 1, 1)
        self.speciemen_voltage = QtWidgets.QLineEdit(self.widget)
        self.speciemen_voltage.setText("")
        self.speciemen_voltage.setObjectName("speciemen_voltage")
        self.gridLayout_3.addWidget(self.speciemen_voltage, 3, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.widget)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 4, 0, 1, 1)
        self.pulse_voltage = QtWidgets.QLineEdit(self.widget)
        self.pulse_voltage.setText("")
        self.pulse_voltage.setObjectName("pulse_voltage")
        self.gridLayout_3.addWidget(self.pulse_voltage, 4, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.widget)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 5, 0, 1, 1)
        self.detection_rate = QtWidgets.QLineEdit(self.widget)
        self.detection_rate.setText("")
        self.detection_rate.setObjectName("detection_rate")
        self.gridLayout_3.addWidget(self.detection_rate, 5, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(20, 30, 488, 715))
        self.widget1.setObjectName("widget1")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.widget1)
        self.label_21.setObjectName("label_21")
        self.gridLayout_5.addWidget(self.label_21, 1, 0, 1, 1)
        self.hdf5_path = QtWidgets.QLineEdit(self.widget1)
        self.hdf5_path.setObjectName("hdf5_path")
        self.gridLayout_5.addWidget(self.hdf5_path, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 2, 0, 1, 1)
        self.ex_time = QtWidgets.QLineEdit(self.widget1)
        self.ex_time.setObjectName("ex_time")
        self.gridLayout_5.addWidget(self.ex_time, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 3, 0, 1, 1)
        self.ex_freq = QtWidgets.QLineEdit(self.widget1)
        self.ex_freq.setObjectName("ex_freq")
        self.gridLayout_5.addWidget(self.ex_freq, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget1)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 4, 0, 1, 1)
        self.vdc_min = QtWidgets.QLineEdit(self.widget1)
        self.vdc_min.setObjectName("vdc_min")
        self.gridLayout_5.addWidget(self.vdc_min, 4, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget1)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 5, 0, 1, 1)
        self.vdc_max = QtWidgets.QLineEdit(self.widget1)
        self.vdc_max.setObjectName("vdc_max")
        self.gridLayout_5.addWidget(self.vdc_max, 5, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget1)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 6, 0, 1, 1)
        self.vdc_steps_up = QtWidgets.QLineEdit(self.widget1)
        self.vdc_steps_up.setObjectName("vdc_steps_up")
        self.gridLayout_5.addWidget(self.vdc_steps_up, 6, 1, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.widget1)
        self.label_28.setObjectName("label_28")
        self.gridLayout_5.addWidget(self.label_28, 7, 0, 1, 1)
        self.vdc_steps_down = QtWidgets.QLineEdit(self.widget1)
        self.vdc_steps_down.setObjectName("vdc_steps_down")
        self.gridLayout_5.addWidget(self.vdc_steps_down, 7, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.widget1)
        self.label_20.setObjectName("label_20")
        self.gridLayout_5.addWidget(self.label_20, 8, 0, 1, 1)
        self.cycle_avg = QtWidgets.QLineEdit(self.widget1)
        self.cycle_avg.setObjectName("cycle_avg")
        self.gridLayout_5.addWidget(self.cycle_avg, 8, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget1)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 9, 0, 1, 1)
        self.vp_min = QtWidgets.QLineEdit(self.widget1)
        self.vp_min.setObjectName("vp_min")
        self.gridLayout_5.addWidget(self.vp_min, 9, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget1)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 10, 0, 1, 1)
        self.vp_max = QtWidgets.QLineEdit(self.widget1)
        self.vp_max.setObjectName("vp_max")
        self.gridLayout_5.addWidget(self.vp_max, 10, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.widget1)
        self.label_25.setObjectName("label_25")
        self.gridLayout_5.addWidget(self.label_25, 11, 0, 1, 1)
        self.pulse_fraction = QtWidgets.QLineEdit(self.widget1)
        self.pulse_fraction.setObjectName("pulse_fraction")
        self.gridLayout_5.addWidget(self.pulse_fraction, 11, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.widget1)
        self.label_23.setObjectName("label_23")
        self.gridLayout_5.addWidget(self.label_23, 12, 0, 1, 1)
        self.pulse_frequency = QtWidgets.QLineEdit(self.widget1)
        self.pulse_frequency.setObjectName("pulse_frequency")
        self.gridLayout_5.addWidget(self.pulse_frequency, 12, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.widget1)
        self.label_17.setObjectName("label_17")
        self.gridLayout_5.addWidget(self.label_17, 13, 0, 1, 1)
        self.detection_rate_init = QtWidgets.QLineEdit(self.widget1)
        self.detection_rate_init.setObjectName("detection_rate_init")
        self.gridLayout_5.addWidget(self.detection_rate_init, 13, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.widget1)
        self.label_22.setObjectName("label_22")
        self.gridLayout_5.addWidget(self.label_22, 14, 0, 1, 1)
        self.hit_displayed = QtWidgets.QLineEdit(self.widget1)
        self.hit_displayed.setObjectName("hit_displayed")
        self.gridLayout_5.addWidget(self.hit_displayed, 14, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.widget1)
        self.label_26.setObjectName("label_26")
        self.gridLayout_5.addWidget(self.label_26, 15, 0, 1, 1)
        self.email = QtWidgets.QLineEdit(self.widget1)
        self.email.setText("")
        self.email.setObjectName("email")
        self.gridLayout_5.addWidget(self.email, 15, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.widget1)
        self.label_27.setObjectName("label_27")
        self.gridLayout_5.addWidget(self.label_27, 16, 0, 1, 1)
        self.tweet = QtWidgets.QComboBox(self.widget1)
        self.tweet.setObjectName("tweet")
        self.tweet.addItem("")
        self.tweet.addItem("")
        self.gridLayout_5.addWidget(self.tweet, 16, 1, 1, 1)
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

    def retranslateUi(self, OXCART):
        _translate = QtCore.QCoreApplication.translate
        OXCART.setWindowTitle(_translate("OXCART", "OXCART"))
        self.label_7.setText(_translate("OXCART", "Voltage"))
        self.start_button.setText(_translate("OXCART", "Start"))
        ###
        self.start_button.clicked.connect(self.tread_main)
        self.tread = MainThread()
        self.tread.signal.connect(self.finished_tread_main)
        self.stop_button.setText(_translate("OXCART", "Stop"))
        self.stop_button.clicked.connect(self.stop_ex)
        ###
        self.label_10.setText(_translate("OXCART", "Detection Rate"))
        self.label_19.setText(_translate("OXCART", "Visualization"))
        self.label_24.setText(_translate("OXCART", "Histogram"))
        self.label_18.setText(_translate("OXCART", "Diagram"))
        self.Error.setText(_translate("OXCART", "<html><head/><body><p><br/></p></body></html>"))
        self.led_load_lock.setText(_translate("OXCART", "Load"))
        self.led_main_chamber.setText(_translate("OXCART", "Main"))
        self.led_cryo.setText(_translate("OXCART", "Cryo"))
        self.cryo_switch.setText(_translate("OXCART", "Cryo"))
        self.main_chamber_switch.setText(_translate("OXCART", "Main Chamber"))
        self.load_lock_switch.setText(_translate("OXCART", "Load Lock"))
        self.label_29.setText(_translate("OXCART", "Overview"))
        self.label_30.setText(_translate("OXCART", "Overview"))
        self.label_31.setText(_translate("OXCART", "Detail"))
        self.label_32.setText(_translate("OXCART", "Detail"))
        self.label_33.setText(_translate("OXCART", "Camera Bottom"))
        self.label_34.setText(_translate("OXCART", "Camera Side"))
        self.light.setText(_translate("OXCART", "Light"))
        self.led_light.setText(_translate("OXCART", "light"))
        self.label_35.setText(_translate("OXCART", "Main Chamber"))
        self.label_36.setText(_translate("OXCART", "Buffer Chamber"))
        self.label_37.setText(_translate("OXCART", "Load lock"))
        ###
        self.main_chamber_switch.clicked.connect(lambda:self.gates(1))
        self.load_lock_switch.clicked.connect(lambda:self.gates(2))
        self.cryo_switch.clicked.connect(lambda:self.gates(3))
        self.light.clicked.connect(lambda:self.light_switch())
        ###
        self.pump_load_loack.setText(_translate("OXCART", "Load Lock Pump"))
        self.label_38.setText(_translate("OXCART", "Temperature (K)"))
        self.label_11.setText(_translate("OXCART", "Run Statistics"))
        self.label_12.setText(_translate("OXCART", "Elapsed Time (S):"))
        self.label_13.setText(_translate("OXCART", "Total Ions"))
        self.label_14.setText(_translate("OXCART", "Specimen Voltage (V)"))
        self.label_16.setText(_translate("OXCART", "Pulse Voltage (V)"))
        self.label_15.setText(_translate("OXCART", "Detection Rate (%)"))
        self.label.setText(_translate("OXCART", "Setup Parameters"))
        self.label_21.setText(_translate("OXCART", "Experiment Name"))
        self.hdf5_path.setText(_translate("OXCART", "test"))
        self.label_2.setText(_translate("OXCART", "Max. Experiment Time (S)"))
        self.ex_time.setText(_translate("OXCART", "90"))
        self.label_3.setText(_translate("OXCART", "Control refresh Freq.(Hz)"))
        self.ex_freq.setText(_translate("OXCART", "10"))
        self.label_4.setText(_translate("OXCART", "Specimen Start Voltage (V)"))
        self.vdc_min.setText(_translate("OXCART", "2000"))
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
        self.hit_displayed.setText(_translate("OXCART", "0"))
        self.label_26.setText(_translate("OXCART", "Email"))
        self.label_27.setText(_translate("OXCART", "Twitter"))
        self.tweet.setItemText(0, _translate("OXCART", "No"))
        self.tweet.setItemText(1, _translate("OXCART", "Yes"))
        self.menuFile.setTitle(_translate("OXCART", "File"))
        self.actionExit.setText(_translate("OXCART", "Exit"))

        # High Voltage visualization ################
        self.x_vdc = list(range(
            1000))  # 1000 time points
        self.y_vdc = [
                         np.nan] * 1000  # 1000 data points
        self.y_vps = [
                         np.nan] * 1000  # 1000 data points
        # Add legend
        self.vdc_time.addLegend()
        pen_vdc = pg.mkPen(color=(255, 0, 0), width=6)
        pen_vps = pg.mkPen(color=(0, 0, 255), width=3)
        self.data_line_vdc = self.vdc_time.plot(self.x_vdc, self.y_vdc, name="High Vol.", pen=pen_vdc)
        self.data_line_vps = self.vdc_time.plot(self.x_vdc, self.y_vps, name="Pulse Vol.", pen=pen_vps)
        self.vdc_time.setBackground('w')
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.vdc_time.setLabel("left", "High Voltage (V)", **styles)
        self.vdc_time.setLabel("bottom", "Time (Sec)", **styles)
        # Add grid
        self.vdc_time.showGrid(x=True, y=True)
        # Add Range
        self.vdc_time.setXRange(-100, 1100, padding=0)
        self.vdc_time.setYRange(-200, 20000, padding=0)


        # Detection Visualization #########################
        self.x_dtec = list(range(
            1000))  # 1000 time points
        self.y_dtec = [
                          np.nan] * 1000  # 1000 data points
        pen_dtec = pg.mkPen(color=(255, 0, 0), width=6)
        self.data_line_dtec = self.detection_rate_viz.plot(self.x_dtec, self.y_dtec, pen=pen_dtec)
        self.detection_rate_viz.setBackground('w')
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.detection_rate_viz.setLabel("left", "Detection Rate", **styles)
        self.detection_rate_viz.setLabel("bottom", "Time (Sec)", **styles)
        # Add grid
        self.detection_rate_viz.showGrid(x=True, y=True)
        # Add Range
        self.detection_rate_viz.setXRange(-100, 1100, padding=0)
        self.detection_rate_viz.setYRange(-100, 2000, padding=0)

        # Detection Temperature #########################
        self.x_tem = list(range(
            1000))  # 1000 time points
        self.y_tem = [
                          np.nan] * 1000  # 1000 data points
        pen_dtec = pg.mkPen(color=(255, 0, 0), width=6)
        self.data_line_tem = self.temperature.plot(self.x_tem, self.y_tem, pen=pen_dtec)
        self.temperature.setBackground('b')
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.temperature.setLabel("left", "Temperature (K)", **styles)
        self.temperature.setLabel("bottom", "Time (Sec)", **styles)
        # Add grid
        self.temperature.showGrid(x=True, y=True)
        # Add Range
        self.temperature.setXRange(-100, 1100, padding=0)
        self.temperature.setYRange(0, 200, padding=0)

        # Visualization #####################

        # creating a scatter plot item
        # using brush to enlarge the of white color with transparency is 50%
        scatter = pg.ScatterPlotItem(
            size=10, brush=pg.mkBrush(255, 255, 255, 120))
        # number of points
        n = 300
        # getting random position
        pos = np.random.normal(size=(2, n), scale=1e2)
        # creating spots using the random position
        spots = [{'pos': pos[:, i], 'data': 1}
                 for i in range(n)] + [{'pos': [0, 0], 'data': 1}]
        # adding points to the scatter plot
        # scatter.addPoints(spots)
        # add item to plot window
        # adding scatter plot item to the plot window
        self.visualization.addItem(scatter)
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.visualization.setLabel("left", "Y", **styles)
        self.visualization.setLabel("bottom", "X", **styles)
        # Add grid
        self.visualization.showGrid(x=True, y=True)
        # Add Range
        self.visualization.setXRange(0, 100, padding=0)
        self.visualization.setYRange(0, 100, padding=0)

        # Histogram ################
        # timer plot and variables
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(
            1000)  # In milliseconds
        self.timer1.timeout.connect(self.update_plot_data)
        self.timer1.start()
        # timer cameras
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(1)
        self.timer2.timeout.connect(self.update_cameras)
        self.timer2.start()

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

    def closeEvent(self, event):

        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               "Are you sure to quit?", QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:

            event.accept()
        else:
            event.ignore()

    def tread_main(self):
        self.start_button.setEnabled(False)
        variables.ex_time = int(self.ex_time.text())
        variables.ex_freq = int(self.ex_freq.text())
        variables.vdc_min = float(self.vdc_min.text())
        variables.vdc_max = float(self.vdc_max.text())
        variables.vdc_step_up = float(self.vdc_steps_up.text())
        variables.vdc_step_down = float(self.vdc_steps_down.text())
        variables.v_p_min = float(self.vp_min.text())
        variables.v_p_max = float(self.vp_max.text())
        variables.pulse_fraction = float(self.pulse_fraction.text()) / 100
        variables.pulse_frequency = int(self.pulse_frequency.text())
        variables.detection_rate = int(self.detection_rate_init.text())
        variables.hdf5_path = self.hdf5_path.text()
        variables.cycle_avg = int(self.cycle_avg.text())
        variables.email = self.email.text()
        if self.tweet.currentText() == 'Yes':
            variables.tweet = True

        # Read the experiment counter
        with open('./png/counter.txt') as f:
            variables.counter = int(f.readlines()[0])
        # Current time and date
        now = datetime.datetime.now()
        subject = "%s_" % variables.counter + \
                  now.strftime("%b-%d-%Y_%H-%M") + "_%s" % variables.hdf5_path
        variables.path = 'D:\\oxcart\\data\\%s' % subject
        # Create folder to save the data
        if not os.path.isdir(variables.path):
            os.makedirs(variables.path, mode=0o777, exist_ok=True)

        self.tread.start()

    def finished_tread_main(self):
        self.start_button.setEnabled(True)

    def stop_ex(self):
        variables.stop_flag = True
        print('STOP Flag is set:', variables.stop_flag)

    def gates(self, gate_num):
        def switch_gate(num):
            with nidaqmx.Task() as task:
                task.do_channels.add_do_chan('Dev2/port0/line%s' % num)
                task.start()
                task.write([True])
                time.sleep(.5)
                task.write([False])

        if gate_num == 1 and variables.flag_load_gate == False and variables.flag_cryo_gate == False:
            if variables.flag_main_gate == False:
                switch_gate(0)
                self.led_main_chamber.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_main_open)
                variables.flag_main_gate = True
            elif variables.flag_main_gate == True:
                switch_gate(1)
                self.led_main_chamber.setPixmap(self.led_red)
                self.diagram.setPixmap(self.diagram_close_all)
                variables.flag_main_gate = False
        elif gate_num == 2 and variables.flag_main_gate == False and variables.flag_cryo_gate == False:
            if variables.flag_load_gate == False:
                switch_gate(2)
                self.led_load_lock.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_load_open)
                variables.flag_load_gate = True
            elif variables.flag_load_gate == True:
                switch_gate(3)
                self.led_load_lock.setPixmap(self.led_red)
                self.diagram.setPixmap(self.diagram_close_all)
                variables.flag_load_gate = False
        elif gate_num == 3 and variables.flag_main_gate == False and variables.flag_load_gate == False:
            if variables.flag_cryo_gate == False:
                switch_gate(4)
                self.led_cryo.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_cryo_open)
                variables.flag_cryo_gate = True
            elif variables.flag_cryo_gate == True:
                switch_gate(5)
                self.led_cryo.setPixmap(self.led_red)
                self.diagram.setPixmap(self.diagram_close_all)
                variables.flag_cryo_gate = False
        else:
            _translate = QtCore.QCoreApplication.translate
            self.Error.setText(_translate("OXCART",
        "<html><head/><body><p><span style=\" color:#ff0000;\">!!! First Close all the Gates</span></p></body></html>"))

    def light_switch(self):
        if variables.light == False:
            self.led_light.setPixmap(self.led_green)
            self.cameras[0].Open()
            self.cameras[0].ExposureTime.SetValue(1500)
            self.cameras[1].Open()
            self.cameras[1].ExposureTime.SetValue(1500)
            # variables.camera_0_ExposureTime = 1500
            # variables.camera_1_ExposureTime = 1500
            variables.light = True
        elif variables.light == True:
            self.led_light.setPixmap(self.led_red)
            self.cameras[0].Open()
            self.cameras[0].ExposureTime.SetValue(10000000)
            self.cameras[1].Open()
            self.cameras[1].ExposureTime.SetValue(1000000)
            # variables.camera_0_ExposureTime = 10000000
            # variables.camera_1_ExposureTime = 1000000
            variables.light = False

    def update_plot_data(self):

        if variables.start_flag == True:
            if variables.index_plot <= 999:
                self.y_vdc = self.y_vdc[
                             :-1]  # Remove the last
                self.y_vps = self.y_vps[
                             :-1]  # Remove the last
                self.y_vdc.insert(variables.index_plot,
                                  int(variables.specimen_voltage))  # Add a new value.
                self.y_vps.insert(variables.index_plot,
                                  int(variables.pulse_voltage))  # Add a new value.
            else:
                # self.x_vdc = self.x_vdc[
                #               1:]  # Remove the first .
                self.x_vdc.append(self.x_vdc[
                                      -1] + 1)  # Add a new value 1 higher than the last.
                # self.y_vdc = self.y_vdc[
                #              1:]  # Remove the first
                # self.y_vps = self.y_vps[
                #              1:]  # Remove the first
                # self.y_vdc.insert(999,
                #                   int(variables.specimen_voltage))  # Add a new value.
                # self.y_vps.insert(999,
                #                   int(variables.pulse_voltage))  # Add a new value.
                self.y_vdc.append(
                    int(variables.specimen_voltage))  # Add a new value.
                self.y_vps.append(
                    int(variables.pulse_voltage))  # Add a new value.
            self.data_line_vdc.setData(self.x_vdc, self.y_vdc)
            self.data_line_vps.setData(self.x_vdc, self.y_vps)

            # # Detection Rate Visualization
            if variables.start_flag == True:
                if variables.index_plot <= 999:
                    self.y_dtec = self.y_dtec[
                                  :-1]  # Remove the first
                    self.y_dtec.insert(variables.index_plot,
                                       int(variables.avg_n_count))  # Add a new value.
                else:
                    self.x_dtec = self.x_dtec[
                                  1:]  # Remove the first element.
                    self.x_dtec.append(self.x_dtec[
                                           -1] + 1)  # Add a new value 1 higher than the last.
                    self.y_dtec = self.y_dtec[1:]
                    self.y_dtec.insert(999, int(variables.avg_n_count))

            self.data_line_dtec.setData(self.x_dtec, self.y_dtec)

            #  Temperature Visualization
            if variables.start_flag == True:
                if variables.index_plot <= 999:
                    self.y_tem = self.y_tem[
                                  :-1]  # Remove the first
                    self.y_tem.insert(variables.index_plot,
                                       int(variables.temperature))  # Add a new value.
                else:
                    self.x_tem = self.x_tem[
                                  1:]  # Remove the first element.
                    self.x_tem.append(self.x_tem[
                                           -1] + 1)  # Add a new value 1 higher than the last.
                    self.y_tem = self.y_tem[1:]
                    self.y_tem.insert(999, int(variables.temperature))

            self.data_line_tem.setData(self.x_tem, self.y_tem)

            # Increase the index
            variables.index_plot += 1

        # Visualization
        if variables.start_flag == False:
            self.x_vdc = list(range(
                1000))  # 1000 time points
            self.y_vdc = [
                             np.nan] * 1000  # 100 data points
            self.y_vps = [
                             np.nan] * 1000  # 100 data points

            self.data_line_vdc.setData(self.x_vdc, self.y_vdc)
            self.data_line_vps.setData(self.x_vdc, self.y_vps)

            self.y_dtec = [np.nan] * 1000

            self.data_line_dtec.setData(self.x_dtec, self.y_dtec)

            self.y_tem = [np.nan] * 1000

            self.data_line_tem.setData(self.x_tem, self.y_tem)

            # Statistics Update
        self.speciemen_voltage.setText(str(float("{:.3f}".format(variables.specimen_voltage))))
        self.pulse_voltage.setText(str(float("{:.3f}".format(variables.pulse_voltage))))
        self.elapsed_time.setText(str(float("{:.3f}".format(variables.elapsed_time))))
        self.total_ions.setText((str(variables.total_ions)))
        self.detection_rate.setText(str
            (float("{:.3f}".format(
            (variables.avg_n_count * 100) / (1 + variables.pulse_frequency * 1000)))))

        # Update the setup parameters
        variables.ex_time = int(self.ex_time.text())
        variables.ex_freq = int(self.ex_freq.text())
        variables.vdc_min = float(self.vdc_min.text())
        if float(self.vdc_max.text()) > 20000:
            _translate = QtCore.QCoreApplication.translate
            self.Error.setText(_translate("OXCART",
                                          "<html><head/><body><p><span style=\" color:#ff0000;\">Maximum possible number is 20KV</span></p></body></html>"))
            self.vdc_max.setText(_translate("OXCART", "4000"))
            variables.vdc_max = float(self.vdc_max.text())
            variables.vdc_step_up = float(self.vdc_steps_up.text())
            variables.vdc_step_down = float(self.vdc_steps_down.text())
            variables.v_p_min = float(self.vp_min.text())
            if float(self.vp_max.text()) > 3281:
                _translate = QtCore.QCoreApplication.translate
            self.Error.setText(_translate("OXCART",
                                          "<html><head/><body><p><span style=\" color:#ff0000;\">Maximum possible number is 3281 V</span></p></body></html>"))
            self.vp_max.setText(_translate("OXCART", "3281"))
            variables.v_p_max = float(self.vp_max.text())
            variables.pulse_fraction = float(self.pulse_fraction.text()) / 100
            variables.pulse_frequency = int(self.pulse_frequency.text())
            variables.detection_rate = int(self.detection_rate_init.text())
            variables.hdf5_path = self.hdf5_path.text()
            variables.cycle_avg = int(self.cycle_avg.text())

    def update_cameras(self):

        self.camera0 = QImage(variables.img0_orig, 500, 500, QImage.Format_RGB888)
        self.camera0 = QtGui.QPixmap(self.camera0)
        self.camera0_zoom = QImage(variables.img0_zoom, 1200, 500, QImage.Format_RGB888)
        self.camera0_zoom = QtGui.QPixmap(self.camera0_zoom)
        self.camera1 = QImage(variables.img1_orig, 500, 500, QImage.Format_RGB888)
        self.camera1 = QtGui.QPixmap(self.camera1)
        self.camera1_zoom = QImage(variables.img1_zoom, 1200, 500, QImage.Format_RGB888)
        self.camera1_zoom = QtGui.QPixmap(self.camera1_zoom)
        # self.camera0 = QPixmap(".\png\\1.png")
        # self.camera0_zoom = QPixmap(".\png\\1_zoom.png")
        # self.camera1 = QPixmap(".\png\\2.png")
        # self.camera1_zoom = QPixmap(".\png\\2_zoom.png")
        self.cam_s_o.setPixmap(self.camera0)
        self.cam_b_o.setPixmap(self.camera1)
        self.cam_s_d.setPixmap(self.camera0_zoom)
        self.cam_b_d.setPixmap(self.camera1_zoom)


class MainThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, ):
        QThread.__init__(self, )
        # run method gets called when we start the thread

    def run(self):
        main_tread = oxcart.main()
        # subprocess.check_output(main_tread)
        self.signal.emit(main_tread)


if __name__ == "__main__":
    # Initialize global experiment variables
    variables.init()

    app = QtWidgets.QApplication(sys.argv)

    # get display resolution
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    print('Screen size is:(%s,%s)' % (width, height))
    # Cameras thread
    camera = camera.Camera()
    cameras, converter = camera.camera_init()
    camera_thread = threading.Thread(target=camera.update_cameras, args=(cameras, converter))
    camera_thread.setDaemon(True)
    camera_thread.start()
    OXCART = QtWidgets.QMainWindow()
    ui = Ui_OXCART(cameras, converter)
    ui.setupUi(OXCART)
    OXCART.show()
    sys.exit(app.exec_())