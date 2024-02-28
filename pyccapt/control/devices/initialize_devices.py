import csv
import time
from datetime import datetime

import serial.tools.list_ports

from pyccapt.control.devices.edwards_tic import EdwardsAGC
from pyccapt.control.devices.pfeiffer_gauges import TPG362


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


def command_cryovac(cmd, com_port_cryovac):
	"""
	Execute a command on Cryovac through serial communication.

	Args:
		cmd: Command to be executed.
		com_port_cryovac: Serial communication object.

	Returns:
		Response code after executing the command.
	"""
	com_port_cryovac.write((cmd + '\r\n').encode())
	time.sleep(0.1)
	response = ''
	while com_port_cryovac.in_waiting > 0:
		response = com_port_cryovac.readline()
	if isinstance(response, bytes):
		response = response.decode("utf-8")
	return response


def command_edwards(conf, variables, cmd, E_AGC, status=None):
	"""
	Execute commands and set flags based on parameters.

	Args:
		conf: Configuration parameters.
		variables: Variables instance.
		cmd: Command to be executed.
		E_AGC: EdwardsAGC instance.
		status: Status of the lock.

	Returns:
		Response code after executing the command.
	"""

	try:
		if variables.flag_pump_load_lock_click and variables.flag_pump_load_lock and status == 'load_lock':
			if conf['pump_ll'] == "on":
				E_AGC.comm('!C910 0')
				E_AGC.comm('!C904 0')
			variables.flag_pump_load_lock_click = False
			variables.flag_pump_load_lock = False
			variables.flag_pump_load_lock_led = False
			time.sleep(1)
		elif variables.flag_pump_load_lock_click and not variables.flag_pump_load_lock and status == 'load_lock':
			if conf['pump_ll'] == "on":
				E_AGC.comm('!C910 1')
				E_AGC.comm('!C904 1')
			variables.flag_pump_load_lock_click = False
			variables.flag_pump_load_lock = True
			variables.flag_pump_load_lock_led = True
			time.sleep(1)

		if variables.flag_pump_cryo_load_lock_click and variables.flag_pump_cryo_load_lock and status == 'cryo_load_lock':
			if conf['pump_cll'] == "on":
				E_AGC.comm('!C910 0')
				E_AGC.comm('!C904 0')
			variables.flag_pump_cryo_load_lock_click = False
			variables.flag_pump_cryo_load_lock = False
			variables.flag_pump_cryo_load_lock_led = False
			time.sleep(1)
		elif (variables.flag_pump_cryo_load_lock_click and not variables.flag_pump_cryo_load_lock and
		      status == 'cryo_load_lock'):
			if conf['pump_cll'] == "on":
				E_AGC.comm('!C910 1')
				E_AGC.comm('!C904 1')
			variables.flag_pump_cryo_load_lock_click = False
			variables.flag_pump_cryo_load_lock = True
			variables.flag_pump_cryo_load_lock_led = True
			time.sleep(1)

		if conf['COM_PORT_gauge_ll'] != "off" or conf['COM_PORT_gauge_cll'] != "off":
			if cmd == 'pressure':
				response_tmp = E_AGC.comm('?V911')
				response_tmp = float(response_tmp.replace(';', ' ').split()[1])

				if response_tmp < 90 and status == 'load_lock':
					variables.flag_pump_load_lock_led = False
				elif response_tmp >= 90 and status == 'load_lock':
					variables.flag_pump_load_lock_led = True
				if response_tmp < 90 and status == 'cryo_load_lock':
					variables.flag_pump_cryo_load_lock_led = False
				elif response_tmp >= 90 and status == 'cryo_load_lock':
					variables.flag_pump_cryo_load_lock_led = True
				response = E_AGC.comm('?V940')
			else:
				print('Unknown command for Edwards TIC Load Lock')
	except Exception as e:
		print(f"An error occurred: {e}")
		response = "Error"  # Set response to indicate an error

	return response


