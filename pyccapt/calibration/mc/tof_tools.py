"""
This is file contains tools for tof processes.
"""

import numpy as np


def mc2tof(mc:"Unit: Da", V:"Unit:volts", xDet:"Unit:mm", yDet:"Unit:mm", flightPathLength:"Unit:mm")->"Unit: Dalton":
    # calculates tof based on idealized geometry / electrostatics and ideal mc
    # m/c = 2 e V (t/L)^2
    xDet = xDet * 1E-2  # xDet from mm to m
    yDet = yDet * 1E-2
    flightPathLength = flightPathLength * 1E-3
    e = 1.6E-19  # coulombs per electron
    amu = 1.66E-27  # conversion kg to Dalton

    flightPathLength = np.sqrt(xDet ** 2 + yDet ** 2 + flightPathLength ** 2)

    t = np.sqrt(((mc * amu * (flightPathLength) ** 2)) / (2 * e * V))# in ns
    t = t * 1E9  # tof from s to ns
    return t

