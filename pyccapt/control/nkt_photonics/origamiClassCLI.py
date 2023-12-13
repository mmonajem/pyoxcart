from time import sleep

import serial


# Control static object for Origami using CLI
# Version 1.1

# Author Ian Baker


class origClass:
	## Control methods

	def Listen(comPort):  # Sets the laser to Listen mode
		# tested works (18/08/2023)
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		# command to the port
		cmd = "ly_oxp2_listen\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			sleep(1)
			return -1

	def Standby(comPort):  # Sets the laser to Standby mode  - warning class 4 laser emissions
		# tested works (18/08/2023)
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "ly_oxp2_standby\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			sleep(1)
			return -1

	def Enable(comPort):  # Turns the laser ON and enables emission - warning class 4 laser emissions
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "ly_oxp2_enabled\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			sleep(1)
			return -1

	def Temp(comPort):  # Displays the laser system temperatures (needs a read back)
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "ly_oxp2_temp_status\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			return dataBack.decode()
		except:
			ser.close()
			sleep(1)
			return -1

	def Power(comPort, power):  # Sets the laser power in nanojoules
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "ly_oxp2_power=" + str(power) + "\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def PowerRead(comPort):  # Displays the laser power setting in nanojoules (needs a read back)
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "ly_oxp2_power?\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def AOM(comPort,
	        power):  # Sets the laser power through AOM control [xxxx range: 0-4000, 0-AOM closed, 4000-AOM opened]
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "e_power=xxxx" + str(power) + "\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def AOMRead(comPort):  # Displays the e_power setting
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "e_power?\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def Freq(comPort, freq):  # Sets the repetition rate frequency index [index range: 0-12] Note: optional command
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)
		cmd = "e_freq " + str(freq) + "\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def FreqRead(comPort):  # Displays the configured repetition rate frequency index
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "e_freq?\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def Div(comPort, division):  # Sets the division factor [Range: 1-1000000]
		# tested works (18/08/2023)
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)
		cmd = "e_div" + str(division) + "\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def DivRead(comPort):  # Displays the configured division factor
		# tested works (18/08/2023)
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "e_div?\r\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def Mode(comPort,
	         mode):  # Sets the power mode of the laser [power modes x=2,3,or 8 where 2=internal,3=external, 8=SPI]
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)
		cmd = "e_mode " + str(mode) + "\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def ModeRead(comPort):  # Displays the power mode setting
		# slightly buggy, doesnt readback properly (18/08/2023)
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)
		cmd = "e_mode?\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def StatusRead(comPort):  # Displays the state of the status LEDs where the output is an 8 bit word in decimal form.
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		""""
		Displays the state of the status LEDs where the output is an 8 bit word in decimal form.
		Example 33 in binary: 00100001 - Standby LED ON | Power LED ON
		Bit 8 On enabled (MSB)
		Bit 7 On disabled
		Bit 6 Standby
		Bit 5 Setup
		Bit 4 Listen
		Bit 3 Warning
		Bit 2 Error
		Bit 1 Power (LSB)
		"""
		cmd = "ly_oxp2_dev_status\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def ModeRead(comPort):  # Displays the power mode setting
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "e_mode?\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			return dataBack.decode()
		except:
			ser.close()
			sleep(1)
			return -1

	def ServiceMode(comPort):  # Sets the laser in service mode (must be in standby)
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "ly_oxp2_service_mode\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def DigitalGateLogic(comPort,
	                     choice):  # Sets the Digital Gate logic [x range: 0 or 1, when a logic low or no connection is detected at the port
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)  # 0 sets the AOM to open and 1 sets the AOM to close]
		cmd = "ly_oxp2_digiop=" + str(choice) + "\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def DigitalGateLogicRead(
			comPort):  # Reads the Digital Gate logic. When a logic low or no connection is detected at the port
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)
		# AOM is open if return value is 0 and closed if return value is 1]
		cmd = "ly_oxp2_digiop?\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def AOMEnable(comPort):  # Enables the output AOM
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "ly_oxp2_output_enable\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def AOMDisable(comPort):  # Disables the output AOM
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "ly_oxp2_output_disable\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1

	def AOMState(comPort):  # Questions the state
		# Open the port
		ser = serial.Serial(
			port=comPort,
			baudrate=38400,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			rtscts=False
		)

		cmd = "ly_oxp2_output?\n"
		try:
			ser.write(cmd.encode())
			sleep(0.1)
			dataStore = []
			while ser.in_waiting:
				dataBack = ser.readline()
				dataStore.append(dataBack.decode())
			ser.close()
			sleep(1)
			return dataBack.decode()
		except:
			ser.close()
			return -1
