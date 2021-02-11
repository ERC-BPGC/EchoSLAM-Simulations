#! /usr/bin/env python

import random
import sys
from math import sqrt

import rospkg
import rospy
from echoslam_ros.srv import BotService, BotServiceResponse


rospack = rospkg.RosPack()
path = rospack.get_path("echoslam_ros")
sys.path.append(path)
from src.robot import Robot

bots = rospy.get_param("/size")
radius = rospy.get_param("/radius")
pose_list = []


def pose_generator():
    global pose_list
    dist_list = []
    i = 0
    distance = lambda point: sqrt(
        (pose_list[i][0] - point[0]) ** 2 + (pose_list[i][1] - point[1]) ** 2
    )
    point = [bots * random.random(), bots * random.random()]
    if len(pose_list) == 0:
        pose_list.append(point)
        return point
    for i in range(len(pose_list)):
        dist_list.append(distance(point))
    while min(dist_list) <= 2 * radius:
        point = [bots * random.random(), bots * random.random()]
        for i in range(len(pose_list)):
            dist_list[i] = distance(point)
    pose_list.append(point)
    return point


response_obj = BotServiceResponse()


def bot_server(request_obj):
    response_obj.bot.x.data = pose_generator()[0]
    response_obj.bot.y.data = pose_generator()[1]
    response_obj.bot.id.data = request_obj.id.data

    print("Server generated reponse:")
    print_response(response_obj)
    ###ADD RANDOM NUMBER ALGO HERE
    return response_obj

def print_response(response_obj):
    print("\t id: {}".format(response_obj.bot.id.data))
    print("\t x: {}".format(response_obj.bot.x.data))
    print("\t y: {}".format(response_obj.bot.y.data))
    
rospy.init_node("bot_server_node")
bot_service = rospy.Service("/bot_service", BotService, bot_server)
print("#######################")
print("BOT-SERVER INITIALIZED")
print("#######################")
rospy.spin()
