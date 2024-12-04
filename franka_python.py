import panda_py
from panda_py import libfranka
import logging

from sympy.physics.units.definitions.unit_definitions import franklin

# Panda hostname/IP and Desk login information of your robot
hostname = '10.31.82.199'
# username = 'student.admin'
# password = 'franka1admin'

# username = 'student.safety'
# password = 'besafestudent'

username = 'student.operator'
password = 'frankarobot1'
logging.basicConfig(level=logging.INFO)


class RobotControl:
    def __init__(self):
        self.desk, self.panda, self.gripper = self.startup()
        self.panda.move_to_start()
        self.gripper.move(0.08, 0.2)

    def startup(self):
        desk = panda_py.Desk(hostname, username, password)
        # desk.unlock()
        desk.activate_fci()
        panda = panda_py.Panda(hostname)
        gripper = libfranka.Gripper(hostname)

        return desk, panda, gripper

    def calibrate(self):
        """
        Touches the franka end factor to the four corners of the workspace. QR codes will be placed at each point
        :return:
        """
        input("press enter to start")
        self.panda.move_to_start()
        pose = self.panda.get_pose()
        pose[0, 3] += .4
        pose[1, 3] -= .15
        self.panda.move_to_pose(pose, speed_factor=0.08)
        pose[2, 3] -= .46
        self.panda.move_to_pose(pose, speed_factor=0.08)
        input("press enter to continue")

        self.panda.move_to_start()
        pose = self.panda.get_pose()
        pose[0, 3] += .4
        pose[1, 3] += .15
        self.panda.move_to_pose(pose, speed_factor=0.08)
        pose[2, 3] -= .46
        self.panda.move_to_pose(pose, speed_factor=0.08)
        input("press enter to continue")

        self.panda.move_to_start()
        pose = self.panda.get_pose()
        pose[0, 3] += .1
        pose[1, 3] -= .15
        self.panda.move_to_pose(pose, speed_factor=0.08)
        pose[2, 3] -= .46
        self.panda.move_to_pose(pose, speed_factor=0.08)
        input("press enter to continue")

        self.panda.move_to_start()
        pose = self.panda.get_pose()
        pose[0, 3] += .1
        pose[1, 3] += .15
        self.panda.move_to_pose(pose, speed_factor=0.08)
        pose[2, 3] -= .46
        self.panda.move_to_pose(pose, speed_factor=0.08)
        input("press enter to continue")

        self.panda.move_to_start()
        pose = self.panda.get_pose()

        return

    def pick_place(self, x, y):
        """
        Runs the pick and place for taking a corresponding block and moving it to the play area
        """
        """
               A = Max camera range, B = Max ranges of the Franka, x,y = current coord, bx,by = current Franka
               cx,cy = target in franka coords (set playing coords)
        :param x:
        :param y:
        :return:
        """

        # bx = x * Bx / Ax
        # by = y * By / Ay
        #set up new x Range to -.1 to +.3 (subtract .1 from ratio value to shift centered coords)
        #set up new y Rance to -.2 to -.2
        # franka_x = (((x - 500) / 500) * .15) + .25
        # franka_y = (((y - 500) / 500) * .15)
        franka_x = x * 0.3/1000 + 0.1
        franka_y = y * 0.3/1000 - 0.15

        print(franka_x, franka_y)
        # First, move and pick up
        self.panda.move_to_start()
        pose = self.panda.get_pose()
        self.gripper.move(0.08, 0.2)
        print(pose)

        pose[0, 3] += 0.25  # front/back
        pose[1, 3] += 0  #left/right
        self.panda.move_to_pose(pose, speed_factor=0.08)
        pose[2, 3] -= .3  #up/down
        print(pose)
        self.panda.move_to_pose(pose, speed_factor=0.08)


        # Do the math to convert to franka x and y
        pose[0, 3] += franka_x - 0.25 # front/back
        pose[1, 3] += franka_y # left/right
        self.panda.move_to_pose(pose, speed_factor=0.08)
        pose[2, 3] -= .47 - 0.3  #up/down
        print(pose)
        self.panda.move_to_pose(pose, speed_factor=0.08)
        # self.panda.move_to_joint_position(panda_py.ik(pose), speed_factor=0.08)
        self.gripper.grasp(0, 0.2, 100, 0.02, 0.04)

        # Now move and place. Need Permanent Target Coordinates
        self.panda.move_to_start()
        pose = self.panda.get_pose()
        pose[0, 3] += 0.3  # front/back
        pose[1, 3] += 0  # left/right
        self.panda.move_to_pose(pose, speed_factor=0.07)
        pose[2, 3] -= .47  # up/down
        print(pose)
        self.panda.move_to_pose(pose, speed_factor=0.07)
        self.gripper.move(0.08, 0.2)

        self.panda.move_to_start()
        pose = self.panda.get_pose()

        pass


def main():
    print("start")
    robot = RobotControl()
    robot.calibrate()
    print("end")


if __name__ == '__main__':
    main()
