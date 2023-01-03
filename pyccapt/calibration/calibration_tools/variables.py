"""
This is the main script for global variables.
"""
import numpy as np
from ipywidgets import widgets

def init():

    global selected_x_fdm
    global selected_y_fdm
    global roi_fdm

    global selected_x1
    global selected_x2
    global selected_y1
    global selected_y2

    # List that stores mass/weights of added elements
    global listMaterial
    global charge
    global element
    global isotope

    global peaks_idx

    global result_path
    global path

    global dld_t_calib
    global dld_t_calib_backup
    global mc_calib
    global mc_calib_backup
    global max_peak
    global peak
    global peak_y
    global peak_width


    selected_x_fdm = 0
    selected_y_fdm = 0
    roi_fdm = 0

    selected_x1 = 0
    selected_x2 = 0
    selected_y1 = 0
    selected_y2 = 0


    listMaterial = []
    charge = []
    element = []
    isotope = []

    peaks_idx = []

    result_path = ''
    path = ''

    dld_t_calib = np.zeros(0)
    dld_t_calib_backup = np.zeros(0)
    mc_calib = np.zeros(0)
    mc_calib_backup = np.zeros(0)
    max_peak = 0
    peak = []
    peak_y = []
    peak_width = []
