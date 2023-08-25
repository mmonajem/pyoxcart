import pyvisa
import time

if __name__ == '__main__':
    # Initialize the pyvisa resource manager
    resources = pyvisa.ResourceManager()
    print(resources.list_resources())

    device_resource = "USB0::0xF4EC::0x1101::SDG6XBAD2R0601::INSTR"

    # Open communication with the waveform generator
    wave_generator = resources.open_resource(device_resource)

    # Print device information
    print(wave_generator.query('*IDN?'))  # Device model
    time.sleep(0.01)

    # Check channel 1 status
    print(wave_generator.query('C1:OUTP?'))
    time.sleep(0.01)

    # Turn off channel 1
    print(wave_generator.write('C1:OUTP OFF'))
    time.sleep(0.01)

    # Set frequency to 200 kHz on channel 1
    print(wave_generator.write('C1:BSWV FRQ,200000'))
    time.sleep(0.01)

    # Set duty cycle to 30% on channel 1
    print(wave_generator.write('C1:BSWV DUTY,30'))
    time.sleep(0.01)

    # Set rising edge to 0.2 ns on channel 1
    print(wave_generator.write('C1:BSWV RISE,0.000000002'))
    time.sleep(0.01)

    # Set 0 second delay on channel 1
    print(wave_generator.write('C1:BSWV DLY,0'))
    time.sleep(0.01)

    # Set high level to 5 V on channel 1
    print(wave_generator.write('C1:BSWV HLEV,5'))
    time.sleep(0.01)

    # Set low level to 0 V on channel 1
    print(wave_generator.write('C1:BSWV LLEV,0'))
    time.sleep(0.01)

    # Set 50 ohm load on channel 1
    print(wave_generator.write('C1:OUTP LOAD,50'))
    time.sleep(0.01)

    # Turn on channel 1
    print(wave_generator.write('C1:OUTP ON'))

    # Close communication with the waveform generator
    wave_generator.close()
