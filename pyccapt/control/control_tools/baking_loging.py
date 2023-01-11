# from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

from mcculw import ul
from mcculw.enums import InfoType, BoardInfo, AiChanType, TcType, TempScale, TInOptions
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime
import pandas as pd
import numpy as np
from threading import Thread
"""
This module contains drivers for the following equipment from Pfeiffer
Vacuum:
* TPG 262 and TPG 261 Dual Gauge. Dual-Channel Measurement and Control
    Unit for Compact Gauges
"""

import time
import serial

# Code translations constants
MEASUREMENT_STATUS = {
    0: 'Measurement data okay',
    1: 'Underrange',
    2: 'Overrange',
    3: 'Sensor error',
    4: 'Sensor off (IKR, PKR, IMR, PBR)',
    5: 'No sensor (output: 5,2.0000E-2 [mbar])',
    6: 'Identification error'
}
GAUGE_IDS = {
    'TPR': 'Pirani Gauge or Pirani Capacitive gauge',
    'IKR9': 'Cold Cathode Gauge 10E-9 ',
    'IKR11': 'Cold Cathode Gauge 10E-11 ',
    'PKR': 'FullRange CC Gauge',
    'PBR': 'FullRange BA Gauge',
    'IMR': 'Pirani / High Pressure Gauge',
    'CMR': 'Linear gauge',
    'noSEn': 'no SEnsor',
    'noid': 'no identifier'
}
PRESSURE_UNITS = {0: 'mbar/bar', 1: 'Torr', 2: 'Pascal'}


class TPG26x(object):
    r"""Abstract class that implements the common driver for the TPG 261 and
    TPG 262 dual channel measurement and control unit. The driver implements
    the following 6 commands out the 39 in the specification:
    * PNR: Program number (firmware version)
    * PR[1,2]: Pressure measurement (measurement data) gauge [1, 2]
    * PRX: Pressure measurement (measurement data) gauge 1 and 2
    * TID: Transmitter identification (gauge identification)
    * UNI: Pressure unit
    * RST: RS232 test
    This class also contains the following class variables, for the specific
    characters that are used in the communication:
    :var ETX: End text (Ctrl-c), chr(3), \\x15
    :var CR: Carriage return, chr(13), \\r
    :var LF: Line feed, chr(10), \\n
    :var ENQ: Enquiry, chr(5), \\x05
    :var ACK: Acknowledge, chr(6), \\x06
    :var NAK: Negative acknowledge, chr(21), \\x15
    """

    ETX = chr(3)  # \x03
    CR = chr(13)
    LF = chr(10)
    ENQ = chr(5)  # \x05
    ACK = chr(6)  # \x06
    NAK = chr(21)  # \x15

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        """
        The constructor class method which initialize internal variables and
        serial connection

        Attributes:
            param port: The COM port to open. See the documentation for
                `pyserial <http://pyserial.sourceforge.net/>`_ for an explanation
                of the possible value. The default value is '/dev/ttyUSB0'.
                :type port: [str or int]
            baud-rate: Data transmission rate (9600, 19200, 38400 where 9600 is the default)
                :type baudrate: [int]
        """

        # The serial connection should be setup with the following parameters:
        # 1 start bit, 8 data bits, No parity bit, 1 stop bit, no hardware
        # handshake. These are all default for Serial and therefore not input
        # below
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1)

    def _cr_lf(self, string):
        """
        Pad carriage return and line feed to a string

        Attributes:
            string: String to pad [str]

        Returns:
            string : the padded string [string]
        """
        return string + self.CR + self.LF

    def _send_command(self, command):
        """
        Send a command and check if it is positively acknowledged

        Attributes:

            command: The command to be sent [str]

        Raises Exception:
            raises IOError: if the negative acknowledged or an unknown response
            is returned
        Returns:
            Does not return anything

        """
        # Write (execute command) through serial communication
        self.serial.write(self._cr_lf(command).encode())
        response = self.serial.readline().decode()
        if response == self._cr_lf(self.NAK):
            message = 'Serial communication returned negative acknowledge'
            raise IOError(message)
        elif response != self._cr_lf(self.ACK):
            message = 'Serial communication returned unknown response:\n{}' \
                      ''.format(repr(response))
            raise IOError(message)

    def _get_data(self):
        """
        Get the data that is ready on the device

        Attributes:
            Does not accept any arguments

        Returns:
            data: raw data from serial communication line [str]
        """
        self.serial.write(self.ENQ.encode())
        data = self.serial.readline().decode()
        return data.rstrip(self.LF).rstrip(self.CR)

    def _clear_output_buffer(self):
        """
        Clear the output buffer
        """

        time.sleep(0.1)
        just_read = 'start value'
        out = ''
        while just_read != '':
            just_read = self.serial.read()
            out += just_read
        return out

    def program_number(self):
        """
        Return the firmware version

        Attributes:
            Does not accept any arguments

        Returns:
            :the firmware version [str]
        """

        self._send_command('PNR')
        return self._get_data()

    def pressure_gauge(self, gauge=1):
        """
        Return the pressure measured by gauge X

        Attributes:
            gauge: The gauge number, 1 or 2 [int]
        Raises Exception:
            :raises ValueError: if gauge is not 1 or 2

        Returns:
            :a tuple the value of pressure along with status code and message
                (value, (status_code, status_message)) [tuple]
        """

        if gauge not in [1, 2]:
            message = 'The input gauge number can only be 1 or 2'
            raise ValueError(message)
        self._send_command('PR' + str(gauge))
        reply = self._get_data()
        status_code = int(reply.split(',')[0])
        value = float(reply.split(',')[1])
        return value, (status_code, MEASUREMENT_STATUS[status_code])

    def pressure_gauges(self):
        """
        Return the pressures measured by the gauges

        Attributes:
            Does not accept any arguments

        Returns:
            :(value1, (status_code1, status_message1), value2,
                (status_code2, status_message2)) [tuple]
        """
        self._send_command('PRX')
        reply = self._get_data()
        # The reply is on the form: x,sx.xxxxEsxx,y,sy.yyyyEsyy
        status_code1 = int(reply.split(',')[0])
        value1 = float(reply.split(',')[1])
        status_code2 = int(reply.split(',')[2])
        value2 = float(reply.split(',')[3])
        return (value1, (status_code1, MEASUREMENT_STATUS[status_code1]),
                value2, (status_code2, MEASUREMENT_STATUS[status_code2]))

    def gauge_identification(self):
        """
        Return the gauge identification

        Attributes:
            Does not accept any arguments

        Returns:
            :(id_code_1, id_1, id_code_2, id_2) [tuples]

        """
        self._send_command('TID')
        reply = self._get_data()
        id1, id2 = reply.split(',')
        return id1, GAUGE_IDS[id1], id2, GAUGE_IDS[id2]

    def pressure_unit(self):
        """
        Return the pressure unit

        Attributes:
            Does not accept any arguments

        Returns:
            :the pressure unit [str]
        """

        self._send_command('UNI')
        unit_code = int(self._get_data())
        return PRESSURE_UNITS[unit_code]

    def rs232_communication_test(self):
        """
        This function tests the RS232 communication.
        Attributes:

            Does not accept any arguments

        Returns:
            :the status of the communication test [boolean]
        """

        # reset serial communication
        self._send_command('RST')
        self.serial.write(self.ENQ)
        # Clear output buffer
        self._clear_output_buffer()
        test_string_out = ''
        # Test serial communication
        for char in 'a1':
            self.serial.write(char)
            test_string_out += self._get_data().rstrip(self.ENQ)
        self._send_command(self.ETX)
        return test_string_out == 'a1'


