import socket
import time
import re
import math

class VisionSystem:
    def __init__(self, vs_ip: str, vs_port: int = 2024):
        self.v = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.v.connect((vs_ip, vs_port))
        print('Connected to Vision system ....SUCCESSFULLY!')

    def receive_data(self):
        while True:
            v_data = b''
            print('send start to cvs')
            while not v_data.endswith(b'>'):
                self.v.send(b'start!')
                v_data += self.v.recv(1)
            # Alternative
            # v_data = bytearray()
            # while not v_data.endswith(b'>'):
            #     print('send start to cvs')
            #     self.v.send(b'start!')
            #     v_data.extend(self.v.recv(100))
                
                
            coor_str = str(v_data, 'UTF-8')
            print(coor_str)
            print("----------------------------------------")
                
            match = re.match(
                r"<\(([^,]+),([^,]+),([^,]+)\),\(([^,]+),([^,]+),([^,]+)\),\(([^,]+),([^,]+)\),\(([^,]+),([^,]+)\)>",
                coor_str
            )
            if match:
                try:
                    x_x1, x_x2, x_ang = map(float, match.group(1, 2, 3))
                    xc_x1, xc_x2, xc_ang = map(float, match.group(4, 5, 6))
                    y_y1, y_y2 = map(float, match.group(7, 8))
                    yc_y1, yc_y2 = map(float, match.group(9, 10))
                                
                    if not any(math.isnan(val) for val in [x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2]):
                        return x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2
                except ValueError:
                    print("Invalid data received, retrying...")
            else:
                print("Received data format is invalid, retrying...")

    @staticmethod
    def find_coords(x_x1, x_x2, x_ang, xc_x1, xc_x2, xc_ang, y_y1, y_y2, yc_y1, yc_y2):
        degree = (x_ang + xc_ang) / 2
        degree_rad = round(degree * (math.pi / 180), 4)
        x_coor = (((xc_x1 + xc_x2) / 2) + ((x_x1 + x_x2) / 2)) / 2
        y_coor = (((yc_y1 + yc_y2) / 2) + ((y_y1 + y_y2) / 2)) / 2
        return degree_rad, x_coor, y_coor

    @staticmethod
    def offset_camera(x_coor, y_coor):
        x_coor_robot = (y_coor + 177) / 1000
        y_coor_robot = -(x_coor + 17) / 1000
        return x_coor_robot, y_coor_robot
