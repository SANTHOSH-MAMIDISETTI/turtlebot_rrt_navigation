#!/usr/bin/env python

import rospy
import numpy as np
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def load_grid(grid_path):
    grid = np.load(grid_path)
    return grid

def is_collision_free(grid, point):
    x, y = point
    if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
        return grid[x, y] == 0
    return False

def rrt(grid, start, goal, max_iter=500):
    tree = {start: None}
    for _ in range(max_iter):
        random_point = (np.random.randint(grid.shape[0]), np.random.randint(grid.shape[1]))
        if not is_collision_free(grid, random_point):
            continue
        nearest_node = min(tree.keys(), key=lambda n: np.linalg.norm(np.array(n) - np.array(random_point)))
        new_node = random_point
        if is_collision_free(grid, new_node):
            tree[new_node] = nearest_node
        if np.linalg.norm(np.array(new_node) - np.array(goal)) < 2:
            tree[goal] = new_node
            break
    path = []
    node = goal
    while node:
        path.append(node)
        node = tree[node]
    return path[::-1]

def navigate_waypoints(waypoints):
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)
    for waypoint in waypoints:
        move_to_waypoint(pub, waypoint)
    rospy.loginfo("Navigation complete")

def move_to_waypoint(pub, waypoint):
    msg = Twist()
    msg.linear.x = 0.2
    pub.publish(msg)

if __name__ == '__main__':
    rospy.init_node('rrt_planner')
    grid_path = rospy.get_param('~grid')
    goal_position = rospy.get_param('~goal_position')
    
    grid = load_grid(grid_path)
    start = (1, 1)
    goal = tuple(goal_position)

    rospy.loginfo("Planning path...")
    waypoints = rrt(grid, start, goal)
    rospy.loginfo(f"Path planned: {waypoints}")

    rospy.loginfo("Navigating...")
    navigate_waypoints(waypoints)
