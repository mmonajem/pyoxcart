import serial.tools.list_ports

com_ports = list(serial.tools.list_ports.comports())
for idx, curr in enumerate(com_ports):
	print("  " + str(idx) + ".)  " + curr.description)
