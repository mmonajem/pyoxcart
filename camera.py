from pypylon import genicam
from pypylon import pylon
import sys
import os
import time
import cv2
import numpy as np
import variables

os.environ["PYLON_CAMEMU"] = "2"

class Camera():

    def __init__(self, devices, tlFactory, cameras, converter):

        self.devices = devices
        self.tlFactory = tlFactory
        self.cameras = cameras
        self.converter = converter

        self.cameras[0].Open()
        self.cameras[0].ExposureAuto.SetValue('Off')
        self.cameras[0].ExposureTime.SetValue(1000000)
        self.cameras[1].Open()
        self.cameras[1].ExposureAuto.SetValue('Off')
        self.cameras[1].ExposureTime.SetValue(350000)

    def update_cameras(self, lock):

        # Starts grabbing for all cameras starting with index 0. The grabbing
        # set up for free-running continuous acquisition.
        self.cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        while self.cameras.IsGrabbing():
            # if variables.light == False:
            #     grabResult0 = self.cameras[0].RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
            #     grabResult1 = self.cameras[1].RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
            # elif variables.light == True:
            grabResult0 = self.cameras[0].RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
            grabResult1 = self.cameras[1].RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)
            image0 = self.converter.Convert(grabResult0)
            img0 = image0.GetArray()
            image1 = self.converter.Convert(grabResult1)
            img1 = image1.GetArray()

            # Original size is 2048 * 2448
            # img0_orig = cv2.resize(img0, dsize=(500, 500), interpolation=cv2.INTER_CUBIC).astype(np.int32)
            img0_orig = cv2.resize(img0, dsize=(2048, 2048), interpolation=cv2.INTER_CUBIC).astype(np.int32)
            img0_zoom = cv2.resize(img0[800:1100, 1800:2300], dsize=(1200, 500), interpolation=cv2.INTER_CUBIC).astype(np.int32)

            # img1_orig = cv2.resize(img1, dsize=(500, 500), interpolation=cv2.INTER_CUBIC).astype(np.int32)
            img1_orig = cv2.resize(img1, dsize=(2048, 2048), interpolation=cv2.INTER_CUBIC).astype(np.int32)
            img1_zoom = cv2.resize(img1[1100:1300, 1000:1500], dsize=(1200, 500), interpolation=cv2.INTER_CUBIC).astype(np.int32)

            if variables.index_save_image % 100 == 0 and variables.start_flag == True:
                cv2.imwrite(variables.path + "\\side_%s.png" %variables.index_save_image, img0_orig)
                cv2.imwrite(variables.path + "\\side_zoom_%s.png" %variables.index_save_image, img0_zoom)
                cv2.imwrite(variables.path + '\\bottom_%s.png' %variables.index_save_image, img1_orig)
                cv2.imwrite(variables.path + '\\bottom_zoom_%s.png' %variables.index_save_image, img1_zoom)

            img0_zoom_marker = cv2.drawMarker(img0_zoom, (1020, 265), (0, 0, 255), markerType=cv2.MARKER_TRIANGLE_UP,
                           markerSize=40, thickness=2, line_type=cv2.LINE_AA)
            img1_zoom_marker = cv2.drawMarker(img1_zoom, (1040, 255), (0, 0, 255), markerType=cv2.MARKER_TRIANGLE_UP,
                           markerSize=40, thickness=2, line_type=cv2.LINE_AA)
            with lock:
                # variables.img0_orig = np.require(img0_orig, np.uint8, 'C')
                variables.img0_zoom = np.require(img0_zoom_marker, np.uint8, 'C')
                # variables.img1_orig = np.require(img1_orig, np.uint8, 'C')
                variables.img1_zoom = np.require(img1_zoom_marker, np.uint8, 'C')

                variables.img0_orig = np.swapaxes(img0_orig, 0, 1)
                # variables.img0_zoom = np.swapaxes(img0_zoom, 0, 1)
                variables.img1_orig = np.swapaxes(img1_orig, 0, 1)
                # variables.img1_zoom = np.swapaxes(img1_zoom, 0, 1)
                variables.index_save_image += 1

            if variables.index_save_image % 100 == 0 and variables.start_flag == True:
                cv2.imwrite(variables.path + "\\side_%s.png" %variables.index_save_image, img0_orig)
                cv2.imwrite(variables.path + "\\side_zoom_%s.png" %variables.index_save_image, img0_zoom)
                cv2.imwrite(variables.path + '\\bottom_%s.png' %variables.index_save_image, img1_orig)
                cv2.imwrite(variables.path + '\\bottom_zoom_%s.png' %variables.index_save_image, img1_zoom)

            grabResult0.Release()
            grabResult1.Release()

            if variables.sample_adjust == True:
                self.camera_s_d()
                variables.sample_adjust = False



    def light_switch(self,):
        if variables.light == False:
            self.cameras[0].Open()
            self.cameras[0].ExposureTime.SetValue(2000)
            # self.cameras[0].AcquisitionFrameRate.SetValue(150)
            self.cameras[1].Open()
            self.cameras[1].ExposureTime.SetValue(2000)
            # self.cameras[1].AcquisitionFrameRate.SetValue(150)
            variables.light = True
            variables.sample_adjust = True
        elif variables.light == True:
            self.cameras[0].Open()
            self.cameras[0].ExposureTime.SetValue(1000000)
            self.cameras[1].Open()
            self.cameras[1].ExposureTime.SetValue(350000)
            variables.light = False
            variables.sample_adjust = False

    def camera_s_d(self,):

        # The exit code of the sample application.
        exitCode = 0
        img0 = []
        img1 = []
        windowName = 'Sample Alignment'

        while self.cameras.IsGrabbing():
            if not self.cameras.IsGrabbing():
                break

            try:
                grabResult = self.cameras.RetrieveResult(200, pylon.TimeoutHandling_ThrowException)

                # When the cameras in the array are created the camera context value
                # is set to the index of the camera in the array.
                # The camera context is a user settable value.
                # This value is attached to each grab result and can be used
                # to determine the camera that produced the grab result.
                cameraContextValue = grabResult.GetCameraContext()

                if grabResult.GrabSucceeded():
                    image = self.converter.Convert(grabResult)  # Access the openCV image data

                    if cameraContextValue == 0:  # If camera 0, save array into img0[]
                        img0 = image.GetArray()
                    else:  # if camera 1, save array into img1[]
                        img1 = image.GetArray()

                    # If there is no img1, the first time, make img1=img0
                    # Need the same length arrays to concatenate
                    if len(img1) == 0:
                        img1 = img0

                    img0_zoom = cv2.resize(img0[800:1100, 1800:2300], dsize=(2448, 1000), interpolation=cv2.INTER_CUBIC)
                    img1_zoom = cv2.resize(img1[1100:1300, 1000:1500], dsize=(2448, 1000),
                                           interpolation=cv2.INTER_CUBIC)
                    # numpy_horizontal = np.hstack((img0, img1))
                    img0_f = np.concatenate((img0, img0_zoom), axis=0)
                    img1_f = np.concatenate((img1, img1_zoom), axis=0)
                    vis = np.concatenate((img0_f, img1_f), axis=1)  # Combine 2 images horizontally
                    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
                    cv2.resizeWindow(windowName, 2500, 1200)
                    cv2.imshow(windowName, vis)  # displays image in specified window
                    k = cv2.waitKey(1)
                    if k == 27:  # If press ESC key
                        print('ESC')
                        cv2.destroyAllWindows()
                        break
            except:
                pass
            grabResult.Release()
            time.sleep(0.05)

            # If window has been closed using the X button, close program
            # getWindowProperty() returns -1 as soon as the window is closed
            if cv2.getWindowProperty(windowName, 0) < 0 or variables.light_swich == False:
                grabResult.Release()
                cv2.destroyAllWindows()
                break



