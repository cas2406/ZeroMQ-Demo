import cv2
import imutils

class Camera:

	def __init__(self, cam_num, windows_name):
		self.windowName = windows_name
		self.camera = cv2.VideoCapture(cam_num)
		self.rotation = 0
		
		# Check if the webcam is opened correctly
		if not self.camera.isOpened():
		    raise IOError("Cannot open webcam")
		cv2.namedWindow(self.windowName, cv2.WINDOW_NORMAL)

	def GetFrame(self):
		ret_val, img = self.camera.read()
		img = imutils.rotate_bound(img, self.rotation)
		return img

	def SetRotation(self, angle):
		self.rotation = angle

	def GetWidth(self):
		return int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH ))

	def GetHeight(self):
		return int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

	def ShowFrame(self, img):
		cv2.imshow(self.windowName, img)
		cv2.waitKey(1)

	def Close(self):
		cv2.destroyAllWindows()
		self.camera.release()