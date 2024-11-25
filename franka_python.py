import panda_py
from panda_py import libfranka
import logging

# Panda hostname/IP and Desk login information of your robot
hostname = '10.31.82.199'
username = 'student.admin'
password = 'franka1admin'
logging.basicConfig(level=logging.INFO)

class RobotControl:
    def __init__(self):
        self.desk, self.panda, self.gripper = self.startup()

    def startup(self):
        desk = panda_py.Desk(hostname, username, password)
        desk.unlock()
        desk.activate_fci()
        panda = panda_py.Panda(hostname)
        gripper = libfranka.Gripper(hostname)

        return desk, panda, gripper

    def calibrate(self):
        """
        Touches the franka end factor to the four corners of the workspace. QR codes will be placed at each point
        :return:
        """
        self.panda.move_to_start()
        pose = self.panda.get_pose()
        pose[0, 3] += .3
        pose[1, 3] -= .3
        self.panda.move_to_pose(pose)
        pose[2, 3] -= .47
        self.panda.move_to_pose(pose)
        input("press enter to continue")

        self.panda.move_to_start()
        pose = self.panda.get_pose()
        pose[0, 3] += .3
        pose[1, 3] += .3
        self.panda.move_to_pose(pose)
        pose[2, 3] -= .47
        self.panda.move_to_pose(pose)
        input("press enter to continue")

        self.panda.move_to_start()
        pose = self.panda.get_pose()
        pose[0, 3] -= .1
        pose[1, 3] -= .3
        self.panda.move_to_pose(pose)
        pose[2, 3] -= .47
        self.panda.move_to_pose(pose)
        input("press enter to continue")

        self.panda.move_to_start()
        pose = self.panda.get_pose()
        pose[0, 3] -= .1
        pose[1, 3] += .3
        self.panda.move_to_pose(pose)
        pose[2, 3] -= .47
        self.panda.move_to_pose(pose)
        input("press enter to continue")

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
        """
        bx = x*Bx/Ax
        by = y*By/Ay
        
        return to start()
        pose = get pose
        
        adjust position x,y
        move to position()
        adjust position drop z
        move to position()
        gripper activate()
        
        return to start()
        pose = get pose
        
        **set position every time for target playing location, cx, cy fixed locations
        
        adjust position x,y ** by cx, cy
        move to position()
        adjust position drop z
        move to position()
        gripper move() (release) function
        
        return to start()
        pose = get pose
        """
        pass

def main():
    robot = RobotControl()
    robot.calibrate()