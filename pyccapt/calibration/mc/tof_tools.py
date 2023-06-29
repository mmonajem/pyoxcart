import numpy as np


def mc2tof(mc: float, V: float, xDet: float, yDet: float, flightPathLength: float) -> float:
    """
    Calculate time of flight (tof) based on idealized geometry and electrostatics using the formula:
    t = sqrt((mc * amu * (flightPathLength^2)) / (2eV)) * 1E9

    Args:
        mc: Mass-to-charge ratio (unit: Dalton)
        V: Voltage (unit: volts)
        xDet: Distance along the x-axis (unit: mm)
        yDet: Distance along the y-axis (unit: mm)
        flightPathLength: Length of the flight path (unit: mm)

    Returns:
        t: Time of flight (unit: ns)
    """
    xDet = xDet * 1E-2  # xDet from mm to m
    yDet = yDet * 1E-2  # yDet from mm to m
    flightPathLength = flightPathLength * 1E-3  # flightPathLength from mm to m
    e = 1.6E-19  # coulombs per electron
    amu = 1.66E-27  # conversion from kg to Dalton

    flightPathLength = np.sqrt(xDet ** 2 + yDet ** 2 + flightPathLength ** 2)

    t = np.sqrt(((mc * amu * (flightPathLength) ** 2)) / (2 * e * V))
    t = t * 1E9  # tof from s to ns

    return t
