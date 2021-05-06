from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
import pyqtgraph as pg
import sys
import numpy as np
import nidaqmx
import time

import oxcart
import variables


class Ui_OXCART(object):
    def setupUi(self, OXCART):
        OXCART.setObjectName("OXCART")
        OXCART.resize(2064, 1703)
        self.centralwidget = QtWidgets.QWidget(OXCART)
        # self.vdc_time = QtWidgets.QWidget(self.centralwidget)
        self.vdc_time = pg.PlotWidget(self.centralwidget)
        self.vdc_time.setGeometry(QtCore.QRect(740, 140, 600, 600))
        self.vdc_time.setObjectName("vdc_time")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1020, 100, 80, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(1660, 1450, 314, 106))
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
        self.label_10.setGeometry(QtCore.QRect(1590, 90, 156, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        # self.detection_rate_viz = QtWidgets.QWidget(self.centralwidget)
        self.detection_rate_viz = pg.PlotWidget(self.centralwidget)
        self.detection_rate_viz.setGeometry(QtCore.QRect(1370, 140, 600, 600))
        self.detection_rate_viz.setObjectName("detection_rate_viz")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(970, 780, 134, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        # self.visualization = QtWidgets.QWidget(self.centralwidget)
        self.visualization = pg.PlotWidget(self.centralwidget)
        self.visualization.setGeometry(QtCore.QRect(740, 820, 600, 600))
        self.visualization.setObjectName("visualization")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(1620, 780, 110, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        # self.histogram = QtWidgets.QWidget(self.centralwidget)
        self.histogram = pg.PlotWidget(self.centralwidget)
        self.histogram.setGeometry(QtCore.QRect(1370, 820, 600, 600))
        self.histogram.setObjectName("histogram")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(20, 910, 101, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.Error = QtWidgets.QLabel(self.centralwidget)
        self.Error.setGeometry(QtCore.QRect(640, 20, 791, 51))
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
        self.diagram.setGeometry(QtCore.QRect(28, 960, 601, 431))
        self.diagram.setText("")
        self.diagram.setObjectName("diagram")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 620, 436, 285))
        self.widget.setObjectName("widget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_11 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 0, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.widget)
        self.label_12.setObjectName("label_12")
        self.gridLayout_5.addWidget(self.label_12, 1, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.widget)
        self.label_21.setObjectName("label_21")
        self.gridLayout_5.addWidget(self.label_21, 6, 0, 1, 1)
        self.hdf5_path = QtWidgets.QLineEdit(self.widget)
        self.hdf5_path.setObjectName("hdf5_path")
        self.gridLayout_5.addWidget(self.hdf5_path, 6, 1, 1, 1)
        self.speciemen_voltage = QtWidgets.QLineEdit(self.widget)
        self.speciemen_voltage.setText("")
        self.speciemen_voltage.setObjectName("speciemen_voltage")
        self.gridLayout_5.addWidget(self.speciemen_voltage, 3, 1, 1, 1)
        self.total_ions = QtWidgets.QLineEdit(self.widget)
        self.total_ions.setText("")
        self.total_ions.setObjectName("total_ions")
        self.gridLayout_5.addWidget(self.total_ions, 2, 1, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.widget)
        self.label_14.setObjectName("label_14")
        self.gridLayout_5.addWidget(self.label_14, 3, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.widget)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 5, 0, 1, 1)
        self.elapsed_time = QtWidgets.QLineEdit(self.widget)
        self.elapsed_time.setText("")
        self.elapsed_time.setObjectName("elapsed_time")
        self.gridLayout_5.addWidget(self.elapsed_time, 1, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.widget)
        self.label_16.setObjectName("label_16")
        self.gridLayout_5.addWidget(self.label_16, 4, 0, 1, 1)
        self.detection_rate = QtWidgets.QLineEdit(self.widget)
        self.detection_rate.setText("")
        self.detection_rate.setObjectName("detection_rate")
        self.gridLayout_5.addWidget(self.detection_rate, 5, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.widget)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 2, 0, 1, 1)
        self.pulse_voltage = QtWidgets.QLineEdit(self.widget)
        self.pulse_voltage.setText("")
        self.pulse_voltage.setObjectName("pulse_voltage")
        self.gridLayout_5.addWidget(self.pulse_voltage, 4, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(20, 1440, 621, 61))
        self.widget1.setObjectName("widget1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.led_buffer_chamber = QtWidgets.QLabel(self.widget1)
        self.led_buffer_chamber.setAlignment(QtCore.Qt.AlignCenter)
        self.led_buffer_chamber.setObjectName("led_buffer_chamber")
        self.gridLayout_4.addWidget(self.led_buffer_chamber, 0, 1, 1, 1)
        self.led_main_chamber = QtWidgets.QLabel(self.widget1)
        self.led_main_chamber.setAlignment(QtCore.Qt.AlignCenter)
        self.led_main_chamber.setObjectName("led_main_chamber")
        self.gridLayout_4.addWidget(self.led_main_chamber, 0, 0, 1, 1)
        self.led_load_lock = QtWidgets.QLabel(self.widget1)
        self.led_load_lock.setAlignment(QtCore.Qt.AlignCenter)
        self.led_load_lock.setObjectName("led_load_lock")
        self.gridLayout_4.addWidget(self.led_load_lock, 0, 2, 1, 1)
        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(20, 1510, 621, 81))
        self.widget2.setObjectName("widget2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.load_lock_switch = QtWidgets.QPushButton(self.widget2)
        self.load_lock_switch.setObjectName("load_lock_switch")
        self.gridLayout.addWidget(self.load_lock_switch, 0, 2, 1, 1)
        self.main_chamber_switch = QtWidgets.QPushButton(self.widget2)
        self.main_chamber_switch.setObjectName("main_chamber_switch")
        self.gridLayout.addWidget(self.main_chamber_switch, 0, 0, 1, 1)
        self.buffer_chamber_switch = QtWidgets.QPushButton(self.widget2)
        self.buffer_chamber_switch.setObjectName("buffer_chamber_switch")
        self.gridLayout.addWidget(self.buffer_chamber_switch, 0, 1, 1, 1)
        self.widget3 = QtWidgets.QWidget(self.centralwidget)
        self.widget3.setGeometry(QtCore.QRect(21, 53, 488, 543))
        self.widget3.setObjectName("widget3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtWidgets.QLabel(self.widget3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.ex_time = QtWidgets.QLineEdit(self.widget3)
        self.ex_time.setObjectName("ex_time")
        self.gridLayout_3.addWidget(self.ex_time, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)
        self.ex_freq = QtWidgets.QLineEdit(self.widget3)
        self.ex_freq.setObjectName("ex_freq")
        self.gridLayout_3.addWidget(self.ex_freq, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 3, 0, 1, 1)
        self.vdc_min = QtWidgets.QLineEdit(self.widget3)
        self.vdc_min.setObjectName("vdc_min")
        self.gridLayout_3.addWidget(self.vdc_min, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 4, 0, 1, 1)
        self.vdc_max = QtWidgets.QLineEdit(self.widget3)
        self.vdc_max.setObjectName("vdc_max")
        self.gridLayout_3.addWidget(self.vdc_max, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget3)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 5, 0, 1, 1)
        self.vdc_steps = QtWidgets.QLineEdit(self.widget3)
        self.vdc_steps.setObjectName("vdc_steps")
        self.gridLayout_3.addWidget(self.vdc_steps, 5, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.widget3)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 6, 0, 1, 1)
        self.cycle_avg = QtWidgets.QLineEdit(self.widget3)
        self.cycle_avg.setObjectName("cycle_avg")
        self.gridLayout_3.addWidget(self.cycle_avg, 6, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget3)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 7, 0, 1, 1)
        self.vp_min = QtWidgets.QLineEdit(self.widget3)
        self.vp_min.setObjectName("vp_min")
        self.gridLayout_3.addWidget(self.vp_min, 7, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget3)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 8, 0, 1, 1)
        self.vp_max = QtWidgets.QLineEdit(self.widget3)
        self.vp_max.setObjectName("vp_max")
        self.gridLayout_3.addWidget(self.vp_max, 8, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.widget3)
        self.label_25.setObjectName("label_25")
        self.gridLayout_3.addWidget(self.label_25, 9, 0, 1, 1)
        self.pulse_fraction = QtWidgets.QLineEdit(self.widget3)
        self.pulse_fraction.setObjectName("pulse_fraction")
        self.gridLayout_3.addWidget(self.pulse_fraction, 9, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.widget3)
        self.label_23.setObjectName("label_23")
        self.gridLayout_3.addWidget(self.label_23, 10, 0, 1, 1)
        self.pulse_frequency = QtWidgets.QLineEdit(self.widget3)
        self.pulse_frequency.setObjectName("pulse_frequency")
        self.gridLayout_3.addWidget(self.pulse_frequency, 10, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.widget3)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 11, 0, 1, 1)
        self.detection_rate_init = QtWidgets.QLineEdit(self.widget3)
        self.detection_rate_init.setObjectName("detection_rate_init")
        self.gridLayout_3.addWidget(self.detection_rate_init, 11, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.widget3)
        self.label_22.setObjectName("label_22")
        self.gridLayout_3.addWidget(self.label_22, 12, 0, 1, 1)
        self.hit_displayed = QtWidgets.QLineEdit(self.widget3)
        self.hit_displayed.setObjectName("hit_displayed")
        self.gridLayout_3.addWidget(self.hit_displayed, 12, 1, 1, 1)
        OXCART.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(OXCART)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2064, 38))
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
        self.Error.setText(_translate("OXCART", "<html><head/><body><p><span style=\" color:#ff0000;\"></span></p></body></html>"))
        self.label_11.setText(_translate("OXCART", "Run Statistics"))
        self.label_12.setText(_translate("OXCART", "Elapsed Time (S):"))
        self.label_21.setText(_translate("OXCART", "HDF5 Path:"))
        self.hdf5_path.setText(_translate("OXCART", "test.h5"))
        self.label_14.setText(_translate("OXCART", "Specimen Voltage (V)"))
        self.label_15.setText(_translate("OXCART", "Detection Rate (%)"))
        self.label_16.setText(_translate("OXCART", "Pulse Voltage (V)"))
        self.label_13.setText(_translate("OXCART", "Total Ions"))
        self.led_buffer_chamber.setText(_translate("OXCART", "Buffer"))
        self.led_main_chamber.setText(_translate("OXCART", "Main"))
        self.led_load_lock.setText(_translate("OXCART", "Load"))
        self.load_lock_switch.setText(_translate("OXCART", "Cryo"))
        self.main_chamber_switch.setText(_translate("OXCART", "Main Chamber"))
        self.buffer_chamber_switch.setText(_translate("OXCART", "Load Lock"))
        ###
        self.main_chamber_switch.clicked.connect(lambda:self.gates(1))
        self.buffer_chamber_switch.clicked.connect(lambda:self.gates(2))
        self.load_lock_switch.clicked.connect(lambda:self.gates(3))
        ###
        self.label.setText(_translate("OXCART", "Setup Parameters"))
        self.label_2.setText(_translate("OXCART", "Max. Experiment Time (S)"))
        self.ex_time.setText(_translate("OXCART", "90"))
        self.label_3.setText(_translate("OXCART", "Control refresh Freq.(Hz)"))
        self.ex_freq.setText(_translate("OXCART", "10"))
        self.label_4.setText(_translate("OXCART", "Specimen Start Voltage (V)"))
        self.vdc_min.setText(_translate("OXCART", "2000"))
        self.label_5.setText(_translate("OXCART", "Specimen Stop Voltage (V)"))
        self.vdc_max.setText(_translate("OXCART", "4000"))
        self.label_6.setText(_translate("OXCART", "K_p"))
        self.vdc_steps.setText(_translate("OXCART", "100"))
        self.label_20.setText(_translate("OXCART", "Cycle for Avg."))
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
        self.menuFile.setTitle(_translate("OXCART", "File"))
        self.actionExit.setText(_translate("OXCART", "Exit"))

        # High Voltage visualization
        self.x_vdc = list(range(1000))  # 1000 time points
        self.y_vdc = [np.nan] * 1000  # 1000 data points
        self.y_vps = [np.nan] * 1000  # 1000 data points
        pen_vdc = pg.mkPen(color=(255, 0, 0), width=6)
        pen_vps = pg.mkPen(color=(0, 0, 255), width=3)
        self.data_line_vdc = self.vdc_time.plot(self.x_vdc, self.y_vdc, name = "High Vol.", pen=pen_vdc)
        self.data_line_vps = self.vdc_time.plot(self.x_vdc, self.y_vps, name = "Pulse Vol.", pen=pen_vps)
        self.vdc_time.setBackground('w')
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.vdc_time.setLabel("left", "High Voltage (V)", **styles)
        self.vdc_time.setLabel("bottom", "Time (Sec)", **styles)
        #Add grid
        self.vdc_time.showGrid(x=True, y=True)
        # Add Range
        self.vdc_time.setXRange(-100, 1100, padding=0)
        self.vdc_time.setYRange(-200, 20000, padding=0)
        # Add legend
        self.vdc_time.addLegend()

        # Detection Visualization
        self.x_dtec = list(range(1000))  # 1000 time points
        self.y_dtec = [np.nan] * 1000  # 1000 data points
        pen_dtec = pg.mkPen(color=(255, 0, 0), width=6)
        self.data_line_dtec =  self.detection_rate_viz.plot(self.x_dtec, self.y_dtec, pen=pen_dtec)
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

        # Visualization

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

        # Histogram
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        # Diagram and LEDs
        self.diagram_close_all = QPixmap('.\png\close_all.png')
        self.diagram_main_open = QPixmap('.\png\main_open.png')
        self.diagram_load_open =  QPixmap('.\png\load_open.png')
        self.diagram_cryo_open =  QPixmap('.\png\cryo_open.png')
        self.led_red = QPixmap('.\png\led-red-on.png')
        self.led_green = QPixmap('.\png\green-led-on.png')

        self.diagram.setPixmap(self.diagram_close_all)
        self.led_main_chamber.setPixmap(self.led_red)
        self.led_buffer_chamber.setPixmap(self.led_red)
        self.led_load_lock.setPixmap(self.led_red)

        # self.pixmap_signal_fan1.emit(ICON_RED_LED if fans_rpm[0] == 0 or fans_voltage[0] == 0 else ICON_GREEN_LED)



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
        variables.vdc_step = float(self.vdc_steps.text())
        variables.v_p_min = float(self.vp_min.text())
        variables.v_p_max = float(self.vp_max.text())
        variables.pulse_fraction = float(self.pulse_fraction.text())/100
        variables.pulse_frequency = int(self.pulse_frequency.text())
        variables.detection_rate = int(self.detection_rate_init.text())
        variables.hdf5_path = self.hdf5_path.text()
        variables.cycle_avg = int(self.cycle_avg.text())

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
                self.led_buffer_chamber.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_load_open)
                variables.flag_load_gate = True
            elif variables.flag_load_gate == True:
                switch_gate(3)
                self.led_buffer_chamber.setPixmap(self.led_red)
                self.diagram.setPixmap(self.diagram_close_all)
                variables.flag_load_gate = False
        elif gate_num == 3 and variables.flag_main_gate == False and variables.flag_load_gate == False:
            if variables.flag_cryo_gate == False:
                switch_gate(4)
                self.led_load_lock.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_cryo_open)
                variables.flag_cryo_gate = True
            elif variables.flag_cryo_gate == True:
                switch_gate(5)
                self.led_load_lock.setPixmap(self.led_red)
                self.diagram.setPixmap(self.diagram_close_all)
                variables.flag_cryo_gate = False
        else:
            _translate = QtCore.QCoreApplication.translate
            self.Error.setText(_translate("OXCART",
                                          "<html><head/><body><p><span style=\" color:#ff0000;\">!!! First Close all the Gates</span></p></body></html>"))

    def update_plot_data(self):

        if variables.start_flag == True:
            if variables.index_plot <= 999:
                self.y_vdc = self.y_vdc[:-1]  # Remove the last
                self.y_vps = self.y_vps[:-1]  # Remove the last
                self.y_vdc.insert(variables.index_plot, int(variables.specimen_voltage))  # Add a new value.
                self.y_vps.insert(variables.index_plot, int(variables.pulse_voltage))  # Add a new value.
            else:
                self.x_dtec = self.x_dtec[1:]  # Remove the first .
                self.x_dtec.append(self.x_dtec[-1] + 1)  # Add a new value 1 higher than the last.
                self.y_vdc = self.y_vdc[1:]  # Remove the first
                self.y_vps = self.y_vps[1:]  # Remove the first
                self.y_vdc.insert(999, int(variables.specimen_voltage))  # Add a new value.
                self.y_vps.insert(999, int(variables.pulse_voltage))  # Add a new value.

            self.data_line_vdc.setData(self.x_vdc, self.y_vdc)
            self.data_line_vps.setData(self.x_vdc, self.y_vps)

            # # Detection Rate Visualization
            if variables.start_flag == True:
                if variables.index_plot <= 999:
                    self.y_dtec = self.y_dtec[:-1]  # Remove the first
                    self.y_dtec.insert(variables.index_plot, int(variables.avg_n_count )) # Add a new value.
                else:
                    self.x_dtec = self.x_dtec[1:]  # Remove the first y element.
                    self.x_dtec.append(self.x_dtec[-1] + 1)  # Add a new value 1 higher than the last.
                    self.y_dtec = self.x_dtec[1:]
                    self.y_dtec.insert(999, int(variables.avg_n_count))

            self.data_line_dtec.setData(self.x_dtec, self.y_dtec)

            # Increase the index
            variables.index_plot += 1

            # Visualization
        if variables.start_flag == False:
            self.y_vdc = [np.nan] * 1000  # 100 data points
            self.y_vps = [np.nan] * 1000  # 100 data points

            self.data_line_vdc.setData(self.x_vdc, self.y_vdc)
            self.data_line_vps.setData(self.x_vdc, self.y_vps)

            self.y_dtec = [np.nan] * 1000

            self.data_line_dtec.setData(self.x_dtec, self.y_dtec)

        # Statistics Update
        self.speciemen_voltage.setText(str(float("{:.3f}".format(variables.specimen_voltage))))
        self.pulse_voltage.setText(str(float("{:.3f}".format(variables.pulse_voltage))))
        self.elapsed_time.setText(str(float("{:.3f}".format(variables.elapsed_time))))
        self.total_ions.setText((str(variables.total_ions)))
        self.detection_rate.setText(str
                (float("{:.3f}".format((variables.avg_n_count * 100)/(1 + variables.pulse_frequency * 1000)))))

        # Update the setup parameters
        variables.ex_time = int(self.ex_time.text())
        variables.ex_freq = int(self.ex_freq.text())
        variables.vdc_min = float(self.vdc_min.text())
        if float(self.vdc_max.text()) > 20000:
            _translate = QtCore.QCoreApplication.translate
            self.Error.setText(_translate("OXCART","<html><head/><body><p><span style=\" color:#ff0000;\">Maximum possible number is 20KV</span></p></body></html>"))
            self.vdc_max.setText(_translate("OXCART", "4000"))
            variables.vdc_max = float(self.vdc_max.text())
        variables.vdc_step = float(self.vdc_steps.text())
        variables.v_p_min = float(self.vp_min.text())
        if float(self.vp_max.text()) > 3281:
            _translate = QtCore.QCoreApplication.translate
            self.Error.setText(_translate("OXCART","<html><head/><body><p><span style=\" color:#ff0000;\">Maximum possible number is 3281 V</span></p></body></html>"))
            self.vp_max.setText(_translate("OXCART", "3281"))
        variables.v_p_max = float(self.vp_max.text())
        variables.pulse_fraction = float(self.pulse_fraction.text())/100
        variables.pulse_frequency = int(self.pulse_frequency.text())
        variables.detection_rate = int(self.detection_rate_init.text())
        variables.hdf5_path = self.hdf5_path.text()
        variables.cycle_avg = int(self.cycle_avg.text())



class MainThread(QThread, Ui_OXCART):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)

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
    print(width, height)

    OXCART = QtWidgets.QMainWindow()
    ui = Ui_OXCART()
    ui.setupUi(OXCART)
    OXCART.show()
    sys.exit(app.exec_())