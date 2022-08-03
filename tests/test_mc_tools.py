
from unittest.mock import patch
<<<<<<< HEAD
=======
import numpy as np
>>>>>>> 82136ce (add unit tests)
import sys
import os

from pyccapt.mc import mc_tools



def test_tof2mcSimple_check_return_type():
<<<<<<< HEAD
    import numpy as np
=======
>>>>>>> 82136ce (add unit tests)
    t = 200
    t0 = 100
    V = 12
    xDet = 100
    yDet = 50
    flightPathLength = 20
    response = mc_tools.tof2mcSimple(t,t0,V,xDet,yDet,flightPathLength)
    assert isinstance(response,np.float64)


@patch.object(mc_tools.logger, "critical")
def test_tof2mcSimple_check_data_type_of_args(mock):
<<<<<<< HEAD
    import numpy as np
=======
>>>>>>> 82136ce (add unit tests)
    t = "200" # String passed while the the function is expecting int/float
    t0 = 100
    V = 12
    xDet = 100
    yDet = 50
    flightPathLength = 20
    response = mc_tools.tof2mcSimple(t,t0,V,xDet,yDet,flightPathLength)
    mock.assert_called_with("Data type of the passed argument is incorrect")

<<<<<<< HEAD
def test_tof2mc_check_return_type():
    import numpy as np
=======

def test_tof2mc_check_return_type():
>>>>>>> 82136ce (add unit tests)
    t = 200
    t0 = 100
    V = 12
    V_pulse = 12
    xDet = 100
    yDet = 50
    flightPathLength = 20
    response = mc_tools.tof2mc(t,t0,V,V_pulse,xDet,yDet,flightPathLength)
    assert isinstance(response,np.float64)


@patch.object(mc_tools.logger, "critical")
def test_tof2mc_check_data_type_of_args(mock):
<<<<<<< HEAD
    import numpy as np
=======
>>>>>>> 82136ce (add unit tests)
    t = "200" # String passed while the the function is expecting int/float
    t0 = 100
    V = 12
    V_pulse = 12
    xDet = 100
    yDet = 50
    flightPathLength = 20
    response = mc_tools.tof2mc(t,t0,V,V_pulse,xDet,yDet,flightPathLength)
    mock.assert_called_with("Data type of the passed argument is incorrect")


@patch.object(mc_tools.logger, "critical")
def test_tof2mc_check_mode(mock):
<<<<<<< HEAD
    import numpy as np
=======
>>>>>>> 82136ce (add unit tests)
    t = 200
    t0 = 100
    V = 12
    V_pulse = 12
    xDet = 100
    yDet = 50
    flightPathLength = 20
    mode = "wrong_mode"
    response = mc_tools.tof2mc(t,t0,V,V_pulse,xDet,yDet,flightPathLength,mode)
    mock.assert_called_with("Enter correct mode type")