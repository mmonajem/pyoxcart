import pyccapt.thorlabs_apt as apt



print(apt.list_available_devices())

# motor = apt.Motor(27261754)
# motor.move_home(True)
# motor.move_by(45)