def initialize_cryovac(com_port_cryovac, variables):
	"""
	Initialize the communication port of Cryovac.

	Args:
		com_port_cryovac: Serial communication object.
		variables: Variables instance.

	Returns:
		None
	"""
	output = command_cryovac('getOutput', com_port_cryovac)
	time.sleep(0.1)
	variables.temperature = float(output.split()[0].replace(',', ''))


def initialize_edwards_tic_load_lock(conf, variables):
	"""
	Initialize TIC load lock parameters.

	Args:
		conf: Configuration parameters.
		variables: Variables instance.

	Returns:
		None
	"""

	E_AGC_ll = EdwardsAGC(variables.COM_PORT_gauge_ll)
	response = command_edwards(conf, variables, 'pressure', E_AGC=E_AGC_ll)
	variables.vacuum_load_lock = float(response.replace(';', ' ').split()[2]) * 0.01
	variables.vacuum_load_lock_backing = float(response.replace(';', ' ').split()[4]) * 0.01


def initialize_edwards_tic_cryo_load_lock(conf, variables):
	"""
	Initialize TIC cryo load lock parameters.

	Args:
		conf: Configuration parameters.
		variables: Variables instance.

	Returns:
		None
	"""
	E_AGC_cll = EdwardsAGC(variables.COM_PORT_gauge_cll)
	response = command_edwards(conf, variables, 'pressure', E_AGC=E_AGC_cll)
	variables.vacuum_cryo_load_lock = float(response.replace(';', ' ').split()[2]) * 0.01
	variables.vacuum_cryo_load_lock_backing = float(response.replace(';', ' ').split()[4]) * 0.01


def initialize_edwards_tic_buffer_chamber(conf, variables):
	"""
	Initialize TIC buffer chamber parameters.

	Args:
		conf: Configuration parameters.
		variables: Variables instance.

	Returns:
		None
	"""
	E_AGC_bc = EdwardsAGC(variables.COM_PORT_gauge_bc)
	response = command_edwards(conf, variables, 'pressure', E_AGC=E_AGC_bc)
	variables.vacuum_buffer_backing = float(response.replace(';', ' ').split()[2]) * 0.01


def initialize_pfeiffer_gauges(variables):
	"""
	Initialize Pfeiffer gauge parameters.

	Args:
		variables: Variables instance.

	Returns:
		None
	"""
	tpg = TPG362(port=variables.COM_PORT_gauge_mc)
	value, _ = tpg.pressure_gauge(2)
	variables.vacuum_main = '{}'.format(value)
	value, _ = tpg.pressure_gauge(1)
	variables.vacuum_buffer = '{}'.format(value)


