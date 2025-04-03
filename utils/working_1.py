import socket, struct , time ,os , math , numpy as np
from scipy.spatial.transform import Rotation as R

v_x = 0
v_y = 0

robot_ip        = '10.10.0.14'       #UR3 .14  UR5 .26
robot_port      = 30003              ####RTDE
gripper_port    = 63352
vs_ip           = '10.10.1.10'
vs_port         = 2023
conv_ip         = '10.10.0.98'
conv_port       = 2002


joint_speed = 0.1

# Robot arm connection and functions
def robot_connection() :

        global arm
        
        ####Establish connection to controller
        arm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        arm.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        arm.connect((robot_ip, robot_port))
        arm_recv = arm.recv(4096)
        if arm_recv :
                print('Connected to Robot RTDE....SUCCESSFULLY!')
        else :
                print('Connected to Robot RTDE...FAILED!')

def robot_home() :
        ##vs ref pos
        global arm
        print('Robot start moveing')
        moveX  = 0.116
        moveY  = -0.300
        moveZ  = 0.02
        moveRx = 2.233
        moveRy = 2.257
        moveRz = -0.039

        cmd_move = str.encode('movej(p['+str(moveX)+','+str(moveY)+','+str(moveZ)+','+str(moveRx)+','+str(moveRy)+','+str(moveRz)+'],0.5,0.5,0,0)\n')
        print (cmd_move)
        arm.send(cmd_move)
        time.sleep(5)
 
def relative_pose(x: float = 0, y: float = 0, z: float = 0, rx: str | float = 0, ry: str | float = 0, rz: str | float = 0) -> str:
        return f"pose_add(get_actual_tcp_pose(), p[{x},{y},{z},{rx},{ry},{rz}])"

def relative_joint(x: float = 0, y: float = 0, z: float = 0, rx: str | float = 0, ry: str | float =0, rz: str | float = 0) -> str:
        return f"pose_add(get_actual_joint_positions())"

def movel(pose, a: float = 0.5, v: float = 0.5, t: float = 0, r: float = 0) -> None:
        global arm
        print(f"movel({pose},{a},{v},{t},{r})\n")
        arm.send(f"movel({pose},{a},{v},{t},{r})\n".encode("UTF-8"))
        time.sleep(1.5)

def movej(pose, a: float = 0.5, v: float = 0.5, t: float = 0, r: float = 0) -> None:
        global arm
        arm.send(f"movej({pose},{a},{v},{t},{r})\n".encode("UTF-8"))
        time.sleep(1)

def pose(x: float, y: float, z: float, rx: float, ry: float, rz: float):
        return f"p[{x},{y},{z},{rx},{ry},{rz}]"

# Gripper connection and functions
def gripper_connection() :
   global g
   #Socket communication
   g = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   g.connect((robot_ip, gripper_port))
   g.sendall(b'GET POS\n')
   g_recv = str(g.recv(10), 'UTF-8')
   if g_recv :
      g.send(b'SET ACT 1\n')
      g_recv = str(g.recv(10), 'UTF-8')
      print (g_recv)
      time.sleep(3)
      g.send(b'SET GTO 1\n')
      g.send(b'SET SPE 255\n')
      g.send(b'SET FOR 255\n')
      print ('Gripper Activated')

def control_gripper(activate: bool):
        g.send(f"SET POS {255 if activate else 0}\n".encode("UTF-8"))
        time.sleep(1)
        g_recv = str(g.recv(255), "UTF-8")
        print(g_recv)

# Conveyer belt connection and functions
def conv_connection():
        global c
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.bind((conv_ip, conv_port))
        print("socket binded to %s" %(conv_port))
        c.listen(1)
        print("socket is listening")
        conv, addr = c.accept()
        with conv:
                print(f"Connected by {addr}")
                conv.sendall(b'activate,tcp,0.0\n')
                time.sleep(1)
                conv.sendall(b'pwr_on,conv,0\n')
                time.sleep(1)
                conv.sendall(b'set_vel,conv,20\n')
                time.sleep(5)
                #conv.sendall(b'commands\n')
                #time.sleep(1)
                conv.sendall(b'jog_fwd,conv,0\n')
                time.sleep(1)
                conv.sendall(b'jog_stop,conv,0\n')
                time.sleep(1)
                conv.sendall(b'pwr_off,conv,0\n')
                time.sleep(1)
                conv_recv = conv.recv(100)
                print(conv_recv)

def conv_direction(forward: bool):
        if forward:
                c.send(b'jog_fwd,conv,0\n')
        else:
                c.send(b'jog_bwd,conv,0\n')

def conv_stop():
        c.send(b'jog_stop,conv,0\n')

def conv_set_speed(speed: int):
        c.send(f'set_vel,conv,{speed}\n'.encode('UTF-8'))

# Vision system connection and functions
def vs_connection():

        ####Establish connection to vision system
        global v
        v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        v.connect((vs_ip, vs_port))
        if v.connect :
                print ('Connected to Vision system ....SUCCESSFULLY!')

