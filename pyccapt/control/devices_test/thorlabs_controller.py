"""
This is the main vew script for controlling Thorlab motors .
"""

import multiprocessing
import time


def thorlab(degree, initialize=False):
    """
    Initialize the Thorlab controller and set it to zero degree
    """
    import thorlabs_apt.core as apt
    motor = apt.Motor(27261754)
    if initialize:
        motor.move_home(True)
    else:
        motor.move_by(degree*2, blocking=True)
        time.sleep(3)
        motor.move_to(degree, blocking=True)






if __name__ == '__main__':



    # import pyccapt.thorlabs_apt.core as apt
    # print(apt.list_available_devices())
    #
    # motor = apt.Motor(27261754)
    # motor.move_home(True)
    # motor.move_by(10)

    # thread = threading.Thread(target=thorlab, args=(10, True))
    # thread.start()
    # thread.join()

    process = multiprocessing.Process(target=thorlab, args=(10, True))
    process.start()
    process.join()

    process = multiprocessing.Process(target=thorlab, args=(10, False))
    process.start()
    process.join()


