import numpy as np
import pandas as pd


class Variables:
    """
    A class that represents all shared variables.

    Attributes:
        pulse_mode (str): The pulse mode.
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
        dataset_name (str): The dataset name.
        result_data_path (str): The result data path.
        result_data_name (str): The result data name.
        dld_t (numpy.ndarray): Array for dld_t.
        self.dld_t_c (numpy.ndarray): Array for dld_t calibration.
        dld_x_det (numpy.ndarray): Array for dld_x_det.
        dld_y_det (numpy.ndarray): Array for dld_y_det.
        dld_high_voltage (numpy.ndarray): Array for dld_high_voltage.
        dld_t_calib (numpy.ndarray): Array for dld_t calibration.
        dld_t_calib_backup (numpy.ndarray): Backup array for dld_t calibration.
        mc (numpy.ndarray): Array for mc.
        self.mc_c (numpy.ndarray): Array for mc calibration.
        mc_calib (numpy.ndarray): Array for mc calibration.
        mc_calib_backup (numpy.ndarray): Backup array for mc calibration.
        max_peak (int): The maximum peak value.
        max_tof (int): The maximum tof value.
        peak (list): List of peaks.
        peak_y (list): List of peak y-values.
        peak_width (list): List of peak widths.
        h_line_pos (list): List of horizontal line positions.
        range_data (data frame): List of range data.
        range_data_backup (data frame): Backup list of range data.
    """

    def __init__(self):
        """
        Initializes all the attributes of MyClass.
        """
        self.pulse_mode = ''

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
        self.h_line_pos = []

        self.listMaterial = []
        self.charge = []
        self.element = []
        self.isotope = []

        self.peaks_idx = []

        self.result_path = ''
        self.path = ''
        self.dataset_name = ''
        self.result_data_path = ''
        self.result_data_name = ''

        self.dld_t = np.zeros(0)
        self.dld_t_c = np.zeros(0)
        self.dld_x_det = np.zeros(0)
        self.dld_y_det = np.zeros(0)
        self.dld_high_voltage = np.zeros(0)
        self.dld_t_calib = np.zeros(0)
        self.dld_t_calib_backup = np.zeros(0)
        self.mc = np.zeros(0)
        self.mc_c = np.zeros(0)
        self.mc_calib = np.zeros(0)
        self.mc_calib_backup = np.zeros(0)
        self.max_peak = 0
        self.max_tof = 0
        self.peak = []
        self.peak_y = []
        self.peak_width = []

        # Create an empty DataFrame with the specified columns
        self.range_data = pd.DataFrame(columns=['ion', 'mass', 'mc', 'mc_low', 'mc_up', 'color', 'element', 'complex',
                                                'isotope', 'charge'])

        self.range_data_backup = None
