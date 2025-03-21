from utils.URARM import URARM
import math
import time

a_ip = "10.10.0.61"
a_port = 30003
g_port = 63352
c_port = 2002

home_pos = [0.116, -0.3, 0.2, 0, -math.pi, 0]

if __name__ == "__main__":
    arm = URARM(a_ip, a_port, g_port, c_port, home_pos)


    # arm.movel(URARM.relative_pose(x=-0.150))
    # while True:
    #     arm.movel(URARM.relative_pose(z=-0.100))
    #     arm.control_gripper(True)

    #     arm.movel(URARM.relative_pose(z=0.100))
    #     arm.movel(URARM.relative_pose(x=0.300))
    #     arm.movel(URARM.relative_pose(z=-0.100))
    #     arm.control_gripper(False)
    #     arm.movel(URARM.relative_pose(z=0.100))

    #     arm.movel(URARM.relative_pose(z=-0.100))
    #     arm.control_gripper(True)

    #     arm.movel(URARM.relative_pose(z=0.100))
    #     arm.movel(URARM.relative_pose(x=-0.300))
    #     arm.movel(URARM.relative_pose(z=-0.100))
    #     arm.control_gripper(False)
    #     arm.movel(URARM.relative_pose(z=0.100))

    #     time.sleep(1)
