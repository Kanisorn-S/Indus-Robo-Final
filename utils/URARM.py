import socket
import time

# movel(pose_add(get_actual_tcp_pose(),p[0.2, 0.1, 0, 0, 0, d2r(31)], 1, 0.5, 0, 0))


class URARM:

    def __init__(
        self,
        robot_ip: str,
        arm_port: int = 30003,
        gripper_port: int = 63352,
        conv_port: int = 2002,
        home_pose=None,
    ):
        # Connection to arm socket
        self.arm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.arm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.arm_socket.connect((robot_ip, arm_port))

        if home_pose:
            self.movel(f"p{str(home_pose)}")
            time.sleep(1)

        # Connection to gripper socket
        self.gripper_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.gripper_socket.connect((robot_ip, gripper_port))
        self.gripper_socket.send(b"GET ACT\n")
        arm_socket_recv = str(self.gripper_socket.recv(10), "UTF-8")
        if "1" in arm_socket_recv:
            print("Gripper Activated")

        # print("get ACT  == " + arm_socket_recv)

        self.gripper_socket.send(b"GET POS\n")
        gripper_socket_recv = str(self.gripper_socket.recv(10), "UTF-8")
        if gripper_socket_recv:
            self.gripper_socket.send(b"SET ACT 1\n")
            gripper_socket_recv = str(self.gripper_socket.recv(255), "UTF-8")
            print(gripper_socket_recv)
            time.sleep(3)
            self.gripper_socket.send(b"SET GTO 1\n")
            self.gripper_socket.send(b"SET SPE 255\n")
            self.gripper_socket.send(b"SET FOR 255\n")

            self.control_gripper(False)
        

    @staticmethod
    def relative_pose(
        x: float = 0,
        y: float = 0,
        z: float = 0,
        rx: str | float = 0,
        ry: str | float = 0,
        rz: str | float = 0,
    ) -> str:
        return f"pose_add(get_actual_tcp_pose(), p[{x},{y},{z},{rx},{ry},{rz}])"

    # not usable, need its library or some shit
    # def get_actual_tcp_pose(self):
    #     self.arm_socket.send(b"GET POS\n")
    #     print(str(self.arm_socket.recv(10), "UTF-8"))

    def movel(
        self, pose, a: float = 1, v: float = 0.5, t: float = 0, r: float = 0
    ) -> None:
        self.arm_socket.send(f"movel({pose},{a},{v},{t},{r})\n".encode("UTF-8"))
        time.sleep(2)

    def control_gripper(self, activate: bool):
        self.gripper_socket.send(f"SET POS {255 if activate else 0}\n".encode("UTF-8"))
        time.sleep(1)
        g_recv = str(self.gripper_socket.recv(255), "UTF-8")
        print(g_recv)

    def send_command_to_arm(self, command: str):
        self.arm_socket.send(command)
        time.sleep(2)
    
    def send_command_to_gripper(self, command: str):
        self.gripper_socket.send(command)
        time.sleep(1)
        g_recv = str(self.gripper_socket.recv(255), "UTF-8")
        print(g_recv)
