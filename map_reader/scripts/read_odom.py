#!/usr/bin/env python

import rospy
import yaml
import geometry_msgs.msg
from geometry_msgs.msg import PoseWithCovarianceStamped
import tf
import rospkg

def main():
	rospy.init_node('odom_reader', anonymous=True)
	rospack = rospkg.RosPack() # Find rospackge locations
	listener = tf.TransformListener()

	with open(rospack.get_path('map_reader')+'/mapCoords.yaml', 'r') as f:
    		doc = yaml.load(f)
	f.close()
	
	arenaPnt1 = doc["arenaTopLeft"]
	arenaPnt2 = doc["arenaBotRight"]

	rospy.set_param("/arenaPnt1", arenaPnt1)
	rospy.set_param("/arenaPnt2", arenaPnt2)

	badSquare1 = doc["deadZoneTopLeft"]
	badSquare2 = doc["deadZoneBotRight"]

	rospy.set_param("/deadZone1", badSquare1)
	rospy.set_param("/deadZone2", badSquare2)

	rospy.set_param("/currentRobotR", 0.0)

	rate = rospy.Rate(10.0)
 	while not rospy.is_shutdown():
		try:
 			(trans, rotate) = listener.lookupTransform('/odom', '/base_link', rospy.Time(0))
 		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
 			continue

		euler = tf.transformations.euler_from_quaternion(rotate)
 		
 		roboX = trans[0]
 		roboY = trans[1]
		roboR = euler[2]
		print roboX
		print roboY
		print roboR
 
 		rospy.set_param("/currentRobotX", roboX)
 		rospy.set_param("/currentRobotY", roboY)
		rospy.set_param("/currentRobotR", roboR)
 
 		rate.sleep()

if __name__ == '__main__': main()
