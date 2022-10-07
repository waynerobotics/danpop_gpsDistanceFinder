#!/usr/bin/env python
# license removed for brevity

import rospy
from nav_msgs.msg import Odometry
from random import randint, random
def gps_talker():
    pub_current = rospy.Publisher('utm_current', Odometry, queue_size=10)
    pub_destination = rospy.Publisher('utm_destination', Odometry, queue_size=10)
    rospy.init_node('dummy_gps_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    #create Odometry objects to fill with data and publish
    current_coords_to_pub = Odometry()
    destination_coords_to_pub = Odometry()
    rand_northing = 4651711.06
    rand_easting = 334361.18
    while not rospy.is_shutdown():
        rand_northing += 0.001
        rand_easting -= 0.001
        destination_northing = 4691041.66
        destination_easting = 329609.86
        gps_str = "{} {} {} {}".format(rand_northing, rand_easting, destination_northing, destination_easting)

        #fill coords_to_pub object with dummy data utilizing its position and orientation types 
        # for the purpose of storing 2 sets of coords in one object
        current_coords_to_pub.pose.pose.position.x = rand_northing
        current_coords_to_pub.pose.pose.position.y = rand_easting
        destination_coords_to_pub.pose.pose.position.x = destination_northing
        destination_coords_to_pub.pose.pose.position.y = destination_easting

        rospy.loginfo(gps_str)
        pub_current.publish(current_coords_to_pub)
        pub_destination.publish(destination_coords_to_pub)
        rate.sleep()

if __name__ == '__main__':
    try:
        gps_talker()
    except rospy.ROSInterruptException:
        pass
