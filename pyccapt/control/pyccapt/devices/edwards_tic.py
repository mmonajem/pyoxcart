"""
This is the main script for Reading the Edward gauges.
"""


import serial
import logging



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

        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', 
                              '%m-%d-%Y %H:%M:%S')
        file_handler = logging.FileHandler('edwards_tic.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

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
        self.log.info("Function - comm | Command - > {}".format(command))
        self.log.info("Function - comm | Comm - > {}".format(comm))
        self.serial.write(comm.encode())
        complete_string = self.serial.readline().decode()
        complete_string = complete_string.strip()
        self.log.info("Function - comm | Response - > {}".format(complete_string))
        return complete_string
