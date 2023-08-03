import os
import sys
import threading

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from pypylon import pylon

# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files
from pyccapt.control.devices.camera import Camera
from pyccapt.control.gui import gui_cameras
from pyccapt.control.gui import gui_gates


class Ui_PyCCAPT(object):

        def __init__(self, variables, conf, camera):
                self.camera = camera
                self.conf = conf
                self.variables = variables

        def setupUi(self, PyCCAPT):
                PyCCAPT.setObjectName("PyCCAPT")
                PyCCAPT.resize(905, 827)
                self.centralwidget = QtWidgets.QWidget(parent=PyCCAPT)
                self.centralwidget.setObjectName("centralwidget")
                self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
                self.gridLayout_5.setObjectName("gridLayout_5")
                self.gridLayout_4 = QtWidgets.QGridLayout()
                self.gridLayout_4.setObjectName("gridLayout_4")
                self.horizontalLayout = QtWidgets.QHBoxLayout()
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.gates_control = QtWidgets.QPushButton(parent=self.centralwidget)
                self.gates_control.setStyleSheet("QPushButton{\n"
                                                 "background: rgb(193, 193, 193)\n"
                                                 "}")
                self.gates_control.setObjectName("gates_control")
                self.horizontalLayout.addWidget(self.gates_control)
                self.pumps_vaccum = QtWidgets.QPushButton(parent=self.centralwidget)
                self.pumps_vaccum.setStyleSheet("QPushButton{\n"
                                                "background: rgb(193, 193, 193)\n"
                                                "}")
                self.pumps_vaccum.setObjectName("pumps_vaccum")
                self.horizontalLayout.addWidget(self.pumps_vaccum)
                self.Camears = QtWidgets.QPushButton(parent=self.centralwidget)
                self.Camears.setStyleSheet("QPushButton{\n"
                                           "background: rgb(193, 193, 193)\n"
                                           "}")
                self.Camears.setObjectName("Camears")
                self.horizontalLayout.addWidget(self.Camears)
                self.laser_control = QtWidgets.QPushButton(parent=self.centralwidget)
                self.laser_control.setStyleSheet("QPushButton{\n"
                                                 "background: rgb(193, 193, 193)\n"
                                                 "}")
                self.laser_control.setObjectName("laser_control")
                self.horizontalLayout.addWidget(self.laser_control)
                self.Visualization = QtWidgets.QPushButton(parent=self.centralwidget)
                self.Visualization.setStyleSheet("QPushButton{\n"
                                                 "background: rgb(193, 193, 193)\n"
                                                 "}")
                self.Visualization.setObjectName("Visualization")
                self.horizontalLayout.addWidget(self.Visualization)
                self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 2)
                self.gridLayout = QtWidgets.QGridLayout()
                self.gridLayout.setObjectName("gridLayout")
                self.label_173 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_173.sizePolicy().hasHeightForWidth())
                self.label_173.setSizePolicy(sizePolicy)
                font = QtGui.QFont()
                font.setBold(True)
                self.label_173.setFont(font)
                self.label_173.setObjectName("label_173")
                self.gridLayout.addWidget(self.label_173, 0, 0, 1, 1)
                self.parameters_source = QtWidgets.QComboBox(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.parameters_source.sizePolicy().hasHeightForWidth())
                self.parameters_source.setSizePolicy(sizePolicy)
                self.parameters_source.setMinimumSize(QtCore.QSize(0, 20))
                self.parameters_source.setStyleSheet("QComboBox{\n"
                                                     "background: rgb(223,223,233)\n"
                                                     "}")
                self.parameters_source.setObjectName("parameters_source")
                self.parameters_source.addItem("")
                self.parameters_source.addItem("")
                self.gridLayout.addWidget(self.parameters_source, 0, 6, 1, 1)
                self.label_174 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_174.sizePolicy().hasHeightForWidth())
                self.label_174.setSizePolicy(sizePolicy)
                self.label_174.setObjectName("label_174")
                self.gridLayout.addWidget(self.label_174, 1, 0, 1, 1)
                self.ex_user = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ex_user.sizePolicy().hasHeightForWidth())
                self.ex_user.setSizePolicy(sizePolicy)
                self.ex_user.setMinimumSize(QtCore.QSize(0, 20))
                self.ex_user.setStyleSheet("QLineEdit{\n"
                                           "background: rgb(223,223,233)\n"
                                           "}")
                self.ex_user.setObjectName("ex_user")
                self.gridLayout.addWidget(self.ex_user, 1, 6, 1, 1)
                self.label_175 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_175.sizePolicy().hasHeightForWidth())
                self.label_175.setSizePolicy(sizePolicy)
                self.label_175.setObjectName("label_175")
                self.gridLayout.addWidget(self.label_175, 2, 0, 1, 1)
                self.ex_name = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ex_name.sizePolicy().hasHeightForWidth())
                self.ex_name.setSizePolicy(sizePolicy)
                self.ex_name.setMinimumSize(QtCore.QSize(0, 20))
                self.ex_name.setMaximumSize(QtCore.QSize(16777215, 100))
                self.ex_name.setStyleSheet("QLineEdit{\n"
                                           "background: rgb(223,223,233)\n"
                                           "}")
                self.ex_name.setObjectName("ex_name")
                self.gridLayout.addWidget(self.ex_name, 2, 6, 1, 1)
                self.label_176 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_176.sizePolicy().hasHeightForWidth())
                self.label_176.setSizePolicy(sizePolicy)
                self.label_176.setObjectName("label_176")
                self.gridLayout.addWidget(self.label_176, 3, 0, 1, 2)
                self.criteria_time = QtWidgets.QCheckBox(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
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
                self.gridLayout.addWidget(self.criteria_time, 3, 3, 1, 1)
                self.ex_time = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ex_time.sizePolicy().hasHeightForWidth())
                self.ex_time.setSizePolicy(sizePolicy)
                self.ex_time.setMinimumSize(QtCore.QSize(0, 20))
                self.ex_time.setStyleSheet("QLineEdit{\n"
                                           "background: rgb(223,223,233)\n"
                                           "}")
                self.ex_time.setObjectName("ex_time")
                self.gridLayout.addWidget(self.ex_time, 3, 6, 1, 1)
                self.label_177 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_177.sizePolicy().hasHeightForWidth())
                self.label_177.setSizePolicy(sizePolicy)
                self.label_177.setObjectName("label_177")
                self.gridLayout.addWidget(self.label_177, 4, 0, 1, 1)
                self.criteria_ions = QtWidgets.QCheckBox(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
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
                self.gridLayout.addWidget(self.criteria_ions, 4, 3, 1, 1)
                self.max_ions = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.max_ions.sizePolicy().hasHeightForWidth())
                self.max_ions.setSizePolicy(sizePolicy)
                self.max_ions.setMinimumSize(QtCore.QSize(0, 20))
                self.max_ions.setStyleSheet("QLineEdit{\n"
                                            "background: rgb(223,223,233)\n"
                                            "}")
                self.max_ions.setObjectName("max_ions")
                self.gridLayout.addWidget(self.max_ions, 4, 6, 1, 1)
                self.label_178 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_178.sizePolicy().hasHeightForWidth())
                self.label_178.setSizePolicy(sizePolicy)
                self.label_178.setObjectName("label_178")
                self.gridLayout.addWidget(self.label_178, 5, 0, 1, 2)
                self.ex_freq = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ex_freq.sizePolicy().hasHeightForWidth())
                self.ex_freq.setSizePolicy(sizePolicy)
                self.ex_freq.setMinimumSize(QtCore.QSize(0, 20))
                self.ex_freq.setStyleSheet("QLineEdit{\n"
                                           "background: rgb(223,223,233)\n"
                                           "}")
                self.ex_freq.setObjectName("ex_freq")
                self.gridLayout.addWidget(self.ex_freq, 5, 6, 1, 1)
                self.label_179 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_179.sizePolicy().hasHeightForWidth())
                self.label_179.setSizePolicy(sizePolicy)
                self.label_179.setObjectName("label_179")
                self.gridLayout.addWidget(self.label_179, 6, 0, 1, 3)
                self.vdc_min = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.vdc_min.sizePolicy().hasHeightForWidth())
                self.vdc_min.setSizePolicy(sizePolicy)
                self.vdc_min.setMinimumSize(QtCore.QSize(0, 20))
                self.vdc_min.setStyleSheet("QLineEdit{\n"
                                           "background: rgb(223,223,233)\n"
                                           "}")
                self.vdc_min.setObjectName("vdc_min")
                self.gridLayout.addWidget(self.vdc_min, 6, 6, 1, 1)
                self.label_180 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_180.sizePolicy().hasHeightForWidth())
                self.label_180.setSizePolicy(sizePolicy)
                self.label_180.setObjectName("label_180")
                self.gridLayout.addWidget(self.label_180, 7, 0, 1, 3)
                self.criteria_vdc = QtWidgets.QCheckBox(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
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
                self.gridLayout.addWidget(self.criteria_vdc, 7, 3, 1, 1)
                self.vdc_max = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.vdc_max.sizePolicy().hasHeightForWidth())
                self.vdc_max.setSizePolicy(sizePolicy)
                self.vdc_max.setMinimumSize(QtCore.QSize(0, 20))
                self.vdc_max.setStyleSheet("QLineEdit{\n"
                                           "background: rgb(223,223,233)\n"
                                           "}")
                self.vdc_max.setObjectName("vdc_max")
                self.gridLayout.addWidget(self.vdc_max, 7, 6, 1, 1)
                self.label_181 = QtWidgets.QLabel(parent=self.centralwidget)
                self.label_181.setObjectName("label_181")
                self.gridLayout.addWidget(self.label_181, 8, 0, 1, 1)
                self.vdc_steps_up = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.vdc_steps_up.sizePolicy().hasHeightForWidth())
                self.vdc_steps_up.setSizePolicy(sizePolicy)
                self.vdc_steps_up.setMinimumSize(QtCore.QSize(0, 20))
                self.vdc_steps_up.setStyleSheet("QLineEdit{\n"
                                                "background: rgb(223,223,233)\n"
                                                "}")
                self.vdc_steps_up.setObjectName("vdc_steps_up")
                self.gridLayout.addWidget(self.vdc_steps_up, 8, 6, 1, 1)
                self.label_182 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_182.sizePolicy().hasHeightForWidth())
                self.label_182.setSizePolicy(sizePolicy)
                self.label_182.setObjectName("label_182")
                self.gridLayout.addWidget(self.label_182, 9, 0, 1, 1)
                self.vdc_steps_down = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.vdc_steps_down.sizePolicy().hasHeightForWidth())
                self.vdc_steps_down.setSizePolicy(sizePolicy)
                self.vdc_steps_down.setMinimumSize(QtCore.QSize(0, 20))
                self.vdc_steps_down.setStyleSheet("QLineEdit{\n"
                                                  "background: rgb(223,223,233)\n"
                                                  "}")
                self.vdc_steps_down.setObjectName("vdc_steps_down")
                self.gridLayout.addWidget(self.vdc_steps_down, 9, 6, 1, 1)
                self.label_191 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_191.sizePolicy().hasHeightForWidth())
                self.label_191.setSizePolicy(sizePolicy)
                self.label_191.setObjectName("label_191")
                self.gridLayout.addWidget(self.label_191, 10, 0, 1, 1)
                self.control_algorithm = QtWidgets.QComboBox(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.control_algorithm.sizePolicy().hasHeightForWidth())
                self.control_algorithm.setSizePolicy(sizePolicy)
                self.control_algorithm.setMinimumSize(QtCore.QSize(0, 20))
                self.control_algorithm.setStyleSheet("QComboBox{\n"
                                                     "background: rgb(223,223,233)\n"
                                                     "}")
                self.control_algorithm.setObjectName("control_algorithm")
                self.control_algorithm.addItem("")
                self.control_algorithm.addItem("")
                self.gridLayout.addWidget(self.control_algorithm, 10, 6, 1, 1)
                self.label_183 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_183.sizePolicy().hasHeightForWidth())
                self.label_183.setSizePolicy(sizePolicy)
                self.label_183.setObjectName("label_183")
                self.gridLayout.addWidget(self.label_183, 11, 0, 1, 1)
                self.cycle_avg = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.cycle_avg.sizePolicy().hasHeightForWidth())
                self.cycle_avg.setSizePolicy(sizePolicy)
                self.cycle_avg.setMinimumSize(QtCore.QSize(0, 20))
                self.cycle_avg.setStyleSheet("QLineEdit{\n"
                                             "background: rgb(223,223,233)\n"
                                             "}")
                self.cycle_avg.setObjectName("cycle_avg")
                self.gridLayout.addWidget(self.cycle_avg, 11, 6, 1, 1)
                self.label_184 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_184.sizePolicy().hasHeightForWidth())
                self.label_184.setSizePolicy(sizePolicy)
                self.label_184.setObjectName("label_184")
                self.gridLayout.addWidget(self.label_184, 12, 0, 1, 1)
                self.vp_min = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.vp_min.sizePolicy().hasHeightForWidth())
                self.vp_min.setSizePolicy(sizePolicy)
                self.vp_min.setMinimumSize(QtCore.QSize(0, 20))
                self.vp_min.setStyleSheet("QLineEdit{\n"
                                          "background: rgb(223,223,233)\n"
                                          "}")
                self.vp_min.setObjectName("vp_min")
                self.gridLayout.addWidget(self.vp_min, 12, 6, 1, 1)
                self.label_185 = QtWidgets.QLabel(parent=self.centralwidget)
                self.label_185.setObjectName("label_185")
                self.gridLayout.addWidget(self.label_185, 13, 0, 1, 2)
                self.vp_max = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.vp_max.sizePolicy().hasHeightForWidth())
                self.vp_max.setSizePolicy(sizePolicy)
                self.vp_max.setMinimumSize(QtCore.QSize(0, 20))
                self.vp_max.setStyleSheet("QLineEdit{\n"
                                          "background: rgb(223,223,233)\n"
                                          "}")
                self.vp_max.setObjectName("vp_max")
                self.gridLayout.addWidget(self.vp_max, 13, 6, 1, 1)
                self.label_186 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_186.sizePolicy().hasHeightForWidth())
                self.label_186.setSizePolicy(sizePolicy)
                self.label_186.setObjectName("label_186")
                self.gridLayout.addWidget(self.label_186, 14, 0, 1, 1)
                self.pulse_fraction = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.pulse_fraction.sizePolicy().hasHeightForWidth())
                self.pulse_fraction.setSizePolicy(sizePolicy)
                self.pulse_fraction.setMinimumSize(QtCore.QSize(0, 20))
                self.pulse_fraction.setStyleSheet("QLineEdit{\n"
                                                  "background: rgb(223,223,233)\n"
                                                  "}")
                self.pulse_fraction.setObjectName("pulse_fraction")
                self.gridLayout.addWidget(self.pulse_fraction, 14, 6, 1, 1)
                self.label_187 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_187.sizePolicy().hasHeightForWidth())
                self.label_187.setSizePolicy(sizePolicy)
                self.label_187.setObjectName("label_187")
                self.gridLayout.addWidget(self.label_187, 15, 0, 1, 1)
                self.pulse_frequency = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.pulse_frequency.sizePolicy().hasHeightForWidth())
                self.pulse_frequency.setSizePolicy(sizePolicy)
                self.pulse_frequency.setMinimumSize(QtCore.QSize(0, 20))
                self.pulse_frequency.setStyleSheet("QLineEdit{\n"
                                                   "background: rgb(223,223,233)\n"
                                                   "}")
                self.pulse_frequency.setObjectName("pulse_frequency")
                self.gridLayout.addWidget(self.pulse_frequency, 15, 6, 1, 1)
                self.label_188 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_188.sizePolicy().hasHeightForWidth())
                self.label_188.setSizePolicy(sizePolicy)
                self.label_188.setObjectName("label_188")
                self.gridLayout.addWidget(self.label_188, 16, 0, 1, 1)
                self.detection_rate_init = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.detection_rate_init.sizePolicy().hasHeightForWidth())
                self.detection_rate_init.setSizePolicy(sizePolicy)
                self.detection_rate_init.setMinimumSize(QtCore.QSize(0, 20))
                self.detection_rate_init.setStyleSheet("QLineEdit{\n"
                                                       "background: rgb(223,223,233)\n"
                                                       "}")
                self.detection_rate_init.setObjectName("detection_rate_init")
                self.gridLayout.addWidget(self.detection_rate_init, 16, 6, 1, 1)
                self.label_189 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_189.sizePolicy().hasHeightForWidth())
                self.label_189.setSizePolicy(sizePolicy)
                self.label_189.setObjectName("label_189")
                self.gridLayout.addWidget(self.label_189, 17, 0, 1, 1)
                self.doubleSpinBox = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
                self.doubleSpinBox.setSizePolicy(sizePolicy)
                self.doubleSpinBox.setMinimumSize(QtCore.QSize(0, 20))
                self.doubleSpinBox.setStyleSheet("QDoubleSpinBox{\n"
                                                 "background: rgb(223,223,233)\n"
                                                 "}")
                self.doubleSpinBox.setObjectName("doubleSpinBox")
                self.gridLayout.addWidget(self.doubleSpinBox, 17, 1, 1, 3)
                self.reset_heatmap = QtWidgets.QPushButton(parent=self.centralwidget)
                self.reset_heatmap.setMinimumSize(QtCore.QSize(0, 20))
                self.reset_heatmap.setObjectName("reset_heatmap")
                self.gridLayout.addWidget(self.reset_heatmap, 17, 4, 1, 2)
                self.hit_displayed = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.hit_displayed.sizePolicy().hasHeightForWidth())
                self.hit_displayed.setSizePolicy(sizePolicy)
                self.hit_displayed.setMinimumSize(QtCore.QSize(0, 20))
                self.hit_displayed.setStyleSheet("QLineEdit{\n"
                                                 "background: rgb(223,223,233)\n"
                                                 "}")
                self.hit_displayed.setObjectName("hit_displayed")
                self.gridLayout.addWidget(self.hit_displayed, 17, 6, 1, 1)
                self.label_190 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_190.sizePolicy().hasHeightForWidth())
                self.label_190.setSizePolicy(sizePolicy)
                self.label_190.setObjectName("label_190")
                self.gridLayout.addWidget(self.label_190, 18, 0, 1, 1)
                self.email = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.email.sizePolicy().hasHeightForWidth())
                self.email.setSizePolicy(sizePolicy)
                self.email.setMinimumSize(QtCore.QSize(0, 20))
                self.email.setStyleSheet("QLineEdit{\n"
                                         "background: rgb(223,223,233)\n"
                                         "}")
                self.email.setText("")
                self.email.setObjectName("email")
                self.gridLayout.addWidget(self.email, 18, 6, 1, 1)
                self.label_192 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_192.sizePolicy().hasHeightForWidth())
                self.label_192.setSizePolicy(sizePolicy)
                self.label_192.setObjectName("label_192")
                self.gridLayout.addWidget(self.label_192, 19, 0, 1, 1)
                self.counter_source = QtWidgets.QComboBox(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.counter_source.sizePolicy().hasHeightForWidth())
                self.counter_source.setSizePolicy(sizePolicy)
                self.counter_source.setMinimumSize(QtCore.QSize(0, 20))
                self.counter_source.setStyleSheet("QComboBox{\n"
                                                  "background: rgb(223,223,233)\n"
                                                  "}")
                self.counter_source.setObjectName("counter_source")
                self.counter_source.addItem("")
                self.counter_source.addItem("")
                self.counter_source.addItem("")
                self.gridLayout.addWidget(self.counter_source, 19, 6, 1, 1)
                self.label_193 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_193.sizePolicy().hasHeightForWidth())
                self.label_193.setSizePolicy(sizePolicy)
                font = QtGui.QFont()
                font.setBold(True)
                self.label_193.setFont(font)
                self.label_193.setObjectName("label_193")
                self.gridLayout.addWidget(self.label_193, 20, 0, 1, 1)
                self.label_194 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_194.sizePolicy().hasHeightForWidth())
                self.label_194.setSizePolicy(sizePolicy)
                self.label_194.setObjectName("label_194")
                self.gridLayout.addWidget(self.label_194, 21, 0, 1, 1)
                self.elapsed_time = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.elapsed_time.sizePolicy().hasHeightForWidth())
                self.elapsed_time.setSizePolicy(sizePolicy)
                self.elapsed_time.setMinimumSize(QtCore.QSize(0, 20))
                self.elapsed_time.setStyleSheet("QLineEdit{\n"
                                                "background: rgb(223,223,233)\n"
                                                "}")
                self.elapsed_time.setText("")
                self.elapsed_time.setObjectName("elapsed_time")
                self.gridLayout.addWidget(self.elapsed_time, 21, 5, 1, 2)
                self.label_195 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_195.sizePolicy().hasHeightForWidth())
                self.label_195.setSizePolicy(sizePolicy)
                self.label_195.setObjectName("label_195")
                self.gridLayout.addWidget(self.label_195, 22, 0, 1, 1)
                self.total_ions = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.total_ions.sizePolicy().hasHeightForWidth())
                self.total_ions.setSizePolicy(sizePolicy)
                self.total_ions.setMinimumSize(QtCore.QSize(0, 20))
                self.total_ions.setStyleSheet("QLineEdit{\n"
                                              "background: rgb(223,223,233)\n"
                                              "}")
                self.total_ions.setText("")
                self.total_ions.setObjectName("total_ions")
                self.gridLayout.addWidget(self.total_ions, 22, 5, 1, 2)
                self.label_196 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_196.sizePolicy().hasHeightForWidth())
                self.label_196.setSizePolicy(sizePolicy)
                self.label_196.setObjectName("label_196")
                self.gridLayout.addWidget(self.label_196, 23, 0, 1, 1)
                self.dc_hold = QtWidgets.QPushButton(parent=self.centralwidget)
                self.dc_hold.setMinimumSize(QtCore.QSize(0, 20))
                self.dc_hold.setObjectName("dc_hold")
                self.gridLayout.addWidget(self.dc_hold, 23, 2, 1, 3)
                self.speciemen_voltage = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.speciemen_voltage.sizePolicy().hasHeightForWidth())
                self.speciemen_voltage.setSizePolicy(sizePolicy)
                self.speciemen_voltage.setMinimumSize(QtCore.QSize(0, 20))
                self.speciemen_voltage.setStyleSheet("QLineEdit{\n"
                                                     "background: rgb(223,223,233)\n"
                                                     "}")
                self.speciemen_voltage.setText("")
                self.speciemen_voltage.setObjectName("speciemen_voltage")
                self.gridLayout.addWidget(self.speciemen_voltage, 23, 5, 1, 2)
                self.label_197 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_197.sizePolicy().hasHeightForWidth())
                self.label_197.setSizePolicy(sizePolicy)
                self.label_197.setObjectName("label_197")
                self.gridLayout.addWidget(self.label_197, 24, 0, 1, 1)
                self.pulse_voltage = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.pulse_voltage.sizePolicy().hasHeightForWidth())
                self.pulse_voltage.setSizePolicy(sizePolicy)
                self.pulse_voltage.setMinimumSize(QtCore.QSize(0, 20))
                self.pulse_voltage.setStyleSheet("QLineEdit{\n"
                                                 "background: rgb(223,223,233)\n"
                                                 "}")
                self.pulse_voltage.setText("")
                self.pulse_voltage.setObjectName("pulse_voltage")
                self.gridLayout.addWidget(self.pulse_voltage, 24, 5, 1, 2)
                self.label_198 = QtWidgets.QLabel(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.label_198.sizePolicy().hasHeightForWidth())
                self.label_198.setSizePolicy(sizePolicy)
                self.label_198.setObjectName("label_198")
                self.gridLayout.addWidget(self.label_198, 25, 0, 1, 1)
                self.detection_rate = QtWidgets.QLineEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                   QtWidgets.QSizePolicy.Policy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.detection_rate.sizePolicy().hasHeightForWidth())
                self.detection_rate.setSizePolicy(sizePolicy)
                self.detection_rate.setMinimumSize(QtCore.QSize(0, 20))
                self.detection_rate.setStyleSheet("QLineEdit{\n"
                                                  "background: rgb(223,223,233)\n"
                                                  "}")
                self.detection_rate.setText("")
                self.detection_rate.setObjectName("detection_rate")
                self.gridLayout.addWidget(self.detection_rate, 25, 5, 1, 2)
                self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)
                self.textEdit = QtWidgets.QTextEdit(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                                   QtWidgets.QSizePolicy.Policy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
                self.textEdit.setSizePolicy(sizePolicy)
                self.textEdit.setMinimumSize(QtCore.QSize(0, 100))
                self.textEdit.setStyleSheet("QWidget{\n"
                                            "border: 2px solid gray;\n"
                                            "border-radius: 10px;\n"
                                            "padding: 0 8px;\n"
                                            "background: rgb(223,223,233)\n"
                                            "}")
                self.textEdit.setObjectName("textEdit")
                self.gridLayout_4.addWidget(self.textEdit, 1, 1, 1, 1)
                self.gridLayout_3 = QtWidgets.QGridLayout()
                self.gridLayout_3.setObjectName("gridLayout_3")
                self.gridLayout_2 = QtWidgets.QGridLayout()
                self.gridLayout_2.setObjectName("gridLayout_2")
                self.Error = QtWidgets.QLabel(parent=self.centralwidget)
                self.Error.setMinimumSize(QtCore.QSize(800, 30))
                font = QtGui.QFont()
                font.setPointSize(13)
                font.setBold(True)
                font.setStrikeOut(False)
                self.Error.setFont(font)
                self.Error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.Error.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse)
                self.Error.setObjectName("Error")
                self.gridLayout_2.addWidget(self.Error, 0, 0, 1, 2)
                self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 2, 1)
                self.start_button = QtWidgets.QPushButton(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed,
                                                   QtWidgets.QSizePolicy.Policy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
                self.start_button.setSizePolicy(sizePolicy)
                self.start_button.setMinimumSize(QtCore.QSize(0, 25))
                self.start_button.setStyleSheet("QPushButton{\n"
                                                "background: rgb(193, 193, 193)\n"
                                                "}")
                self.start_button.setObjectName("start_button")
                self.gridLayout_3.addWidget(self.start_button, 0, 1, 1, 1)
                self.stop_button = QtWidgets.QPushButton(parent=self.centralwidget)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed,
                                                   QtWidgets.QSizePolicy.Policy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
                self.stop_button.setSizePolicy(sizePolicy)
                self.stop_button.setMinimumSize(QtCore.QSize(0, 25))
                self.stop_button.setStyleSheet("QPushButton{\n"
                                               "background: rgb(193, 193, 193)\n"
                                               "}")
                self.stop_button.setObjectName("stop_button")
                self.gridLayout_3.addWidget(self.stop_button, 1, 1, 1, 1)
                self.gridLayout_4.addLayout(self.gridLayout_3, 2, 0, 1, 2)
                self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
                PyCCAPT.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(parent=PyCCAPT)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 905, 22))
                self.menubar.setObjectName("menubar")
                self.menuFile = QtWidgets.QMenu(parent=self.menubar)
                self.menuFile.setObjectName("menuFile")
                self.menuEdit = QtWidgets.QMenu(parent=self.menubar)
                self.menuEdit.setObjectName("menuEdit")
                self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
                self.menuHelp.setObjectName("menuHelp")
                self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
                self.menuSettings.setObjectName("menuSettings")
                self.menuView = QtWidgets.QMenu(parent=self.menubar)
                self.menuView.setObjectName("menuView")
                PyCCAPT.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(parent=PyCCAPT)
                self.statusbar.setObjectName("statusbar")
                PyCCAPT.setStatusBar(self.statusbar)
                self.actionExit = QtGui.QAction(parent=PyCCAPT)
                self.actionExit.setObjectName("actionExit")
                self.actiontake_sceernshot = QtGui.QAction(parent=PyCCAPT)
                self.actiontake_sceernshot.setObjectName("actiontake_sceernshot")
                self.menuFile.addAction(self.actionExit)
                self.menuEdit.addAction(self.actiontake_sceernshot)
                self.menubar.addAction(self.menuFile.menuAction())
                self.menubar.addAction(self.menuEdit.menuAction())
                self.menubar.addAction(self.menuView.menuAction())
                self.menubar.addAction(self.menuSettings.menuAction())
                self.menubar.addAction(self.menuHelp.menuAction())

                self.retranslateUi(PyCCAPT)
                QtCore.QMetaObject.connectSlotsByName(PyCCAPT)
                PyCCAPT.setTabOrder(self.parameters_source, self.ex_user)
                PyCCAPT.setTabOrder(self.ex_user, self.ex_name)
                PyCCAPT.setTabOrder(self.ex_name, self.criteria_time)
                PyCCAPT.setTabOrder(self.criteria_time, self.ex_time)
                PyCCAPT.setTabOrder(self.ex_time, self.criteria_ions)
                PyCCAPT.setTabOrder(self.criteria_ions, self.max_ions)
                PyCCAPT.setTabOrder(self.max_ions, self.ex_freq)
                PyCCAPT.setTabOrder(self.ex_freq, self.vdc_min)
                PyCCAPT.setTabOrder(self.vdc_min, self.criteria_vdc)
                PyCCAPT.setTabOrder(self.criteria_vdc, self.vdc_max)
                PyCCAPT.setTabOrder(self.vdc_max, self.vdc_steps_up)
                PyCCAPT.setTabOrder(self.vdc_steps_up, self.vdc_steps_down)
                PyCCAPT.setTabOrder(self.vdc_steps_down, self.control_algorithm)
                PyCCAPT.setTabOrder(self.control_algorithm, self.cycle_avg)
                PyCCAPT.setTabOrder(self.cycle_avg, self.vp_min)
                PyCCAPT.setTabOrder(self.vp_min, self.vp_max)
                PyCCAPT.setTabOrder(self.vp_max, self.pulse_fraction)
                PyCCAPT.setTabOrder(self.pulse_fraction, self.pulse_frequency)
                PyCCAPT.setTabOrder(self.pulse_frequency, self.detection_rate_init)
                PyCCAPT.setTabOrder(self.detection_rate_init, self.doubleSpinBox)
                PyCCAPT.setTabOrder(self.doubleSpinBox, self.reset_heatmap)
                PyCCAPT.setTabOrder(self.reset_heatmap, self.hit_displayed)
                PyCCAPT.setTabOrder(self.hit_displayed, self.email)
                PyCCAPT.setTabOrder(self.email, self.counter_source)
                PyCCAPT.setTabOrder(self.counter_source, self.textEdit)
                PyCCAPT.setTabOrder(self.textEdit, self.start_button)
                PyCCAPT.setTabOrder(self.start_button, self.stop_button)
                PyCCAPT.setTabOrder(self.stop_button, self.gates_control)
                PyCCAPT.setTabOrder(self.gates_control, self.pumps_vaccum)
                PyCCAPT.setTabOrder(self.pumps_vaccum, self.Camears)
                PyCCAPT.setTabOrder(self.Camears, self.laser_control)
                PyCCAPT.setTabOrder(self.laser_control, self.Visualization)
                PyCCAPT.setTabOrder(self.Visualization, self.dc_hold)
                PyCCAPT.setTabOrder(self.dc_hold, self.elapsed_time)
                PyCCAPT.setTabOrder(self.elapsed_time, self.total_ions)
                PyCCAPT.setTabOrder(self.total_ions, self.speciemen_voltage)
                PyCCAPT.setTabOrder(self.speciemen_voltage, self.pulse_voltage)
                PyCCAPT.setTabOrder(self.pulse_voltage, self.detection_rate)

                ###
                self.Camears.clicked.connect(self.open_cameras_win)
                self.gates_control.clicked.connect(self.open_gates_win)

        def retranslateUi(self, PyCCAPT):
                _translate = QtCore.QCoreApplication.translate
                ###
                PyCCAPT.setWindowTitle(_translate("PyCCAPT", "PyCCAPT APT Experiment Control"))
                PyCCAPT.setWindowIcon(QtGui.QIcon('./files/logo3.png'))
                ###
                self.gates_control.setText(_translate("PyCCAPT", "Gates Control"))
                self.pumps_vaccum.setText(_translate("PyCCAPT", "Pumps & Vacuum"))
                self.Camears.setText(_translate("PyCCAPT", "Cameras & Alingment"))
                self.laser_control.setText(_translate("PyCCAPT", "Laser Control"))
                self.Visualization.setText(_translate("PyCCAPT", "Visualization"))
                self.label_173.setText(_translate("PyCCAPT", "Setup Parameters"))
                self.parameters_source.setItemText(0, _translate("PyCCAPT", "TextBox"))
                self.parameters_source.setItemText(1, _translate("PyCCAPT", "TextLine"))
                self.label_174.setText(_translate("PyCCAPT", "Experiment User"))
                self.ex_user.setText(_translate("PyCCAPT", "user"))
                self.label_175.setText(_translate("PyCCAPT", "Experiment Name"))
                self.ex_name.setText(_translate("PyCCAPT", "test"))
                self.label_176.setText(_translate("PyCCAPT", "Max. Experiment Time (S)"))
                self.ex_time.setText(_translate("PyCCAPT", "900"))
                self.label_177.setText(_translate("PyCCAPT", "Max. Number of Ions"))
                self.max_ions.setText(_translate("PyCCAPT", "4000"))
                self.label_178.setText(_translate("PyCCAPT", "Control refresh Freq.(Hz)"))
                self.ex_freq.setText(_translate("PyCCAPT", "10"))
                self.label_179.setText(_translate("PyCCAPT", "Specimen Start Voltage (V)"))
                self.vdc_min.setText(_translate("PyCCAPT", "500"))
                self.label_180.setText(_translate("PyCCAPT", "Specimen Stop Voltage (V)"))
                self.vdc_max.setText(_translate("PyCCAPT", "4000"))
                self.label_181.setText(_translate("PyCCAPT", "K_p Upwards"))
                self.vdc_steps_up.setText(_translate("PyCCAPT", "100"))
                self.label_182.setText(_translate("PyCCAPT", "K_p Downwards"))
                self.vdc_steps_down.setText(_translate("PyCCAPT", "100"))
                self.label_191.setText(_translate("PyCCAPT", "Control Algorithm"))
                self.control_algorithm.setItemText(0, _translate("PyCCAPT", "Proportional"))
                self.control_algorithm.setItemText(1, _translate("PyCCAPT", "PID"))
                self.label_183.setText(_translate("PyCCAPT", "Cycle for Avg. (Hz)"))
                self.cycle_avg.setText(_translate("PyCCAPT", "10"))
                self.label_184.setText(_translate("PyCCAPT", "Pulse Min. Voltage (V)"))
                self.vp_min.setText(_translate("PyCCAPT", "328"))
                self.label_185.setText(_translate("PyCCAPT", "Pulse Max. Voltage (V)"))
                self.vp_max.setText(_translate("PyCCAPT", "3281"))
                self.label_186.setText(_translate("PyCCAPT", "Pulse Fraction (%)"))
                self.pulse_fraction.setText(_translate("PyCCAPT", "20"))
                self.label_187.setText(_translate("PyCCAPT", "Pulse Frequency (KHz)"))
                self.pulse_frequency.setText(_translate("PyCCAPT", "200"))
                self.label_188.setText(_translate("PyCCAPT", "Detection Rate (%)"))
                self.detection_rate_init.setText(_translate("PyCCAPT", "1"))
                self.label_189.setText(_translate("PyCCAPT", "# Hits Displayed"))
                self.reset_heatmap.setText(_translate("PyCCAPT", "Reset"))
                self.hit_displayed.setText(_translate("PyCCAPT", "20000"))
                self.label_190.setText(_translate("PyCCAPT", "Email"))
                self.label_192.setText(_translate("PyCCAPT", "Counter Source"))
                self.counter_source.setItemText(0, _translate("PyCCAPT", "TDC"))
                self.counter_source.setItemText(1, _translate("PyCCAPT", "DRS"))
                self.counter_source.setItemText(2, _translate("PyCCAPT", "Pulse Counter"))
                self.label_193.setText(_translate("PyCCAPT", "Run Statistics"))
                self.label_194.setText(_translate("PyCCAPT", "Elapsed Time (S):"))
                self.label_195.setText(_translate("PyCCAPT", "Total Ions"))
                self.label_196.setText(_translate("PyCCAPT", "Specimen Voltage (V)"))
                self.dc_hold.setText(_translate("PyCCAPT", "Hold"))
                self.label_197.setText(_translate("PyCCAPT", "Pulse Voltage (V)"))
                self.label_198.setText(_translate("PyCCAPT", "Detection Rate (%)"))
                self.textEdit.setHtml(_translate("PyCCAPT",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">{ex_user=user1;</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt;\">ex_name=test1;ex_time=90;max_ions=2000;ex_freq=10;vdc_min=500;vdc_max=4000;vdc_steps_up=100;vdc_steps_down=100;</span><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">control_algorithm=pid;</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt;\">vp_min=328;vp_max=3281;pulse_fraction=20;pulse_frequency=200;detection_rate_init=1;hit_displayed=20000;email=;counter_source=TDC</span><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">;criteria_time=True;criteria_ions=False;criteria_vdc=False}</span></p>\n"
                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">{ex_user=user2;ex_name=test2;ex_time=100;max_ions=3000;ex_freq=5;vdc_min=1000;vdc_max=3000;vdc_steps_up=50;vdc_steps_down=50;control_algorithm=proportional;vp_min=400;vp_max=2000;pulse_fraction=15;pulse_frequency=200;detection_rate_init=2;hit_displayed=40000;email=;counter_source=Pulse Counter;criteria_time=False;criteria_ions=False;criteria_vdc=True}</span></p></body></html>"))
                self.Error.setText(_translate("PyCCAPT", "<html><head/><body><p><br/></p></body></html>"))
                self.start_button.setText(_translate("PyCCAPT", "Start"))
                self.stop_button.setText(_translate("PyCCAPT", "Stop"))
                self.menuFile.setTitle(_translate("PyCCAPT", "File"))
                self.menuEdit.setTitle(_translate("PyCCAPT", "Edit"))
                self.menuHelp.setTitle(_translate("PyCCAPT", "Help"))
                self.menuSettings.setTitle(_translate("PyCCAPT", "Settings"))
                self.menuView.setTitle(_translate("PyCCAPT", "View"))
                self.actionExit.setText(_translate("PyCCAPT", "Exit"))
                self.actiontake_sceernshot.setText(_translate("PyCCAPT", "take sceernshot"))

        def open_cameras_win(self, ):
                if hasattr(self, 'Cameras_alignment') and self.Cameras_alignment.isVisible():
                        self.Cameras_alignment.raise_()
                        self.Cameras_alignment.activateWindow()
                else:
                        self.Cameras_alignment = QtWidgets.QWidget(flags=Qt.WindowType.Tool)
                        self.cameras = gui_cameras.Ui_Cameras_Alignment(self.variables, self.conf, self.camera)
                        self.cameras.setupUi(self.Cameras_alignment)
                        self.Cameras_alignment.show()

        def open_gates_win(self, ):
                if hasattr(self, 'Gates') and self.Gates.isVisible():
                        self.Gates.raise_()
                        self.Gates.activateWindow()
                else:
                        self.Gates = QtWidgets.QWidget(flags=Qt.WindowType.Tool)
                        self.gates = gui_gates.Ui_Gates(self.variables, self.conf)
                        self.gates.setupUi(self.Gates)
                        self.Gates.show()


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
        PyCCAPT = QtWidgets.QMainWindow()
        ui = Ui_PyCCAPT(variables, conf, camera)
        ui.setupUi(PyCCAPT)
        PyCCAPT.show()
        sys.exit(app.exec())
