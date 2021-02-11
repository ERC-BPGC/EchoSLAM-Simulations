from echoslam_ros.msg import Bot
# from echoslam.msg import Bot
import rospkg
import rospy
import random 
import numpy as np
from pointhelper import *
from trilaterate import *
import acoustics as ac 

class Robot:
	msg = None
	topic_name = '/RF'

	transmitter_pos = [0,0]	# position of transmitter wrt center of bot
	transmitted_wave = None
	
	def __init__(self, id=0, teamsize=1, radius=1, pos=(0,0), ori=0):
		self.id = id
		# self.bot_radius = rospy.get_param('/radius')
		self.teamsize = teamsize		# number of bots in a team
		self.bot_radius = radius		# radius of the circular bot
		self.pos = np.array(pos, dtype=np.float32)	# abs position of bot
		self.ori = ori					# angle of bot with x axis
	
	def init_comms(self):
		self.sub = rospy.Subscriber(self.topic_name, Bot, self.callback_RF)
		self.pub = rospy.Publisher(self.topic_name, Bot, queue_size=3)
		self.transmit_delay = 1.0		# time delay between transmissions, (seconds)
		rospy.init_node(self.get_bot_name())
		print('Starting {}...'.format(self.get_bot_name()))


	def init_mic_array(self, num_mics, radius=None, sampling_rate=44100, num_samples=200):
		if radius is None:
			marray_radius = self.bot_radius
		else:
			marray_radius = radius
		
		self.mic_array = ac.MicArray(num_mics, marray_radius,
								sampling_rate, num_samples, self.pos)

	# args are corners of rectangle in cartesian
	def init_random_pos(self, corner1, corner2):
		self.pos[0] = random.uniform(corner1[0], corner2[0])
		self.pos[1] = random.uniform(corner1[1], corner2[1])

	### 20/08/2020 : Aditya Bidwai
	def set_pose(self, response_obj):
		self.pos[0] = response_obj.bot.x.data
		self.pos[1] = response_obj.bot.y.data
	###

	# compile bot info into a message
	# must call 
	def init_msg(self):
		self.msg = Bot()
		self.msg.id.data = self.id
		self.msg.x.data = self.pos[0]
		self.msg.y.data = self.pos[1]

	def callback_RF(self, msg):
		# ignore messages sent by itself
		if msg.id.data != self.id:
			print(self.get_bot_name()+" callback:")

			source_pos = np.array((msg.x.data, msg.y.data))
			self.record_waveforms(source_pos)
			# tofs = robot.calc_TOFs()
			# est_src_pos = robot.trilaterate(tofs)
			print("Actual rel_src_pos = ", source_pos-self.pos)

		# check if bot that just transmitted is the one before
		if msg.id.data % self.teamsize == self.id - 1:
			rospy.sleep(self.transmit_delay)
			self.transmit()

	def get_bot_name(self):
		return 'bot' + str(self.id)

	def transmit(self):
		self.pub.publish(self.msg)

	def create_transmitted_wave(self, w_freq):
		self.transmitted_wave = ac.Waveform.sine(
				amp=1.0,
				freq=w_freq,
				sampling_rate=self.mic_array.sampling_rate,
				num_samples=self.mic_array.num_samples
			)
		return self.transmitted_wave
	
	def get_transmitted_wave(self):
		if self.transmitted_wave is None:
			self.create_transmitted_wave(1000)
		return self.transmitted_wave

	def record_waveforms(self, source_pos):
		tm_wave = self.get_transmitted_wave()
		self.mic_array.simulate_waveforms(source_pos, tm_wave)
		
		return self.mic_array.waveforms

	# # source_pos is 2D np.array of global position of other bot's transmitter
	# def getMicDOFs(self, source_pos):
	# 	micDOFs = []
	# 	for mic_pos in self.mic_array:
	# 		thisDOF = distance(mic_pos+self.pos, source_pos)
	# 		micDOFs.append((mic_pos, thisDOF))

	# 	return micDOFs

	# returns 2D vector of relative position of other robot wrt this robot
	# static method?
	def trilaterate(self, micDOFs):
		est_rel_pos = geo_trilaterate(micDOFs)
		return est_rel_pos

	def print_details(self):
		print(self.get_bot_name() + " details:")
		print("\t Pos: {}".format(self.pos))
		print("\t Radius: {}".format(self.bot_radius))

	