class TPG362(TPG26x):
    """Driver for the TPG 261 dual channel measurement and control unit"""

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        """
        This construction method initializes internal variables and serial connection.

        Attributes:

            port: The COM port to open. See the documentation for
                `pyserial <http://pyserial.sourceforge.net/>`_ for an explanation
                of the possible value. The default value is '/dev/ttyUSB0'. [str or int]

            baud-rate: data transmission rate (9600, 19200, 38400 where 9600 is the default) [int]
        """
        super(TPG362, self).__init__(port=port, baudrate=baudrate)


def daq_tc():
    device_to_show = "USB-TC"
    board_num = 0

    # Verify board is Board 0 in InstaCal.  If not, show message...
    print("Looking for Board 0 in InstaCal to be {0} series...".format(device_to_show))

    try:
        # Get the devices name...
        board_name = ul.get_board_name(board_num)

    except Exception as e:
        if ul.ErrorCode(1):
            # No board at that number throws error
            print("\nNo board found at Board 0.")
            print(e)
            return

    else:
        if device_to_show in board_name:
            # Board 0 is the desired device...
            print("{0} found as Board number {1}.\n".format(board_name, board_num))
            ul.flash_led(board_num)

        else:
            # Board 0 is NOT desired device...
            print("\nNo {0} series found as Board 0. Please run InstaCal.".format(device_to_show))
            return

    try:
        # select a channel
        channel = 1
        # Set thermocouple type to type K
        ul.set_config(
            InfoType.BOARDINFO, board_num, channel, BoardInfo.CHANTCTYPE,
            TcType.K)
        # Set the temperature scale to Fahrenheit
        ul.set_config(
            InfoType.BOARDINFO, board_num, channel, BoardInfo.TEMPSCALE,
            TempScale.CELSIUS)
        # Set data rate to 60Hz
        ul.set_config(
            InfoType.BOARDINFO, board_num, channel, BoardInfo.ADDATARATE, 60)

        # Read data from the channel:
        # channel_list = ['MC_NEG', 'MC_Det', 'Mc-Top', 'MC-Gate', 'BC-Top', 'BC-Pump']
        # for i in range(6):
        #
        #     options = TInOptions.NOFILTER
        #     value_temperature = ul.t_in(board_num, i, TempScale.CELSIUS, options)
        #     print("Channel{:d} - {:s}:  {:.3f} Degrees.".format(i, channel_list[i], value_temperature))

    except Exception as e:
        print('\n', e)

