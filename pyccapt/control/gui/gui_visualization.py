import multiprocessing
import os
import sys
import time

import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
# from numba import njit
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer

# Local module and scripts
from pyccapt.control.control import share_variables, read_files, tof2mc_simple
from pyccapt.control.devices import initialize_devices


class Ui_Visualization(object):

    def __init__(self, variables, conf, x_plot, y_plot, t_plot, main_v_dc_plot):

        """
        Constructor for the Visualization UI class.

        Args:
            variables (object): Global experiment variables.
            conf (dict): Configuration settings.
            x_plot (multiprocessing.Array): Array for storing the x-axis values of the mass spectrum.
            y_plot (multiprocessing.Array): Array for storing the y-axis values of the mass spectrum.
            t_plot (multiprocessing.Array): Array for storing the time values of the mass spectrum.
            main_v_dc_plot (multiprocessing.Array): Array for storing the main voltage values of the mass spectrum.

        """
        self.styles = None
        self.num_event_mc_tof = None
        self.mc_tof_last_events_flag = False
        self.change_detection_rate_range = False
        self.start_time_metadata = 0
        self.start_main_exp = 0
        self.index_plot_start = 0
        self.variables = variables
        self.conf = conf
        self.x_plot = x_plot
        self.y_plot = y_plot
        self.t_plot = t_plot
        self.main_v_dc_plot = main_v_dc_plot
        self.counter_source = ''
        self.index_plot_save = 0
        self.index_plot = 0
        self.index_wait_on_plot_start = 0
        self.index_auto_scale_graph = 0

        self.xx = []
        self.yy = []
        self.tt = []
        self.main_v_dc_dld = []

        self.update_timer = QTimer()  # Create a QTimer for updating graphs
        self.update_timer.timeout.connect(self.update_graphs)  # Connect it to the update_graphs slot
        self.index_plot_heatmap = 0  # Index for the heatmap plot
        self.visualization_window = None  # In♠itialize the attribute

    def setupUi(self, Visualization):
        """
        Setup the UI for the Visualization window.

        Args:
            Visualization (QMainWindow): Visualization window.

        Return:
            None
        """
        Visualization.setObjectName("Visualization")
        Visualization.resize(808, 558)
        self.gridLayout_3 = QtWidgets.QGridLayout(Visualization)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_200 = QtWidgets.QLabel(parent=Visualization)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_200.setFont(font)
        self.label_200.setObjectName("label_200")
        self.verticalLayout_3.addWidget(self.label_200)
        ####
        # self.vdc_time = QtWidgets.QGraphicsView(parent=Visualization)
        self.vdc_time = pg.PlotWidget(parent=Visualization)
        self.vdc_time.setBackground('w')
        ####
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.vdc_time.sizePolicy().hasHeightForWidth())
        self.vdc_time.setSizePolicy(sizePolicy)
        self.vdc_time.setMinimumSize(QtCore.QSize(250, 250))
        self.vdc_time.setStyleSheet("QWidget{\n"
                                    "                                                    border: 0.5px solid gray;\n"
                                    "                                                    }\n"
                                    "                                                ")
        self.vdc_time.setObjectName("vdc_time")
        self.verticalLayout_3.addWidget(self.vdc_time)
        self.label_207 = QtWidgets.QLabel(parent=Visualization)
        self.label_207.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_207.setFont(font)
        self.label_207.setObjectName("label_207")
        self.verticalLayout_3.addWidget(self.label_207)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_201 = QtWidgets.QLabel(parent=Visualization)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_201.setFont(font)
        self.label_201.setObjectName("label_201")
        self.verticalLayout_2.addWidget(self.label_201)
        ####
        # self.detection_rate_viz = QtWidgets.QGraphicsView(parent=Visualization)
        self.detection_rate_viz = pg.PlotWidget(parent=Visualization)
        self.detection_rate_viz.setBackground('w')
        ####
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.detection_rate_viz.sizePolicy().hasHeightForWidth())
        self.detection_rate_viz.setSizePolicy(sizePolicy)
        self.detection_rate_viz.setMinimumSize(QtCore.QSize(250, 250))
        self.detection_rate_viz.setStyleSheet("QWidget{\n"
                                              "                                            border: 0.5px solid gray;\n"
                                              "                                            }\n"
                                              "                                        ")
        self.detection_rate_viz.setObjectName("detection_rate_viz")
        self.verticalLayout_2.addWidget(self.detection_rate_viz)
        self.detection_rate_range_switch = QtWidgets.QPushButton(parent=Visualization)
        self.detection_rate_range_switch.setMinimumSize(QtCore.QSize(0, 20))
        self.detection_rate_range_switch.setMaximumSize(QtCore.QSize(100, 16777215))
        self.detection_rate_range_switch.setObjectName("detection_rate_range_switch")
        self.verticalLayout_2.addWidget(self.detection_rate_range_switch)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_206 = QtWidgets.QLabel(parent=Visualization)
        font = QtGui.QFont()
        font.setBold(True)
        self.label_206.setFont(font)
        self.label_206.setObjectName("label_206")
        self.verticalLayout.addWidget(self.label_206)
        ###
        # self.detector_heatmap = QtWidgets.QGraphicsView(parent=Visualization)
        self.detector_heatmap = pg.PlotWidget(parent=Visualization)
        self.detector_heatmap.setBackground('w')
        ###
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.detector_heatmap.sizePolicy().hasHeightForWidth())
        self.detector_heatmap.setSizePolicy(sizePolicy)
        self.detector_heatmap.setMinimumSize(QtCore.QSize(250, 250))
        self.detector_heatmap.setStyleSheet("QWidget{\n"
                                            "                                            border: 0.5px solid gray;\n"
                                            "                                            }\n"
                                            "                                        ")
        self.detector_heatmap.setObjectName("detector_heatmap")
        self.verticalLayout.addWidget(self.detector_heatmap)
        self.reset_heatmap_v = QtWidgets.QPushButton(parent=Visualization)
        self.reset_heatmap_v.setMinimumSize(QtCore.QSize(0, 20))
        self.reset_heatmap_v.setMaximumSize(QtCore.QSize(60, 16777215))
        self.reset_heatmap_v.setObjectName("reset_heatmap_v")
        self.verticalLayout.addWidget(self.reset_heatmap_v)
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)
        ####
        # self.histogram = QtWidgets.QGraphicsView(parent=Visualization)
        self.histogram = pg.PlotWidget(parent=Visualization)
        self.histogram.setBackground('w')
        ####
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.histogram.sizePolicy().hasHeightForWidth())
        self.histogram.setSizePolicy(sizePolicy)
        self.histogram.setMinimumSize(QtCore.QSize(750, 150))
        self.histogram.setStyleSheet("QWidget{\n"
                                     "                                            border: 0.5px solid gray;\n"
                                     "                                            }\n"
                                     "                                        ")
        self.histogram.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.histogram.setObjectName("histogram")
        self.gridLayout.addWidget(self.histogram, 1, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spectrum_switch = QtWidgets.QPushButton(parent=Visualization)
        self.spectrum_switch.setMinimumSize(QtCore.QSize(0, 20))
        self.spectrum_switch.setMaximumSize(QtCore.QSize(60, 16777215))
        self.spectrum_switch.setObjectName("spectrum_switch")
        self.horizontalLayout.addWidget(self.spectrum_switch)
        self.spectrum_last_events_switch = QtWidgets.QPushButton(parent=Visualization)
        self.spectrum_last_events_switch.setMinimumSize(QtCore.QSize(0, 20))
        self.spectrum_last_events_switch.setMaximumSize(QtCore.QSize(100, 16777215))
        self.spectrum_last_events_switch.setObjectName("spectrum_last_events_switch")
        self.horizontalLayout.addWidget(self.spectrum_last_events_switch)
        self.num_last_events = QtWidgets.QLineEdit(parent=Visualization)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.num_last_events.sizePolicy().hasHeightForWidth())
        self.num_last_events.setSizePolicy(sizePolicy)
        self.num_last_events.setMinimumSize(QtCore.QSize(100, 20))
        self.num_last_events.setStyleSheet("QLineEdit{\n"
                                           "                                            background: rgb(223,223,233)\n"
                                           "                                            }\n"
                                           "                                        ")
        self.num_last_events.setObjectName("num_last_events")
        self.horizontalLayout.addWidget(self.num_last_events)
        self.label_208 = QtWidgets.QLabel(parent=Visualization)
        self.label_208.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_208.setFont(font)
        self.label_208.setObjectName("label_208")
        self.horizontalLayout.addWidget(self.label_208)
        self.max_mc = QtWidgets.QLineEdit(parent=Visualization)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_mc.sizePolicy().hasHeightForWidth())
        self.max_mc.setSizePolicy(sizePolicy)
        self.max_mc.setMinimumSize(QtCore.QSize(100, 20))
        self.max_mc.setStyleSheet("QLineEdit{\n"
                                  "                                            background: rgb(223,223,233)\n"
                                  "                                            }\n"
                                  "                                        ")
        self.max_mc.setObjectName("max_mc")
        self.horizontalLayout.addWidget(self.max_mc)
        self.label_209 = QtWidgets.QLabel(parent=Visualization)
        self.label_209.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_209.setFont(font)
        self.label_209.setObjectName("label_209")
        self.horizontalLayout.addWidget(self.label_209)
        self.max_tof = QtWidgets.QLineEdit(parent=Visualization)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_tof.sizePolicy().hasHeightForWidth())
        self.max_tof.setSizePolicy(sizePolicy)
        self.max_tof.setMinimumSize(QtCore.QSize(100, 20))
        self.max_tof.setStyleSheet("QLineEdit{\n"
                                   "                                            background: rgb(223,223,233)\n"
                                   "                                            }\n"
                                   "                                        ")
        self.max_tof.setObjectName("max_tof")
        self.horizontalLayout.addWidget(self.max_tof)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Visualization)
        QtCore.QMetaObject.connectSlotsByName(Visualization)
        Visualization.setTabOrder(self.detection_rate_range_switch, self.reset_heatmap_v)
        Visualization.setTabOrder(self.reset_heatmap_v, self.spectrum_switch)
        Visualization.setTabOrder(self.spectrum_switch, self.spectrum_last_events_switch)
        Visualization.setTabOrder(self.spectrum_last_events_switch, self.num_last_events)
        Visualization.setTabOrder(self.num_last_events, self.max_mc)
        Visualization.setTabOrder(self.max_mc, self.max_tof)
        Visualization.setTabOrder(self.max_tof, self.vdc_time)
        Visualization.setTabOrder(self.vdc_time, self.detection_rate_viz)
        Visualization.setTabOrder(self.detection_rate_viz, self.detector_heatmap)
        Visualization.setTabOrder(self.detector_heatmap, self.histogram)

        ###
        # Start the update timer with a 500 ms interval (2 times per second)
        self.update_timer.start(500)

        # High Voltage visualization ################
        self.x_vdc = [i * 0.5 for i in range(200)]  # 100 time points
        self.y_vdc = [0.0] * 200  # 200 data points, all initialized to 0.0
        self.y_vdc[:] = [np.nan] * len(self.y_vdc)
        pen_vdc = pg.mkPen(color=(255, 0, 0), width=6)
        self.data_line_vdc = self.vdc_time.plot(self.x_vdc, self.y_vdc, pen=pen_vdc)
        self.vdc_time.plotItem.setMouseEnabled(x=False)  # Only allow zoom in Y-axis
        # Add Axis Labels
        self.styles = {"color": "#f00", "font-size": "12px"}
        self.vdc_time.setLabel("left", "High Voltage", units='V', **self.styles)
        self.vdc_time.setLabel("bottom", "Time (s)", **self.styles)
        # Add grid
        self.vdc_time.showGrid(x=True, y=True)
        # Add Range
        self.vdc_time.setXRange(0, 100)
        self.vdc_time.setYRange(0, 15000)

        # Detection Visualization #########################
        self.x_dtec = [i * 0.5 for i in range(200)]  # 100 time points
        self.y_dtec = [0.0] * 200  # 200 data points, all initialized to 0.0
        self.y_dtec[:] = [np.nan] * len(self.y_vdc)
        pen_dtec = pg.mkPen(color=(255, 0, 0), width=6)
        self.data_line_dtec = self.detection_rate_viz.plot(self.x_dtec, self.y_dtec, pen=pen_dtec)

        # Add Axis Labels
        self.detection_rate_viz.setLabel("left", "Detection rate (%)", **self.styles)
        self.detection_rate_viz.setLabel("bottom", "Time (s)", **self.styles)

        # Add grid
        self.detection_rate_viz.showGrid(x=True, y=True)
        self.detection_rate_viz.plotItem.setMouseEnabled(x=False)  # Only allow zoom in Y-axis
        # Add Range
        self.detection_rate_viz.setXRange(0, 100)
        self.detection_rate_viz.setYRange(0, 100)

        # detector heatmep #####################
        self.scatter = pg.ScatterPlotItem(
            size=self.variables.hitmap_plot_size, brush='black')
        self.detector_circle = QtWidgets.QGraphicsEllipseItem(-40, -40, 80, 80)  # x, y, width, height
        self.detector_circle.setPen(pg.mkPen(color=(255, 0, 0), width=2))
        self.detector_heatmap.addItem(self.detector_circle)
        self.detector_heatmap.setLabel("left", "X_det", units='mm', **self.styles)
        self.detector_heatmap.setLabel("bottom", "Y_det", units='mm', **self.styles)

        # Histogram #########################
        # Add Axis Labels
        self.histogram.plotItem.setMouseEnabled(y=False)  # Only allow zoom in X-axis
        self.histogram.setLabel("left", "Event Counts", **self.styles)
        self.histogram.setLogMode(y=True)
        if self.conf["visualization"] == "tof":
	        self.histogram.setLabel("bottom", "Time", units='ns', **self.styles)
        elif self.conf["visualization"] == "mc":
	        self.histogram.setLabel("bottom", "m/c", units='Da', **self.styles)

        self.visualization_window = Visualization  # Assign the attribute when setting up the UI

        self.reset_heatmap_v.clicked.connect(self.reset_heatmap)
        self.histogram.addLegend(offset=(-10, 10))

        self.original_button_style = self.detection_rate_range_switch.styleSheet()
        self.detection_rate_range_switch.clicked.connect(self.detection_rate_range)
        self.spectrum_switch.clicked.connect(self.spectrum_switch_mc_tof)
        self.spectrum_last_events_switch.clicked.connect(self.spectrum_last_events)
        self.num_last_events.editingFinished.connect(self.parameters_changes)
        self.max_mc.editingFinished.connect(self.parameters_changes)
        self.max_tof.editingFinished.connect(self.parameters_changes)

    def retranslateUi(self, Visualization):
        """
                        Set the text of the widgets
                        Args:
                           Visualization: The main window

                        Return:
                           None
                        """
        _translate = QtCore.QCoreApplication.translate
        ###
        # Visualization.setWindowTitle(_translate("Visualization", "Form"))
        Visualization.setWindowTitle(_translate("Visualization", "PyCCAPT Visualization"))
        Visualization.setWindowIcon(QtGui.QIcon('./files/logo.png'))
        ###
        self.label_200.setText(_translate("Visualization", "Voltage"))
        self.label_207.setText(_translate("Visualization", "Spectrum"))
        self.label_201.setText(_translate("Visualization", "Detection Rate"))
        self.detection_rate_range_switch.setText(_translate("Visualization", "Short range"))
        self.label_206.setText(_translate("Visualization", "Detector Heatmap"))
        self.reset_heatmap_v.setText(_translate("Visualization", "Reset"))
        self.spectrum_switch.setText(_translate("Visualization", "mc/tof"))
        self.spectrum_last_events_switch.setText(_translate("Visualization", "Last events"))
        self.num_last_events.setText(_translate("Visualization", "10000"))
        self.label_208.setText(_translate("Visualization", "Max mc (Da)"))
        self.max_mc.setText(_translate("Visualization", "200"))
        self.label_209.setText(_translate("Visualization", "Max tof (ns)"))
        self.max_tof.setText(_translate("Visualization", "5000"))


    def reset_heatmap(self):
        """
        Reset the heatmap
        Args:
            None

        Return:
            None
        """
        # with self.variables.lock_setup_parameters:
        if not self.variables.reset_heatmap:
            self.variables.reset_heatmap = True

    def detection_rate_range(self):
        """
        Change the time range of the detection rate

        Args:
            None

        Return:
            None
        """
        self.change_detection_rate_range = not self.change_detection_rate_range

        if self.change_detection_rate_range:
            self.detection_rate_range_switch.setStyleSheet("QPushButton{\n"
                                                           "background: rgb(0, 255, 26)\n"
                                                           "}")
        else:
            self.detection_rate_range_switch.setStyleSheet(self.original_button_style)

    def update_graphs(self, ):
        """
        Update the graphs
        Args:
            None

        Return:
            None
        """
        if self.index_auto_scale_graph == 30:
            self.vdc_time.enableAutoRange(axis='x')
            self.histogram.enableAutoRange(axis='y')
            self.detection_rate_viz.enableAutoRange(axis='x')
            self.detection_rate_viz.enableAutoRange(axis='y')
            self.detector_heatmap.enableAutoRange(axis='x')
            self.detector_heatmap.enableAutoRange(axis='y')
            self.index_auto_scale_graph = 0

        self.index_auto_scale_graph += 1

        if self.variables.plot_clear_flag:
            self.x_vdc = [i * 0.5 for i in range(200)]  # 100 time points
            self.y_vdc = [0.0] * 200  # 200 data points, all initialized to 0.0
            self.y_vdc[:] = [np.nan] * len(self.y_vdc)

            self.vdc_time.clear()
            pen_vdc = pg.mkPen(color=(255, 0, 0), width=6)
            self.data_line_vdc = self.vdc_time.plot(self.x_vdc, self.y_vdc, pen=pen_vdc)

            self.x_dtec = [i * 0.5 for i in range(200)]  # 100 time points
            self.y_dtec = [0.0] * 200  # 200 data points, all initialized to 0.0
            self.y_dtec[:] = [np.nan] * len(self.y_vdc)

            self.detection_rate_viz.clear()
            pen_dtec = pg.mkPen(color=(255, 0, 0), width=6)
            self.data_line_dtec = self.detection_rate_viz.plot(self.x_dtec, self.y_dtec, pen=pen_dtec)

            self.histogram.clear()

            self.detector_heatmap.clear()
            self.detector_heatmap.addItem(self.detector_circle)
            self.variables.plot_clear_flag = False
            self.index_plot = 0
            self.index_plot_start = 0
            self.index_plot_save = 0
            self.index_plot_heatmap = 0
            self.start_time_metadata = 0
            self.variables.detection_rate_current_plot = 0

            self.xx = []
            self.yy = []
            self.tt = []
            self.main_v_dc_dld = []

        # with self.variables.lock_statistics and self.variables.lock_setup_parameters:
        if self.variables.start_flag and self.variables.flag_visualization_start:
            if self.index_plot_start == 0:
                self.start_main_exp = time.time()
                self.start_time = time.time()
                self.start_time_metadata = time.time()
                self.index_plot_start += 1
            self.variables.elapsed_time = time.time() - self.start_time
            # with self.variables.lock_statistics:
            if self.index_wait_on_plot_start <= 16:
                if self.index_wait_on_plot_start == 0:
                    self.counter_source = self.variables.counter_source
                self.index_wait_on_plot_start += 1

            # V_dc and V_p
            if self.index_plot < len(self.y_vdc):
                self.y_vdc[self.index_plot] = int(self.variables.specimen_voltage_plot)  # Add a new value.

            else:
                x_vdc_last = self.x_vdc[-1]
                self.x_vdc.append(x_vdc_last + 0.5)  # Add a new value 1 higher than the last.
                self.y_vdc.append(int(self.variables.specimen_voltage_plot))

            # Set the maximum number of data points to display
            max_display_points = 200
            # Downsample the data if needed
            if len(self.x_vdc) > max_display_points:
                step = len(self.x_vdc) // max_display_points
                x_vdc_downsampled = self.x_vdc[::step]
                y_vdc_downsampled = self.y_vdc[::step]
                self.data_line_vdc.setData(x_vdc_downsampled, y_vdc_downsampled)
            else:
                self.data_line_vdc.setData(self.x_vdc, self.y_vdc)

            # Detection Rate Visualization
            # with self.variables.lock_statistics:
            if self.index_plot < len(self.y_dtec):
                self.y_dtec[self.index_plot] = self.variables.detection_rate_current_plot  # Add a new value.
            else:
                # self.x_dtec = self.x_dtec[1:]  # Remove the first element.
                x_dtec_last = self.x_dtec[-1]
                self.x_dtec.append(x_dtec_last + 0.5)  # Add a new value 1 higher than the last.
                self.y_dtec.append(self.variables.detection_rate_current_plot)

            # self.data_line_dtec.setData(self.x_dtec, self.y_dtec)
            # Set the maximum number of data points to display
            max_display_points = 200
            # Downsample the data if needed
            if len(self.x_dtec) > max_display_points and not self.change_detection_rate_range:
                step = len(self.x_dtec) // max_display_points
                x_dtec_downsampled = self.x_dtec[::step]
                y_dtec_downsampled = self.y_dtec[::step]
                self.data_line_dtec.setData(x_dtec_downsampled, y_dtec_downsampled)
            elif len(self.x_dtec) > max_display_points and self.change_detection_rate_range:
                x_dtec_downsampled = self.x_dtec[-max_display_points:]
                y_dtec_downsampled = self.y_dtec[-max_display_points:]
                self.data_line_dtec.setData(x_dtec_downsampled, y_dtec_downsampled)
            else:
                self.data_line_dtec.setData(self.x_dtec, self.y_dtec)
            # Increase the index
            # with self.variables.lock_statistics:
            self.index_plot += 1
            # mass spectrum

            if self.counter_source == 'TDC' and self.variables.total_ions > 0 and \
                    self.index_wait_on_plot_start > 16:

                while not self.x_plot.empty() and not self.y_plot.empty() and not self.t_plot.empty() and \
                        not self.main_v_dc_plot.empty():
                    data = self.x_plot.get()
                    self.xx.extend(data)
                    data = self.y_plot.get()
                    self.yy.extend(data)
                    data = self.t_plot.get()
                    self.tt.extend(data)
                    data = self.main_v_dc_plot.get()
                    self.main_v_dc_dld.extend(data)

                xx = np.array(self.xx)
                yy = np.array(self.yy)
                tt = np.array(self.tt)
                main_v_dc_dld = np.array(self.main_v_dc_dld)
                try:
                    if self.conf["visualization"] == "tof":
                        viz = tt[tt < self.conf["max_tof"]]
                    elif self.conf["visualization"] == "mc":
                        max_lenght = min(len(xx), len(yy), len(tt), len(main_v_dc_dld))
                        xx_max_lenght = xx[:max_lenght]
                        yy_max_lenght = yy[:max_lenght]
                        tt_max_lenght = tt[:max_lenght]
                        main_v_dc_dld_max_lenght = main_v_dc_dld[:max_lenght]

                        if self.mc_tof_last_events_flag:
	                        xx_max_lenght = xx_max_lenght[-self.num_event_mc_tof:]
	                        yy_max_lenght = yy_max_lenght[-self.num_event_mc_tof:]
	                        tt_max_lenght = tt_max_lenght[-self.num_event_mc_tof:]
	                        main_v_dc_dld_max_lenght = main_v_dc_dld_max_lenght[-self.num_event_mc_tof:]

                        viz = tof2mc_simple.tof_2_mc(tt_max_lenght, self.conf["t_0"],
                                                     main_v_dc_dld_max_lenght,
                                                     xx_max_lenght,
                                                     yy_max_lenght,
                                                     flightPathLength=self.conf["flight_path_length"])
                        if self.conf["visualization"] == "mc":
	                        viz = viz[viz < self.conf["max_mass"]]
                        elif self.conf["visualization"] == "tof":
	                        viz = tt_max_lenght[tt_max_lenght < self.conf["max_tof"]]

                    bin_size = self.conf["bin_size"]
                    # bins = np.linspace(np.min(viz), np.max(viz), round(np.max(viz) / bin_size))
                    # Efficient histogram computation
                    y_tof_mc, x_tof_mc = efficient_histogram(viz, bin_size)
                    self.histogram.clear()
                    self.histogram.plot(x_tof_mc, y_tof_mc, stepMode="center", fillLevel=0, fillOutline=True,
                                        brush='black', name="num ions: %s" % len(xx))
                # Create y-values for the steps by repeating the values in hist
                # y_tof_mc = np.repeat(y_tof_mc, 2)
                # # Create x-values for the steps by using the bin edges
                # x_tof_mc = x_tof_mc.repeat(2)[1:-1]
                # x_tof_mc = np.append(x_tof_mc, x_tof_mc[-1])
                # self.histogram.plot(x_tof_mc, y_tof_mc, stepMode=True, fillLevel=0, fillOutline=False,
                #                     brush=(0, 0, 0, 150), name="num ions: %s" % self.variables.total_ions)

                except Exception as e:
                    print(
                        f"{initialize_devices.bcolors.FAIL}Error: Cannot plot Histogram correctly{initialize_devices.bcolors.ENDC}")
                    print(e)
                # Visualization
                try:
                    # adding points to the scatter plot
                    self.scatter.setSize(self.variables.hitmap_plot_size)
                    hit_display = self.variables.hit_display

                    min_length = min(len(xx), len(yy))
                    x = xx[-min_length:] * 10
                    y = yy[-min_length:] * 10
                    if self.variables.reset_heatmap:
                        self.index_plot_heatmap = len(x)
                        self.variables.reset_heatmap = False
                    if self.index_plot_heatmap > 0:
                        x = x[self.index_plot_heatmap:]
                        y = y[self.index_plot_heatmap:]

                    x = x[-hit_display:]
                    y = y[-hit_display:]

                    self.scatter.clear()
                    self.scatter.setData(x=x, y=y)
                    # add item to plot window
                    # adding scatter plot item to the plot window
                    self.detector_heatmap.clear()
                    self.detector_heatmap.addItem(self.scatter)
                    self.detector_heatmap.addItem(self.detector_circle)
                except Exception as e:
                    print(
                        f"{initialize_devices.bcolors.FAIL}Error: Cannot plot Ions correctly{initialize_devices.bcolors.ENDC}")
                    print(e)
            # save plots to the file
            if time.time() - self.start_time_metadata >= self.variables.save_meta_interval_visualization:
                path_meta = self.variables.path_meta
                exporter = pg.exporters.ImageExporter(self.vdc_time.plotItem)
                exporter.params['width'] = 1000  # Set the width of the image
                exporter.params['height'] = 800  # Set the height of the image
                exporter.export(path_meta + '/visualization_v_dc_p_%s.png' % self.index_plot_save)
                exporter = pg.exporters.ImageExporter(self.detection_rate_viz.plotItem)
                exporter.params['width'] = 1000  # Set the width of the image
                exporter.params['height'] = 800  # Set the height of the image
                exporter.export(path_meta + '/visualization_detection_rate_%s.png' % self.index_plot_save)
                exporter = pg.exporters.ImageExporter(self.detector_heatmap.plotItem)
                exporter.params['width'] = 1000  # Set the width of the image
                exporter.params['height'] = 800  # Set the height of the image
                exporter.export(path_meta + '/visualization_detector_%s.png' % self.index_plot_save)
                exporter = pg.exporters.ImageExporter(self.histogram.plotItem)
                exporter.params['width'] = 1000  # Set the width of the image
                exporter.params['height'] = 800  # Set the height of the image
                exporter.export(path_meta + '/visualization_mc_tof_%s.png' % self.index_plot_save)

                screenshot = QtWidgets.QApplication.primaryScreen().grabWindow(self.visualization_window.winId())
                screenshot.save(path_meta + '/visualization_screenshot_%s.png' % self.index_plot_save, 'png')
                self.start_time_metadata = time.time()
                # Increase the index
                self.index_plot_save += 1

    def spectrum_switch_mc_tof(self):
	    """
		Switch between mass spectrum and time of flight spectrum
		Args:
			None

		Return:
			None
		"""
	    if self.conf["visualization"] == "tof":
		    self.conf["visualization"] = "mc"
		    self.histogram.setLabel("bottom", "m/c", units='Da', **self.styles)
	    elif self.conf["visualization"] == "mc":
		    self.conf["visualization"] = "tof"
		    self.histogram.setLabel("bottom", "Time", units='ns', **self.styles)

    def spectrum_last_events(self):
	    """
		Display the last events in the mass spectrum
		Args:
			None

		Return:
			None
		"""
	    self.mc_tof_last_events_flag = not self.mc_tof_last_events_flag
	    if self.mc_tof_last_events_flag:
		    self.spectrum_last_events_switch.setStyleSheet("QPushButton{\n"
		                                                   "background: rgb(0, 255, 26)\n"
		                                                   "}")
	    else:
		    self.spectrum_last_events_switch.setStyleSheet(self.original_button_style)

    def parameters_changes(self):
	    """
		Change the parameters for the mass spectrum
		Args:
			None

		Return:
			None
		"""
	    if self.num_last_events.text().isdigit():
		    self.num_event_mc_tof = int(self.num_last_events.text())
	    if self.max_mc.text().isdigit():
		    self.conf["max_mass"] = int(self.max_mc.text())
	    if self.max_tof.text().isdigit():
		    self.conf["max_tof"] = int(self.max_tof.text())

    def stop(self):
        """
        Stop any background activity
        Args:
            None

        Return:
            None
            """
        # Add any additional cleanup code here
        pass


