"""
This is the script for testing signal generator.
"""

import pyvisa
import time

if __name__ == '__main__':
    resources = pyvisa.ResourceManager()
    print(resources.list_resources())

    device_resource = "USB0::0xF4EC::0x1101::SDG6XBAD2R0601::INSTR"

    wave_generator = resources.open_resource(device_resource)
    print(wave_generator.query('*IDN?')) # device model
    time.sleep(0.01)
    print(wave_generator.query('C1:OUTP?')) # Check channel 1 status
    time.sleep(0.01)
    print(wave_generator.write('C1:OUTP OFF')) # Turn off the channel 1
    time.sleep(0.01)
    print(wave_generator.write('C1:BSWV FRQ,200000')) # Set 200Khz frequency on the channel 1
    time.sleep(0.01)
    print(wave_generator.write('C1:BSWV DUTY,30')) # Set 30% duty cycle on the channel 1
    time.sleep(0.01)
    print(wave_generator.write('C1:BSWV RISE,0.000000002')) # Set 0.2ns rising edge  on the channel 1
    time.sleep(0.01)
    print(wave_generator.write('C1:BSWV DLY,0')) # Set 0 second delay on the channel 1
    time.sleep(0.01)
    print(wave_generator.write('C1:BSWV HLEV,5')) # Set 5b high level on the channel 1
    time.sleep(0.01)
    print(wave_generator.write('C1:BSWV LLEV,0')) # Set 0v low level on the channel 1
    time.sleep(0.01)
    print(wave_generator.write('C1:OUTP LOAD,50')) # Set 50 ohm load on the channel 1
    time.sleep(0.01)
    print(wave_generator.write('C1:OUTP ON')) # Turn on the channel 1