import socket
import time
import struct
import math

class URARM:

    HOME_X = 0.116
    HOME_Y = -0.300
    HOME_Z = 0.08
    HOME_RX = 2.233
    HOME_RY = 2.257
    HOME_RZ = -0.039 
    # HOME_JOINT = [-0.8062151114093226, -1.6997678915606897, -1.0278661886798304, -2.017801109944479, 1.5453407764434814, 2.3251354694366455]
    HOME_JOINT = [1.6437987089157104, -1.2341769377337855, 0.41770029067993164, -0.7451713720904749, -1.6114829222308558, 1.6332783699035645]
    ROTATE_TCP_SLEEP = 1
    MOVEL_SLEEP = 1.5
    TOTAL_SLEEP = ROTATE_TCP_SLEEP + (2 * MOVEL_SLEEP)
    # HOME_X = 0.116
    # HOME_Y = -0.300
    # HOME_Z = 0.2
    # HOME_RX = 126 * math.pi / 180
    # HOME_RY = 128 * math.pi / 180
    # HOME_RZ = 0
    # HOME_JOINT = [1.6437866687774658, -1.2342007795916956, 0.4176163673400879, -0.7450755278216761, -1.6113866011248987, 1.6333143711090088]

    def __init__(self, robot_ip: str, robot_port: int = 30003):
        print(self.TOTAL_SLEEP)
        self.arm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.arm.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.arm.connect((robot_ip, robot_port))
        arm_recv = self.arm.recv(4096)
        if arm_recv:
            print('Connected to Robot RTDE....SUCCESSFULLY!')
        else:
            print('Connected to Robot RTDE...FAILED!')

    def move_home(self):
        print('Robot start moving to home position')
        cmd_move = str.encode(f'movel(p[{self.HOME_X},{self.HOME_Y},{self.HOME_Z},{self.HOME_RX},{self.HOME_RY},{self.HOME_RZ}],a=0.5,v=0.5,t=1,r=0)\n')
        self.arm.send(cmd_move)
        time.sleep(5)

    def movel(self, pose, a: float = 0.5, v: float = 0.5, t: float = 0, r: float = 0):
        self.arm.send(f"movel({pose},{a},{v},{t},{r})\n".encode("UTF-8"))
        # time.sleep(self.MOVEL_SLEEP)
        if 0.75*t > 0:
            time.sleep(0.75*t)
        else:
            time.sleep(self.MOVEL_SLEEP)

    def movej(self, pose, a: float = 0.5, v: float = 0.5, t: float = 0, r: float = 0):
        self.arm.send(f"movej({pose},{a},{v},{t},{r})\n".encode("UTF-8"))
        if 0.75*t > 0:
            time.sleep(0.75*t)
        else:
            time.sleep(self.MOVEL_SLEEP)
        # time.sleep(1.5)
    
    def rotate_TCP(self, rx: float = 0, ry: float = 0, rz: float = 0, t: float = 0):
        self.movel(f'[{self.HOME_JOINT[0]},{self.HOME_JOINT[1]},{self.HOME_JOINT[2]},{self.HOME_JOINT[3] + rx},{self.HOME_JOINT[4] + ry},{self.HOME_JOINT[5] + rz}]', t=t)
        # time.sleep(self.ROTATE_TCP_SLEEP)
        if 0.75*t > 0:
            time.sleep(0.75*t)
        else:
            time.sleep(self.ROTATE_TCP_SLEEP)

    def get_current_joint_angle(self):
        self.arm.send(b"get_actual_joint_positions()\n")
        arm_recv = self.arm.recv(1108)
        joint_positions = struct.unpack('!6d', arm_recv[252:300])
        print("actual joint positions:", joint_positions)
        return joint_positions

    def get_actual_tcp_pose(self):
        self.arm.send(b"get_actual_tcp_pose()\n")
        arm_recv = self.arm.recv(1108)
        tcp_pose = struct.unpack("!6d", arm_recv[300+36*8:300+(36+6)*8])
        print("actual tcp pose:", tcp_pose)
        return tcp_pose

    def grab_after_t(self, x_rel: float, y_rel: float, rz: float, t1: float, t2: float, t3: float, t4: float):
        total_time = t1 + t2 + t3 + t4
        print("Total time:", total_time)
        x_m = x_rel - (0.02 * (total_time - 2.5))
        print("Meeting point:", x_m)
        self.rotate_TCP(rz=rz, t=t1)
        self.movel(URARM.relative_pose(z=-0.18), t=t2)
        self.movel(URARM.relative_pose(x=x_m, y=y_rel), t=t3)
        self.movel(URARM.relative_pose(z=-0.17), t=t4)

    
    @staticmethod
    def pose(x: float, y: float, z: float, rx: float, ry: float, rz: float):
        return f"p[{x},{y},{z},{rx},{ry},{rz}]"

    @staticmethod
    def relative_pose(x: float = 0, y: float = 0, z: float = 0, rx: float = 0, ry: float = 0, rz: float = 0):
        return f"pose_add(get_actual_tcp_pose(), p[{x},{y},{z},{rx},{ry},{rz}])"
