Setting the JSON file
======================================
To run the GUI, you need to set the JSON file.
The JSON file is a Python dictionary that contains the following keys:


.. figure:: json.jpg

Visualization
-----------------
The GUI will show tof or mass-to-charge ratio. You can choose
tof or mc. There is also some constant parameters like flight path length, max of DC voltage and etc. that should be
specified int he JSON file.

Devices
-----------------
The parameters from tdc to edge_counter is all the devices you want to control. you can
turn on or off the devices with the command.


ports
-----------------
All the parameters which start with COM are the serial ports of the devices. you can run the
com_port.py script from tools folder to print out all the available serial ports. Then
you should passing each port to the corresponding device. It is also possible to test all the devices
separately with scripts in devices_test module.



