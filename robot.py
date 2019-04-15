import urx
import zmq
from urx import Robot
import atexit
import threading
import time

def exit_handler():
    try:
        print('[WARNING] shuttingdown')
        context.destroy()
        socket.close()
        rob.close()
    except:
        pass

#This is a blocking function
def GoToA(rob, acc, vel): # WARNING these are just some random coordinates, use with cautions
    rob.movej([1.3309369477972157, -0.0733355294156182, -0.2958665475683944, 1.3865948497915126, 1.556625095892939, -2.300487086253772], acc=acc, vel=vel)

#This is a blocking function
def GoToB(rob, acc, vel): # WARNING these are just some random coordinates, use with cautions
    rob.movej([1.6309369447972157, -1.0733355294156182, -2.2958665475683944, -1.3865948497915126, 1.556625095892939, -2.300487086253772], acc=acc, vel=vel)


if __name__ == "__main__":
    print('[INFO] Starting robot node')

    atexit.register(exit_handler)
    print('[INFO] registered exit handler')

    try:
        port = '5556'
        context = zmq.Context()
        socket = context.socket(zmq.PAIR)
        #socket.connect("tcp://127.0.0.1:%s" % port) # use local communication over network, can also be remote ip
        socket.connect('ipc:///tmp/stream.pipe') # use local inter process communication
        print('[INFO] created ZeroMQ Pair')
    except:
        print('[CRITICAL] Failed setting up ZeroMQ')
        exit()

    v = 0.6 #Robot velocity
    a = 0.4 #Robot accelerate 

    try:
        print('[INFO] Connecting to UR10 @ 192.168.0.5')
        #robot = urx.Robot("192.168.0.5", True)
        print('[INFO] Connected to UR10')
    except:
        print('[CRITICAL] failed to connect to UR10')
        exit()

    print('[INFO] Robot node ready')
    socket.send_string("%s" % ('robot_ready'))

    while True:
        try:
            #check for a message, this is a non-blocking function, so the rest of the while loop will keep running. 
            #any message that is received while the loop is past this try catch block will be placed in a queue and loaded when the loop restarts
            msg = socket.recv(flags=zmq.NOBLOCK)
            print ('[INFO] Robot node received: ', msg)
            if msg == b'MoveToA':
                #GoToA(robot, a ,v)
                time.sleep(4) #when not connected to an robot arm just use sleep to simulate the time it would take for the robot arm to move
                socket.send_string("%s" % ('robot_at_a'))
                socket.send_string("%s" % ('robot_ready'))
            elif msg == b'MoveToB':
                #GoToB(robot)
                time.sleep(4) 
                socket.send_string("%s" % ('robot_at_b'))
                socket.send_string("%s" % ('robot_ready'))
        except zmq.Again as e:
            pass
    
    