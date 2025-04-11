from classes.URARM import URARM
from classes.Gripper import Gripper
from classes.ConveyorBelt import ConveyorBelt
from classes.VisionSystem import VisionSystem
import time
import math

def main():
    # Define IP addresses for the robot, vision system, and conveyor belt
    robot_ip = '10.10.0.14'
    vs_ip = '10.10.1.10'
    conv_ip = '0.0.0.0'

    # Initialize the robot, gripper, conveyor belt, and vision system
    robot = URARM(robot_ip)
    gripper = Gripper(robot_ip)
    # vision = VisionSystem(vs_ip)


    # Move the robot to the home position
    # robot.get_current_joint_angle();
    robot.move_home()
    robot.get_actual_tcp_pose()

    # Initialize the conveyor belt
    # conveyor = ConveyorBelt(conv_ip)
    # time.sleep(1)  # Wait for the conveyor to start

    # Get and process the x, y coordinates and orientation of the object from the vision system
    # x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2 = vision.receive_data()
    # degree, x_coor, y_coor = vision.find_coords(x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2)
    # x_coor_rel, y_coor_rel = vision.offset_camera(x_coor, y_coor)
    # print(f"Degree: {degree}, x_coor: {x_coor_rel}, y_coor: {y_coor_rel}")

    # Move the robot to the object location and pick up the object
    # degree = 10 * math.pi / 180
    # robot.rotate_TCP(rz=degree)
    # robot.movel(URARM.relative_pose(z=-0.1)) # Move down to allow movement to the object (might remove if not needed)
    # robot.movel(URARM.relative_pose(x=x_coor_rel, y=y_coor_rel))
    # robot.movel(URARM.relative_pose(z=-0.16))
    # gripper.control_gripper(True)
    # robot.movel(URARM.relative_pose(z=0.16))
    # robot.move_home()

if __name__ == '__main__':
    main()
