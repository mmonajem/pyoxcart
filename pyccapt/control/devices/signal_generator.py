"""
This is the main script for initializing and controlling signal generator.
"""

import time

import pyvisa


# Local module and scripts


def initialize_signal_generator(variables, freq):
    """
    This function initializes the  signal generator functionality by utilizing pyvisa module

    Attributes:
        freq: frequency at which signal need to generated

    Returns:
        Does not return anything

    """

    resources = pyvisa.ResourceManager()

    freq1_command = 'C1:BSWV FRQ,%s' % (freq * 1000)

    freq2_command = 'C2:BSWV FRQ,%s' % (freq * 1000)

    device_resource = variables.COM_PORT_signal_generator

    wave_generator = resources.open_resource(device_resource)

    wave_generator.write('C1:OUTP OFF') # Turn off the channel 1
    time.sleep(0.01)
    wave_generator.write(freq1_command) # Set output frequency on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:BSWV DUTY,1') # Set 30% duty cycle on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:BSWV RISE,0.000000002') # Set 0.2ns rising edge  on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:BSWV DLY,0') # Set 0 second delay on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:BSWV HLEV,5') # Set 5v high level on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:BSWV LLEV,0') # Set 0v low level on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:OUTP LOAD,50') # Set 50 ohm load on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:OUTP ON')# Turn on the channel 1

    wave_generator.write('C2:OUTP OFF')  # Turn off the channel 2
    time.sleep(0.01)
    wave_generator.write(freq2_command)  # Set output frequency on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:BSWV DUTY,1')  # Set 30% duty cycle on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:BSWV RISE,0.000000002')  # Set 0.2ns rising edge  on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:BSWV DLY,0') # Set 0 second delay on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:BSWV HLEV,5')  # Set 5v high level on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:BSWV LLEV,0')  # Set 0v low level on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:OUTP LOAD,50')  # Set 50 ohm load on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:OUTP ON') # Turn on the channel 1


def turn_off_signal_generator():

    """
    This function stops the signal generator functionality by utilizing pyvisa module.
    Turns off the channels in use.

    Attributes:
        Does not return anything

    Returns:
        Does not return anything

    """

    resources = pyvisa.ResourceManager()

    device_resource = "USB0::0xF4EC::0x1101::SDG6XBAD2R0601::INSTR"

    wave_generator = resources.open_resource(device_resource)

    wave_generator.write('C2:OUTP OFF')  # Turn off the channel 2
    time.sleep(0.01)
    wave_generator.write('C1:OUTP OFF') # Turn off the channel 1
    time.sleep(0.01)

