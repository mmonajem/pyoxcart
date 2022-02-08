"""
This is the main script is load the GUI base on the configuration file.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""

from dataclasses import dataclass
import sys
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
# Serial ports and Camera libraries
import serial.tools.list_ports
from pypylon import pylon

# Local module and scripts
from tools import variables,read_files
from devices.camera import Camera
from devices import initialize_devices
from gui import gui_oxcart, gui_physic
import json

configFile= 'config.json'




if __name__ == "__main__":

    conf = read_files.read_json_file(configFile)

    if conf['mode'] == 'advance':

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
        # width, height = screen_resolution.width(), screen_resolution.height()
        # print('Screen size is:(%s,%s)' % (width, height))
        OXCART = QtWidgets.QMainWindow()
        lock = threading.Lock()
        ui = gui_oxcart.Ui_OXCART(camera.devices, camera.tlFactory, camera.cameras, camera.converter, lock, app, conf)
        ui.setupUi(OXCART)
        OXCART.show()
        sys.exit(app.exec_())

    elif conf['mode'] == 'simple':

        # Initialize global experiment variables
        variables.init()

        app = QtWidgets.QApplication(sys.argv)
        APT_Physic = QtWidgets.QMainWindow()
        lock = threading.Lock()
        ui = gui_physic.Ui_APT_Physic(lock, app, conf)
        ui.setupUi(APT_Physic)
        APT_Physic.show()
        sys.exit(app.exec_())
