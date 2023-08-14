import numpy as np


def tof_2_mc(t, t0, V, xDet, yDet, flightPathLength):
	"""
	Calculate the m/c for

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

	t = t * 1E-9  # is tof in ns
	t = t - t0  # t0 correction

	xDet = xDet * 1E-2  # xDet is in cm
	yDet = yDet * 1E-2  # yDet is in cm
	flightPathLength = flightPathLength * 1E-3  # flightPathLength is in mm
	e = 1.6E-19  # coulombs per electron
	amu = 1.66E-27  # conversion kg to Dalton

	flightPathLength = np.sqrt(xDet ** 2 + yDet ** 2 + flightPathLength ** 2)

	mc = 2 * e * V * (t / flightPathLength) ** 2
	mc = mc / amu  # conversion from kg/C to Da 6.022E23 g/mol, 1.6E-19C/ec
	return mc
