"""
This is the main script is load the GUI base on the configuration file.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""
import visa
import time
from pyvisa import constants

resources = visa.ResourceManager('@py')
print(resources.list_resources())
# v_p = resources.open_resource('ASRL4::INSTR', baud_rate=9600, data_bits=8, parity=constants.Parity.none, stop_bits=constants.StopBits.one, write_termination="\n", read_termination="\n")
v_p = resources.open_resource('ASRL4::INSTR')
#Return the Rigol's ID string to tell us it's there
print(v_p.query('*IDN?'))
print(v_p.query('SYST:LOCK:OWN?'))


# v_p.write('SYST:LOCK:STATE 1')
if __name__ == '__main__':
    try:
        v_p.query('*RST')
    except:

        v_p.write('VOLT 0')
        print(v_p.query('VOLT?'))


        v_p.write('VOLT 15')
        print(v_p.query('VOLT?'))
        time.sleep(5)

        v_p.write('OUTPut ON')
        time.sleep(5)

        print(v_p.query('VOLT?'))
        time.sleep(5)

        v_p.write('OUTPut OFF')


        v_p.close()