def read():
    # daq_tc()
    tpg = TPG362(port='COM5')
    unit = tpg.pressure_unit()

    # create the pandas data frame

    index = 0
    while True:
        print('-----------', index, 'seconds', '--------------')
        gauge_bc, _ = tpg.pressure_gauge(1)
        # print('pressure BC is {} {}'.format(gauge_bc, unit))

        gauge_mc, _ = tpg.pressure_gauge(2)
        # print('pressure MC is {} {}'.format(gauge_mc, unit))

        board_num = 0
        channel_list = ['MC_NEG', 'MC_Det', 'Mc_Top', 'MC_Gate', 'BC_Top', 'BC_Pump']
        value_temperature = []
        for i in range(6):
            options = TInOptions.NOFILTER
            val = float(ul.t_in(board_num, i, TempScale.CELSIUS, options))
            value_temperature.append(round(val, 3))
            # print("Channel{:d} - {:s}:  {:.3f} Degrees.".format(i, channel_list[i], value_temperature[i]))
        value_temperature = np.array(value_temperature, dtype=np.dtype(float))

        new_row = [now.strftime("%d-%m-%Y"), datetime.now().strftime('%H:%M:%S'), gauge_mc, gauge_bc,
                   value_temperature[0], value_temperature[1], value_temperature[2],
                   value_temperature[3], value_temperature[4], value_temperature[5]]

        data.loc[len(data)] = new_row

        time.sleep(0.5)
        index = index + 1
        if index % 20 == 0:
            try:
                data.to_csv(file_name, sep=';', index=False)
            except:
                data.to_csv(file_name_backup, sep=';', index=False)
                print('csv File cannot be saved')
                print('close the csv file')

def animate(i,):
    time = data['Time'].to_numpy()
    MC_NEG = data['MC_NEG'].to_numpy()
    MC_Det = data['MC_Det'].to_numpy()
    Mc_Top = data['Mc_Top'].to_numpy()
    MC_Gate = data['MC_Gate'].to_numpy()
    BC_Top = data['BC_Top'].to_numpy()
    BC_Pump = data['BC_Pump'].to_numpy()
    MC_vacuum = data['MC_vacuum'].to_numpy()
    BC_vacuum = data['BC_vacuum'].to_numpy()

    ax1.clear()
    ax2.clear()

    ax1.plot(time[-20:], MC_NEG[-20:], label='MC_NEG', color='b')
    ax1.plot(time[-20:], MC_Det[-20:], label='MC_Det', color='g')
    ax1.plot(time[-20:], Mc_Top[-20:], label='Mc_Top', color='r')
    ax1.plot(time[-20:], MC_Gate[-20:], label='MC_Gate', color='c')
    ax1.plot(time[-20:], BC_Top[-20:], label='BC_Top', color='m')
    ax1.plot(time[-20:], BC_Pump[-20:], label='BC_Pump', color='y')

    ax2.plot(time[-20:], MC_vacuum[-20:], label='MC_vacuum', color='orange')
    ax2.plot(time[-20:], BC_vacuum[-20:], label='BC_vacuum', color='darkviolet')

    ax1.set_title('Baking Temperature')
    ax2.set_title('Baking Vacuum')

    ax1.set_ylabel('Temperature (C)')
    ax2.set_ylabel('Vacuum (mbar)')

    ax1.legend(loc='upper right')
    ax2.legend(['MC_vacuum', 'BC_vacuum'], loc='upper right')


style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)


if __name__ == '__main__':
    # datetime object containing current date and time
    now = datetime.now()
    now_time = now.strftime("%d-%m-%Y_%H-%M-%S")
    global file_name
    file_name = 'baking_loging_%s.csv' % now_time
    global file_name_backup
    file_name_backup = 'backup_baking_loging_%s.csv' % now_time
    global data
    data = pd.DataFrame(
        columns=['data','Time', 'MC_vacuum', 'BC_vacuum', 'MC_NEG', 'MC_Det', 'Mc_Top', 'MC_Gate', 'BC_Top', 'BC_Pump'])



    thread_read = Thread(target=read)
    thread_read.daemon = True
    thread_read.start()

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

    try:
        data.to_csv(file_name, sep=';', index=False)
    except:
        data.to_csv(file_name_backup, sep=';', index=False)



