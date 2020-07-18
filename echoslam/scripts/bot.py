#! /usr/bin/env python

from echoslam.msg import Bot
import rospy
import sys
import getopt
import json
from random import random


bot = Bot()
bot.id.data = None
bot.x.data = None
bot.y.data = None

bot_teamsize = None
bot_name = "bot1"


topic_name = "RF"

def callback(msg):
	#rospy.loginfo(msg.id.data, ': I heard', msg.x.data, msg.y.data)
	print "I am " + str(msg.id.data)
	print "I heard" + str(msg.x.data) + " " + str(msg.y.data) 

rospy.init_node(bot_name)
sub = rospy.Subscriber(topic_name, Bot, callback)
pub = rospy.Publisher(topic_name, Bot, queue_size=1)

if len(sys.argv) <=1:
	print('Please enter id and teamsize')
	sys.exit(2)

try:
	optlist, _ = getopt.getopt(sys.argv[1:], "i:n:", ['id=','teamsize=']) 
except getopt.GetoptError:
	print('Invalid args, exiting...')
	sys.exit(2)
for opt, arg in optlist:
	if opt in ('-i', '--id'):
		bot_id = int(arg)
	elif opt in ('-n', '--teamsize'):
		teamsize = int(arg)

if bot_id is None or teamsize is None:
	print('Please enter both id and teamsize')
	sys.exit(2)

bot.id.data = bot_id
bot.x.data = random()*10
bot.y.data= random()*10

rate=rospy.Rate(2)

while not rospy.is_shutdown():
	pub.publish(bot)
	rate.sleep()
