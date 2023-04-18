"""
This is the script for testing BASLER cameras.
"""

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


from pypylon import genicam
from pypylon import pylon
import sys
import time

try:
    import cv2
except:
    print('Please install opencv2')
import numpy as np



def camera():
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
    img0 = []
    img1 = []
    windowName = 'title'

    try:

        # Get the transport layer factory.
        tlFactory = pylon.TlFactory.GetInstance()

        # Get all attached devices and exit application if no device is found.
        devices = tlFactory.EnumerateDevices()
        for device in devices:
            print('devices name:', device.GetFriendlyName())
        if len(devices) == 0:
            raise pylon.RUNTIME_EXCEPTION("No camera present.")

        # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
        cameras = pylon.InstantCameraArray(min(len(devices), maxCamerasToUse))
        print(cameras)
        # l = cameras.GetSize()

        # Create and attach all Pylon Devices.
        for i, cam in enumerate(cameras):
            cam.Attach(tlFactory.CreateDevice(devices[i]))
            cam.Open()
            cam.Width = 2448
            cam.Height = 2048
            cam.ExposureTime.SetValue(800000)
            # Print the model name of the camera.
            print("Using device ", cam.GetDeviceInfo().GetModelName())
            # print("Exposure time ", cam.ExposureTime.GetValue())

        # Starts grabbing for all cameras starting with index 0. The grabbing
        # is started for one camera after the other. That's why the images of all
        # cameras are not taken at the same time.
        # However, a hardware trigger setup can be used to cause all cameras to grab images synchronously.
        # According to their default configuration, the cameras are
        # set up for free-running continuous acquisition.
        cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

        # converting to opencv bgr format
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        while cameras.IsGrabbing():
            # Grab c_countOfImagesToGrab from the cameras.
            # for i in range(countOfImagesToGrab):
            if not cameras.IsGrabbing():
                break

            grabResult = cameras.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)

            # When the cameras in the array are created the camera context value
            # is set to the index of the camera in the array.
            # The camera context is a user settable value.
            # This value is attached to each grab result and can be used
            # to determine the camera that produced the grab result.
            cameraContextValue = grabResult.GetCameraContext()

            # Print the index and the model name of the camera.
            # print("Camera ", cameraContextValue, ": ", cameras[cameraContextValue].GetDeviceInfo().GetModelName())

            # Now, the image data can be processed.
            # print("GrabSucceeded: ", grabResult.GrabSucceeded())
            # print("SizeX: ", grabResult.GetWidth())
            # print("SizeY: ", grabResult.GetHeight())
            # img = grabResult.GetArray()
            # print("Gray value of first pixel: ", img[0, 0])

            if grabResult.GrabSucceeded():
                image = converter.Convert(grabResult)  # Access the openCV image data
                if cameraContextValue == 0:  # If camera 0, save array into img0[]
                    img0 = image.GetArray()
                else:  # if camera 1, save array into img1[]
                    img1 = image.GetArray()

                # If there is no img1, the first time, make img1=img0
                # Need the same length arrays to concatenate
                if len(img1) == 0:
                    img1 = img0

                img0_zoom = cv2.resize(img0[800:1100, 1800:2300], dsize=(2448, 1000), interpolation=cv2.INTER_CUBIC)
                img1_zoom = cv2.resize(img1[1100:1300, 1000:1500], dsize=(2448, 1000), interpolation=cv2.INTER_CUBIC)
                # numpy_horizontal = np.hstack((img0, img1))
                img0_f = np.concatenate((img0, img0_zoom), axis=0)
                img1_f = np.concatenate((img1, img1_zoom), axis=0)
                vis = np.concatenate((img0_f, img1_f), axis=1)  # Combine 2 images horizontally
                cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(windowName, 1500, 600)
                cv2.imshow(windowName, vis)  # displays image in specified window
                k = cv2.waitKey(1)
                if k == 27:  # If press ESC key
                    print('ESC')
                    cv2.destroyAllWindows()
                    break

            else:
                print("Error: ", grabResult.ErrorCode)
                # grabResult.ErrorDescription does not work properly in python could throw UnicodeDecodeError
            grabResult.Release()
            time.sleep(0.05)

            # If window has been closed using the X button, close program
            # getWindowProperty() returns -1 as soon as the window is closed
            if cv2.getWindowProperty(windowName, 0) < 0:
                cv2.destroyAllWindows()
                break

    except genicam.GenericException as e:
        # Error handling
        print("An exception occurred.", e.GetDescription())
        exitCode = 1

    # Comment the following two lines to disable waiting on exit.
    sys.exit(exitCode)


if __name__ == '__main__':
    camera()