def state_update(conf, variables, emitter):
	"""
	Read gauge parameters and update variables.

	Args:
		conf: Configuration parameters.
		variables: Variables instance.
		emitter: Emitter instance.

	Returns:
		None
	"""

	if conf['gauges'] == "on":
		if conf['COM_PORT_gauge_mc'] != "off":
			try:
				tpg = TPG362(port=variables.COM_PORT_gauge_mc)
			except Exception as e:
				print(f"Error initializing TPG362 on port {variables.COM_PORT_gauge_mc}: {e}")
				tpg = None

		if conf['COM_PORT_gauge_bc'] != "off":
			try:
				E_AGC_bc = EdwardsAGC(variables.COM_PORT_gauge_bc, variables)
			except Exception as e:
				print(f"Error initializing EdwardsAGC (BC) on port {variables.COM_PORT_gauge_bc}: {e}")
				E_AGC_bc = None

		if conf['COM_PORT_gauge_ll'] != "off":
			try:
				E_AGC_ll = EdwardsAGC(variables.COM_PORT_gauge_ll, variables)
			except Exception as e:
				print(f"Error initializing EdwardsAGC (LL) on port {variables.COM_PORT_gauge_ll}: {e}")
				E_AGC_ll = None

		if conf['COM_PORT_gauge_cll'] != "off":
			try:
				E_AGC_cll = EdwardsAGC(variables.COM_PORT_gauge_cll, variables)
			except Exception as e:
				print(f"Error initializing EdwardsAGC (CLL) on port {variables.COM_PORT_gauge_cll}: {e}")
				E_AGC_cll = None

	if conf['cryo'] == "off":
		print('The cryo temperature monitoring is off')
	else:
		try:
			com_port_cryovac = serial.Serial(
				port=variables.COM_PORT_cryo,
				baudrate=9600,
				bytesize=serial.EIGHTBITS,
				parity=serial.PARITY_NONE,
				stopbits=serial.STOPBITS_ONE
			)
			initialize_cryovac(com_port_cryovac, variables)
		except Exception as e:
			com_port_cryovac = None
			print('Can not initialize the cryovac')
			print(e)

		start_time = time.time()
		log_time_time_interval = conf['log_time_time_interval']
		vacuum_main = 'N/A'
		vacuum_buffer = 'N/A'
		vacuum_buffer_backing = 'N/A'
		vacuum_load_lock = 'N/A'
		vacuum_load_lock_backing = 'N/A'
		vacuum_cryo_load_lock = 'N/A'
		vacuum_cryo_load_lock_backing = 'N/A'
		set_temperature_tmp = 0
		while emitter.bool_flag_while_loop:
			if conf['cryo'] == "on":
				try:
					output = command_cryovac('getOutput', com_port_cryovac)
				except Exception as e:
					print(e)
					print("cannot read the cryo temperature")
					output = '0'
				try:
					temperature_stage = float(output.split()[0].replace(',', ''))
					temperature_cryo_head = float(output.split()[2].replace(',', ''))
				except Exception as e:
					print(e)
					# Handle the case where response is not a valid float
					temperature = -1
				variables.temperature = temperature_stage
				emitter.temp_stage.emit(temperature_stage)
				emitter.temp_cryo_head.emit(temperature_cryo_head)

				if variables.set_temperature != set_temperature_tmp:
					try:
						res = command_cryovac(f'Out1.PID.Setpoint {variables.set_temperature}', com_port_cryovac)
						set_temperature_tmp = variables.set_temperature
					except Exception as e:
						print(e)
						print("cannot set the cryo temperature")

			if conf['COM_PORT_gauge_mc'] != "off":
				value, _ = tpg.pressure_gauge(2)
				try:
					vacuum_main = '{}'.format(value)
				except Exception as e:
					print(f"Error reading Temperature:{e}")
					# Handle the case where response is not a valid float
					vacuum_main = -1
				variables.vacuum_main = vacuum_main
				emitter.vacuum_main.emit(float(vacuum_main))
				value, _ = tpg.pressure_gauge(1)
				try:
					vacuum_buffer = '{}'.format(value)
				except Exception as e:
					print(f"Error reading BC:{e}")
					# Handle the case where response is not a valid float
					vacuum_buffer = -1
				emitter.vacuum_buffer.emit(float(vacuum_buffer))
			if conf['pump_ll'] != "off":
				response = command_edwards(conf, variables, 'pressure', E_AGC=E_AGC_ll, status='load_lock')

				try:
					vacuum_load_lock = float(response.replace(';', ' ').split()[2]) * 0.01
				except Exception as e:
					print(f"Error reading LL:{e}")
					# Handle the case where response is not a valid float
					vacuum_load_lock = -1
				try:
					vacuum_load_lock_backing = float(response.replace(';', ' ').split()[4]) * 0.01
				except Exception as e:
					print(f"Error reading LL backing:{e}")
					# Handle the case where response is not a valid float
					vacuum_load_lock_backing = -1
				emitter.vacuum_load_lock.emit(vacuum_load_lock)
				emitter.vacuum_load_lock_back.emit(vacuum_load_lock_backing)
			if conf['pump_cll'] != "off":
				response = command_edwards(conf, variables, 'pressure', E_AGC=E_AGC_cll, status='cryo_load_lock')

				try:
					vacuum_cryo_load_lock = float(response.replace(';', ' ').split()[2]) * 0.01
				except Exception as e:
					print(f"Error reading CLL:{e}")
					# Handle the case where response is not a valid float
					vacuum_cryo_load_lock = -1
				try:
					vacuum_cryo_load_lock_backing = float(response.replace(';', ' ').split()[4]) * 0.01
				except Exception as e:
					print(f"Error reading CLL backing:{e}")
					# Handle the case where response is not a valid float
					vacuum_cryo_load_lock_backing = -1
				emitter.vacuum_cryo_load_lock.emit(vacuum_cryo_load_lock)
				emitter.vacuum_cryo_load_lock_back.emit(vacuum_cryo_load_lock_backing)

			if conf['COM_PORT_gauge_bc'] != "off":
				response = command_edwards(conf, variables, 'pressure', E_AGC=E_AGC_bc)
				try:
					vacuum_buffer_backing = float(response.replace(';', ' ').split()[2]) * 0.01
				except Exception as e:
					print(f"Error reading BC backing:{e}")
					# Handle the case where response is not a valid float
					vacuum_buffer_backing = -1
				variables.vacuum_buffer_backing = vacuum_buffer_backing
				emitter.vacuum_buffer_back.emit(vacuum_buffer_backing)

			elapsed_time = time.time() - start_time
			# Every 30 minutes, log the vacuum levels
			if elapsed_time > log_time_time_interval:
				start_time = time.time()
				try:
					log_vacuum_levels(vacuum_main, vacuum_buffer, vacuum_buffer_backing, vacuum_load_lock,
					                  vacuum_load_lock_backing, vacuum_cryo_load_lock, vacuum_cryo_load_lock_backing)
				except Exception as e:
					print(e)
					print("cannot log the vacuum levels")
			time.sleep(1)


