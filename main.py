import cv2
import zmq
import atexit
from Camera import Camera

def exit_handler():
	try:
		print('[WARNING] shuttingdown')
		cam.Close()
		socket.close()
		context.destroy()
	except:
		pass

	


def RobotCanMoveToA(robot_ready, robot_current_position):
	if robot_ready == True and (robot_current_position == '' or robot_current_position != 'a'):
		return True
	else:
		return False

def RobotCanMoveToB(robot_ready, robot_current_position):
	if robot_ready == True and (robot_current_position == '' or robot_current_position != 'b'):
		return True
	else:
		return False


if __name__ == '__main__':
	print('[INFO] Starting up')

	atexit.register(exit_handler)
	print('[INFO] registered exit handler')

	print('[INFO] initializing camera')
	cam = Camera(0,'main_window')
	print('[INFO] done initializing camera')

	try:
		print('[INFO] Setting up ZeroMQ')
		port = "5556"
		context = zmq.Context()
		socket = context.socket(zmq.PAIR)
		#socket.bind('tcp://*:%s' % port) # use local communication over network, can also be remote ip
		socket.bind('ipc:///tmp/stream.pipe') # use local inter process communication [ONLY WORKS ON UNIX SYSTEMS]
		print('[INFO] Done setting up ZeroMQ')
	except:
		print('[CRITICAL] failed to setup ZeroMQ')
		exit()

	robot_ready = False
	robot_current_position = ''

	while True:
		try:
			#check for a message, this is a non-blocking function, so the rest of the while loop will keep running. 
			#any message that is received while the loop is past this try catch block will be placed in a queue and loaded when the loop restarts
			msg = socket.recv(flags=zmq.NOBLOCK)
			print ('[INFO] Main node received: ', msg)
			if msg == b'robot_ready':
				robot_ready = True
			elif msg == b'robot_at_b':
				robot_current_position = 'b'
			elif msg == b'robot_at_a':
				robot_current_position = 'a'

		except zmq.Again as e:
			pass

		img = cam.GetFrame()
		cam.ShowFrame(img)

		if RobotCanMoveToA(robot_ready, robot_current_position):
			socket.send_string("%s" % ('MoveToA'))
			robot_ready = False

		elif RobotCanMoveToB(robot_ready, robot_current_position):
			socket.send_string("%s" % ('MoveToB'))
			robot_ready = False