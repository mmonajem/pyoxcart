import numpy as np


def tof_bin2mc_sc(t, t0, V, xDet, yDet, flightPathLength):
	"""
	Calculate the m/c for Surface Concept delay line.

	Args:
		t (float): Time in TOF bins.
		t0 (float): T0 correction.
		V (float): Voltage.
		xDet (float): X-coordinate of the detector.
		yDet (float): Y-coordinate of the detector.
		flightPathLength (float): Flight path length.

	Returns:
		float: Calculated m/c value.
	"""
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
    return mc

def tof_bin2mc_roentdec(t, t0, V, xDet, yDet, flightPathLength):
	"""
	Calculate the m/c for Roentdec delay line.

	Args:
		t (float): Time in TOF bins.
		t0 (float): T0 correction.
		V (float): Voltage.
		xDet (float): X-coordinate of the detector.
		yDet (float): Y-coordinate of the detector.
		flightPathLength (float): Flight path length.

	Returns:
		float: Calculated m/c value.
	"""
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
    return mc
