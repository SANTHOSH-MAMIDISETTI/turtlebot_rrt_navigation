cmake_minimum_required(VERSION 3.0.2)
project(turtlebot_plan_nav)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  nav_msgs
  std_msgs
)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})
