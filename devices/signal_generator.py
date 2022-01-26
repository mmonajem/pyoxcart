import pyvisa
import time


'''
Documentation: pyvisa
PyVISA is a Python package that enables you to control all kinds 
of measurement devices independently of the interface 
(e.g. GPIB, RS232, USB, Ethernet). 

Module reference: "https://pyvisa.readthedocs.io/en/latest/"

'''



def initialize_signal_generator(freq):
    '''
    This function initializes the  signal generator fucntionality by utlizing pyvisa module

    Atrributes:
        freq: frequency at which signal need to generated
    Returns:
        Does not return anything
    
    '''

    resources = pyvisa.ResourceManager()

    freq1_command = 'C1:BSWV FRQ,%s' % (freq * 1000)

    freq2_command = 'C2:BSWV FRQ,%s' % (freq * 1000)

    device_resource = "USB0::0xF4EC::0x1101::SDG6XBAD2R0601::INSTR"

    wave_generator = resources.open_resource(device_resource)

    wave_generator.write('C1:OUTP OFF') # Turn off the channel 1
    time.sleep(0.01)
    wave_generator.write(freq1_command) # Set output frequency on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:BSWV DUTY,30') # Set 30% duty cycle on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:BSWV RISE,0.000000002') # Set 0.2ns rising edge  on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:BSWV DLY,0') # Set 0 second delay on the channel 1
    time.sleep(0.01)
    wave_generator.write('C1:BSWV HLEV,5') # Set 5b high level on the channel 1
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
    wave_generator.write('C2:BSWV DUTY,30')  # Set 30% duty cycle on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:BSWV RISE,0.000000002')  # Set 0.2ns rising edge  on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:BSWV DLY,0') # Set 0 second delay on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:BSWV HLEV,5')  # Set 5b high level on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:BSWV LLEV,0')  # Set 0v low level on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:OUTP LOAD,50')  # Set 50 ohm load on the channel 2
    time.sleep(0.01)
    wave_generator.write('C2:OUTP ON') # Turn on the channel 1

def turn_off_signal_generator():

    '''
    This function stops the signal generator fucntionality by utlizing pyvisa module.
    Turns off the channels in use.

    Atrributes:
        Does not return anything
    Returns:
        Does not return anything
    
    '''

    resources = pyvisa.ResourceManager()

    device_resource = "USB0::0xF4EC::0x1101::SDG6XBAD2R0601::INSTR"

    wave_generator = resources.open_resource(device_resource)

    wave_generator.write('C2:OUTP OFF')  # Turn off the channel 2
    time.sleep(0.01)
    wave_generator.write('C1:OUTP OFF') # Turn off the channel 1
    time.sleep(0.01)

