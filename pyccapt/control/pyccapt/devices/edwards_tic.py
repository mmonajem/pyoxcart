"""
This is the main script for Reading the Edward gauges.
"""

import serial

from pyccapt.control_tools import loggi



class EdwardsAGC(object):
    """
    Primitive driver for Edwards Active Gauge Controller
    Complete manual found at
    http://www.idealvac.com/files/brochures/Edwards_AGC_D386-52-880_IssueM.pdf 
    """

    def __init__(self, port):
        """
        The constructor function to initialze serial lib parameters

        Attributes:
            port: Port on which serial communication to established
        Returns:
            Does not return anything
        """
        self.port = port
        self.serial = serial.Serial(self.port, baudrate=9600, timeout=0.5)

        self.log_edwards_tic = loggi.logger_creator('edwards_tic', 'edwards_tic.log')


    def comm(self, command):
        """ 
        This class method implements a serial communication using the serial library.
        Reads and the raw data through and returns it.

        Attributes:
            command: command to be written on serial line
        Returns:
            Returns the string read through serial 

        """
        comm = command + "\r\n"
        self.log_edwards_tic.info("Function - comm | Command - > {} | type -> {} ".format(command,type(command)))
        self.log_edwards_tic.info("Function - comm | Comm - > {}".format(comm))
        self.serial.write(comm.encode())
        complete_string = self.serial.readline().decode()
        complete_string = complete_string.strip()
        self.log_edwards_tic.info("Function - comm | Response - > {}".format(complete_string))
        return complete_string
