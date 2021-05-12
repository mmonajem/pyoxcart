
import cv2
import os
import numpy as np
from pypylon import pylon

import variables

os.environ["PYLON_CAMEMU"] = "2"

class Camera():

    def update_cameras(self, cameras, converter):
        while True:
            cameras[0].Open()
            cameras[0].ExposureTime.SetValue(variables.camera_0_ExposureTime)
            cameras[1].Open()
            cameras[1].ExposureTime.SetValue(variables.camera_1_ExposureTime)
            if variables.light == False:
                grabResult0 = cameras[0].RetrieveResult(10000000, pylon.TimeoutHandling_ThrowException)
                grabResult1 = cameras[1].RetrieveResult(1000000, pylon.TimeoutHandling_ThrowException)
            elif variables.light == True:
                grabResult0 = cameras[0].RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)
                grabResult1 = cameras[1].RetrieveResult(10000, pylon.TimeoutHandling_ThrowException)
            image0 = converter.Convert(grabResult0)
            img0 = image0.GetArray()
            image1 = converter.Convert(grabResult1)
            img1 = image1.GetArray()

            img0_orig = cv2.resize(img0, dsize=(500, 500), interpolation=cv2.INTER_CUBIC).astype(np.int32)
            img0_zoom = img0[800:1100, 1800:2300]
            img0_zoom = cv2.resize(img0_zoom, dsize=(1200, 500), interpolation=cv2.INTER_CUBIC).astype(np.int32)
            img1_orig = cv2.resize(img1, dsize=(500, 500), interpolation=cv2.INTER_CUBIC).astype(np.int32)
            img1_zoom = img1[1050:1300, 1000:1500]
            img1_zoom = cv2.resize(img1_zoom, dsize=(1200, 500), interpolation=cv2.INTER_CUBIC).astype(np.int32)
            # Saving images - So far it is not possible to not save and load images in a proper way with ImageQt
            variables.img0_orig = np.require(img0_orig, np.uint8, 'C')
            variables.img0_zoom = np.require(img0_zoom, np.uint8, 'C')
            variables.img1_orig = np.require(img1_orig, np.uint8, 'C')
            variables.img1_zoom = np.require(img1_zoom, np.uint8, 'C')
            # cv2.imwrite(".\png\\1.png", img0_orig)
            # cv2.imwrite(".\png\\1_zoom.png", img0_zoom)
            # cv2.imwrite('.\png\\2.png', img1_orig)
            # cv2.imwrite('.\png\\2_zoom.png', img1_zoom)

    def camera_init(self,):
        # Limits the amount of cameras used for grabbing.
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

        # Create and attach all Pylon Devices.
        for i, cam in enumerate(cameras):
            cam.Attach(tlFactory.CreateDevice(devices[i]))

            # Print the model name of the camera.
            print("Using camera ", cam.GetDeviceInfo().GetModelName())

        if variables.light == True:
            cameras[0].Open()
            cameras[0].ExposureTime.SetValue(3000)
            cameras[1].Open()
            cameras[1].ExposureTime.SetValue(3000)
        elif variables.light == False:
            cameras[0].Open()
            cameras[0].ExposureTime.SetValue(10000000)
            cameras[1].Open()
            cameras[1].ExposureTime.SetValue(1000000)

        # Starts grabbing for all cameras starting with index 0. The grabbing
        # set up for free-running continuous acquisition.
        cameras.StartGrabbing()

        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        return cameras, converter

    def light_switch(self, cameras):
        if variables.light == False:
            variables.light = True
            cameras[0].Open()
            cameras[0].ExposureTime.SetValue(3000)
            cameras[1].Open()
            cameras[1].ExposureTime.SetValue(3000)
        elif variables.light == True:
            variables.light = False
            cameras[0].Open()
            cameras[0].ExposureTime.SetValue(10000000)
            cameras[1].Open()
            cameras[1].ExposureTime.SetValue(1000000)

