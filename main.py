from classes.URARM import URARM
from classes.Gripper import Gripper
from classes.ConveyorBelt import ConveyorBelt
from classes.VisionSystem import VisionSystem
import time
import math
import socket

def main():
    # Define IP addresses for the robot, vision system, and conveyor belt
    robot_ip = '10.10.0.14'
    vs_ip = '10.10.1.10'
    conv_ip = '0.0.0.0'

    # Initialize the robot, gripper, conveyor belt, and vision system
    robot = URARM(robot_ip)
    gripper = Gripper(robot_ip)
    vision = VisionSystem(vs_ip)


    # Move the robot to the home position
    robot.move_home()
    # robot.get_current_joint_angle();

    # Initialize the conveyor belt
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.bind((conv_ip, 2002))
    c.listen(1)
    print("Conveyor belt socket is listening")
    conv, addr = c.accept()
    print(f"Connected by {addr}")
    conv.sendall(b'activate,tcp\n')
    time.sleep(1)
    conv.sendall(b'pwr_on,conv,0\n')
    time.sleep(1)
    conv.sendall(b'set_vel,conv,30\n')
    time.sleep(1)
    conv.sendall(b'jog_fwd,conv,0\n')
    # time.sleep(3)
    # conv.sendall(b'jog_stop,conv,0\n')
    # conveyor = ConveyorBelt(conv_ip)
    # time.sleep(5)  # Wait for the conveyor to start
    # conveyor.stop()  # Stop the conveyor belt

    # Get and process the x, y coordinates and orientation of the object from the vision system
    x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2 = vision.receive_data()
    degree, x_coor, y_coor = vision.find_coords(x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2)
    x_coor_rel, y_coor_rel = vision.offset_camera(x_coor, y_coor)
    print(f"Degree: {degree}, x_coor: {x_coor_rel}, y_coor: {y_coor_rel}")

    # Move the robot to the object location and pick up the object
    robot.grab_after_t(x_rel=x_coor_rel, y_rel=y_coor_rel, rz=-degree, t1=0.7, t2=0.7, t3=0.7, t4=0.7)
    # robot.rotate_TCP(rz=-degree)
    # robot.movel(URARM.relative_pose(z=-0.17)) # Move down to allow movement to the object (might remove if not needed)
    # robot.movel(URARM.relative_pose(x=x_coor_rel, y=y_coor_rel))
    # robot.movel(URARM.relative_pose(z=-0.16))
    gripper.control_gripper(True)
    # robot.movel(URARM.relative_pose(z=0.16))
    robot.move_home()

    print(conv)
    conv.sendall(b'jog_stop,conv,0\n')
    time.sleep(1)
    print(conv.recv(1024).decode())

def home():
    # Define IP addresses for the robot, vision system, and conveyor belt
    robot_ip = '10.10.0.14'


    # Initialize the robot, gripper, conveyor belt, and vision system
    robot = URARM(robot_ip)


    # Move the robot to the home position
    time.sleep(2)
    # robot.move_home()
    robot.get_current_joint_angle();


if __name__ == '__main__':
    main()
    # home()
