"""
This is the script containing simple version of m/c calculation.
"""

import numpy as np

from pyccapt.control.control_tools import loggi, variables


def tof_bin2mc_sc(t, t0, V, xDet, yDet, flightPathLength):
    """
    Calculate the m/c for Surface Concept delay line.
    """
    if variables.log:
        log_tof = loggi.logger_creator('tof2mc_simple', 'tof2mc_simple.log', path=variables.log_path)
        log_tof.info("Function - tof_bin2mc_sc | t- > {} | type - {}".format(t, type(t)))
        log_tof.info("Function - tof_bin2mc_sc | t0- > {} | type - {}".format(t0, type(t0)))
        log_tof.info("Function - tof_bin2mc_sc | V- > {} | type - {}".format(V, type(V)))
        log_tof.info("Function - tof_bin2mc_sc | xDet- > {} | type - {}".format(xDet, type(xDet)))
        log_tof.info("Function - tof_bin2mc_sc | yDet- > {} | type - {}".format(yDet, type(yDet)))
        log_tof.info("Function - tof_bin2mc_sc | flightPathLength- > {} | type - {}".format(flightPathLength, type(flightPathLength)))

    # calculates m/c based on idealized geometry / electrostatics
    # m/c = 2 e V (t/L)^2

    TOFFACTOR = 27.432 / (1000 * 4)  # 27.432 ps/bin, tof in ns, data is TDC time sum
    DETBINS = 4900
    BINNINGFAC = 2
    XYFACTOR = 78 / DETBINS * BINNINGFAC  # XXX mm/bin
    XYBINSHIFT = DETBINS / BINNINGFAC / 2  # to center detector

    xDet = (xDet - XYBINSHIFT) * XYFACTOR
    yDet = (yDet - XYBINSHIFT) * XYFACTOR

    t = t * TOFFACTOR

    t = t * 1E-9  # tof in ns

    t = t - t0  # t0 correction

    xDet = xDet * 1E-3  # xDet in mm
    yDet = yDet * 1E-3
    flightPathLength = flightPathLength * 1E-3
    e = 1.6E-19  # coulombs per electron
    amu = 1.66E-27  # conversion kg to Dalton

    flightPathLength = np.sqrt(xDet ** 2 + yDet ** 2 + flightPathLength ** 2)

    mc = 2 * e * V * (t / flightPathLength) ** 2
    mc = mc / amu  # conversion from kg/C to Da 6.022E23 g/mol, 1.6E-19C/ec
    if variables.log:
        log_tof.info("Function - tof_bin2mc_sc | response- > {} | type - {}".format(mc, type(mc)))
    return mc


def tof_bin2mc_ro(t, t0, V, xDet, yDet, flightPathLength):
    """
    Calculate the m/c for Roentdec delay line.
    """
    if variables.log:
        log_tof = loggi.logger_creator('tof2mc_simple', 'tof2mc_simple.log', path=variables.log_path)
        log_tof.info("Function - tof_bin2mc_ro | t- > {} | type - {}".format(t, type(t)))
        log_tof.info("Function - tof_bin2mc_ro | t0- > {} | type - {}".format(t0, type(t0)))
        log_tof.info("Function - tof_bin2mc_ro | V- > {} | type - {}".format(V, type(V)))
        log_tof.info("Function - tof_bin2mc_ro | xDet- > {} | type - {}".format(xDet, type(xDet)))
        log_tof.info("Function - tof_bin2mc_ro | yDet- > {} | type - {}".format(yDet, type(yDet)))
        log_tof.info("Function - tof_bin2mc_ro | flightPathLength- > {} | type - {}".format(flightPathLength, type(flightPathLength)))
    # calculates m/c based on idealized geometry / electrostatics
    # m/c = 2 e V (t/L)^2

    TOFFACTOR = 27.432 / (1000 * 4)  # 27.432 ps/bin, tof in ns, data is TDC time sum
    DETBINS = 4900
    BINNINGFAC = 2
    XYFACTOR = 78 / DETBINS * BINNINGFAC  # XXX mm/bin
    XYBINSHIFT = DETBINS / BINNINGFAC / 2  # to center detector

    xDet = (xDet - XYBINSHIFT) * XYFACTOR
    yDet = (yDet - XYBINSHIFT) * XYFACTOR

    t = t * TOFFACTOR

    t = t * 1E-9  # tof in ns

    t = t - t0  # t0 correction

    xDet = xDet * 1E-3  # xDet in mm
    yDet = yDet * 1E-3
    flightPathLength = flightPathLength * 1E-3
    e = 1.6E-19  # coulombs per electron
    amu = 1.66E-27  # conversion kg to Dalton

    flightPathLength = np.sqrt(xDet ** 2 + yDet ** 2 + flightPathLength ** 2)

    mc = 2 * e * V * (t / flightPathLength) ** 2
    mc = mc / amu  # conversion from kg/C to Da 6.022E23 g/mol, 1.6E-19C/ec
    if variables.log:
        log_tof.info("Function - tof_bin2mc_sc | response- > {} | type - {}".format(mc, type(mc)))

    return mc


