#! /usr/bin/env python 

import rospy 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from echoslam_ros.msg import Bot 

rospy.init_node("plotter_node")
bots = rospy.get_param("/size")
bot_x = []
bot_y = []

for i in range(bots):
	bot_x.append(i)
	bot_y.append(i)

def callback(msg):
	global bot_x
	global bot_y
	bot_x[msg.id.data - 1] = msg.x.data
	bot_y[msg.id.data - 1] = msg.y.data

sub = rospy.Subscriber("/RF", Bot, callback)

plt.axis([0, bots, 0, bots])
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Position Visualization Plot")

while not rospy.is_shutdown():
	plt.plot(bot_x, bot_y, 'ro')
	plt.pause(0.1)
	plt.clf()
	