def efficient_histogram(viz, bin_size):
    bins = np.arange(np.min(viz), np.max(viz) + bin_size, bin_size)
    hist, edges = np.histogram(viz, bins=bins)
    hist[hist == 0] = 1  # Avoid log(0)
    return hist, edges


class VisualizationWindow(QtWidgets.QWidget):
    """
    Widget for the Visualization window.
    """
    closed = QtCore.pyqtSignal()  # Define a custom closed signal

    def __init__(self, variables, gui_visualization, visualization_close_event,
                 visualization_win_front, *args, **kwargs):
        """
        Constructor for the VisualizationWindow class.

        Args:
            variables: Shared variables.
            gui_visualization: Instance of the Visualization.
            visualization_close_event: Event for the Visualization window closed.
            visualization_win_front: Event for the Visualization window front.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Return:
            None
        """
        super().__init__(*args, **kwargs)
        self.gui_visualization = gui_visualization
        self.variables = variables
        self.visualization_win_front = visualization_win_front
        self.visualization_close_event = visualization_close_event
        self.show()
        self.showMinimized()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_if_should)
        self.timer.start(500)  # Check every 1000 milliseconds (1 second)

    def closeEvent(self, event):
        """
        Close event for the window.

        Args:
            event: Close event.

        Return:
            None
        """
        event.ignore()
        self.showMinimized()
        self.visualization_close_event.set()

    def check_if_should(self):
        """
        Check if the window should be shown.

        Args:
            None

        Return:
            None
        """
        if self.visualization_win_front.is_set():
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self.show()
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowType.WindowStaysOnTopHint)
            self.visualization_win_front.clear()  # Reset the flag
        if self.variables.flag_visualization_win_show:
            self.show()
            self.variables.flag_visualization_win_show = False

    def setWindowStyleFusion(self):
        # Set the Fusion style
        QtWidgets.QApplication.setStyle("Fusion")


