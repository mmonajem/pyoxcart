import serial

class EdwardsAGC(object):
    """ Primitive driver for Edwards Active Gauge Controler
    Complete manual found at
    http://www.idealvac.com/files/brochures/Edwards_AGC_D386-52-880_IssueM.pdf """


    def __init__(self, port='COM1'):
        self.serial = serial.Serial(port, baudrate=9600, timeout=0.5)


    def comm(self, command):
        """ Implements basic communication """
        comm = command + "\r\n"
        self.serial.write(comm.encode())
        complete_string = self.serial.readline().decode()
        complete_string = complete_string.strip()
        return complete_string

# if __name__ == '__main__':
#     E_AGC = EdwardsAGC()
#
#     print(E_AGC.comm('?V913'))
#     print(E_AGC.comm('?S929'))  # unit of pressure
#     # print(E_AGC.comm('!C933 1'))         # Turbo pump On 1 and Off 0
