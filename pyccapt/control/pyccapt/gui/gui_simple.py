"""
This is the main script of main GUI of the simple Atom Probe control GUI.
"""

import numpy as np
import threading
import datetime
import os
# PyQt and PyQtgraph libraries
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QScreen
import pyqtgraph as pg
import pyqtgraph.exporters

# Local module and scripts
from pyccapt.apt import apt_tdc_roetdec
from pyccapt.control_tools import variables, tof2mc_simple
from pyccapt.devices import initialize_devices


class UI_APT_S(object):
    """
    The GUI class of simple atom probe GUI
    """

    def __init__(self, lock, app, conf):
        self.lock = lock  # Lock for thread ...
        self.app = app
        self.conf = conf

    def setupUi(self, UI_APT_S):
        UI_APT_S.setObjectName("UI_APT_S")
        UI_APT_S.resize(1400, 838)
        self.centralwidget = QtWidgets.QWidget(UI_APT_S)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_43 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy)
        self.label_43.setObjectName("label_43")
        self.gridLayout.addWidget(self.label_43, 0, 0, 1, 1)
        self.ex_user = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ex_user.sizePolicy().hasHeightForWidth())
        self.ex_user.setSizePolicy(sizePolicy)
        self.ex_user.setStyleSheet("QLineEdit{\n"
                                   "background: rgb(223,223,233)\n"
                                   "}")
        self.ex_user.setObjectName("ex_user")
        self.gridLayout.addWidget(self.ex_user, 0, 3, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 1, 0, 1, 1)
        self.ex_name = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ex_name.sizePolicy().hasHeightForWidth())
        self.ex_name.setSizePolicy(sizePolicy)
        self.ex_name.setStyleSheet("QLineEdit{\n"
                                   "background: rgb(223,223,233)\n"
                                   "}")
        self.ex_name.setObjectName("ex_name")
        self.gridLayout.addWidget(self.ex_name, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 2)
        self.criteria_time = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
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
        self.gridLayout.addWidget(self.criteria_time, 2, 2, 1, 1)
        self.ex_time = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ex_time.sizePolicy().hasHeightForWidth())
        self.ex_time.setSizePolicy(sizePolicy)
        self.ex_time.setStyleSheet("QLineEdit{\n"
                                   "background: rgb(223,223,233)\n"
                                   "}")
        self.ex_time.setObjectName("ex_time")
        self.gridLayout.addWidget(self.ex_time, 2, 3, 1, 1)
        self.label_41 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_41.sizePolicy().hasHeightForWidth())
        self.label_41.setSizePolicy(sizePolicy)
        self.label_41.setObjectName("label_41")
        self.gridLayout.addWidget(self.label_41, 3, 0, 1, 1)
        self.criteria_ions = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
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
        self.gridLayout.addWidget(self.criteria_ions, 3, 2, 1, 1)
        self.max_ions = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_ions.sizePolicy().hasHeightForWidth())
        self.max_ions.setSizePolicy(sizePolicy)
        self.max_ions.setStyleSheet("QLineEdit{\n"
                                    "background: rgb(223,223,233)\n"
                                    "}")
        self.max_ions.setObjectName("max_ions")
        self.gridLayout.addWidget(self.max_ions, 3, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 2)
        self.ex_freq = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ex_freq.sizePolicy().hasHeightForWidth())
        self.ex_freq.setSizePolicy(sizePolicy)
        self.ex_freq.setStyleSheet("QLineEdit{\n"
                                   "background: rgb(223,223,233)\n"
                                   "}")
        self.ex_freq.setObjectName("ex_freq")
        self.gridLayout.addWidget(self.ex_freq, 4, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 2)
        self.vdc_min = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vdc_min.sizePolicy().hasHeightForWidth())
        self.vdc_min.setSizePolicy(sizePolicy)
        self.vdc_min.setStyleSheet("QLineEdit{\n"
                                   "background: rgb(223,223,233)\n"
                                   "}")
        self.vdc_min.setObjectName("vdc_min")
        self.gridLayout.addWidget(self.vdc_min, 5, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 2)
        self.criteria_vdc = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
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
        self.gridLayout.addWidget(self.criteria_vdc, 6, 2, 1, 1)
        self.vdc_max = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vdc_max.sizePolicy().hasHeightForWidth())
        self.vdc_max.setSizePolicy(sizePolicy)
        self.vdc_max.setStyleSheet("QLineEdit{\n"
                                   "background: rgb(223,223,233)\n"
                                   "}")
        self.vdc_max.setObjectName("vdc_max")
        self.gridLayout.addWidget(self.vdc_max, 6, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)
        self.vdc_steps_up = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vdc_steps_up.sizePolicy().hasHeightForWidth())
        self.vdc_steps_up.setSizePolicy(sizePolicy)
        self.vdc_steps_up.setStyleSheet("QLineEdit{\n"
                                        "background: rgb(223,223,233)\n"
                                        "}")
        self.vdc_steps_up.setObjectName("vdc_steps_up")
        self.gridLayout.addWidget(self.vdc_steps_up, 7, 3, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setObjectName("label_28")
        self.gridLayout.addWidget(self.label_28, 8, 0, 1, 1)
        self.vdc_steps_down = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vdc_steps_down.sizePolicy().hasHeightForWidth())
        self.vdc_steps_down.setSizePolicy(sizePolicy)
        self.vdc_steps_down.setStyleSheet("QLineEdit{\n"
                                          "background: rgb(223,223,233)\n"
                                          "}")
        self.vdc_steps_down.setObjectName("vdc_steps_down")
        self.gridLayout.addWidget(self.vdc_steps_down, 8, 3, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 9, 0, 1, 1)
        self.cycle_avg = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cycle_avg.sizePolicy().hasHeightForWidth())
        self.cycle_avg.setSizePolicy(sizePolicy)
        self.cycle_avg.setStyleSheet("QLineEdit{\n"
                                     "background: rgb(223,223,233)\n"
                                     "}")
        self.cycle_avg.setObjectName("cycle_avg")
        self.gridLayout.addWidget(self.cycle_avg, 9, 3, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 10, 0, 1, 1)
        self.pulse_fraction = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pulse_fraction.sizePolicy().hasHeightForWidth())
        self.pulse_fraction.setSizePolicy(sizePolicy)
        self.pulse_fraction.setStyleSheet("QLineEdit{\n"
                                          "background: rgb(223,223,233)\n"
                                          "}")
        self.pulse_fraction.setObjectName("pulse_fraction")
        self.gridLayout.addWidget(self.pulse_fraction, 10, 3, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 11, 0, 1, 1)
        self.pulse_frequency = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pulse_frequency.sizePolicy().hasHeightForWidth())
        self.pulse_frequency.setSizePolicy(sizePolicy)
        self.pulse_frequency.setStyleSheet("QLineEdit{\n"
                                           "background: rgb(223,223,233)\n"
                                           "}")
        self.pulse_frequency.setObjectName("pulse_frequency")
        self.gridLayout.addWidget(self.pulse_frequency, 11, 3, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 12, 0, 1, 1)
        self.detection_rate_init = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detection_rate_init.sizePolicy().hasHeightForWidth())
        self.detection_rate_init.setSizePolicy(sizePolicy)
        self.detection_rate_init.setStyleSheet("QLineEdit{\n"
                                               "background: rgb(223,223,233)\n"
                                               "}")
        self.detection_rate_init.setObjectName("detection_rate_init")
        self.gridLayout.addWidget(self.detection_rate_init, 12, 3, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 13, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy)
        self.doubleSpinBox.setStyleSheet("QDoubleSpinBox{\n"
                                         "background: rgb(223,223,233)\n"
                                         "}")
        self.doubleSpinBox.setProperty("value", 1.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout.addWidget(self.doubleSpinBox, 13, 2, 1, 1)
        self.hit_displayed = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hit_displayed.sizePolicy().hasHeightForWidth())
        self.hit_displayed.setSizePolicy(sizePolicy)
        self.hit_displayed.setStyleSheet("QLineEdit{\n"
                                         "background: rgb(223,223,233)\n"
                                         "}")
        self.hit_displayed.setObjectName("hit_displayed")
        self.gridLayout.addWidget(self.hit_displayed, 13, 3, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 14, 0, 1, 1)
        self.email = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.email.sizePolicy().hasHeightForWidth())
        self.email.setSizePolicy(sizePolicy)
        self.email.setStyleSheet("QLineEdit{\n"
                                 "background: rgb(223,223,233)\n"
                                 "}")
        self.email.setText("")
        self.email.setObjectName("email")
        self.gridLayout.addWidget(self.email, 14, 3, 1, 1)
        self.label_42 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy)
        self.label_42.setObjectName("label_42")
        self.gridLayout.addWidget(self.label_42, 15, 0, 1, 1)
        self.counter_source = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.counter_source.sizePolicy().hasHeightForWidth())
        self.counter_source.setSizePolicy(sizePolicy)
        self.counter_source.setObjectName("counter_source")
        self.counter_source.addItem("")
        self.gridLayout.addWidget(self.counter_source, 15, 3, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.gridLayout.addWidget(self.label_29, 16, 0, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_31.sizePolicy().hasHeightForWidth())
        self.label_31.setSizePolicy(sizePolicy)
        self.label_31.setObjectName("label_31")
        self.gridLayout.addWidget(self.label_31, 17, 0, 1, 1)
        self.criteria_laser = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
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
        self.gridLayout.addWidget(self.criteria_laser, 17, 2, 1, 1)
        self.fixed_laser = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fixed_laser.sizePolicy().hasHeightForWidth())
        self.fixed_laser.setSizePolicy(sizePolicy)
        self.fixed_laser.setStyleSheet("QLineEdit{\n"
                                       "background: rgb(223,223,233)\n"
                                       "}")
        self.fixed_laser.setText("0")
        self.fixed_laser.setObjectName("fixed_laser")
        self.gridLayout.addWidget(self.fixed_laser, 17, 3, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 18, 0, 1, 1)
        self.laser_num_ions_per_step = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_num_ions_per_step.sizePolicy().hasHeightForWidth())
        self.laser_num_ions_per_step.setSizePolicy(sizePolicy)
        self.laser_num_ions_per_step.setStyleSheet("QLineEdit{\n"
                                                   "background: rgb(223,223,233)\n"
                                                   "}")
        self.laser_num_ions_per_step.setObjectName("laser_num_ions_per_step")
        self.gridLayout.addWidget(self.laser_num_ions_per_step, 18, 3, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_30.sizePolicy().hasHeightForWidth())
        self.label_30.setSizePolicy(sizePolicy)
        self.label_30.setObjectName("label_30")
        self.gridLayout.addWidget(self.label_30, 19, 0, 1, 1)
        self.laser_increase_per_step = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_increase_per_step.sizePolicy().hasHeightForWidth())
        self.laser_increase_per_step.setSizePolicy(sizePolicy)
        self.laser_increase_per_step.setStyleSheet("QLineEdit{\n"
                                                   "background: rgb(223,223,233)\n"
                                                   "}")
        self.laser_increase_per_step.setObjectName("laser_increase_per_step")
        self.gridLayout.addWidget(self.laser_increase_per_step, 19, 3, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 20, 0, 1, 1)
        self.laser_start = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_start.sizePolicy().hasHeightForWidth())
        self.laser_start.setSizePolicy(sizePolicy)
        self.laser_start.setStyleSheet("QLineEdit{\n"
                                       "background: rgb(223,223,233)\n"
                                       "}")
        self.laser_start.setObjectName("laser_start")
        self.gridLayout.addWidget(self.laser_start, 20, 3, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 21, 0, 1, 1)
        self.laser_stop = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laser_stop.sizePolicy().hasHeightForWidth())
        self.laser_stop.setSizePolicy(sizePolicy)
        self.laser_stop.setStyleSheet("QLineEdit{\n"
                                      "background: rgb(223,223,233)\n"
                                      "}")
        self.laser_stop.setObjectName("laser_stop")
        self.gridLayout.addWidget(self.laser_stop, 21, 3, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 22, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 23, 0, 1, 1)
        self.elapsed_time = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.elapsed_time.sizePolicy().hasHeightForWidth())
        self.elapsed_time.setSizePolicy(sizePolicy)
        self.elapsed_time.setStyleSheet("QLineEdit{\n"
                                        "background: rgb(223,223,233)\n"
                                        "}")
        self.elapsed_time.setText("")
        self.elapsed_time.setObjectName("elapsed_time")
        self.gridLayout.addWidget(self.elapsed_time, 23, 1, 1, 3)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 24, 0, 1, 1)
        self.total_ions = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.total_ions.sizePolicy().hasHeightForWidth())
        self.total_ions.setSizePolicy(sizePolicy)
        self.total_ions.setStyleSheet("QLineEdit{\n"
                                      "background: rgb(223,223,233)\n"
                                      "}")
        self.total_ions.setText("")
        self.total_ions.setObjectName("total_ions")
        self.gridLayout.addWidget(self.total_ions, 24, 1, 1, 3)
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 25, 0, 1, 1)
        self.speciemen_voltage = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speciemen_voltage.sizePolicy().hasHeightForWidth())
        self.speciemen_voltage.setSizePolicy(sizePolicy)
        self.speciemen_voltage.setStyleSheet("QLineEdit{\n"
                                             "background: rgb(223,223,233)\n"
                                             "}")
        self.speciemen_voltage.setText("")
        self.speciemen_voltage.setObjectName("speciemen_voltage")
        self.gridLayout.addWidget(self.speciemen_voltage, 25, 1, 1, 3)
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 26, 0, 1, 1)
        self.detection_rate = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.detection_rate.sizePolicy().hasHeightForWidth())
        self.detection_rate.setSizePolicy(sizePolicy)
        self.detection_rate.setStyleSheet("QLineEdit{\n"
                                          "background: rgb(223,223,233)\n"
                                          "}")
        self.detection_rate.setText("")
        self.detection_rate.setObjectName("detection_rate")
        self.gridLayout.addWidget(self.detection_rate, 26, 1, 1, 3)
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
        self.gridLayout.addWidget(self.start_button, 27, 1, 1, 2)
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
        self.gridLayout.addWidget(self.stop_button, 28, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_4.addWidget(self.label_10)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # self.vdc_time = QtWidgets.QWidget(self.centralwidget)
        self.vdc_time = pg.PlotWidget(self.centralwidget)
        self.vdc_time.setMinimumSize(QtCore.QSize(0, 0))
        self.vdc_time.setStyleSheet("QWidget{\n"
                                    "border: 2px solid gray;\n"
                                    "border-radius: 10px;\n"
                                    "padding: 4 4px;\n"
                                    "}")
        self.vdc_time.setObjectName("vdc_time")
        self.horizontalLayout_2.addWidget(self.vdc_time)
        # self.detection_rate_viz = QtWidgets.QWidget(self.centralwidget)
        self.detection_rate_viz = pg.PlotWidget(self.centralwidget)
        self.detection_rate_viz.setMinimumSize(QtCore.QSize(0, 0))
        self.detection_rate_viz.setStyleSheet("QWidget{\n"
                                              "border: 2px solid gray;\n"
                                              "border-radius: 10px;\n"
                                              "padding: 4 4px;\n"
                                              "}")
        self.detection_rate_viz.setObjectName("detection_rate_viz")
        self.horizontalLayout_2.addWidget(self.detection_rate_viz)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        ###
        # self.visualization = QtWidgets.QWidget(self.centralwidget)
        self.visualization = pg.PlotWidget(self.centralwidget)
        self.visualization.setObjectName("visualization")
        self.detector_circle = pg.QtGui.QGraphicsEllipseItem(-40, -40, 80, 80)  # x, y, width, height
        self.detector_circle.setPen(pg.mkPen(color=(255, 0, 0), width=1))
        self.visualization.addItem(self.detector_circle)
        ###
        self.visualization.setMinimumSize(QtCore.QSize(0, 0))
        self.visualization.setAcceptDrops(True)
        self.visualization.setStyleSheet("QWidget{\n"
                                         "border: 2px solid gray;\n"
                                         "border-radius: 10px;\n"
                                         "padding: 4 4px;\n"
                                         "}")
        self.visualization.setObjectName("visualization")
        self.horizontalLayout.addWidget(self.visualization)
        # self.histogram = QtWidgets.QGraphicsView(self.centralwidget)
        self.histogram = pg.PlotWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.histogram.sizePolicy().hasHeightForWidth())
        self.histogram.setSizePolicy(sizePolicy)
        self.histogram.setMinimumSize(QtCore.QSize(0, 0))
        self.histogram.setStyleSheet("QWidget{\n"
                                     "border: 2px solid gray;\n"
                                     "border-radius: 10px;\n"
                                     "padding: 4 4px;\n"
                                     "}")
        self.histogram.setObjectName("histogram")
        self.horizontalLayout.addWidget(self.histogram)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Error = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.Error.setFont(font)
        self.Error.setAlignment(QtCore.Qt.AlignCenter)
        self.Error.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.Error.setObjectName("Error")
        self.verticalLayout.addWidget(self.Error)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 1, 1, 1)
        UI_APT_S.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(UI_APT_S)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 999, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        UI_APT_S.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(UI_APT_S)
        self.statusbar.setObjectName("statusbar")
        UI_APT_S.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(UI_APT_S)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(UI_APT_S)
        QtCore.QMetaObject.connectSlotsByName(UI_APT_S)

    def retranslateUi(self, UI_APT_S):
        _translate = QtCore.QCoreApplication.translate
        UI_APT_S.setWindowTitle(_translate("UI_APT_S", "APT Control Software"))
        self.label_43.setText(_translate("UI_APT_S", "Experiment User"))
        self.ex_user.setText(_translate("UI_APT_S", "user"))
        self.label_21.setText(_translate("UI_APT_S", "Experiment Name"))
        self.ex_name.setText(_translate("UI_APT_S", "test"))
        self.label_2.setText(_translate("UI_APT_S", "Max. Experiment Time (S)"))
        self.ex_time.setText(_translate("UI_APT_S", "90"))
        self.label_41.setText(_translate("UI_APT_S", "Max. Number of Ions"))
        self.max_ions.setText(_translate("UI_APT_S", "2000"))
        self.label_3.setText(_translate("UI_APT_S", "Control refresh Freq.(Hz)"))
        self.ex_freq.setText(_translate("UI_APT_S", "10"))
        self.label_4.setText(_translate("UI_APT_S", "Specimen Start Voltage (V)"))
        self.vdc_min.setText(_translate("UI_APT_S", "500"))
        self.label_5.setText(_translate("UI_APT_S", "Specimen Stop Voltage (V)"))
        self.vdc_max.setText(_translate("UI_APT_S", "4000"))
        self.label_6.setText(_translate("UI_APT_S", "K_p Upwards"))
        self.vdc_steps_up.setText(_translate("UI_APT_S", "100"))
        self.label_28.setText(_translate("UI_APT_S", "K_p Downwards"))
        self.vdc_steps_down.setText(_translate("UI_APT_S", "100"))
        self.label_20.setText(_translate("UI_APT_S", "Cycle for Avg. (Hz)"))
        self.cycle_avg.setText(_translate("UI_APT_S", "10"))
        self.label_25.setText(_translate("UI_APT_S", "Pulse Fraction (%)"))
        self.pulse_fraction.setText(_translate("UI_APT_S", "20"))
        self.label_23.setText(_translate("UI_APT_S", "Pulse Frequency (KHz)"))
        self.pulse_frequency.setText(_translate("UI_APT_S", "200"))
        self.label_17.setText(_translate("UI_APT_S", "Detection Rate (%)"))
        self.detection_rate_init.setText(_translate("UI_APT_S", "1"))
        self.label_22.setText(_translate("UI_APT_S", "# Hits Displayed"))
        self.hit_displayed.setText(_translate("UI_APT_S", "20000"))
        self.label_26.setText(_translate("UI_APT_S", "Email"))
        self.label_42.setText(_translate("UI_APT_S", "Counter Source"))
        self.counter_source.setItemText(0, _translate("UI_APT_S", "TDC"))
        self.label_29.setText(_translate("UI_APT_S", "Laser Control"))
        self.label_31.setText(_translate("UI_APT_S", "Fix"))
        self.label_18.setText(_translate("UI_APT_S", "# Ions per step"))
        self.laser_num_ions_per_step.setText(_translate("UI_APT_S", "2000"))
        self.label_30.setText(_translate("UI_APT_S", "Increase per Step "))
        self.laser_increase_per_step.setText(_translate("UI_APT_S", "2"))
        self.label_16.setText(_translate("UI_APT_S", "Start"))
        self.laser_start.setText(_translate("UI_APT_S", "10"))
        self.label_27.setText(_translate("UI_APT_S", "Stop"))
        self.laser_stop.setText(_translate("UI_APT_S", "40"))
        self.label_11.setText(_translate("UI_APT_S", "Run Statistics"))
        self.label_12.setText(_translate("UI_APT_S", "Elapsed Time (S):"))
        self.label_13.setText(_translate("UI_APT_S", "Total Ions"))
        self.label_14.setText(_translate("UI_APT_S", "Specimen Voltage (V)"))
        self.label_15.setText(_translate("UI_APT_S", "Detection Rate (%)"))
        self.start_button.setText(_translate("UI_APT_S", "Start"))
        ###
        UI_APT_S.setWindowIcon(QtGui.QIcon('./files/logo3.png'))
        self._translate = QtCore.QCoreApplication.translate
        self.start_button.clicked.connect(self.thread_main)
        self.thread = MainThread(self.conf)
        self.thread.signal.connect(self.finished_thread_main)
        self.stop_button.setText(_translate("APT_Physic", "Stop"))
        self.stop_button.clicked.connect(self.stop_ex)
        ###
        self.label_7.setText(_translate("UI_APT_S", "Voltage"))
        self.label_10.setText(_translate("UI_APT_S", "Detection Rate"))
        self.label_19.setText(_translate("UI_APT_S", "Visualization"))
        self.label_24.setText(_translate("UI_APT_S", "TOF"))
        self.Error.setText(_translate("UI_APT_S", "<html><head/><body><p><br/></p></body></html>"))
        self.menuFile.setTitle(_translate("UI_APT_S", "File"))
        self.actionExit.setText(_translate("UI_APT_S", "Exit"))

        ############
        self.doubleSpinBox.setValue(1.0)
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.histogram.setLabel("left", "Frequency (counts)", **styles)
        self.histogram.setLabel("bottom", "Time (ns)", **styles)

        # High Voltage visualization ################
        self.x_vdc = np.arange(1000)  # 1000 time points
        self.y_vdc = np.zeros(1000)  # 1000 data points
        self.y_vdc[:] = np.nan
        # Add legend
        self.vdc_time.addLegend()
        pen_vdc = pg.mkPen(color=(255, 0, 0), width=6)
        self.data_line_vdc = self.vdc_time.plot(self.x_vdc, self.y_vdc, name="High Vol.", pen=pen_vdc)
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

        # Visualization #####################
        self.scatter = pg.ScatterPlotItem(
            size=self.doubleSpinBox.value(), brush=pg.mkBrush(255, 255, 255, 120))
        self.visualization.getPlotItem().hideAxis('bottom')
        self.visualization.getPlotItem().hideAxis('left')

        # timer plot, variables
        self.timer2 = QtCore.QTimer()
        self.timer2.setInterval(1000)
        self.timer2.timeout.connect(self.update_plot_data)
        self.timer2.start()
        self.timer3 = QtCore.QTimer()
        self.timer3.setInterval(2000)
        self.timer3.timeout.connect(self.statistics)
        self.timer3.start()

    def thread_main(self):
        """
            Main thread for running experiment
            """
        self.start_button.setEnabled(False)  # Disable the start button in the GUI
        variables.plot_clear_flag = True  # Change the flag to clear the plots in GUI

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
        variables.counter_source = str(self.counter_source.currentText())
        variables.fixed_laser = int(float(self.fixed_laser.text()))
        variables.laser_num_ions_per_step = int(float(self.laser_num_ions_per_step.text()))
        variables.laser_increase_per_step = int(float(self.laser_increase_per_step.text()))
        variables.laser_start = int(float(self.laser_start.text()))
        variables.laser_stop = int(float(self.laser_stop.text()))
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
        if self.criteria_laser.isChecked():
            variables.criteria_laser = True
        elif not self.criteria_laser.isChecked():
            variables.criteria_laser = False

        # Read the experiment counter
        with open('./files/counter_physic.txt') as f:
            variables.counter = int(f.readlines()[0])
        # Current time and date
        now = datetime.datetime.now()
        variables.exp_name = "%s_" % variables.counter + \
                             now.strftime("%b-%d-%Y_%H-%M") + "_%s" % variables.hdf5_path
        p = os.path.abspath(os.path.join(__file__, "../../../.."))
        variables.path = os.path.join(p, 'data_laser_pulse_mode\\%s' % variables.exp_name)
        # Create folder to save the data
        if not os.path.isdir(variables.path):
            os.makedirs(variables.path, mode=0o777, exist_ok=True)
        # start the run methos of MainThread Class, which is main function of apt_voltage.py
        self.thread.start()

    def finished_thread_main(self):
        """
            The function that is run after end of experiment(MainThread)
            """
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        QScreen.grabWindow(self.app.primaryScreen(),
                           QApplication.desktop().winId()).save(variables.path + '/screenshot.png')

    def stop_ex(self):
        """
            The function that is run if STOP button is pressed
            """
        if variables.start_flag == True:
            variables.stop_flag = True  # Set the STOP flag
            self.stop_button.setEnabled(False)  # Disable the stop button

    def thread_worker(self, target):
        """
            The function for creating workers
            """
        return threading.Thread(target=target)

    def update_plot_data(self):
        """
            The function for updating plots
            """
        if variables.index_auto_scale_graph == 30:
            self.vdc_time.enableAutoRange(axis='x')
            self.detection_rate_viz.enableAutoRange(axis='x')
            variables.index_auto_scale_graph = 0

        self.vdc_time.disableAutoRange()
        self.detection_rate_viz.disableAutoRange()

        variables.index_auto_scale_graph += 1

        if variables.plot_clear_flag:
            self.x_vdc = np.arange(1000)  # 1000 time points
            self.y_vdc = np.zeros(1000)  # 1000 data points
            self.y_vdc[:] = np.nan

            self.data_line_vdc.setData(self.x_vdc, self.y_vdc)

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
                # V_dc
                if variables.index_plot <= 999:
                    self.y_vdc[variables.index_plot] = int(
                        variables.specimen_voltage)  # Add a new value.
                else:
                    self.x_vdc = np.append(self.x_vdc,
                                           self.x_vdc[
                                               -1] + 1)  # Add a new value 1 higher than the last.
                    self.y_vdc = np.append(self.y_vdc,
                                           int(variables.specimen_voltage))  # Add a new value.

                self.data_line_vdc.setData(self.x_vdc, self.y_vdc)

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
                            viz = tof2mc_simple.tof_bin2mc_sc(variables.t[:max_lenght], 0,
                                                              variables.main_v_dc_dld[:max_lenght],
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

                    except:
                        print(
                            f"{initialize_devices.bcolors.FAIL}Error: Cannot plot Histogram correctly{initialize_devices.bcolors.ENDC}")

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
                    except:
                        print(
                            f"{initialize_devices.FAIL}Error: Cannot plot Ions correctly{initialize_devices.bcolors.ENDC}")

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
        self.elapsed_time.setText(str(float("{:.3f}".format(variables.elapsed_time))))
        self.total_ions.setText((str(variables.total_ions)))
        self.detection_rate.setText(str
            (float("{:.3f}".format(
            (variables.avg_n_count * 100) / (1 + variables.pulse_frequency * 1000)))))

    def statistics(self):
        """
            The function for updating statistics in the GUI
            """

        # Clean up the error message
        if variables.index_warning_message == 15:
            _translate = QtCore.QCoreApplication.translate
            self.Error.setText(_translate("APT_Physic",
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
            variables.counter_source = str(self.counter_source.currentText())
            variables.fixed_laser = int(float(self.fixed_laser.text()))
            variables.laser_num_ions_per_step = int(float(self.laser_num_ions_per_step.text()))
            variables.laser_increase_per_step = int(float(self.laser_increase_per_step.text()))
            variables.laser_start = int(float(self.laser_start.text()))
            variables.laser_stop = int(float(self.laser_stop.text()))

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
            if self.criteria_laser.isChecked():
                variables.criteria_laser = True
            elif not self.criteria_laser.isChecked():
                variables.criteria_laser = False

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


        except Exception as e:
            print(e)
            print(
                f"{initialize_devices.bcolors.FAIL}Error: Cannot update setup parameters{initialize_devices.bcolors.ENDC}")


class MainThread(QThread):
    """
    A class for creating main_thread for the APT experiments
    The run method create thread of main function in the experiment script
    """

    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self, conf):
        QThread.__init__(self, )
        self.conf = conf

    def run(self):
        main_thread = apt_tdc_roetdec.main(self.conf)
        self.signal.emit(main_thread)
