import time
import serial.tools.list_ports

from pfeiffer_gauges import TPG362
from edwards_tic import EdwardsAGC
import variables

# get available COM ports and store as list
com_ports = list(serial.tools.list_ports.comports())

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

# apply command to the Cryovac
def command_cryovac(cmd, com_port_cryovac):
    com_port_cryovac.write(
        (cmd + '\r\n').encode())  # send cmd to device # might not work with older devices -> "LF" only needed!
    time.sleep(0.1)  # small sleep for response
    response = ''
    while com_port_cryovac.in_waiting > 0:
        response = com_port_cryovac.readline()  # all characters received, read line till '\r\n'
    return response.decode("utf-8")

def command_edwards(cmd, lock, E_AGC, status=None):
    if variables.flag_pump_load_lock_click and variables.flag_pump_load_lock and status == 'load_lock':
        E_AGC.comm('!C910 0')  # Backing Pump off
        E_AGC.comm('!C904 0')  # Turbo Pump off
        with lock:
            variables.flag_pump_load_lock_click = False
            variables.flag_pump_load_lock = False
            variables.flag_pump_load_lock_led = False
            time.sleep(1)
    elif variables.flag_pump_load_lock_click and not variables.flag_pump_load_lock and status == 'load_lock':
        E_AGC.comm('!C910 1')  # Backing Pump on
        E_AGC.comm('!C904 1')  # Turbo Pump on
        with lock:
            variables.flag_pump_load_lock_click = False
            variables.flag_pump_load_lock = True
            variables.flag_pump_load_lock_led = True
            time.sleep(1)
    if cmd == 'presure':
        response_tmp = E_AGC.comm('?V911')
        response_tmp = float(response_tmp.replace(';', ' ').split()[1])
        if response_tmp < 90 and status == 'load_lock':
            variables.flag_pump_load_lock_led = False
        elif response_tmp >= 90 and status == 'load_lock':
            variables.flag_pump_load_lock_led = True
        response = E_AGC.comm('?V940')
    else:
        print('Unknown command for Edwards TIC Load Lock')

    return response

def initialize_cryovac(com_port_cryovac):
    # Setting the com port of Cryovac
    output = command_cryovac('getOutput', com_port_cryovac)
    variables.temperature = float(output.split()[0].replace(',', ''))

def initialize_edwards_tic_load_lock():
    E_AGC_ll = EdwardsAGC(variables.COM_PORT_edwards_ll)
    response = command_edwards('presure', lock=None, E_AGC=E_AGC_ll)
    variables.vacuum_load_lock = float(response.replace(';', ' ').split()[2]) * 0.01
    variables.vacuum_load_lock_backing = float(response.replace(';', ' ').split()[4]) * 0.01

def initialize_edwards_tic_buffer_chamber():
    E_AGC_bc = EdwardsAGC(variables.COM_PORT_edwards_bc)
    response = command_edwards('presure', lock=None, E_AGC=E_AGC_bc, )
    variables.vacuum_buffer_backing = float(response.replace(';', ' ').split()[2]) * 0.01

def initialize_pfeiffer_gauges():
    """
    The function for initializing Pfeiffer gauge
    """
    tpg = TPG362(port=variables.COM_PORT_pfeiffer)
    value, _ = tpg.pressure_gauge(2)
    # unit = tpg.pressure_unit()
    variables.vacuum_main = '{}'.format(value)
    value, _ = tpg.pressure_gauge(1)
    # unit = tpg.pressure_unit()
    variables.vacuum_buffer = '{}'.format(value)

def gauges_update(lock, com_port_cryovac):
    """
    The function for reading gauges
    """
    tpg = TPG362(port=variables.COM_PORT_pfeiffer)
    E_AGC_ll = EdwardsAGC(variables.COM_PORT_edwards_ll)
    E_AGC_bc = EdwardsAGC(variables.COM_PORT_edwards_bc)
    while True:
        #  Temperature update
        output = command_cryovac('getOutput', com_port_cryovac)
        with lock:
            variables.temperature = float(output.split()[0].replace(',', ''))
        # Pfeiffer gauges update
        value, _ = tpg.pressure_gauge(2)
        # unit = tpg.pressure_unit()
        with lock:
            variables.vacuum_main = '{}'.format(value)
        value, _ = tpg.pressure_gauge(1)
        # unit = tpg.pressure_unit()
        with lock:
            variables.vacuum_buffer = '{}'.format(value)
        # Edwards Load Lock update
        response = command_edwards('presure', lock, E_AGC=E_AGC_ll, status='load_lock')
        with lock:
            variables.vacuum_load_lock = float(response.replace(';', ' ').split()[2]) * 0.01
            variables.vacuum_load_lock_backing = float(response.replace(';', ' ').split()[4]) * 0.01

        # Edwards Buffer Chamber update
        response = command_edwards('presure', lock, E_AGC=E_AGC_bc)
        with lock:
            variables.vaccum_buffer_backing = float(response.replace(';', ' ').split()[2]) * 0.01
        time.sleep(1)
