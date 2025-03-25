import socket
import time

class ConveyorBelt:
    def __init__(self, conv_ip: str, conv_port: int = 2002):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.bind((conv_ip, conv_port))
        self.c.listen(1)
        print("Conveyor belt socket is listening")
        self.conv, self.addr = self.c.accept()
        print(f"Connected by {self.addr}")

    def set_speed(self, speed: int):
        self.conv.send(f'set_vel,conv,{speed}\n'.encode('UTF-8'))

    def start(self, forward: bool = True):
        self.conv.send(b'jog_fwd,conv,0\n' if forward else b'jog_bwd,conv,0\n')

    def stop(self):
        self.conv.send(b'jog_stop,conv,0\n')
