import socket
import time

class ConveyorBelt:
    def __init__(self, conv_ip: str, conv_port: int = 2002):
        self.conv_ip = conv_ip
        self.conv_port = conv_port
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.bind((conv_ip, conv_port))
        self.c.listen(1)
        print("Conveyor belt socket is listening")
        self.conv, self.addr = self.c.accept()
        # with self.conv: 
        print(f"Connected by {self.addr}") 

        self.conv.sendall(b'activate,tcp\n') 
        time.sleep(1) 
        self.conv.sendall(b'pwr_on,conv,0\n') 
        time.sleep(1) 
        self.conv.sendall(b'set_vel,conv,20\n') 
        time.sleep(1) 
        self.conv.sendall(b'jog_fwd,conv,0\n') 
        # time.sleep(5)



        conv_recv = self.conv.recv(100) 
        print (conv_recv) 
    

    # def set_speed(self, speed: int):
    #     self.conv.sendall(f'set_vel,conv,{speed}\n'.encode('UTF-8'))

    # def start(self, forward: bool = True):
    #     self.conv.sendall(b'jog_fwd,conv,0\n' if forward else b'jog_bwd,conv,0\n')

    def stop(self):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.bind((self.conv_ip, self.conv_port))
        self.c.listen(1)
        print("Conveyor belt socket is listening")
        self.conv, self.addr = self.c.accept()
        # with self.conv: 
        print(f"Connected by {self.addr}") 
        self.conv.sendall(b'jog_stop,conv,0\n')
