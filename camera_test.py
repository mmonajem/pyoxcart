# Grab_MultipleCameras.cpp
# ============================================================================
# This sample illustrates how to grab and process images from multiple cameras
# using the CInstantCameraArray class. The CInstantCameraArray class represents
# an array of instant camera objects. It provides almost the same interface
# as the instant camera for grabbing.
# The main purpose of the CInstantCameraArray is to simplify waiting for images and
# camera events of multiple cameras in one thread. This is done by providing a single
# RetrieveResult method for all cameras in the array.
# Alternatively, the grabbing can be started using the internal grab loop threads
# of all cameras in the CInstantCameraArray. The grabbed images can then be processed by one or more
# image event handlers. Please note that this is not shown in this example.
# ============================================================================

import os
import time

os.environ["PYLON_CAMEMU"] = "2"

from pypylon import genicam
from pypylon import pylon
import sys
import cv2

# Number of images to be grabbed.
countOfImagesToGrab = 10

# Limits the amount of cameras used for grabbing.
# It is important to manage the available bandwidth when grabbing with multiple cameras.
# This applies, for instance, if two GigE cameras are connected to the same network adapter via a switch.
# To manage the bandwidth, the GevSCPD interpacket delay parameter and the GevSCFTD transmission delay
# parameter can be set for each GigE camera device.
# The "Controlling Packet Transmission Timing with the Interpacket and Frame Transmission Delays on Basler GigE Vision Cameras"
# Application Notes (AW000649xx000)
# provide more information about this topic.
# The bandwidth used by a FireWire camera device can be limited by adjusting the packet size.
maxCamerasToUse = 2

# The exit code of the sample application.
exitCode = 0



# Get the transport layer factory.
tlFactory = pylon.TlFactory.GetInstance()

# Get all attached devices and exit application if no device is found.
devices = tlFactory.EnumerateDevices()


if len(devices) == 0:
    raise pylon.RuntimeException("No camera present.")

# Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse))


l = cameras.GetSize()
# Create and attach all Pylon Devices.
for i, cam in enumerate(cameras):
    cam.Attach(tlFactory.CreateDevice(devices[i]))

    # Print the model name of the camera.
    print("Using device ", cam.GetDeviceInfo().GetModelName())


cameras[0].Open()
# cameras[0].ExposureTime.SetValue(10000000)
cameras[0].ExposureTime.SetValue(3000)
cameras[1].Open()
# cameras[1].ExposureTime.SetValue(1000000)
cameras[1].ExposureTime.SetValue(3000)

# Starts grabbing for all cameras starting with index 0. The grabbing
# is started for one camera after the other. That's why the images of all
# cameras are not taken at the same time.
# However, a hardware trigger setup can be used to cause all cameras to grab images synchronously.
# According to their default configuration, the cameras are
# set up for free-running continuous acquisition.
cameras.StartGrabbing()



converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

# Grab c_countOfImagesToGrab from the cameras.
for i in range(countOfImagesToGrab):
    if not cameras.IsGrabbing():
        break

    if i <=4:
        grabResult = cameras[0].RetrieveResult(10000000, pylon.TimeoutHandling_ThrowException)
    else:
        grabResult = cameras[1].RetrieveResult(1000000, pylon.TimeoutHandling_ThrowException)

    # When the cameras in the array are created the camera context value
    # is set to the index of the camera in the array.
    # The camera context is a user settable value.
    # This value is attached to each grab result and can be used
    # to determine the camera that produced the grab result.
    cameraContextValue = grabResult.GetCameraContext()

    # Print the index and the model name of the camera.
    print("Camera ", cameraContextValue, ": ", cameras[cameraContextValue].GetDeviceInfo().GetModelName())

    # Now, the image data can be processed.
    print("GrabSucceeded: ", grabResult.GrabSucceeded())
    print("SizeX: ", grabResult.GetWidth())
    print("SizeY: ", grabResult.GetHeight())
    image = converter.Convert(grabResult)
    img = image.GetArray()
    cv2.imwrite('./camera_%s_%s.png' %(cameraContextValue, i), img)
    # cv2.imshow('title', img)
    # time.sleep(1)
    print("Gray value of first pixel: ", img[0, 0])

time.sleep(3)