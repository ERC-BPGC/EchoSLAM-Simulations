#! /usr/bin/env python

"""TODO:
	1. understand tis bot server thing lmao
	2. comments for robot class
	3. robot.ori + trilateration implementation
	4. 
"""


from echoslam_ros.msg import Bot #28/08/2020 : Aditya changed echoslam to echoslam_ROS in this line.
from echoslam_ros.srv import *
from std_msgs.msg import Int32
import sys
import rospkg
import rospy
import getopt
import numpy as np 
from random import random

rospack = rospkg.RosPack()
path = rospack.get_path('echoslam_ROS')
sys.path.append(path)
from src.robot import Robot

###### 20/08/2020 : Aditya ?? what does this do?
def bot_server_client(request_obj):
	response_obj = bot_server_proxy(request_obj)
	#####ADD RANDOM ALGO HERE
	return response_obj
######

np.set_printoptions(precision=4)

rospy.wait_for_service('/bot_service')
bot_server_proxy = rospy.ServiceProxy('/bot_service', BotService)
robot = Robot(radius=0.2)			# create Robot object

def main():
	# procure teamsize and id from param server
	try:
		robot.teamsize = rospy.get_param("/size")
		robot.id = rospy.get_param("id")
	except KeyError as error:
		print('The parameter {} was not found'.format(error))
		print('Exiting...')
		sys.exit(2)

	robot.set_pose(bot_server_client(BotServiceRequest(Int32(robot.id)))) # ??
	robot.init_mic_array(num_mics=6, radius=0.1)
	robot.init_msg()							# must call before pub.publish(robot.msg)
	robot.init_comms()							# initialise node and pub/sub
	robot.print_details()	

	# bot1 will be initialised last, and it will start the msg chain
	if robot.id == 1:
		rospy.sleep(1.0)
		print('Bot1 initialising conversation...')
		robot.transmit()

	rospy.spin()

if __name__ == '__main__':
	main()
