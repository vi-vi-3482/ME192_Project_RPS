import panda_py
from panda_py import libfranka
import logging

# Panda hostname/IP and Desk login information of your robot
hostname = '192.168.3.100'
username = 'user'
password = 'password'
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

        return

    def pick_place(self, x, y):
        """
        Runs the pick and place for taking a corresponding block and moving it to the play area
        :param x:
        :param y:
        :return:
        """
        pass