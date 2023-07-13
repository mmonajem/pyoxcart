import numpy as np

from pyccapt.calibration.calibration_tools import logging_library


def tof2mcSimple(t: int, t0: int, V: float, xDet: int, yDet: int, flightPathLength: int) -> float:
    """
    Calculate m/c based on idealized geometry and electrostatics using the formula:
    m/c = 2eV(t/L)^2

    Args:
        t: Time (unit: ns)
        t0: Initial time (unit: ns)
        V: Voltage (unit: volts)
        xDet: Distance along the x-axis (unit: mm)
        yDet: Distance along the y-axis (unit: mm)
        flightPathLength: Length of the flight path (unit: mm)

    Returns:
        mc: Mass-to-charge ratio (unit: Dalton)
    """
    logger = logging_library.logger_creator('data_loadcrop')

    try:
        t = t - t0  # t0 correction
        t = t * 1E-9  # tof from ns to s
        xDet = xDet * 1E-2  # xDet from cm to m
        yDet = yDet * 1E-2  # yDet from cm to m
        flightPathLength = flightPathLength * 1E-3  # flightPathLength from mm to m

        e = 1.6E-19  # coulombs per electron
        amu = 1.66E-27  # conversion from kg to Dalton

        flightPathLength = np.sqrt(xDet ** 2 + yDet ** 2 + flightPathLength ** 2)

        mc = 2 * e * V * (t / flightPathLength) ** 2
        mc = mc / amu  # conversion from kg/C to Da (6.022E23 g/mol, 1.6E-19C/ec)

        return mc
    except TypeError as error:
        logger.info(error)
        logger.critical("Data type of the passed argument is incorrect")


def tof2mc(t: int, t0: int, V: float, xDet: int, yDet: int,
           flightPathLength: int, V_pulse: float, mode: str = 'voltage') -> float:
    """
    Calculate m/c based on idealized geometry and electrostatics using the formula:
    m/c = 2eα(V + βV_pulse)(t/L)^2

    Args:
        t: Time (unit: ns)
        t0: Initial time (unit: ns)
        V: Voltage (unit: volts)
        V_pulse: Voltage pulse (unit: volts)
        xDet: Distance along the x-axis (unit: mm)
        yDet: Distance along the y-axis (unit: mm)
        flightPathLength: Length of the flight path (unit: mm)
        mode: Type of mode ('voltage' or 'laser')

    Returns:
        mc: Mass-to-charge ratio (unit: Dalton)
    """
    logger = logging_library.logger_creator('data_loadcrop')

    try:
        # cThe value of α is greater than one, accounting for the fact thatThe value of a
        # is slightly greater than one, accounting for the fact that the
        # evaporation pulse is slightly amplified due to reflections and
        # impedance mismatches along the pulse transmission line.
        alpha = 1.015
        # cThe value of b is less
        # than one, accounting for the fact that the ions field evaporate,
        # on average, not at the peak of the evaporation pulse, but
        # during the ascending and descending edges of the incoming
        # evaporation pulse.
        beta = 0.7

        t = t - t0  # t0 correction
        t = t * 1E-9  # tof from ns to s
        xDet = xDet * 1E-2  # xDet from cm to m
        yDet = yDet * 1E-2  # yDet from cm to m
        flightPathLength = flightPathLength * 1E-3  # flightPathLength from mm to m

        e = 1.6E-19  # coulombs per electron
        amu = 1.66E-27  # conversion from kg to Dalton

        flightPathLength = np.sqrt(xDet ** 2 + yDet ** 2 + flightPathLength ** 2)

        if mode == 'dc_voltage':
            mc = 2 * V * e * (t / flightPathLength) ** 2
        elif mode == 'dc_plus_p_voltage':
            mc = 2 * alpha * (V + beta * V_pulse) * e * (t / flightPathLength) ** 2

        mc = mc / amu  # conversion from kg/C to Da (6.022E23 g/mol, 1.6E-19C/ec)

        return mc
    except TypeError as error:
        logger.critical(error)
        logger.critical("Data type of the passed argument is incorrect")
    except UnboundLocalError as error:
        logger.critical(error)
        logger.critical("Enter correct mode type")
