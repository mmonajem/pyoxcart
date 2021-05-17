import serial.tools.list_ports
import time
# get available COM ports and store as list
com_ports = list(serial.tools.list_ports.comports())

# get number of available COM ports
no_com_ports = len(com_ports)

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
        baudrate = 9600,                     # 115200
        bytesize= serial.EIGHTBITS,            # 8
        parity= serial.PARITY_NONE,            # N
        stopbits= serial.STOPBITS_ONE          # 1
    )

    if com_port.is_open:
        com_port.flushInput()
        com_port.flushOutput()
        print("Opened Port: " + com_ports[com_port_idx].device)


        # while the entered cmd wasn't "exit"
        while True:
            cmd = input(">>: ") # get the cmd to send

            if cmd == 'exit':   # leave loop
                break
            else:
                com_port.write((cmd + '\r\n').encode())  # send cmd to device # might not work with older devices -> "LF" only needed!
                time.sleep(0.001)                          # small sleep for response

            response = ''

            while com_port.in_waiting > 0:
                response = com_port.readline()           # all characters received, read line till '\r\n'

            if response != '':
                print("<<: " + response.decode("utf-8")) # decode bytes received to string
            else:
                print("<< Error, no Response!")


    else:
        print("Couldn't open Port!")
        exit()
    com_port.close()
else:
    print("No COM ports available!")
    exit()
