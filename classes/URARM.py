import socket
import time
import struct

class URARM:

    HOME_X = 0.116
    HOME_Y = -0.300
    HOME_Z = 0.02
    HOME_RX = 2.233
    HOME_RY = 2.257
    HOME_RZ = -0.039

    def __init__(self, robot_ip: str, robot_port: int = 30003):
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
        cmd_move = str.encode(f'movel(p[{self.HOME_X},{self.HOME_Y},{self.HOME_Z},{self.HOME_RX},{self.HOME_RY},{self.HOME_RZ}],a=0.5,v=0.5,t=0,r=0)\n')
        self.arm.send(cmd_move)
        time.sleep(5)

    def movel(self, pose, a: float = 0.5, v: float = 0.5, t: float = 0, r: float = 0):
        self.arm.send(f"movel({pose},{a},{v},{t},{r})\n".encode("UTF-8"))
        time.sleep(1.5)

    def movej(self, pose, a: float = 0.5, v: float = 0.5, t: float = 0, r: float = 0):
        self.arm.send(f"movej({pose},{a},{v},{t},{r})\n".encode("UTF-8"))
        time.sleep(1.5)
    
    def rotate_TCP(self, rx: float = 0, ry: float = 0, rz: float = 0):
        self.arm.send(b"get_actual_tcp_pose()\n")
        arm_recv = self.arm.recv(1108)
        joint_positions = struct.unpack('!6d', arm_recv[252:300])
        self.movel(f"p[{joint_positions[0]},{joint_positions[1]},{joint_positions[2]},{joint_positions[3] + rx},{joint_positions[4] + ry},{joint_positions[5] + rz}]")

    @staticmethod
    def pose(x: float, y: float, z: float, rx: float, ry: float, rz: float):
        return f"p[{x},{y},{z},{rx},{ry},{rz}]"

    @staticmethod
    def relative_pose(x: float = 0, y: float = 0, z: float = 0, rx: float = 0, ry: float = 0, rz: float = 0):
        return f"pose_add(get_actual_tcp_pose(), p[{x},{y},{z},{rx},{ry},{rz}])"
