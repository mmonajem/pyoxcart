"""
This is the script that print all the com port of the system.
It is usful to find the com port of the device.
"""

import serial.tools.list_ports

# get available COM ports and store as list
com_ports = list(serial.tools.list_ports.comports())

print(*com_ports, sep="\n")