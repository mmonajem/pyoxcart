"""
This is the main script is load the GUI base on the configuration file.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""


def init():

    global selected_x_fdm
    global selected_y_fdm
    global roi_fdm

    global selected_x1
    global selected_x2

    # List that stores mass/weights of added elements
    global listMaterial

    global peaks_idx

    global result_path
    global path


    selected_x_fdm = 0
    selected_y_fdm = 0
    roi_fdm = 0

    selected_x1 = 0
    selected_x2 = 0


    listMaterial = []

    peaks_idx = []

    result_path = ''
    path = ''
