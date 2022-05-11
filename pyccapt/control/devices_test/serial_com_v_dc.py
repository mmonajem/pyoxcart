"""
This is the script for testing high voltage power supply FUG.
"""

##
 # @file serial_com.py
 #
 # @author Birkmaier Thomas
 #
 # @version v0.00
 #
 # @par Development System
 # - Hardware: --
 # - IDE     : Microsoft Visual Studio Code
 #
 # @brief Example program to send commands using a COM Port.
 #
 # @details How to use this example:
 #  - Use this link to set up Visual Studio Code for Python:
 #    https://code.visualstudio.com/docs/python/python-tutorial
 #  - Use information provided by this link to install pySerial library
 #  - Run this Python script
 #  - Program shows you available COM ports
 #  - Choose the port you want to send commands to
 #  - Example command ">S0 10.00"
 #  - Device responds "#0 >S0:1.000000E+1"
 #  - Example command ">S0?"
 #  - Device responds "#1 >S0:0.000000E+00"
 #  - Type "exit" to exit the program
 #
 # @note This is just an example to show how to create a connection. Be aware
 # that This is not production ready code!
 #
 # @copyright
 # THIS DOCUMENT/MEDIA IS THE PERSONAL PROPERTY OF FuG GMBH
 # AND WAS CREATED AND COPYRIGHTED BY FuG GMBH IN 2018. ALL
 # RIGHTS TO ITS USE ARE RESERVED.  THIS  MATERIAL  MAY NOT BE USED,
 # COPIED OR DISCLOSED  TO ANY THIRD PARTY WITHOUT THE PRIOR WRITTEN
 # AGREEMENT OF FuG GMBH. (c) 2019 FuG GMBH.
 #
 ##

# package needed to list available COM ports
import serial.tools.list_ports

# package needed for sleep
import time

# get available COM ports and store as list
com_ports = list(serial.tools.list_ports.comports())
print(com_ports)

# get number of available COM ports
no_com_ports = len(com_ports)

if __name__ == '__main__':
    # print out user information
    if no_com_ports > 0:
        print("Total no. of available COM ports: " + str(no_com_ports))

        # show all available COM ports
        for idx, curr in enumerate(com_ports):
            print("  " + str(idx) + ".)  " + curr.description)

        # user chooses COM port to connect to -> if wrong value entered, stay in loop
        while True:
            try:
                com_port_idx = int(input("Enter number of COM port to connect to (0 - " + str(no_com_ports - 1) + "): "))
            except:
                print("Incorrect value for COM port! Enter a Number (0 - " + str(no_com_ports - 1) + ")")
                continue
            else:
                if com_port_idx > no_com_ports or com_port_idx < 0:
                    continue
                break

        # configure the COM port to talk to. Default values: 115200,8,N,1
        com_port = serial.Serial(
            port = com_ports[com_port_idx].device, # chosen COM port
            baudrate = 115200,                     # 115200
            bytesize= serial.EIGHTBITS,            # 8
            parity= serial.PARITY_NONE,            # N
            stopbits= serial.STOPBITS_ONE          # 1
        )

        if com_port.is_open:
            com_port.flushInput()
            com_port.flushOutput()
            print("Opened Port: " + com_ports[com_port_idx].device)

            # while the entered cmd wasn't "exit"
            # while True:
            #     cmd = input(">>: ") # get the cmd to send
            #
            #     if cmd == 'exit':   # leave loop
            #         break
            #     else:
            #         com_port.write((cmd + '\r\n').encode())  # send cmd to device # might not work with older devices -> "LF" only needed!
            #         time.sleep(0.1)                          # small sleep for response
            #
            #     response = ''
            #
            #     while com_port.in_waiting > 0:
            #         response = com_port.readline()           # all characters received, read line till '\r\n'
            #
            #     if response != '':
            #         print("<<: " + response.decode("utf-8")) # decode bytes received to string
            #     else:
            #         print("<< Error, no Response!")

            def command(cmd):
                com_port.write(
                    (cmd + '\r\n').encode())  # send cmd to device # might not work with older devices -> "LF" only needed!
                time.sleep(0.001)  # small sleep for response
                response = ''

                while com_port.in_waiting > 0:
                    response = com_port.readline()  # all characters received, read line till '\r\n'

                if response != '':
                    print("<<: " + response.decode("utf-8"))  # decode bytes received to string
                else:
                    print("<< Error, no Response!")

            # cmd_list = [">S1 3.0e-4",">S0B 1", ">S0R 250", ">S0 15000", "F0", ">S0?", ">DON?",
            #             ">S0A?", "F1",]
            cmd_list = [">S1 3.0e-4"]
            for cmd in range(len(cmd_list)):
                command(cmd_list[cmd])
            for i in range(20):
                time.sleep(2)
                command(">S0A?")
                command(">S1A?")
            command('F0')

        else:
            print("Couldn't open Port!")
            exit()
        com_port.close()
    else:
        print("No COM ports available!")
        exit()
