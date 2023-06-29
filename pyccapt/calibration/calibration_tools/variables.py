import numpy as np


# def init():
#
#     global selected_x_fdm
#     global selected_y_fdm
#     global roi_fdm
#
#     global selected_calculated
#     global selected_x1
#     global selected_x2
#     global selected_y1
#     global selected_y2
#     global selected_z1
#     global selected_z2
#
#     # List that stores mass/weights of added elements
#     global listMaterial
#     global charge
#     global element
#     global isotope
#
#     global peaks_idx
#
#     global result_path
#     global path
#
#     global dld_t_calib
#     global dld_t_calib_backup
#     global mc_calib
#     global mc_calib_backup
#     global max_peak
#     global peak
#     global peak_y
#     global peak_width
#
#
#     selected_x_fdm = 0
#     selected_y_fdm = 0
#     roi_fdm = 0
#
#     selected_calculated = False
#     selected_x1 = 0
#     selected_x2 = 0
#     selected_y1 = 0
#     selected_y2 = 0
#     selected_z1 = 0
#     selected_z2 = 0
#
#
#     listMaterial = []
#     charge = []
#     element = []
#     isotope = []
#
#     peaks_idx = []
#
#     result_path = ''
#     path = ''
#
#     dld_t_calib = np.zeros(0)
#     dld_t_calib_backup = np.zeros(0)
#     mc_calib = np.zeros(0)
#     mc_calib_backup = np.zeros(0)
#     max_peak = 0
#     peak = []
#     peak_y = []
#     peak_width = []
class Variables:
    """
    A class that represents all shared variables.

    Attributes:
        selected_x_fdm (int): The value of selected_x_fdm.
        selected_y_fdm (int): The value of selected_y_fdm.
        roi_fdm (int): The value of roi_fdm.
        selected_calculated (bool): Indicates if selected values are calculated.
        selected_x1 (int): The value of selected_x1.
        selected_x2 (int): The value of selected_x2.
        selected_y1 (int): The value of selected_y1.
        selected_y2 (int): The value of selected_y2.
        selected_z1 (int): The value of selected_z1.
        selected_z2 (int): The value of selected_z2.
        listMaterial (list): List that stores mass/weights of added elements.
        charge (list): List of charges.
        element (list): List of elements.
        isotope (list): List of isotopes.
        peaks_idx (list): List of peaks indices.
        result_path (str): The result path.
        path (str): The path.
        dld_t_calib (numpy.ndarray): Array for dld_t calibration.
        dld_t_calib_backup (numpy.ndarray): Backup array for dld_t calibration.
        mc_calib (numpy.ndarray): Array for mc calibration.
        mc_calib_backup (numpy.ndarray): Backup array for mc calibration.
        max_peak (int): The maximum peak value.
        peak (list): List of peaks.
        peak_y (list): List of peak y-values.
        peak_width (list): List of peak widths.
    """

    def __init__(self):
        """
        Initializes all the attributes of MyClass.
        """
        self.selected_x_fdm = 0
        self.selected_y_fdm = 0
        self.roi_fdm = 0

        self.selected_calculated = False
        self.selected_x1 = 0
        self.selected_x2 = 0
        self.selected_y1 = 0
        self.selected_y2 = 0
        self.selected_z1 = 0
        self.selected_z2 = 0

        self.listMaterial = []
        self.charge = []
        self.element = []
        self.isotope = []

        self.peaks_idx = []

        self.result_path = ''
        self.path = ''

        self.dld_t_calib = np.zeros(0)
        self.dld_t_calib_backup = np.zeros(0)
        self.mc_calib = np.zeros(0)
        self.mc_calib_backup = np.zeros(0)
        self.max_peak = 0
        self.peak = []
        self.peak_y = []
        self.peak_width = []
