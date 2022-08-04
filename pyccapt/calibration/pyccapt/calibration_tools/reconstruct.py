import numpy as np
import math


def cart2pol(x, y):
    """
    x, y are the detector hit coordinates in mm
    :param x:
    :param y:
    :return rho, phi:
    """
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(rho, phi):
    """
    :param rho:
    :param phi:
    :return x, y:
    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y

def atom_probe_recons_pad(detx, dety, dld_v, flight_path_length, ion_volume, radius=55*1E-9, Fevap=65, det_eff=50, kf=3.0, icf=1.4):
    """
    :param detx:
    :param dety:
    :param hv:
    :param kf:
    :param icf:
    :param flight_path_length:
    :param ion_volume:
    :param det_eff:
    :param radius_evolution:
    :return:
    """

    r = dld_v / kf * Fevap

    m = flight_path_length / (icf * r)

    x = detx / m
    y = dety / m

    det_area = (78/2)**2 * math.pi

    # dz = omega / det_eff = s_a  # s_a = s_d / m**2
    dz = ion_volume * m**2 / det_area * det_eff


    ### calculate z coordinate
    # the z shift with respect to the top of the cap is Rspec - zP
    zp = radius_evolution - zp

    # accumulative part of z
    omega = 1. / ion_volume / det_eff  # atomic volume in nm ^ 3
    omega[math.isnan(omega)] = 0

    # magnification M at ion index
    M = flight_path_length / icf / radius_evolution
    # currently evaporating area of the specimen
    specArea = det_eff / M**2
    # individual depth increment
    dz = omega / specArea

    # wide angle correction
    cum_z = np.cumsum(np.double(dz))
    z = cum_z + zp

    return x, y, z


def atom_probe_recons_from_detector(detx, dety, hv, flight_path_length, kf=3.0, det_eff=50, icf=1.4, Fevap=65, avgDens=60.2):
    """
    # atom probe reconstruction after: Gault et al., Ultramicroscopy 111(2011) 448 - 457
    x, y are the detector hit coordinates in mm
    kf is the field factor and ICF is the image compression factor
    :param detx:
    :param dety:
    :param hv:
    :param kf:
    :param icf:
    :param flight_path_length:
    :param ion_volume:
    :param det_eff:
    :param radius_evolution:
    :return:
    """

    ## constants and variable setup
    # specimen parameters
    # avgDens # atomic density in atoms / nm3
    # Fevap  # evaporation field in V / nm

    # detector coordinates in polar form
    ang, rad = cart2pol(detx, dety)

    # calculating effective detector area:
    Adet = ((np.max(rad)) ** 2) * math.pi()

    # radius evolution from voltage curve (in nm)
    Rspec = hv / (kf * Fevap)

    ## calcualte x and y coordinates

    # launch angle relative to specimen axis
    thetaP = math.atan(rad / flight_path_length)  # mm / mm
    theta = thetaP + math.asin((icf - 1) * math.sin(thetaP))

    # distance from axis and z shift of each hit
    zP, d = pol2cart(theta, Rspec)  # nm

    # x and y coordinates from the angle on the detector and the distance to
    # the specimen axis.
    x, y = pol2cart(ang, d)  # nm

    ## calculate z coordinate
    # the z shift with respect to the top of the cap is Rspec - zP
    zP = Rspec - zP

    # accumulative part of z
    omega = 1 / avgDens  # atomic volume in nm ^ 3

    # nm ^ 3 * mm ^ 2 * V ^ 2 / nm ^ 2 / (mm ^ 2 * V ^ 2)
    dz = omega * (flight_path_length ** 2) * (kf ** 2) * (Fevap ** 2) / (det_eff * Adet * (icf ** 2)) * (hv ** 2)

    # wide angle correction
    cumZ = math.cumsum(np.double(dz))
    z = cumZ + zP

    return x, y, z

def atom_probe_recons_geiser(detx, dety, flight_path_length, ion_volume, radius_evolution, det_eff=50, icf=1.4):
    """
    :param detx:
    :param dety:
    :param hv:
    :param kf:
    :param icf:
    :param flight_path_length:
    :param ion_volume:
    :param det_eff:
    :param radius_evolution:
    :return:
    """
    ### fundamental bdata reconstruction
    # detector coordinates in polar form
    ang, rad = cart2pol(detx, dety)

    # launch angle relative to specimen axis
    thetaP = math.atan(rad / flight_path_length)  # mm / mm

    # image compression correction
    theta = thetaP + math.asin((icf - 1) * math.sin(thetaP))

    # distance from axis and z shift of each hit
    zp, d = pol2cart(theta, radius_evolution)  # nm

    # x and y coordinates from the angle on the detector and the distance to
    # the specimen axis.
    x, y = pol2cart(ang, d)  # nm

    ### calculate z coordinate
    # the z shift with respect to the top of the cap is Rspec - zP
    zp = radius_evolution - zp

    # accumulative part of z
    omega = 1. / ion_volume / det_eff  # atomic volume in nm ^ 3
    omega[math.isnan(omega)] = 0

    # magnification M at ion index
    M = flight_path_length / icf / radius_evolution
    # currently evaporating area of the specimen
    specArea = det_eff / M ** 2
    # individual depth increment
    dz = omega / specArea

    # wide angle correction
    cum_z = np.cumsum(np.double(dz))
    z = cum_z + zp

    return x, y, z



