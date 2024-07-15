import time

import cv2
import numpy as np
from pypylon import pylon


class Cameras:
    """
    This class is used to control the BASLER Cameras.
    """

    def __init__(self, variables, emitter):
        """
        Constructor function which initializes and setups all variables
        and parameters for the class.

        Args:
            variables: The class object of the Variables class.
            emitter: The class object of the Emitter class.

        Return:
            None
        """
        self.variables = variables
        self.emitter = emitter
        self.index_save_image = 0

    def initialize_cameras(self):
        """
        Initializes and sets up the cameras.

        Args:
            None

        Return:
            None
        """
        try:
            maxCamerasToUse = 2
            self.tlFactory = pylon.TlFactory.GetInstance()
            self.devices = self.tlFactory.EnumerateDevices()

            if len(self.devices) == 0:
                raise pylon.RuntimeException("No camera present.")

            self.cameras = pylon.InstantCameraArray(min(len(self.devices), maxCamerasToUse))

            for i, cam in enumerate(self.cameras):
                cam.Attach(self.tlFactory.CreateDevice(self.devices[i]))
            self.converter = pylon.ImageFormatConverter()
            self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

            self.cameras[0].Open()
            self.cameras[0].ExposureAuto.SetValue('Off')
            self.cameras[0].ExposureTime.SetValue(400000)
            self.cameras[1].Open()
            self.cameras[1].ExposureAuto.SetValue('Off')
            self.cameras[1].ExposureTime.SetValue(1000000)
        except Exception as e:
            print('Error in initializing the camera class')
            print(e)

    def update_cameras(self):
        """
        This class method sets up the cameras to capture the required images.

        Args:
            None

        Return:
            None
        """
        retry_attempts = 5
        for attempt in range(retry_attempts):
            self.initialize_cameras()
            try:
                self.cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                start_time = time.time()
                while self.cameras.IsGrabbing():
                    current_time = time.time()
                    try:
                        grabResult0 = self.cameras[0].RetrieveResult(8000, pylon.TimeoutHandling_ThrowException)
                        grabResult1 = self.cameras[1].RetrieveResult(8000, pylon.TimeoutHandling_ThrowException)
                        image0 = self.converter.Convert(grabResult0)
                        img0 = image0.GetArray()
                        image1 = self.converter.Convert(grabResult1)
                        img1 = image1.GetArray()
                    except Exception as e:
                        print(f"Error in grabbing the images from the camera: {e}")
                        break

                    self.img0_orig = img0

                    crop_region = (1100, 900, 500, 200)
                    self.img0_zoom = self.img0_orig[crop_region[1]:crop_region[1] + crop_region[3],
                                     crop_region[0]:crop_region[0] + crop_region[2]]

                    self.img1_orig = img1
                    self.img1_orig = cv2.rotate(self.img1_orig, cv2.ROTATE_90_CLOCKWISE)
                    crop_region = (800, 1370, 800, 400)
                    self.img1_zoom = self.img1_orig[crop_region[1]:crop_region[1] + crop_region[3],
                                     crop_region[0]:crop_region[0] + crop_region[2]]

                    self.emitter.img0_zoom.emit(np.swapaxes(self.img0_zoom, 0, 1))
                    self.emitter.img1_zoom.emit(np.swapaxes(self.img1_zoom, 0, 1))

                    self.emitter.img0_orig.emit(np.swapaxes(self.img0_orig, 0, 1))
                    self.emitter.img1_orig.emit(np.swapaxes(self.img1_orig, 0, 1))

                    if self.variables.clear_index_save_image:
                        self.variables.clear_index_save_image = False
                        self.index_save_image = 0

                    if current_time - start_time >= self.variables.save_meta_interval_camera and self.variables.start_flag:
                        start_time = time.time()
                        path_meta = self.variables.path_meta
                        cv2.imwrite(path_meta + "/camera_side_%s.png" % self.index_save_image, self.img0_orig)
                        cv2.imwrite(path_meta + "/camera_side_zoom_%s.png" % self.index_save_image, self.img0_zoom)
                        cv2.imwrite(path_meta + '/camera_bottom_%s.png' % self.index_save_image, self.img1_orig)
                        cv2.imwrite(path_meta + '/camera_bottom_zoom_%s.png' % self.index_save_image, self.img1_zoom)
                        self.index_save_image += 1
                        time.sleep(0.5)

                    grabResult0.Release()
                    grabResult1.Release()

                    if self.variables.light_switch:
                        self.light_switch()
                        self.variables.light_switch = False

                    if self.variables.light:
                        time.sleep(0.5)
                    else:
                        time.sleep(0.2)

                    if not self.variables.flag_camera_grab:
                        break
                break  # Exit the retry loop if successful
            except Exception as e:
                print(f"Error during update_cameras attempt {attempt + 1}: {e}")
                self.initialize_cameras()
                time.sleep(1)

    def light_switch(self):
        """
        This class method sets the Exposure time based on a flag.

        Args:
            None

        Return:
            None
        """
        try:
            if self.variables.light:
                self.cameras[0].Open()
                self.cameras[0].ExposureTime.SetValue(10000)
                self.cameras[1].Open()
                self.cameras[1].ExposureTime.SetValue(10000)
            else:
                self.cameras[0].Open()
                self.cameras[0].ExposureTime.SetValue(400000)
                self.cameras[1].Open()
                self.cameras[1].ExposureTime.SetValue(1000000)
        except Exception as e:
            print(f"Error in switching the light: {e}")


def cameras_run(variable, emitter):
    """
    This function is used to run the cameras.

    Args:
        variable: The class object of the Variables class.
        emitter: The class object of the Emitter class.
    Return:
        None
    """
    camera = Cameras(variable, emitter)
    camera.update_cameras()
