"""
This is file contains tools for mass calibration process.
"""

import numpy as np

# Local module and scripts
from pyccapt.calibration.calibration_tools import logging_library



def tof2mcSimple(t:"Unit: ns", t0:"Unit:ns", V:"Unit:volts", xDet:"Unit:mm", yDet:"Unit:mm", flightPathLength:"Unit:mm")->"Unit: Dalton":
    """
        This function calculates m/c based on idealized geometry/ electrostatics.
        m/c = 2 e V (t/L)^2

        Attributes:
            t: time (type: int)
            t0: initial time (type: int)
            V: voltage (type: int/float)
            xDet: Distance along x axis  (type: int)
            yDet: Distance along y axis  (type: int)
            flightPathLength: length of flight path  (type: int)
        Returns:
            mc: (type: float)
    """
    logger = logging_library.logger_creator('data_loadcrop')
    try:
        t = t - t0  # t0 correction

        t = t * 1E-9  # tof from ns to s

        xDet = xDet * 1E-2  # xDet from cm to m
        yDet = yDet * 1E-2
        flightPathLength = flightPathLength * 1E-3
        e = 1.6E-19  # coulombs per electron
        amu = 1.66E-27  # conversion kg to Dalton

        flightPathLength = np.sqrt(xDet ** 2 + yDet ** 2 + flightPathLength ** 2)

        mc = 2 * e * V * (t / flightPathLength) ** 2
        mc = mc / amu  # conversion from kg/C to Da 6.022E23 g/mol, 1.6E-19C/ec
        return mc
    except TypeError as error:
        logger.info(error)
        logger.critical("Data type of the passed argument is incorrect")


def tof2mc(t:"Unit:ns", t0:"Unit:ns", V:"Unit:volts", 
           V_pulse:"Unit:volts", xDet:"Unit:mm", yDet:"Unit:mm",
           flightPathLength:"Unit:mm", mode='voltage')->"Unit:Dalton":
    logger = logging_library.logger_creator('data_loadcrop')
    """
        This function calculates m/c based on idealized geometry/ electrostatics.
        m/c = 2 e alpha (V + beta V_p) (t/L)^2

        Attributes:
            t: time (type: int)
            t0: initial time (type: int)
            V: voltage (type: int/float)
            xDet: Distance along x axis  (type: int)
            yDet: Distance along y axis  (type: int)
            flightPathLength: length of flight path  (type: int)
            mode: type of mode (voltage/laser)
        Returns:
            mc: (type: float)
    """
    # 
    try:
        alpha = 1.015
        beta = 0.7

        # t0 is in ns
        t = t - t0  # t0 correction

        t = t * 1E-9  # tof in s

        xDet = xDet * 1E-2  # xDet in cm
        yDet = yDet * 1E-2
        flightPathLength = flightPathLength * 1E-3
        e = 1.6E-19  # coulombs per electron
        amu = 1.66E-27  # conversion kg to Dalton

        flightPathLength = np.sqrt(xDet ** 2 + yDet ** 2 + flightPathLength ** 2)

        if mode == 'voltage':
            # mc = 2 * e * alpha * (V + beta * V_pulse) * (t / flightPathLength)**2
            mc = 2 * V * e * (t / flightPathLength) ** 2
        elif mode == 'laser':
            mc = 2 * V * e * (t / flightPathLength) ** 2

        mc = mc / amu  # converstion from kg/C to Da 6.022E23 g/mol, 1.6E-19C/ec
        return mc
    except TypeError as error:
        logger.critical(error)
        logger.critical("Data type of the passed argument is incorrect")
    except UnboundLocalError as error:
        logger.critical(error)
        logger.critical("Enter correct mode type")