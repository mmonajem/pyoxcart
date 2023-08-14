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
	This class is used to control the BASLER Cameras.
	"""

	def __init__(self, devices, tlFactory, cameras, converter, variables, emitter):
		"""
		Constructor function which initializes and setups all variables
		and parameters for the class.
		"""

		self.devices = devices
		self.tlFactory = tlFactory
		self.cameras = cameras
		self.converter = converter
		self.variables = variables
		self.emitter = emitter
		self.cameras[0].Open()
		self.cameras[0].ExposureAuto.SetValue('Off')
		self.cameras[0].ExposureTime.SetValue(800000)
		self.cameras[1].Open()
		self.cameras[1].ExposureAuto.SetValue('Off')
		self.cameras[1].ExposureTime.SetValue(100000)

		self.thread_read = Thread(target=self.camera_s_d)
		self.thread_read.daemon = True
		self.index_save_image = 0

	def update_cameras(self):
		"""
		This class method sets up the cameras to capture the required images.
		"""
		self.thread_read.start()

		self.cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
		start_time = time.time()
		while self.cameras.IsGrabbing():
			current_time = time.time()
			elapsed_time = current_time - start_time

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
			# Define the region to crop: (x, y, width, height)
			crop_region = (1640, 900, 300, 100)
			# Crop the image
			self.img0_zoom = self.img0_orig[crop_region[1]:crop_region[1] + crop_region[3],
			                 crop_region[0]:crop_region[0] + crop_region[2]]

			self.img1_orig = img1
			# Define the region to crop: (x, y, width, height)
			crop_region = (2050, 1000, 300, 100)
			# Crop the image
			self.img1_zoom = self.img1_orig[crop_region[1]:crop_region[1] + crop_region[3],
			                 crop_region[0]:crop_region[0] + crop_region[2]]

			# Acquire the lock and releases after process using context manager
			# To ensure that the marked array is a C-contiguous array

			self.emitter.img0_zoom.emit(np.swapaxes(self.img0_zoom, 0, 1))
			self.emitter.img1_zoom.emit(np.swapaxes(self.img1_zoom, 0, 1))

			# Interchange two axes of an array.
			self.emitter.img0_orig.emit(np.swapaxes(self.img0_orig, 0, 1))
			self.emitter.img1_orig.emit(np.swapaxes(self.img1_orig, 0, 1))

			# Store the captured processed image at a desired location.
			# with self.variables.lock_statistics:
			if elapsed_time >= self.variables.save_meta_interval and self.variables.start_flag:
				start_time = current_time  # Update the start time
				cv2.imwrite(self.variables.path_meta + "/side_%s.png" % self.index_save_image, self.img0_orig)
				cv2.imwrite(self.variables.path_meta + "/side_zoom_%s.png" % self.index_save_image, self.img0_zoom)
				cv2.imwrite(self.variables.path_meta + '/bottom_%s.png' % self.index_save_image, self.img1_orig)
				cv2.imwrite(self.variables.path_meta + '/bottom_zoom_%s.png' % self.index_save_image,
				            self.img1_zoom)
				self.index_save_image += 1
				start_time = time.time()

			grabResult0.Release()
			grabResult1.Release()

			if self.variables.start_flag:
				time.sleep(0.5)
			else:
				time.sleep(0.1)

			# with self.variables.lock_setup_parameters:
			if not self.variables.flag_camera_grab:
				break

	def light_switch(self):
		"""
		This class method sets the Exposure time based on a flag.
		"""

		# with self.variables.lock_setup_parameters:
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
		This class method captures the images through the cameras,
		processes them and displays the processed image.
		"""

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
			if not self.variables.flag_camera_grab:
				break
