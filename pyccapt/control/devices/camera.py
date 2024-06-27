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
		try:
			# Limits the amount of cameras used for grabbing.
			# The bandwidth used by a FireWire camera device can be limited by adjusting the packet size.
			maxCamerasToUse = 2
			# The exit code of the sample application.
			exitCode = 0
			# Get the transport layer factory.
			self.tlFactory = pylon.TlFactory.GetInstance()
			# Get all attached devices and exit application if no device is found.
			self.devices = self.tlFactory.EnumerateDevices()

			if len(self.devices) == 0:
				raise pylon.RuntimeException("No camera present.")

			# Create an array of instant cameras for the found devices and avoid exceeding a maximum number of
			# devices.
			self.cameras = pylon.InstantCameraArray(min(len(self.devices), maxCamerasToUse))

			# Create and attach all Pylon Devices.
			for i, cam in enumerate(self.cameras):
				cam.Attach(self.tlFactory.CreateDevice(self.devices[i]))
			self.converter = pylon.ImageFormatConverter()

			# converting to opencv bgr format
			self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
			self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
		except Exception as e:
			print('Error in initializing the camera class')
			print(e)

		self.variables = variables
		self.emitter = emitter
		self.cameras[0].Open()
		self.cameras[0].ExposureAuto.SetValue('Off')
		self.cameras[0].ExposureTime.SetValue(400000)
		self.cameras[1].Open()
		self.cameras[1].ExposureAuto.SetValue('Off')
		self.cameras[1].ExposureTime.SetValue(1000000)

		self.index_save_image = 0

	def update_cameras(self):
		"""
		This class method sets up the cameras to capture the required images.

		Args:
			None

		Return:
			None
		"""

		self.cameras.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
		start_time = time.time()
		while self.cameras.IsGrabbing():
			current_time = time.time()

			try:
				# Fetch the raw images from camera
				grabResult0 = self.cameras[0].RetrieveResult(8000, pylon.TimeoutHandling_ThrowException)
				grabResult1 = self.cameras[1].RetrieveResult(8000, pylon.TimeoutHandling_ThrowException)
				image0 = self.converter.Convert(grabResult0)
				img0 = image0.GetArray()
				image1 = self.converter.Convert(grabResult1)
				img1 = image1.GetArray()
			except Exception as e:
				print(f"Error in grabbing the images from the camera: {e}")
				continue



			# Original size is 2048 * 2448
			# Resize the original to the required size. Utilize the openCV tool.
			self.img0_orig = img0

			# Define the region to crop: (x, y, width, height) side camera
			crop_region = (1100, 900, 500, 200)
			# Crop the image
			self.img0_zoom = self.img0_orig[crop_region[1]:crop_region[1] + crop_region[3],
			                 crop_region[0]:crop_region[0] + crop_region[2]]

			self.img1_orig = img1
			# Rotate img1_orig by 90 degrees counter-clockwise
			self.img1_orig = cv2.rotate(self.img1_orig, cv2.ROTATE_90_CLOCKWISE)
			# Define the region to crop: (x, y, width, height) bottom camera
			crop_region = (600, 1300, 800, 400)
			# Crop the image
			self.img1_zoom = self.img1_orig[crop_region[1]:crop_region[1] + crop_region[3],
			                 crop_region[0]:crop_region[0] + crop_region[2]]

			self.emitter.img0_zoom.emit(np.swapaxes(self.img0_zoom, 0, 1))
			self.emitter.img1_zoom.emit(np.swapaxes(self.img1_zoom, 0, 1))

			# Interchange two axes of an array.
			self.emitter.img0_orig.emit(np.swapaxes(self.img0_orig, 0, 1))
			self.emitter.img1_orig.emit(np.swapaxes(self.img1_orig, 0, 1))

			if self.variables.clear_index_save_image:
				self.variables.clear_index_save_image = False
				self.index_save_image = 0
			# Store the captured processed image at a desired location.
			if current_time - start_time >= self.variables.save_meta_interval_camera and self.variables.start_flag:
				start_time = time.time()  # Update the start time
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

	def light_switch(self):
		"""
		This class method sets the Exposure time based on a flag.

		Args:
			None

		Return:
			None
		"""
		try:
			# set the exposure time to see sharp images
			if self.variables.light:
				self.cameras[0].Open()
				self.cameras[0].ExposureTime.SetValue(200)
				self.cameras[1].Open()
				self.cameras[1].ExposureTime.SetValue(10000)
			elif not self.variables.light:
				self.cameras[0].Open()
				self.cameras[0].ExposureTime.SetValue(400000)
				self.cameras[1].Open()
				self.cameras[1].ExposureTime.SetValue(1000000)
		except Exception as e:
			print(f"Error in switching the light: {e}")



def cameras_run(variable, emmiter):
	"""
	This function is used to run the cameras.

	Args:
		variable: The class object of the Variables class.
		emmiter: The class object of the Emitter class.
	Return:
		None
	"""
	camera = Cameras(variable, emmiter)
	camera.update_cameras()