def run_visualization_window(variables, conf, visualization_closed_event, visualization_win_front,
                             x_plot, y_plot, t_plot, main_v_dc_plot):
    """
    Run the Cameras window in a separate process.

    Args:
        variables: Shared variables.
        conf: Configuration dictionary.
        visualization_closed_event: Event for the Visualization window closed.
        visualization_win_front: Event for the Visualization window front.
        x_plot: x plot
        y_plot: y plot
        t_plot: t plot
        main_v_dc_plot: main v dc plot

    Return:
        None
    """
    app = QtWidgets.QApplication(sys.argv)  # <-- Create a new QApplication instance
    app.setStyle('Fusion')

    gui_visualization = Ui_Visualization(variables, conf, x_plot, y_plot, t_plot, main_v_dc_plot)
    Cameras_alignment = VisualizationWindow(variables, gui_visualization, visualization_closed_event,
                                            visualization_win_front, flags=QtCore.Qt.WindowType.Tool)
    gui_visualization.setupUi(Cameras_alignment)
    sys.exit(app.exec())  # <-- Start the event loop for this QApplication instance


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
    manager = multiprocessing.Manager()
    ns = manager.Namespace()
    variables = share_variables.Variables(conf, ns)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    Visualization = QtWidgets.QWidget()
    x_plot = multiprocessing.Queue()
    y_plot = multiprocessing.Queue()
    t_plot = multiprocessing.Queue()
    main_v_dc_plot = multiprocessing.Queue()
    ui = Ui_Visualization(variables, conf, x_plot, y_plot, t_plot, main_v_dc_plot)
    ui.setupUi(Visualization)
    Visualization.show()
    sys.exit(app.exec())

