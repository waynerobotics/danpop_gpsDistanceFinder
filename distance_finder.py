#!/usr/bin/env python

from math import sqrt
import math
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32

#create class for better data and pub/sub handling
class distance_finder:
    def __init__(self):
        #declare and define publish and subscriber topics within the self function
        self.pub = rospy.Publisher('distance_finder_chatter', Float32, queue_size=10)
        self.sub_current = rospy.Subscriber("utm_current", Odometry, self.currentCoordsCallback)
        self.sub_destination = rospy.Subscriber("utm_destination", Odometry, self.destinationCoordsCallback)
        
        #coord array stored in the object and updated as new data is recieved
        #[x1,y1,x2,y2]
        self.coords = [0,0,0,0]

    def destinationCoordsCallback(self, data):
        self.coords[2] = data.pose.pose.position.x
        self.coords[3] = data.pose.pose.position.y

    def currentCoordsCallback(self, data):
        self.coords[0] = data.pose.pose.position.x
        self.coords[1] = data.pose.pose.position.y

    def publishDistance(self):
        #log info into terminal
        rospy.loginfo("(%f,%f) ---> (%f,%f)" % (self.coords[0], self.coords[1], self.coords[2], self.coords[3]))
        #calculate distance with UTM coords
        distance = sqrt(pow(self.coords[2] - self.coords[0], 2) + pow(self.coords[3] - self.coords[1], 2))
        #publish distance
        self.pub.publish(distance)

if __name__ == '__main__':
    try:
        rospy.init_node('distance_finder', anonymous=True)
        myNode = distance_finder()
        r = rospy.Rate(10)
        #publish distance float every 10hz
        while not rospy.is_shutdown():
            myNode.publishDistance()
            r.sleep()
    except rospy.ROSInterruptException:
        pass
