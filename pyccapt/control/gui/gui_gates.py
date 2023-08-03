import os
import sys
import time

import nidaqmx
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap

# Local module and scripts
from pyccapt.control.control_tools import share_variables, read_files


class Ui_Gates(object):

    def __init__(self, variables, conf):
        self.variables = variables
        self.conf = conf

    def setupUi(self, Ui_Gates):
        Ui_Gates.setObjectName("Ui_Gates")
        Ui_Gates.resize(398, 357)
        self.gridLayout_2 = QtWidgets.QGridLayout(Ui_Gates)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.diagram = QtWidgets.QLabel(parent=Ui_Gates)
        self.diagram.setMinimumSize(QtCore.QSize(378, 246))
        self.diagram.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.diagram.setStyleSheet("QWidget{\n"
                                   "border: 2px solid gray;\n"
                                   "background: rgb(255, 255, 255)\n"
                                   "}")
        self.diagram.setText("")
        self.diagram.setObjectName("diagram")
        self.gridLayout.addWidget(self.diagram, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.led_main_chamber = QtWidgets.QLabel(parent=Ui_Gates)
        self.led_main_chamber.setMinimumSize(QtCore.QSize(50, 50))
        self.led_main_chamber.setMaximumSize(QtCore.QSize(50, 50))
        self.led_main_chamber.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.led_main_chamber.setObjectName("led_main_chamber")
        self.horizontalLayout.addWidget(self.led_main_chamber)
        self.led_load_lock = QtWidgets.QLabel(parent=Ui_Gates)
        self.led_load_lock.setMinimumSize(QtCore.QSize(50, 50))
        self.led_load_lock.setMaximumSize(QtCore.QSize(50, 50))
        self.led_load_lock.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.led_load_lock.setObjectName("led_load_lock")
        self.horizontalLayout.addWidget(self.led_load_lock)
        self.led_cryo = QtWidgets.QLabel(parent=Ui_Gates)
        self.led_cryo.setMinimumSize(QtCore.QSize(50, 50))
        self.led_cryo.setMaximumSize(QtCore.QSize(50, 50))
        self.led_cryo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.led_cryo.setObjectName("led_cryo")
        self.horizontalLayout.addWidget(self.led_cryo)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.main_chamber_switch = QtWidgets.QPushButton(parent=Ui_Gates)
        self.main_chamber_switch.setMinimumSize(QtCore.QSize(0, 25))
        self.main_chamber_switch.setStyleSheet("QPushButton{\n"
                                               "background: rgb(193, 193, 193)\n"
                                               "}")
        self.main_chamber_switch.setObjectName("main_chamber_switch")
        self.horizontalLayout_2.addWidget(self.main_chamber_switch)
        self.load_lock_switch = QtWidgets.QPushButton(parent=Ui_Gates)
        self.load_lock_switch.setMinimumSize(QtCore.QSize(0, 25))
        self.load_lock_switch.setStyleSheet("QPushButton{\n"
                                            "background: rgb(193, 193, 193)\n"
                                            "}")
        self.load_lock_switch.setObjectName("load_lock_switch")
        self.horizontalLayout_2.addWidget(self.load_lock_switch)
        self.cryo_switch = QtWidgets.QPushButton(parent=Ui_Gates)
        self.cryo_switch.setMinimumSize(QtCore.QSize(0, 25))
        self.cryo_switch.setStyleSheet("QPushButton{\n"
                                       "background: rgb(193, 193, 193)\n"
                                       "}")
        self.cryo_switch.setObjectName("cryo_switch")
        self.horizontalLayout_2.addWidget(self.cryo_switch)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Ui_Gates)
        QtCore.QMetaObject.connectSlotsByName(Ui_Gates)
        Ui_Gates.setTabOrder(self.main_chamber_switch, self.load_lock_switch)
        Ui_Gates.setTabOrder(self.load_lock_switch, self.cryo_switch)

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

        ###
        self.main_chamber_switch.clicked.connect(lambda: self.gates(1))
        self.load_lock_switch.clicked.connect(lambda: self.gates(2))
        self.cryo_switch.clicked.connect(lambda: self.gates(3))

    def retranslateUi(self, Ui_Gates):
        _translate = QtCore.QCoreApplication.translate
        ###
        Ui_Gates.setWindowTitle(_translate("Ui_Gates", "PyCCAPT Gates Control"))
        Ui_Gates.setWindowIcon(QtGui.QIcon('./files/logo3.png'))
        ###
        self.led_main_chamber.setText(_translate("Ui_Gates", "Main"))
        self.led_load_lock.setText(_translate("Ui_Gates", "Load"))
        self.led_cryo.setText(_translate("Ui_Gates", "Cryo"))
        self.main_chamber_switch.setText(_translate("Ui_Gates", "Main Chamber"))
        self.load_lock_switch.setText(_translate("Ui_Gates", "Load Lock"))
        self.cryo_switch.setText(_translate("Ui_Gates", "Cryo"))

    def gates(self, gate_num):
        """
                The function for closing or opening gates
                """

        def switch_gate(num):
            """
                            The function for applying the command of closing or opening gate
                            """
            with nidaqmx.Task() as task:
                if self.conf["gates"] != "off":
                    task.do_channels.add_do_chan(self.conf["COM_PORT_gates"] + 'line%s' % num)
                    task.start()
                    task.write([True])
                    time.sleep(.5)
                    task.write([False])
                else:
                    print('The gates control is off')

        # Main gate
        if not self.variables.start_flag and gate_num == 1 and not self.variables.flag_load_gate \
                and not self.variables.flag_cryo_gate and self.variables.flag_pump_load_lock:
            if not self.variables.flag_main_gate:  # Open the main gate
                switch_gate(0)
                self.led_main_chamber.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_main_open)
                self.variables.flag_main_gate = True
            elif self.variables.flag_main_gate:  # Close the main gate
                switch_gate(1)
                self.led_main_chamber.setPixmap(self.led_red)
                self.diagram.setPixmap(self.diagram_close_all)
                self.variables.flag_main_gate = False
        # Buffer gate
        elif not self.variables.start_flag and gate_num == 2 and not self.variables.flag_main_gate \
                and not self.variables.flag_cryo_gate and self.variables.flag_pump_load_lock:
            if not self.variables.flag_load_gate:  # Open the main gate
                switch_gate(2)
                self.led_load_lock.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_load_open)
                self.variables.flag_load_gate = True
            elif self.variables.flag_load_gate:  # Close the main gate
                switch_gate(3)
                self.led_load_lock.setPixmap(self.led_red)
                self.diagram.setPixmap(self.diagram_close_all)
                self.variables.flag_load_gate = False
        # Cryo gate
        elif not self.variables.start_flag and gate_num == 3 and not self.variables.flag_main_gate \
                and not self.variables.flag_load_gate and self.variables.flag_pump_load_lock:
            if not self.variables.flag_cryo_gate:  # Open the main gate
                switch_gate(4)
                self.led_cryo.setPixmap(self.led_green)
                self.diagram.setPixmap(self.diagram_cryo_open)
                self.variables.flag_cryo_gate = True
            elif self.variables.flag_cryo_gate:  # Close the main gate
                switch_gate(5)
                self.led_cryo.setPixmap(self.led_red)
                self.diagram.setPixmap(self.diagram_close_all)
                self.variables.flag_cryo_gate = False
        # Show the error message in the GUI
        else:
            _translate = QtCore.QCoreApplication.translate
            self.Error.setText(_translate("OXCART",
                                          "<html><head/><body><p><span style=\" color:#ff0000;\">!!! First Close all "
                                          "the Gates and switch on the pump !!!</span></p></body></html>"))


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

    app = QtWidgets.QApplication(sys.argv)
    Gates = QtWidgets.QWidget()
    ui = Ui_Gates(variables, conf)
    ui.setupUi(Gates)
    Gates.show()
    sys.exit(app.exec())
