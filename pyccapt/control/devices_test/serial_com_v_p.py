import time
import pyvisa

if __name__ == '__main__':
    # Initialize the pyvisa resource manager
    resources = pyvisa.ResourceManager('@py')
    print(resources.list_resources())

    # Open the communication with the instrument
    v_p = resources.open_resource('ASRL4::INSTR')

    # Return the Rigol's ID string to identify the instrument
    print(v_p.query('*IDN?'))
    print(v_p.query('SYST:LOCK:OWN?'))

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
