import os
import re
import sys

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from pyccapt.control.apt import apt_exp_control
# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files
from pyccapt.control.gui import gui_baking
from pyccapt.control.gui import gui_cameras
from pyccapt.control.gui import gui_gates
from pyccapt.control.gui import gui_laser_control
from pyccapt.control.gui import gui_pumps_vacuum
from pyccapt.control.gui import gui_stage_control
from pyccapt.control.gui import gui_visualization


class Ui_PyCCAPT(object):

	def __init__(self, variables, conf, SignalEmitter, parent=None):
		self.conf = conf
		self.variables = variables
		self.emitter = SignalEmitter
		self.parent = parent

	def setupUi(self, PyCCAPT):
		PyCCAPT.setObjectName("PyCCAPT")
		PyCCAPT.resize(905, 844)
		self.centralwidget = QtWidgets.QWidget(parent=PyCCAPT)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout_5.setObjectName("gridLayout_5")
		self.gridLayout_4 = QtWidgets.QGridLayout()
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.gates_control = QtWidgets.QPushButton(parent=self.centralwidget)
		self.gates_control.setMinimumSize(QtCore.QSize(0, 40))
		self.gates_control.setStyleSheet("QPushButton{\n"
		                                 "                                                background: rgb(85, 170, 255)\n"
		                                 "                                                }                   ")
		self.gates_control.setObjectName("gates_control")
		self.horizontalLayout.addWidget(self.gates_control)
		self.pumps_vaccum = QtWidgets.QPushButton(parent=self.centralwidget)
		self.pumps_vaccum.setMinimumSize(QtCore.QSize(0, 40))
		self.pumps_vaccum.setStyleSheet("QPushButton{\n"
		                                "                                                background: rgb(85, 170, 255)\n"
		                                "                                                }\n"
		                                "                                            ")
		self.pumps_vaccum.setObjectName("pumps_vaccum")
		self.horizontalLayout.addWidget(self.pumps_vaccum)
		self.Camears = QtWidgets.QPushButton(parent=self.centralwidget)
		self.Camears.setMinimumSize(QtCore.QSize(0, 40))
		self.Camears.setStyleSheet("QPushButton{\n"
		                           "                                                background: rgb(85, 170, 255)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.Camears.setObjectName("Camears")
		self.horizontalLayout.addWidget(self.Camears)
		self.laser_control = QtWidgets.QPushButton(parent=self.centralwidget)
		self.laser_control.setMinimumSize(QtCore.QSize(0, 40))
		self.laser_control.setSizeIncrement(QtCore.QSize(0, 0))
		self.laser_control.setStyleSheet("QPushButton{\n"
		                                 "                                                background: rgb(85, 170, 255)\n"
		                                 "                                                }")
		self.laser_control.setObjectName("laser_control")
		self.horizontalLayout.addWidget(self.laser_control)
		self.stage_control = QtWidgets.QPushButton(parent=self.centralwidget)
		self.stage_control.setMinimumSize(QtCore.QSize(0, 40))
		self.stage_control.setSizeIncrement(QtCore.QSize(0, 0))
		self.stage_control.setStyleSheet("QPushButton{\n"
		                                 "                                                background: rgb(85, 170, 255)\n"
		                                 "                                                }")
		self.stage_control.setObjectName("stage_control")
		self.horizontalLayout.addWidget(self.stage_control)
		self.visualization = QtWidgets.QPushButton(parent=self.centralwidget)
		self.visualization.setMinimumSize(QtCore.QSize(0, 40))
		self.visualization.setSizeIncrement(QtCore.QSize(0, 0))
		self.visualization.setStyleSheet("QPushButton{\n"
		                                 "                                                background: rgb(85, 170, 255)\n"
		                                 "                                                }")
		self.visualization.setObjectName("Visualization")
		self.horizontalLayout.addWidget(self.visualization)
		self.baking = QtWidgets.QPushButton(parent=self.centralwidget)
		self.baking.setMinimumSize(QtCore.QSize(0, 40))
		self.baking.setSizeIncrement(QtCore.QSize(0, 0))
		self.baking.setStyleSheet("QPushButton{\n"
		                          "                                                background: rgb(85, 170, 255)\n"
		                          "                                                }")
		self.baking.setObjectName("baking")
		self.horizontalLayout.addWidget(self.baking)
		self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 2)
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		self.label_197 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_197.sizePolicy().hasHeightForWidth())
		self.label_197.setSizePolicy(sizePolicy)
		self.label_197.setObjectName("label_197")
		self.gridLayout.addWidget(self.label_197, 23, 0, 1, 1)
		self.detection_rate_init = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.detection_rate_init.sizePolicy().hasHeightForWidth())
		self.detection_rate_init.setSizePolicy(sizePolicy)
		self.detection_rate_init.setMinimumSize(QtCore.QSize(0, 20))
		self.detection_rate_init.setStyleSheet("QLineEdit{\n"
		                                       "                                                background: rgb(223,223,233)\n"
		                                       "                                                }\n"
		                                       "                                            ")
		self.detection_rate_init.setObjectName("detection_rate_init")
		self.gridLayout.addWidget(self.detection_rate_init, 15, 6, 1, 1)
		self.label_176 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_176.sizePolicy().hasHeightForWidth())
		self.label_176.setSizePolicy(sizePolicy)
		self.label_176.setObjectName("label_176")
		self.gridLayout.addWidget(self.label_176, 3, 0, 1, 2)
		self.label_188 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_188.sizePolicy().hasHeightForWidth())
		self.label_188.setSizePolicy(sizePolicy)
		self.label_188.setObjectName("label_188")
		self.gridLayout.addWidget(self.label_188, 15, 0, 1, 1)
		self.label_193 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_193.sizePolicy().hasHeightForWidth())
		self.label_193.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_193.setFont(font)
		self.label_193.setObjectName("label_193")
		self.gridLayout.addWidget(self.label_193, 19, 0, 1, 1)
		self.label_198 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_198.sizePolicy().hasHeightForWidth())
		self.label_198.setSizePolicy(sizePolicy)
		self.label_198.setObjectName("label_198")
		self.gridLayout.addWidget(self.label_198, 24, 0, 1, 1)
		self.ex_name = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ex_name.sizePolicy().hasHeightForWidth())
		self.ex_name.setSizePolicy(sizePolicy)
		self.ex_name.setMinimumSize(QtCore.QSize(0, 20))
		self.ex_name.setMaximumSize(QtCore.QSize(16777215, 100))
		self.ex_name.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.ex_name.setObjectName("ex_name")
		self.gridLayout.addWidget(self.ex_name, 2, 6, 1, 1)
		self.label_177 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_177.sizePolicy().hasHeightForWidth())
		self.label_177.setSizePolicy(sizePolicy)
		self.label_177.setObjectName("label_177")
		self.gridLayout.addWidget(self.label_177, 4, 0, 1, 1)
		self.label_192 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_192.sizePolicy().hasHeightForWidth())
		self.label_192.setSizePolicy(sizePolicy)
		self.label_192.setObjectName("label_192")
		self.gridLayout.addWidget(self.label_192, 18, 0, 1, 1)
		self.control_algorithm = QtWidgets.QComboBox(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.control_algorithm.sizePolicy().hasHeightForWidth())
		self.control_algorithm.setSizePolicy(sizePolicy)
		self.control_algorithm.setMinimumSize(QtCore.QSize(0, 20))
		self.control_algorithm.setStyleSheet("QComboBox{\n"
		                                     "                                                background: rgb(223,223,233)\n"
		                                     "                                                }\n"
		                                     "                                            ")
		self.control_algorithm.setObjectName("control_algorithm")
		self.control_algorithm.addItem("")
		self.control_algorithm.addItem("")
		self.gridLayout.addWidget(self.control_algorithm, 10, 6, 1, 1)
		self.hit_displayed = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.hit_displayed.sizePolicy().hasHeightForWidth())
		self.hit_displayed.setSizePolicy(sizePolicy)
		self.hit_displayed.setMinimumSize(QtCore.QSize(0, 20))
		self.hit_displayed.setStyleSheet("QLineEdit{\n"
		                                 "                                                background: rgb(223,223,233)\n"
		                                 "                                                }\n"
		                                 "                                            ")
		self.hit_displayed.setObjectName("hit_displayed")
		self.gridLayout.addWidget(self.hit_displayed, 16, 6, 1, 1)
		self.label_179 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_179.sizePolicy().hasHeightForWidth())
		self.label_179.setSizePolicy(sizePolicy)
		self.label_179.setObjectName("label_179")
		self.gridLayout.addWidget(self.label_179, 6, 0, 1, 3)
		self.label_195 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_195.sizePolicy().hasHeightForWidth())
		self.label_195.setSizePolicy(sizePolicy)
		self.label_195.setObjectName("label_195")
		self.gridLayout.addWidget(self.label_195, 21, 0, 1, 1)
		self.elapsed_time = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.elapsed_time.sizePolicy().hasHeightForWidth())
		self.elapsed_time.setSizePolicy(sizePolicy)
		self.elapsed_time.setMinimumSize(QtCore.QSize(0, 20))
		self.elapsed_time.setStyleSheet("QLineEdit{\n"
		                                "                                                background: rgb(223,223,233)\n"
		                                "                                                }\n"
		                                "                                            ")
		self.elapsed_time.setText("")
		self.elapsed_time.setObjectName("elapsed_time")
		self.gridLayout.addWidget(self.elapsed_time, 20, 5, 1, 2)
		self.ex_user = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ex_user.sizePolicy().hasHeightForWidth())
		self.ex_user.setSizePolicy(sizePolicy)
		self.ex_user.setMinimumSize(QtCore.QSize(0, 20))
		self.ex_user.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.ex_user.setObjectName("ex_user")
		self.gridLayout.addWidget(self.ex_user, 1, 6, 1, 1)
		self.label_174 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_174.sizePolicy().hasHeightForWidth())
		self.label_174.setSizePolicy(sizePolicy)
		self.label_174.setObjectName("label_174")
		self.gridLayout.addWidget(self.label_174, 1, 0, 1, 1)
		self.pulse_fraction = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pulse_fraction.sizePolicy().hasHeightForWidth())
		self.pulse_fraction.setSizePolicy(sizePolicy)
		self.pulse_fraction.setMinimumSize(QtCore.QSize(0, 20))
		self.pulse_fraction.setStyleSheet("QLineEdit{\n"
		                                  "                                                background: rgb(223,223,233)\n"
		                                  "                                                }\n"
		                                  "                                            ")
		self.pulse_fraction.setObjectName("pulse_fraction")
		self.gridLayout.addWidget(self.pulse_fraction, 13, 6, 1, 1)
		self.counter_source = QtWidgets.QComboBox(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.counter_source.sizePolicy().hasHeightForWidth())
		self.counter_source.setSizePolicy(sizePolicy)
		self.counter_source.setMinimumSize(QtCore.QSize(0, 20))
		self.counter_source.setStyleSheet("QComboBox{\n"
		                                  "                                                background: rgb(223,223,233)\n"
		                                  "                                                }\n"
		                                  "                                            ")
		self.counter_source.setObjectName("counter_source")
		self.counter_source.addItem("")
		self.counter_source.addItem("")
		self.gridLayout.addWidget(self.counter_source, 18, 6, 1, 1)
		self.label_182 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_182.sizePolicy().hasHeightForWidth())
		self.label_182.setSizePolicy(sizePolicy)
		self.label_182.setObjectName("label_182")
		self.gridLayout.addWidget(self.label_182, 9, 0, 1, 1)
		self.label_189 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_189.sizePolicy().hasHeightForWidth())
		self.label_189.setSizePolicy(sizePolicy)
		self.label_189.setObjectName("label_189")
		self.gridLayout.addWidget(self.label_189, 16, 0, 1, 1)
		self.label_184 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_184.sizePolicy().hasHeightForWidth())
		self.label_184.setSizePolicy(sizePolicy)
		self.label_184.setObjectName("label_184")
		self.gridLayout.addWidget(self.label_184, 11, 0, 1, 1)
		self.pulse_frequency = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pulse_frequency.sizePolicy().hasHeightForWidth())
		self.pulse_frequency.setSizePolicy(sizePolicy)
		self.pulse_frequency.setMinimumSize(QtCore.QSize(0, 20))
		self.pulse_frequency.setStyleSheet("QLineEdit{\n"
		                                   "                                                background: rgb(223,223,233)\n"
		                                   "                                                }\n"
		                                   "                                            ")
		self.pulse_frequency.setObjectName("pulse_frequency")
		self.gridLayout.addWidget(self.pulse_frequency, 14, 6, 1, 1)
		self.email = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.email.sizePolicy().hasHeightForWidth())
		self.email.setSizePolicy(sizePolicy)
		self.email.setMinimumSize(QtCore.QSize(0, 20))
		self.email.setStyleSheet("QLineEdit{\n"
		                         "                                                background: rgb(223,223,233)\n"
		                         "                                                }\n"
		                         "                                            ")
		self.email.setText("")
		self.email.setObjectName("email")
		self.gridLayout.addWidget(self.email, 17, 6, 1, 1)
		self.label_190 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_190.sizePolicy().hasHeightForWidth())
		self.label_190.setSizePolicy(sizePolicy)
		self.label_190.setObjectName("label_190")
		self.gridLayout.addWidget(self.label_190, 17, 0, 1, 1)
		self.hitmap_plot_size = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.hitmap_plot_size.sizePolicy().hasHeightForWidth())
		self.hitmap_plot_size.setSizePolicy(sizePolicy)
		self.hitmap_plot_size.setMinimumSize(QtCore.QSize(0, 20))
		self.hitmap_plot_size.setStyleSheet("QDoubleSpinBox{\n"
		                                    "                                                background: rgb(223,223,233)\n"
		                                    "                                                }\n"
		                                    "                                            ")
		self.hitmap_plot_size.setObjectName("hitmap_plot_size")
		self.gridLayout.addWidget(self.hitmap_plot_size, 16, 1, 1, 3)
		self.label_194 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_194.sizePolicy().hasHeightForWidth())
		self.label_194.setSizePolicy(sizePolicy)
		self.label_194.setObjectName("label_194")
		self.gridLayout.addWidget(self.label_194, 20, 0, 1, 1)
		self.dc_hold = QtWidgets.QPushButton(parent=self.centralwidget)
		self.dc_hold.setMinimumSize(QtCore.QSize(0, 20))
		self.dc_hold.setObjectName("dc_hold")
		self.gridLayout.addWidget(self.dc_hold, 22, 2, 1, 3)
		self.label_175 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_175.sizePolicy().hasHeightForWidth())
		self.label_175.setSizePolicy(sizePolicy)
		self.label_175.setObjectName("label_175")
		self.gridLayout.addWidget(self.label_175, 2, 0, 1, 1)
		self.label_178 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_178.sizePolicy().hasHeightForWidth())
		self.label_178.setSizePolicy(sizePolicy)
		self.label_178.setObjectName("label_178")
		self.gridLayout.addWidget(self.label_178, 5, 0, 1, 2)
		self.parameters_source = QtWidgets.QComboBox(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.parameters_source.sizePolicy().hasHeightForWidth())
		self.parameters_source.setSizePolicy(sizePolicy)
		self.parameters_source.setMinimumSize(QtCore.QSize(0, 20))
		self.parameters_source.setStyleSheet("QComboBox{\n"
		                                     "                                                background: rgb(223,223,233)\n"
		                                     "                                                }\n"
		                                     "                                            ")
		self.parameters_source.setObjectName("parameters_source")
		self.parameters_source.addItem("")
		self.parameters_source.addItem("")
		self.gridLayout.addWidget(self.parameters_source, 0, 6, 1, 1)
		self.criteria_vdc = QtWidgets.QCheckBox(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.criteria_vdc.sizePolicy().hasHeightForWidth())
		self.criteria_vdc.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setItalic(False)
		self.criteria_vdc.setFont(font)
		self.criteria_vdc.setMouseTracking(True)
		self.criteria_vdc.setStyleSheet("QCheckBox{\n"
		                                "                                                background: rgb(223,223,233)\n"
		                                "                                                }\n"
		                                "                                            ")
		self.criteria_vdc.setText("")
		self.criteria_vdc.setChecked(True)
		self.criteria_vdc.setObjectName("criteria_vdc")
		self.gridLayout.addWidget(self.criteria_vdc, 7, 3, 1, 1)
		self.label_180 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_180.sizePolicy().hasHeightForWidth())
		self.label_180.setSizePolicy(sizePolicy)
		self.label_180.setObjectName("label_180")
		self.gridLayout.addWidget(self.label_180, 7, 0, 1, 3)
		self.criteria_time = QtWidgets.QCheckBox(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.criteria_time.sizePolicy().hasHeightForWidth())
		self.criteria_time.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setItalic(False)
		self.criteria_time.setFont(font)
		self.criteria_time.setMouseTracking(True)
		self.criteria_time.setStyleSheet("QCheckBox{\n"
		                                 "                                                background: rgb(223,223,233)\n"
		                                 "                                                }\n"
		                                 "                                            ")
		self.criteria_time.setText("")
		self.criteria_time.setChecked(True)
		self.criteria_time.setObjectName("criteria_time")
		self.gridLayout.addWidget(self.criteria_time, 3, 3, 1, 1)
		self.label_186 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_186.sizePolicy().hasHeightForWidth())
		self.label_186.setSizePolicy(sizePolicy)
		self.label_186.setObjectName("label_186")
		self.gridLayout.addWidget(self.label_186, 13, 0, 1, 1)
		self.speciemen_voltage = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.speciemen_voltage.sizePolicy().hasHeightForWidth())
		self.speciemen_voltage.setSizePolicy(sizePolicy)
		self.speciemen_voltage.setMinimumSize(QtCore.QSize(0, 20))
		self.speciemen_voltage.setStyleSheet("QLineEdit{\n"
		                                     "                                                background: rgb(223,223,233)\n"
		                                     "                                                }\n"
		                                     "                                            ")
		self.speciemen_voltage.setText("")
		self.speciemen_voltage.setObjectName("speciemen_voltage")
		self.gridLayout.addWidget(self.speciemen_voltage, 22, 5, 1, 2)
		self.criteria_ions = QtWidgets.QCheckBox(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.criteria_ions.sizePolicy().hasHeightForWidth())
		self.criteria_ions.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setItalic(False)
		self.criteria_ions.setFont(font)
		self.criteria_ions.setMouseTracking(True)
		self.criteria_ions.setStyleSheet("QCheckBox{\n"
		                                 "                                                background: rgb(223,223,233)\n"
		                                 "                                                }\n"
		                                 "                                            ")
		self.criteria_ions.setText("")
		self.criteria_ions.setChecked(True)
		self.criteria_ions.setObjectName("criteria_ions")
		self.gridLayout.addWidget(self.criteria_ions, 4, 3, 1, 1)
		self.label_173 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_173.sizePolicy().hasHeightForWidth())
		self.label_173.setSizePolicy(sizePolicy)
		font = QtGui.QFont()
		font.setBold(True)
		self.label_173.setFont(font)
		self.label_173.setObjectName("label_173")
		self.gridLayout.addWidget(self.label_173, 0, 0, 1, 1)
		self.label_191 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_191.sizePolicy().hasHeightForWidth())
		self.label_191.setSizePolicy(sizePolicy)
		self.label_191.setObjectName("label_191")
		self.gridLayout.addWidget(self.label_191, 10, 0, 1, 1)
		self.vdc_steps_down = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vdc_steps_down.sizePolicy().hasHeightForWidth())
		self.vdc_steps_down.setSizePolicy(sizePolicy)
		self.vdc_steps_down.setMinimumSize(QtCore.QSize(0, 20))
		self.vdc_steps_down.setStyleSheet("QLineEdit{\n"
		                                  "                                                background: rgb(223,223,233)\n"
		                                  "                                                }\n"
		                                  "                                            ")
		self.vdc_steps_down.setObjectName("vdc_steps_down")
		self.gridLayout.addWidget(self.vdc_steps_down, 9, 6, 1, 1)
		self.vp_min = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vp_min.sizePolicy().hasHeightForWidth())
		self.vp_min.setSizePolicy(sizePolicy)
		self.vp_min.setMinimumSize(QtCore.QSize(0, 20))
		self.vp_min.setStyleSheet("QLineEdit{\n"
		                          "                                                background: rgb(223,223,233)\n"
		                          "                                                }\n"
		                          "                                            ")
		self.vp_min.setObjectName("vp_min")
		self.gridLayout.addWidget(self.vp_min, 11, 6, 1, 1)
		self.label_187 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_187.sizePolicy().hasHeightForWidth())
		self.label_187.setSizePolicy(sizePolicy)
		self.label_187.setObjectName("label_187")
		self.gridLayout.addWidget(self.label_187, 14, 0, 1, 1)
		self.max_ions = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.max_ions.sizePolicy().hasHeightForWidth())
		self.max_ions.setSizePolicy(sizePolicy)
		self.max_ions.setMinimumSize(QtCore.QSize(0, 20))
		self.max_ions.setStyleSheet("QLineEdit{\n"
		                            "                                                background: rgb(223,223,233)\n"
		                            "                                                }\n"
		                            "                                            ")
		self.max_ions.setObjectName("max_ions")
		self.gridLayout.addWidget(self.max_ions, 4, 6, 1, 1)
		self.label_185 = QtWidgets.QLabel(parent=self.centralwidget)
		self.label_185.setObjectName("label_185")
		self.gridLayout.addWidget(self.label_185, 12, 0, 1, 2)
		self.vp_max = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vp_max.sizePolicy().hasHeightForWidth())
		self.vp_max.setSizePolicy(sizePolicy)
		self.vp_max.setMinimumSize(QtCore.QSize(0, 20))
		self.vp_max.setStyleSheet("QLineEdit{\n"
		                          "                                                background: rgb(223,223,233)\n"
		                          "                                                }\n"
		                          "                                            ")
		self.vp_max.setObjectName("vp_max")
		self.gridLayout.addWidget(self.vp_max, 12, 6, 1, 1)
		self.pulse_voltage = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pulse_voltage.sizePolicy().hasHeightForWidth())
		self.pulse_voltage.setSizePolicy(sizePolicy)
		self.pulse_voltage.setMinimumSize(QtCore.QSize(0, 20))
		self.pulse_voltage.setStyleSheet("QLineEdit{\n"
		                                 "                                                background: rgb(223,223,233)\n"
		                                 "                                                }\n"
		                                 "                                            ")
		self.pulse_voltage.setText("")
		self.pulse_voltage.setObjectName("pulse_voltage")
		self.gridLayout.addWidget(self.pulse_voltage, 23, 5, 1, 2)
		self.detection_rate = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.detection_rate.sizePolicy().hasHeightForWidth())
		self.detection_rate.setSizePolicy(sizePolicy)
		self.detection_rate.setMinimumSize(QtCore.QSize(0, 20))
		self.detection_rate.setStyleSheet("QLineEdit{\n"
		                                  "                                                background: rgb(223,223,233)\n"
		                                  "                                                }\n"
		                                  "                                            ")
		self.detection_rate.setText("")
		self.detection_rate.setObjectName("detection_rate")
		self.gridLayout.addWidget(self.detection_rate, 24, 5, 1, 2)
		self.ex_freq = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ex_freq.sizePolicy().hasHeightForWidth())
		self.ex_freq.setSizePolicy(sizePolicy)
		self.ex_freq.setMinimumSize(QtCore.QSize(0, 20))
		self.ex_freq.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.ex_freq.setObjectName("ex_freq")
		self.gridLayout.addWidget(self.ex_freq, 5, 6, 1, 1)
		self.label_181 = QtWidgets.QLabel(parent=self.centralwidget)
		self.label_181.setObjectName("label_181")
		self.gridLayout.addWidget(self.label_181, 8, 0, 1, 1)
		self.reset_heatmap = QtWidgets.QPushButton(parent=self.centralwidget)
		self.reset_heatmap.setMinimumSize(QtCore.QSize(0, 20))
		self.reset_heatmap.setObjectName("reset_heatmap")
		self.gridLayout.addWidget(self.reset_heatmap, 16, 4, 1, 2)
		self.ex_time = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.ex_time.sizePolicy().hasHeightForWidth())
		self.ex_time.setSizePolicy(sizePolicy)
		self.ex_time.setMinimumSize(QtCore.QSize(0, 20))
		self.ex_time.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.ex_time.setObjectName("ex_time")
		self.gridLayout.addWidget(self.ex_time, 3, 6, 1, 1)
		self.vdc_max = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vdc_max.sizePolicy().hasHeightForWidth())
		self.vdc_max.setSizePolicy(sizePolicy)
		self.vdc_max.setMinimumSize(QtCore.QSize(0, 20))
		self.vdc_max.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.vdc_max.setObjectName("vdc_max")
		self.gridLayout.addWidget(self.vdc_max, 7, 6, 1, 1)
		self.vdc_min = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vdc_min.sizePolicy().hasHeightForWidth())
		self.vdc_min.setSizePolicy(sizePolicy)
		self.vdc_min.setMinimumSize(QtCore.QSize(0, 20))
		self.vdc_min.setStyleSheet("QLineEdit{\n"
		                           "                                                background: rgb(223,223,233)\n"
		                           "                                                }\n"
		                           "                                            ")
		self.vdc_min.setObjectName("vdc_min")
		self.gridLayout.addWidget(self.vdc_min, 6, 6, 1, 1)
		self.vdc_steps_up = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.vdc_steps_up.sizePolicy().hasHeightForWidth())
		self.vdc_steps_up.setSizePolicy(sizePolicy)
		self.vdc_steps_up.setMinimumSize(QtCore.QSize(0, 20))
		self.vdc_steps_up.setStyleSheet("QLineEdit{\n"
		                                "                                                background: rgb(223,223,233)\n"
		                                "                                                }\n"
		                                "                                            ")
		self.vdc_steps_up.setObjectName("vdc_steps_up")
		self.gridLayout.addWidget(self.vdc_steps_up, 8, 6, 1, 1)
		self.total_ions = QtWidgets.QLineEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.total_ions.sizePolicy().hasHeightForWidth())
		self.total_ions.setSizePolicy(sizePolicy)
		self.total_ions.setMinimumSize(QtCore.QSize(0, 20))
		self.total_ions.setStyleSheet("QLineEdit{\n"
		                              "                                                background: rgb(223,223,233)\n"
		                              "                                                }\n"
		                              "                                            ")
		self.total_ions.setText("")
		self.total_ions.setObjectName("total_ions")
		self.gridLayout.addWidget(self.total_ions, 21, 5, 1, 2)
		self.label_196 = QtWidgets.QLabel(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.label_196.sizePolicy().hasHeightForWidth())
		self.label_196.setSizePolicy(sizePolicy)
		self.label_196.setObjectName("label_196")
		self.gridLayout.addWidget(self.label_196, 22, 0, 1, 1)
		self.gridLayout_4.addLayout(self.gridLayout, 1, 0, 1, 1)
		self.text_line = QtWidgets.QTextEdit(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
		                                   QtWidgets.QSizePolicy.Policy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.text_line.sizePolicy().hasHeightForWidth())
		self.text_line.setSizePolicy(sizePolicy)
		self.text_line.setMinimumSize(QtCore.QSize(0, 100))
		self.text_line.setStyleSheet("QWidget{\n"
		                             "                                        border: 2px solid gray;\n"
		                             "                                        border-radius: 10px;\n"
		                             "                                        padding: 0 8px;\n"
		                             "                                        background: rgb(223,223,233)\n"
		                             "                                        }\n"
		                             "                                    ")
		self.text_line.setObjectName("text_line")
		self.gridLayout_4.addWidget(self.text_line, 1, 1, 1, 1)
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
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
		self.start_button.setSizePolicy(sizePolicy)
		self.start_button.setMinimumSize(QtCore.QSize(0, 25))
		self.start_button.setStyleSheet("QPushButton{\n"
		                                "                                                background: rgb(193, 193, 193)\n"
		                                "                                                }\n"
		                                "                                            ")
		self.start_button.setObjectName("start_button")
		self.gridLayout_3.addWidget(self.start_button, 0, 1, 1, 1)
		self.stop_button = QtWidgets.QPushButton(parent=self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
		self.stop_button.setSizePolicy(sizePolicy)
		self.stop_button.setMinimumSize(QtCore.QSize(0, 25))
		self.stop_button.setStyleSheet("QPushButton{\n"
		                               "                                                background: rgb(193, 193, 193)\n"
		                               "                                                }\n"
		                               "                                            ")
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
		self.actionAbout = QtGui.QAction(parent=PyCCAPT)
		self.actionAbout.setObjectName("actionAbout")
		self.menuFile.addAction(self.actionExit)
		self.menuEdit.addAction(self.actiontake_sceernshot)
		self.menuHelp.addAction(self.actionAbout)
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
		PyCCAPT.setTabOrder(self.control_algorithm, self.vp_min)
		PyCCAPT.setTabOrder(self.vp_min, self.vp_max)
		PyCCAPT.setTabOrder(self.vp_max, self.pulse_fraction)
		PyCCAPT.setTabOrder(self.pulse_fraction, self.pulse_frequency)
		PyCCAPT.setTabOrder(self.pulse_frequency, self.detection_rate_init)
		PyCCAPT.setTabOrder(self.detection_rate_init, self.hitmap_plot_size)
		PyCCAPT.setTabOrder(self.hitmap_plot_size, self.reset_heatmap)
		PyCCAPT.setTabOrder(self.reset_heatmap, self.hit_displayed)
		PyCCAPT.setTabOrder(self.hit_displayed, self.email)
		PyCCAPT.setTabOrder(self.email, self.counter_source)
		PyCCAPT.setTabOrder(self.counter_source, self.text_line)
		PyCCAPT.setTabOrder(self.text_line, self.start_button)
		PyCCAPT.setTabOrder(self.start_button, self.stop_button)
		PyCCAPT.setTabOrder(self.stop_button, self.gates_control)
		PyCCAPT.setTabOrder(self.gates_control, self.pumps_vaccum)
		PyCCAPT.setTabOrder(self.pumps_vaccum, self.Camears)
		PyCCAPT.setTabOrder(self.Camears, self.laser_control)
		PyCCAPT.setTabOrder(self.laser_control, self.visualization)
		PyCCAPT.setTabOrder(self.visualization, self.dc_hold)
		PyCCAPT.setTabOrder(self.dc_hold, self.elapsed_time)
		PyCCAPT.setTabOrder(self.elapsed_time, self.total_ions)
		PyCCAPT.setTabOrder(self.total_ions, self.speciemen_voltage)
		PyCCAPT.setTabOrder(self.speciemen_voltage, self.pulse_voltage)
		PyCCAPT.setTabOrder(self.pulse_voltage, self.detection_rate)

		###
		self.Camears.clicked.connect(self.open_cameras_win)
		self.gates_control.clicked.connect(self.open_gates_win)
		self.laser_control.clicked.connect(self.open_laser_control_win)
		self.stage_control.clicked.connect(self.open_stage_control_win)
		self.pumps_vaccum.clicked.connect(self.open_pumps_vacuum_win)
		self.visualization.clicked.connect(self.open_visualization_win)
		self.baking.clicked.connect(self.open_baking_win)
		# Create a QTimer to hide the warning message after 8 seconds
		self.timer = QtCore.QTimer(self.parent)
		self.timer.timeout.connect(self.hideMessage)

		###
		self.setup_parameters_changes()
		self.parameters_source.currentIndexChanged.connect(self.setup_parameters_changes)
		self.ex_user.editingFinished.connect(self.setup_parameters_changes)
		self.ex_name.editingFinished.connect(self.setup_parameters_changes)
		self.ex_time.editingFinished.connect(self.setup_parameters_changes)
		self.max_ions.editingFinished.connect(self.setup_parameters_changes)
		self.ex_freq.editingFinished.connect(self.setup_parameters_changes)
		self.vdc_min.editingFinished.connect(self.setup_parameters_changes)
		self.vdc_max.editingFinished.connect(self.setup_parameters_changes)
		self.vdc_steps_up.editingFinished.connect(self.setup_parameters_changes)
		self.vdc_steps_down.editingFinished.connect(self.setup_parameters_changes)
		self.vp_min.editingFinished.connect(self.setup_parameters_changes)
		self.vp_max.editingFinished.connect(self.setup_parameters_changes)
		self.pulse_fraction.editingFinished.connect(self.setup_parameters_changes)
		self.pulse_frequency.editingFinished.connect(self.setup_parameters_changes)
		self.detection_rate_init.editingFinished.connect(self.setup_parameters_changes)
		self.hit_displayed.editingFinished.connect(self.setup_parameters_changes)
		self.email.editingFinished.connect(self.setup_parameters_changes)
		self.counter_source.currentIndexChanged.connect(self.setup_parameters_changes)
		self.hitmap_plot_size.valueChanged.connect(self.setup_parameters_changes)
		self.control_algorithm.currentIndexChanged.connect(self.setup_parameters_changes)
		self.parameters_source.currentIndexChanged.connect(self.setup_parameters_changes)
		self.criteria_vdc.stateChanged.connect(self.setup_parameters_changes)
		self.criteria_time.stateChanged.connect(self.setup_parameters_changes)
		self.criteria_ions.stateChanged.connect(self.setup_parameters_changes)
		###
		self.start_button.clicked.connect(self.start_experiment_clicked)
		self.stop_button.clicked.connect(self.stop_experiment_clicked)
		self.reset_heatmap.clicked.connect(self.reset_heatmap_clicked)
		self.dc_hold.clicked.connect(self.dc_hold_clicked)

		self.hitmap_plot_size.setValue(1.0)
		self.hitmap_plot_size.setSingleStep(0.1)
		self.hitmap_plot_size.setDecimals(1)

		self.emitter.elapsed_time.connect(self.update_elapsed_time)
		self.emitter.total_ions.connect(self.update_total_ions)
		self.emitter.speciemen_voltage.connect(self.update_speciemen_voltage)
		self.emitter.pulse_voltage.connect(self.update_pulse_voltage)
		self.emitter.detection_rate.connect(self.update_detection_rate)

		self.result_list = []

	def retranslateUi(self, PyCCAPT):
		_translate = QtCore.QCoreApplication.translate
		###
		# PyCCAPT.setWindowTitle(_translate("PyCCAPT", "OXCART"))
		_translate = QtCore.QCoreApplication.translate
		PyCCAPT.setWindowTitle(_translate("PyCCAPT", "PyCCAPT APT Experiment Control"))
		PyCCAPT.setWindowIcon(QtGui.QIcon('./files/logo3.png'))
		###
		self.gates_control.setText(_translate("PyCCAPT", "Gates Control"))
		self.pumps_vaccum.setText(_translate("PyCCAPT", "Pumps & Vacuum"))
		self.Camears.setText(_translate("PyCCAPT", "Cameras & Alingment"))
		self.laser_control.setText(_translate("PyCCAPT", "Laser Control"))
		self.stage_control.setText(_translate("PyCCAPT", "Stage Control"))
		self.visualization.setText(_translate("PyCCAPT", "Visualization"))
		self.baking.setText(_translate("PyCCAPT", "Baking"))
		self.label_197.setText(_translate("PyCCAPT", "Pulse Voltage (V)"))
		self.detection_rate_init.setText(_translate("PyCCAPT", "1"))
		self.label_176.setText(_translate("PyCCAPT", "Max. Experiment Time (S)"))
		self.label_188.setText(_translate("PyCCAPT", "Detection Rate (%)"))
		self.label_193.setText(_translate("PyCCAPT", "Run Statistics"))
		self.label_198.setText(_translate("PyCCAPT", "Detection Rate (%)"))
		self.ex_name.setText(_translate("PyCCAPT", "test"))
		self.label_177.setText(_translate("PyCCAPT", "Max. Number of Ions"))
		self.label_192.setText(_translate("PyCCAPT", "Detection Mode"))
		self.control_algorithm.setItemText(0, _translate("PyCCAPT", "Proportional"))
		self.control_algorithm.setItemText(1, _translate("PyCCAPT", "PID"))
		self.hit_displayed.setText(_translate("PyCCAPT", "20000"))
		self.label_179.setText(_translate("PyCCAPT", "Specimen Start Voltage (V)"))
		self.label_195.setText(_translate("PyCCAPT", "Total Ions"))
		self.ex_user.setText(_translate("PyCCAPT", "user"))
		self.label_174.setText(_translate("PyCCAPT", "Experiment User"))
		self.pulse_fraction.setText(_translate("PyCCAPT", "20"))
		self.counter_source.setItemText(0, _translate("PyCCAPT", "TDC"))
		self.counter_source.setItemText(1, _translate("PyCCAPT", "Digitizer"))
		self.label_182.setText(_translate("PyCCAPT", "K_p Downwards"))
		self.label_189.setText(_translate("PyCCAPT", "# Hits Displayed"))
		self.label_184.setText(_translate("PyCCAPT", "Pulse Min. Voltage (V)"))
		self.pulse_frequency.setText(_translate("PyCCAPT", "200"))
		self.label_190.setText(_translate("PyCCAPT", "Email"))
		self.label_194.setText(_translate("PyCCAPT", "Elapsed Time (S):"))
		self.dc_hold.setText(_translate("PyCCAPT", "Hold"))
		self.label_175.setText(_translate("PyCCAPT", "Experiment Name"))
		self.label_178.setText(_translate("PyCCAPT", "Control refresh Freq.(Hz)"))
		self.parameters_source.setItemText(0, _translate("PyCCAPT", "TextBox"))
		self.parameters_source.setItemText(1, _translate("PyCCAPT", "TextLine"))
		self.label_180.setText(_translate("PyCCAPT", "Specimen Stop Voltage (V)"))
		self.label_186.setText(_translate("PyCCAPT", "Pulse Fraction (%)"))
		self.label_173.setText(_translate("PyCCAPT", "Setup Parameters"))
		self.label_191.setText(_translate("PyCCAPT", "Control Algorithm"))
		self.vdc_steps_down.setText(_translate("PyCCAPT", "100"))
		self.vp_min.setText(_translate("PyCCAPT", "328"))
		self.label_187.setText(_translate("PyCCAPT", "Pulse Frequency (KHz)"))
		self.max_ions.setText(_translate("PyCCAPT", "4000"))
		self.label_185.setText(_translate("PyCCAPT", "Pulse Max. Voltage (V)"))
		self.vp_max.setText(_translate("PyCCAPT", "3281"))
		self.ex_freq.setText(_translate("PyCCAPT", "10"))
		self.label_181.setText(_translate("PyCCAPT", "K_p Upwards"))
		self.reset_heatmap.setText(_translate("PyCCAPT", "Reset"))
		self.ex_time.setText(_translate("PyCCAPT", "900"))
		self.vdc_max.setText(_translate("PyCCAPT", "4000"))
		self.vdc_min.setText(_translate("PyCCAPT", "500"))
		self.vdc_steps_up.setText(_translate("PyCCAPT", "100"))
		self.label_196.setText(_translate("PyCCAPT", "Specimen Voltage (V)"))
		self.text_line.setHtml(_translate("PyCCAPT",
		                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
		                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
		                                  "p, li { white-space: pre-wrap; }\n"
		                                  "</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">{ex_user=user1;</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt;\">ex_name=test1;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt;\">ex_time=90;max_ions=2000;ex_freq=10;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt;\">vdc_min=500;vdc_max=4000;vdc_steps_up=100;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt;\">vdc_steps_down=100;</span><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">control_algorithm=PID;</span><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt;\">vp_min=328;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt;\">vp_max=3281;pulse_fraction=20;pulse_frequency=200;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt;\">detection_rate_init=1;hit_displayed=20000;email=;counter_source=TDC</span><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">criteria_time=True;criteria_ions=False;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">criteria_vdc=False}</span>                                        </p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">{ex_user=user2;ex_name=test2;ex_time=100;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">max_ions=3000;ex_freq=5;vdc_min=1000;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">vdc_max=3000;vdc_steps_up=50;vdc_steps_down=50;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">control_algorithm=proportional;vp_min=400;vp_max=2000;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">pulse_fraction=15;pulse_frequency=200;detection_rate_init=2;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">hit_displayed=40000;email=;counter_source=DRS;</span></p>\n"
		                                  "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono,monospace\'; font-size:8pt; color:#000000;\">criteria_time=False;criteria_ions=False;criteria_vdc=True}</span>                                    </p></body></html>"))
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
		self.actionAbout.setText(_translate("PyCCAPT", "About PyCCAPT"))

	def update_elapsed_time(self, value):
		self.elapsed_time.setText(str("{:.3f}".format(value)))

	def update_total_ions(self, value):
		self.total_ions.setText(str(value))

	def update_speciemen_voltage(self, value):
		self.speciemen_voltage.setText(str("{:.3f}".format(value)))

	def update_pulse_voltage(self, value):
		self.pulse_voltage.setText(str("{:.3f}".format(value)))

	def update_detection_rate(self, value):
		self.detection_rate.setText(str("{:.3f}".format(value)))

	def read_text_lines(self, ):
		def convert_value(value):
			# Try to convert to integer
			try:
				return int(value)
			except ValueError:
				# If not an integer, check if it's a boolean value
				if value.lower() == 'true':
					return True
				elif value.lower() == 'false':
					return False
				else:
					# If not a boolean, return the original value as string
					return value

		lines = self.text_line.toPlainText()
		pattern = r"{(.*?)}"
		matches = re.findall(pattern, lines, re.DOTALL)

		# Define the required keys for each dictionary
		required_keys = [
			'ex_user', 'ex_name', 'ex_time', 'max_ions', 'ex_freq', 'vdc_min', 'vdc_max',
			'vdc_steps_up', 'vdc_steps_down', 'control_algorithm', 'vp_min', 'vp_max',
			'pulse_fraction', 'pulse_frequency', 'detection_rate_init', 'hit_displayed',
			'email', 'counter_source', 'criteria_time', 'criteria_ions', 'criteria_vdc'
		]

		# Process each match and create a dictionary for each item
		for match in matches:
			item_dict = {}
			elements = match.split(";")
			for element in elements:
				key, value = element.split("=")
				item_dict[key.strip()] = convert_value(value.strip())

			# Check if all the required keys are present in the dictionary
			assert all(
				key in item_dict for key in required_keys), f"Missing keys in dictionary: {item_dict}"
			self.result_list.append(item_dict)
		self.variables.number_of_experiment_in_text_line = len(self.result_list)
		if self.variables.index_experiment_in_text_line < len(self.result_list):
			index_line = self.variables.index_experiment_in_text_line
			self.variables.ex_user = self.result_list[index_line]['ex_user']
			self.variables.ex_name = self.result_list[index_line]['ex_name']
			self.variables.ex_time = self.result_list[index_line]['ex_time']
			self.variables.max_ions = self.result_list[index_line]['max_ions']
			self.variables.ex_freq = self.result_list[index_line]['ex_freq']
			self.variables.vdc_min = self.result_list[index_line]['vdc_min']
			if self.result_list[index_line]['vdc_max'] < self.conf['max_vdc']:
				self.variables.vdc_max = self.result_list[index_line]['vdc_max']
			elif self.result_list[index_line]['vdc_max'] > self.conf['max_vdc']:
				self.error_message("Maximum possible Vdc is " + str(self.conf['max_vdc']))
			self.variables.vdc_steps_up = self.result_list[index_line]['vdc_steps_up']
			self.variables.vdc_steps_down = self.result_list[index_line]['vdc_steps_down']
			self.variables.control_algorithm = self.result_list[index_line]['control_algorithm']
			self.variables.vp_min = self.result_list[index_line]['vp_min']
			if self.result_list[index_line]['vp_max'] < self.conf['max_vp']:
				self.variables.vp_max = self.result_list[index_line]['vp_max']
			elif self.result_list[index_line]['vp_max'] > self.conf['max_vp']:
				self.error_message("Maximum possible V_p is " + str(self.conf['max_vp']))
			self.variables.pulse_fraction = self.result_list[index_line]['pulse_fraction']
			self.variables.pulse_frequency = self.result_list[index_line]['pulse_frequency']
			self.variables.detection_rate_init = self.result_list[index_line]['detection_rate_init']
			self.variables.hit_displayed = self.result_list[index_line]['hit_displayed']
			self.variables.email = self.result_list[index_line]['email']
			self.variables.counter_source = self.result_list[index_line]['counter_source']
			self.variables.criteria_time = self.result_list[index_line]['criteria_time']
			self.variables.criteria_ions = self.result_list[index_line]['criteria_ions']
			self.variables.criteria_vdc = self.result_list[index_line]['criteria_vdc']

	def setup_parameters_changes(self):
		with self.variables.lock_setup_parameters:
			if self.parameters_source.currentText() == 'TextLine':
				self.read_text_lines()
			else:
				self.variables.user_name = self.ex_user.text()
				self.variables.ex_name = self.ex_name.text()
				self.variables.ex_time = int(float(self.ex_time.text()))
				self.variables.ex_freq = int(float(self.ex_freq.text()))
				self.variables.max_ions = int(float(self.max_ions.text()))
				self.variables.vdc_min = int(float(self.vdc_min.text()))
				self.variables.detection_rate = float(self.detection_rate_init.text())
				self.variables.hit_display = int(float(self.hit_displayed.text()))
				self.variables.pulse_fraction = int(float(self.pulse_fraction.text())) / 100
				self.variables.pulse_frequency = float(self.pulse_frequency.text())
				self.variables.hdf5_path = self.ex_name.text()
				self.variables.email = self.email.text()
				self.variables.vdc_step_up = int(float(self.vdc_steps_up.text()))
				self.variables.vdc_step_down = int(float(self.vdc_steps_down.text()))
				self.variables.v_p_min = int(float(self.vp_min.text()))
				self.variables.v_p_max = int(float(self.vp_max.text()))
				self.variables.counter_source = str(self.counter_source.currentText())
				self.variables.hitmap_plot_size = self.hitmap_plot_size.value()

				if float(self.vp_max.text()) > self.conf['max_vp']:
					self.error_message.setText("Maximum possible number is " + str(self.conf['max_vp']))
					_translate = QtCore.QCoreApplication.translate
					self.vp_max.setText(_translate("PyCCAPT", self.conf['max_vp']))
				else:
					self.variables.v_p_max = int(float(self.vp_max.text()))

				if int(float(self.vdc_max.text())) > self.conf['max_vdc']:
					self.error_message("Maximum possible number is " + str(self.conf['max_vdc']))
					_translate = QtCore.QCoreApplication.translate
					self.vdc_max.setText(_translate("PyCCAPT", str(variables.vdc_max)))
				else:
					self.variables.vdc_max = int(float(self.vdc_max.text()))

				if self.criteria_time.isChecked():
					self.variables.criteria_time = True
				elif not self.criteria_time.isChecked():
					self.variables.criteria_time = False
				if self.criteria_ions.isChecked():
					self.variables.criteria_ions = True
				elif not self.criteria_ions.isChecked():
					self.variables.criteria_ions = False
				if self.criteria_vdc.isChecked():
					self.variables.criteria_vdc = True
				elif not self.criteria_vdc.isChecked():
					self.variables.criteria_vdc = False

	def start_experiment_clicked(self):
		with self.variables.lock_statistics:
			self.variables.start_flag = True  # Set the start flag
		self.start_button.setEnabled(False)  # Disable the star button
		self.counter_source.setEnabled(False)  # Disable the counter source
		self.start_experiment_worker()

	def stop_experiment_clicked(self):
		with self.variables.lock_statistics:
			if self.variables.start_flag:
				self.variables.stop_flag = True  # Set the STOP flag
				self.stop_button.setEnabled(False)  # Disable the stop button
				self.start_button.setEnabled(True)  # Disable the start button

	def start_experiment_worker(self):
		apt_exp_con = apt_exp_control.APT_Exp_Control(self.variables, self.conf, self.emitter)
		self.exp_worker = ExperimentWorker(apt_exp_con)
		self.exp_worker.finished.connect(self.on_stop_experiment_worker)
		self.emitter.elapsed_time.emit(0.0)
		self.emitter.total_ions.emit(0)
		self.emitter.speciemen_voltage.emit(0.0)
		self.emitter.pulse_voltage.emit(0.0)
		self.emitter.detection_rate.emit(0.0)
		self.exp_worker.start()

	def on_stop_experiment_worker(self):
		self.start_button.setEnabled(True)
		self.stop_button.setEnabled(True)

		# for getting screenshot of GUI
		screen = QtWidgets.QApplication.primaryScreen()
		w = self.centralwidget
		screenshot = screen.grabWindow(w.winId())
		with self.variables.lock_setup_parameters:
			screenshot.save(self.variables.path + '\last_screen_shot.png', 'png')

		with self.variables.lock_statistics:
			if self.variables.index_experiment_in_text_line < len(
					self.result_list):  # Do next experiment in case of TextLine
				self.variables.index_experiment_in_text_line += 1
				self.start_experiment_worker()
			else:
				variables.index_line = 0

	def reset_heatmap_clicked(self):
		with self.variables.lock_setup_parameters:
			if not self.variables.reset_heatmap:
				self.variables.reset_heatmap = True

	def dc_hold_clicked(self):
		with self.variables.lock_setup_parameters:
			if not self.variables.vdc_hold:
				self.variables.vdc_hold = True
				self.dc_hold.setStyleSheet("QPushButton{\n"
				                           "background: rgb(0, 255, 26)\n"
				                           "}")
			elif self.variables.vdc_hold:
				self.variables.vdc_hold = False
				self.dc_hold.setStyleSheet("QPushButton{\n"
				                           "background: rgb(193, 193, 193)\n"
				                           "}")

	def open_cameras_win(self):
		if hasattr(self, 'Cameras_alignment') and self.Cameras_alignment.isVisible():
			self.Cameras_alignment.raise_()
			self.Cameras_alignment.activateWindow()
		else:
			self.SignalEmitter_Cameras = gui_cameras.SignalEmitter()
			self.gui_cameras_alignment = gui_cameras.Ui_Cameras_Alignment(self.variables, self.conf,
			                                                              self.SignalEmitter_Cameras)
			self.Cameras_alignment = gui_cameras.CamerasAlignmentWindow(self.gui_cameras_alignment,
			                                                            flags=QtCore.Qt.WindowType.Tool)
			self.gui_cameras_alignment.setupUi(self.Cameras_alignment)
			self.Cameras_alignment.show()

	def open_gates_win(self):
		if hasattr(self, 'Gates') and self.Gates.isVisible():
			self.Gates.raise_()
			self.Gates.activateWindow()
		else:
			self.gui_gates = gui_gates.Ui_Gates(self.variables, self.conf)
			self.Gates = gui_gates.GatesWindow(self.gui_gates, flags=QtCore.Qt.WindowType.Tool)
			self.gui_gates.setupUi(self.Gates)
			self.Gates.show()

	def open_pumps_vacuum_win(self, ):
		if hasattr(self, 'Pumps_Vacuum') and self.Pumps_vacuum.isVisible():
			self.Pumps_vacuum.raise_()
			self.Pumps_vacuum.activateWindow()
		else:
			self.SignalEmitter_Pumps_Vacuum = gui_pumps_vacuum.SignalEmitter()
			self.gui_pumps_vacuum = gui_pumps_vacuum.Ui_Pumps_Vacuum(self.variables, self.conf,
			                                                         self.SignalEmitter_Pumps_Vacuum)
			self.Pumps_vacuum = gui_pumps_vacuum.PumpsVacuumWindow(self.gui_pumps_vacuum,
			                                                       self.SignalEmitter_Pumps_Vacuum,
			                                                       flags=Qt.WindowType.Tool)
			self.gui_pumps_vacuum.setupUi(self.Pumps_vacuum)
			self.Pumps_vacuum.show()

	def open_laser_control_win(self):
		if hasattr(self, 'Laser_Control') and self.Laser_control.isVisible():
			self.Laser_control.raise_()
			self.Laser_control.activateWindow()
		else:
			self.gui_laser_control = gui_laser_control.Ui_Laser_Control(self.variables, self.conf)
			self.Laser_control = gui_laser_control.LaserControlWindow(self.gui_laser_control,
			                                                          flags=Qt.WindowType.Tool)
			self.gui_laser_control.setupUi(self.Laser_control)
			self.Laser_control.show()

	def open_stage_control_win(self):
		if hasattr(self, 'Stage_Control') and self.Stage_control.isVisible():
			self.Stage_control.raise_()
			self.Stage_control.activateWindow()
		else:
			self.gui_stage_control = gui_stage_control.Ui_Stage_Control(self.variables, self.conf)
			self.Stage_control = gui_stage_control.StageControlWindow(self.gui_stage_control,
			                                                          flags=Qt.WindowType.Tool)
			self.gui_stage_control.setupUi(self.Stage_control)
			self.Stage_control.show()

	def open_visualization_win(self, ):
		if hasattr(self, 'Visualization') and self.Visualization.isVisible():
			self.Visualization.raise_()
			self.Visualization.activateWindow()
		else:
			self.gui_visualization = gui_visualization.Ui_Visualization(self.variables, self.conf)
			self.Visualization = gui_visualization.VisualizationWindow(self.gui_visualization,
			                                                           flags=Qt.WindowType.Tool)
			self.gui_visualization.setupUi(self.Visualization)
			self.Visualization.show()

	def open_baking_win(self):

		if not (
				(hasattr(self, 'Cameras_alignment') and self.Cameras_alignment.isVisible()) or
				(hasattr(self, 'Gates') and self.Gates.isVisible()) or
				(hasattr(self, 'Pumps_Vacuum') and self.Pumps_vacuum.isVisible()) or
				(hasattr(self, 'Laser_Control') and self.Laser_control.isVisible()) or
				(hasattr(self, 'Stage_Control') and self.Stage_control.isVisible()) or
				(hasattr(self, 'Visualization') and self.Visualization.isVisible())
		):
			if hasattr(self, 'Baking') and self.Baking.isVisible():
				self.Baking.raise_()
				self.Baking.activateWindow()
			else:
				self.gui_baking = gui_baking.Ui_Baking(self.variables, self.conf)
				self.Baking = gui_baking.BakingWindow(self.gui_baking, flags=Qt.WindowType.Tool)
				self.gui_baking.setupUi(self.Baking)
				self.Baking.show()

		else:
			self.error_message("Close all other windows before opening the baking window")

	def error_message(self, message):
		_translate = QtCore.QCoreApplication.translate
		self.Error.setText(_translate("OXCART",
		                              "<html><head/><body><p><span style=\" color:#ff0000;\">"
		                              + message + "</span></p></body></html>"))

		self.timer.start(8000)

	def hideMessage(self):
		# Hide the message and stop the timer
		_translate = QtCore.QCoreApplication.translate
		self.Error.setText(_translate("OXCART",
		                              "<html><head/><body><p><span style=\" "
		                              "color:#ff0000;\"></span></p></body></html>"))

		self.timer.stop()


class SignalEmitter(QtCore.QObject):
	elapsed_time = QtCore.pyqtSignal(float)
	total_ions = QtCore.pyqtSignal(int)
	speciemen_voltage = QtCore.pyqtSignal(float)
	pulse_voltage = QtCore.pyqtSignal(float)
	detection_rate = QtCore.pyqtSignal(float)


class ExperimentWorker(QtCore.QThread):
	"""
	A class for creating main_thread
	The run method create thread of main function in the voltage atom prob script
	"""
	finished = QtCore.pyqtSignal()

	def __init__(self, apt_experiment_control):
		QtCore.QThread.__init__(self, )
		self.apt_experiment_control = apt_experiment_control

	def run(self):
		self.apt_experiment_control.run_experiment()
		self.finished.emit()


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

	app = QtWidgets.QApplication(sys.argv)
	PyCCAPT = QtWidgets.QMainWindow()
	signal_emitter = SignalEmitter()
	ui = Ui_PyCCAPT(variables, conf, signal_emitter)
	ui.setupUi(PyCCAPT)
	PyCCAPT.show()
	sys.exit(app.exec())