# Format of the data received from VS is [x, y, rz]
def vs_recv():
        v_data = ''
        while v_data == '':
                print('send start to cvs')
                v.send(b'start!')
                v_data = v.recv(100)
        
        coor_str = str(v_data, 'UTF-8')
        print(coor_str)
        # Extract variables from the formatted string
        import re
        match = re.match(
            r"<\(([^,]+),([^,]+),([^,]+)\),\(([^,]+),([^,]+),([^,]+)\),\(([^,]+),([^,]+)\),\(([^,]+),([^,]+)\)>",
            coor_str
        )
        if match:
                x_x1, x_x2, x_ang = map(float, match.group(1, 2, 3))
                xc_x1, xc_x2, xc_ang = map(float, match.group(4, 5, 6))
                y_y1, y_y2 = map(float, match.group(7, 8))
                yc_y1, yc_y2 = map(float, match.group(9, 10))
                
                # Print the extracted variables in a human-readable format
                # print("Extracted Variables:")
                # print(f"x_x1: {x_x1}, x_x2: {x_x2}, x_ang: {x_ang}")
                # print(f"xc_x1: {xc_x1}, xc_x2: {xc_x2}, xc_ang: {xc_ang}")
                # print(f"y_y1: {y_y1}, y_y2: {y_y2}")
                # print(f"yc_y1: {yc_y1}, yc_y2: {yc_y2}")
                
                return x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2
        else:
                raise ValueError("Received data format is invalid")

def find_coords(x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2):
        degree = (x_ang + xc_ang) / 2
        print(degree)
        degree_rad = round(((x_ang + xc_ang) / 2) * (math.pi / (180)), 4)
        x_coor = (((xc_x1 + xc_x2) / 2) + ((x_x1 + x_x2) / 2)) / 2
        y_coor = (((yc_y1 + yc_y2) / 2) + ((y_y1 + y_y2) / 2)) / 2
        print(f"Degree: {degree}, x_coor: {x_coor}, y_coor: {y_coor}")
        return degree_rad, x_coor, y_coor

def offset_camera(x_coor, y_coor):
        x_coor_robot = (y_coor + 160) / 1000
        y_coor_robot = - x_coor / 1000
        print(f"Offset x_coor: {x_coor_robot}, y_coor: {y_coor_robot}")
        return x_coor_robot, y_coor_robot

def test_vs():
        vs_connection()
        robot_connection()
        gripper_connection()
        # robot_home()

        # while True:
        x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2 = vs_recv()
        degree, x_coor, y_coor = find_coords(x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2)
        x_coor_robot, y_coor_robot = offset_camera(x_coor, y_coor)
        print(f"Degree: {degree}, x_coor_robot: {x_coor_robot}, y_coor_robot: {y_coor_robot}")
        arm.send(b"get_actual_joint_positions()\n")
        arm_recv = arm.recv(1108)
        joint_positions = struct.unpack('!6d', arm_recv[252:300])
        print(joint_positions)
        # movel(f'[{joint_positions[0]},{joint_positions[1]},{joint_positions[2]},{joint_positions[3]},{joint_positions[4]},{joint_positions[5]-degree}]')
        # movel(relative_pose(z=-0.1))
        # movel(relative_pose(x=x_coor_robot, y=y_coor_robot))
        # movel(relative_pose(z=-0.16))
        # control_gripper(True)
        # movel(relative_pose(z=0.16))
        # robot_home()
        time.sleep(1)

def grab_linear(x: float, y:float, rz: float):
        print('Grabbing the object...')
        movel(pose(x, y, 0.07, 2.233, 2.257, rz))
        movel(relative_pose(0, 0, -0.03, 0, 0, 0))
        control_gripper(True)
        movel(relative_pose(0, 0, 0.03, 0, 0, 0))

def test():
        print("Begin testing system...")
        # robot_connection()
        # print("----------------------")
        # gripper_connection()
        # print("----------------------")
        conv_connection()
        print("----------------------")
        
        while True:
                user_input = input("Press '1' for Robot arm control\n'2' for Gripper control\n'3' for Conveyer belt control\nPress 'X' to exit\n")
                if user_input.upper() == 'X':
                        print("Exiting the test function...")
                        break
                elif user_input == '1':
                        # Robot arm control
                        print("Robot arm control")
                        user_input = input("Press '0' to move robot arm to home\n'1' to movel robot arm with relative position\n'2' to movej robot arm with relative position\n")
                        if user_input == '0':
                                robot_home()
                        elif user_input == '1':
                                x = float(input("Enter x: "))
                                y = float(input("Enter y: "))
                                z = float(input("Enter z: "))
                                rx = float(input("Enter rx: "))
                                ry = float(input("Enter ry: "))
                                rz = float(input("Enter rz: "))
                                movel(relative_pose(x, y, z, rx, ry, rz))
                        elif user_input == '2':
                                x = float(input("Enter x: "))
                                y = float(input("Enter y: "))
                                z = float(input("Enter z: "))
                                rx = float(input("Enter rx: "))
                                ry = float(input("Enter ry: "))
                                rz = float(input("Enter rz: "))
                                movej(relative_pose(x, y, z, rx, ry, rz))
                        elif user_input == '3':
                                movel(pose(0.05, -0.3, 0.07, 2.233, 2.257, -0.039))

                elif user_input == '2':
                        # Gripper control
                        print("Gripper control")
                        user_input = input("Press '1' to activate gripper\n'0' to deactivate gripper\n")
                        if user_input == '1':
                                control_gripper(True)
                        elif user_input == '0':
                                control_gripper(False)
                elif user_input == '3':
                        # Conveyer belt control
                        print("Conveyer belt control")
                        user_input = input("Press '0' to deactivate conveyer belt\n'1' to activate conveyer belt forward\n'2' to activate conveyer belt backward\n'3' to set conveyer belt speed\n")
                        if user_input == '0':
                                conv_stop()
                        elif user_input == '1':
                                conv_direction(True)
                        elif user_input == '2':
                                conv_direction(False)
                        elif user_input == '3':
                                speed = int(input("Enter speed: "))
                                conv_set_speed(speed)

def test_conv():
        conv_connection()
        print("----------------------")
              
if __name__ == '__main__':
    import sys
    # test()
    test_vs()
    # test_conv()

