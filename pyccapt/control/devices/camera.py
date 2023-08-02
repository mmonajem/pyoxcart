"""
This is the main script for controlling the BASLER Cameras.
"""

import time
from threading import Thread

import cv2
import numpy as np
from pypylon import pylon


# Local module and scripts


class Camera:
    """
        This camera modules is designed to setup and initiate the camera in the installation.
        This camera module allows user to capture images using the installed cameras,
        process the image and display as per desired window size.
    """

    def __init__(self, devices, tlFactory, cameras, converter, variables):
        """
        Constructor function which intializes and setups all variables
        and parameter for the class.
        """

        self.devices = devices
        self.tlFactory = tlFactory
        self.cameras = cameras
        self.converter = converter
        self.variables = variables
        self.cameras[0].Open()
        self.cameras[0].ExposureAuto.SetValue('Off')
        self.cameras[0].ExposureTime.SetValue(800000)
        self.cameras[1].Open()
        self.cameras[1].ExposureAuto.SetValue('Off')
        self.cameras[1].ExposureTime.SetValue(100000)

        self.thread_read = Thread(target=self.camera_s_d)
        self.thread_read.daemon = True

    def update_cameras(self):
        """
        Note : Changed function to break it down into simpler functions

        This class method setup the cameras to capture the required images. It initiates
        image capture for all cameras attached starting with index 0.The grabbing
        set up for free-running continuous acquisition.

        Attributes:

        Returns:
            Does not return anything.
        """
        self.thread_read.start()

        self.cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        while self.cameras.IsGrabbing():

            # Fetch the raw images from camera
            grabResult0 = self.cameras[0].RetrieveResult(2000, pylon.TimeoutHandling_ThrowException)
            grabResult1 = self.cameras[1].RetrieveResult(2000, pylon.TimeoutHandling_ThrowException)

            image0 = self.converter.Convert(grabResult0)
            img0 = image0.GetArray()
            image1 = self.converter.Convert(grabResult1)
            img1 = image1.GetArray()

            # Original size is 2048 * 2448
            # Resize the original to the required size. Utilize the openCV tool.
            self.img0_orig = img0
            self.img0_zoom = cv2.resize(img0[750:1150, 1650:2250], dsize=(1200, 500),
                                        interpolation=cv2.INTER_CUBIC).astype(
                np.int32)

            # img1_orig = cv2.resize(img1, dsize=(2048, 2048), interpolation=cv2.INTER_CUBIC).astype(np.int32)
            self.img1_orig = img1
            self.img1_zoom = cv2.resize(img1[900:1250, 1800:2350], dsize=(1200, 500),
                                        interpolation=cv2.INTER_CUBIC).astype(
                np.int32)

            # The function cv::drawMarker draws a marker on a given position in the image.
            # first is x direction
            # second is y direction
            self.img0_zoom_marker = cv2.drawMarker(self.img0_zoom, (490, 280), (0, 0, 255),
                                                   markerType=cv2.MARKER_TRIANGLE_UP,
                                                   markerSize=40, thickness=2, line_type=cv2.LINE_AA)
            self.img1_zoom_marker = cv2.drawMarker(self.img1_zoom, (435, 300), (0, 0, 255),
                                                   markerType=cv2.MARKER_TRIANGLE_UP,
                                                   markerSize=40, thickness=2, line_type=cv2.LINE_AA)

            # Acquire the lock and releases after process using context manager
            # To ensure that the marked array is a C-contiguous array

            self.variables.img0_zoom = np.require(self.img0_zoom_marker, np.uint8, 'C')
            self.variables.img1_zoom = np.require(self.img1_zoom_marker, np.uint8, 'C')

            # Interchange two axes of an array.
            self.variables.img0_orig = np.swapaxes(self.img0_orig, 0, 1)
            self.variables.img1_orig = np.swapaxes(self.img1_orig, 0, 1)
            self.variables.index_save_image += 1

            # Store the captured processed image at a desired location.
            if self.variables.index_save_image % 100 == 0 and self.variables.start_flag:
                cv2.imwrite(self.variables.path + "/side_%s.png" % self.variables.index_save_image, self.img0_orig)
                cv2.imwrite(self.variables.path + "/side_zoom_%s.png" % self.variables.index_save_image, self.img0_zoom)
                cv2.imwrite(self.variables.path + '/bottom_%s.png' % self.variables.index_save_image, self.img1_orig)
                cv2.imwrite(self.variables.path + '/bottom_zoom_%s.png' % self.variables.index_save_image,
                            self.img1_zoom)

            grabResult0.Release()
            grabResult1.Release()
            if self.variables.start_flag == True:
                time.sleep(0.5)

    def light_switch(self, ):
        """
            This class method sets the Exposure time based on a flag.
            It reads the flag from the imported "variables" file.

            Attributes:
                Does not accept any arguments.
            Return:
                Does not return anything.
        """
        if not self.variables.light:
            self.cameras[0].Open()
            self.cameras[0].ExposureTime.SetValue(400)
            self.cameras[1].Open()
            self.cameras[1].ExposureTime.SetValue(2000)
            self.variables.light = True
        elif self.variables.light:
            self.cameras[0].Open()
            self.cameras[0].ExposureTime.SetValue(800000)
            self.cameras[1].Open()
            self.cameras[1].ExposureTime.SetValue(100000)
            self.variables.light = False

    def camera_s_d(self, ):
        """
        This class method captures the images through the cameras, processes it
        and displays the processed image. Utilizes OpenCv module and Numpy modules
        to process the captured image. Utilizes OpenCV module to display the captured
        image in a window.

        Attributes:
            Does not accept any arguments
        Return
            Does not return anything.
        """

        # # The exit code of the sample application.
        windowName = 'Sample Alignment'

        while True:
            if self.variables.alignment_window:

                img0_zoom = cv2.resize(self.img0_orig[850:1050, 1550:1950], dsize=(2448, 1000),
                                       interpolation=cv2.INTER_CUBIC)
                img1_zoom = cv2.resize(self.img1_orig[1020:1170, 1700:2050], dsize=(2448, 1000),
                                       interpolation=cv2.INTER_CUBIC)
                img0_zoom = cv2.drawMarker(img0_zoom, (2120, 600), (0, 0, 255),
                                           markerType=cv2.MARKER_TRIANGLE_UP,
                                           markerSize=80, thickness=2, line_type=cv2.LINE_AA)
                img1_zoom = cv2.drawMarker(img1_zoom, (2120, 560), (0, 0, 255),
                                           markerType=cv2.MARKER_TRIANGLE_UP,
                                           markerSize=80, thickness=2, line_type=cv2.LINE_AA)
                img0_f = np.concatenate((self.img0_orig, img0_zoom), axis=0)
                img1_f = np.concatenate((self.img1_orig, img1_zoom), axis=0)
                vis = np.concatenate((img0_f, img1_f), axis=1)  # Combine 2 images horizontally
                # # Label the window
                cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
                # Resize the window
                cv2.resizeWindow(windowName, 2500, 1200)
                # displays image in specified window
                cv2.imshow(windowName, vis)
                k = cv2.waitKey(1)
                if k == 27:
                    break

            else:
                cv2.destroyAllWindows()
                time.sleep(1)
                pass