def log_vacuum_levels(main_chamber, buffer_chamber, buffer_chamber_pre, load_lock, load_lock_pre,
                      cryo_load_lock, cryo_load_lock_pre):
	"""
	Log vacuum levels to a text file and a CSV file.

	Args:
		main_chamber (float): Vacuum level of the main chamber.
		buffer_chamber (float): Vacuum level of the buffer chamber.
		buffer_chamber_pre (float): Vacuum level of the buffer chamber backing pump.
		load_lock (float): Vacuum level of the load lock.
		load_lock_pre(float): Vacuum level of the load lock backing pump.
		cryo_load_lock (float): Vacuum level of the cryo load lock.
		cryo_load_lock_pre (float): Vacuum level of the cryo load lock backing pump.

	Returns:
		None

	"""

	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	with open("./files/vacuum_log.txt", "a") as log_file:
		log_file.write(f"{timestamp}: Main Chamber={main_chamber}, Buffer Chamber={buffer_chamber}, "
		               f"Buffer Chamber Pre={buffer_chamber_pre}, Load Lock={load_lock}, "
		               f"Load Lock Pre={load_lock_pre}, Cryo Load Lock={cryo_load_lock}, "
		               f"Cryo Load Lock Pre={cryo_load_lock_pre}\n")

	row = [timestamp, main_chamber, buffer_chamber, buffer_chamber_pre, load_lock, load_lock_pre, cryo_load_lock,
	       cryo_load_lock_pre]
	header = ["Timestamp", "Main Chamber", "Buffer Chamber", "Buffer Chamber Backing Pump", "Load Lock",
	          "Load Lock Backing", 'Cryo Load Lock', 'Cryo Load Lock Backing']

	try:
		with open("./files/vacuum_log.csv", 'r') as log_file:
			file_empty = not log_file.readline()
	except FileNotFoundError:
		file_empty = True

	# Write to CSV file
	with open("./files/vacuum_log.csv", "a", newline='') as log_file:
		csv_writer = csv.writer(log_file)

		# Write the header if the file is empty
		if file_empty:
			csv_writer.writerow(header)

		# Write the data row
		csv_writer.writerow(row)
