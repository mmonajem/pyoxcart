from pyccapt.control.nkt_photonics import origamiClassCLI

# Customise your comport to your Origami address
comPort = "COM9"

origami = origamiClassCLI.origClass(comPort)
origami.open_port()

# Set the laser into standby mode
# databack = origami.Standby()
# print(databack)

# put in Interbus mode. if you want use the company GUI you have to run the below command. After that you can use the GUI
# BNut the CLI commands are not working anymore
# You have to reactivate the CLI mode from the company GUI
dataBack = origami.InterbusEnable()
print(dataBack)
