import serial

# Example Program using the control object
# Version 1.1

# Author Ian Baker

if __name__ == "__main__":
	# Customise your comport to your Origami address
	comPort = "COM9"

	# Open the port
	ser = serial.Serial(
		port=comPort,
		baudrate=38400,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		rtscts=False,
		timeout=1
	)

	# Command to be sent
	cmd = "ly_oxp2_nktpbus=1\n"

	try:
		# Write the command to the serial port
		ser.write(cmd.encode())

		# Read and print the response
		response = ser.readline().decode("utf-8")
		print("Response:", response)

	except Exception as e:
		print("Exception:", e)
	except serial.SerialException as e:
		print("Error: ", e)

	finally:
		# Close the serial port
		ser.close()
