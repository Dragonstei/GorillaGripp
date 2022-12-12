#!/usr/bin/env pybricks-micropython
# Make sure to put the line above as the first line of code, or else the EV3 will not work

# [Stan] Ideas to improve software:
# Make use of the cmd and sys library to create an environment in a terminal
# where it's possible to read/send data to the robot while running

# Imports from Standard Library (remove if not planning to create cmd environment)
import cmd, sys

# User imports
import robot

# [Stan] Explaination on writing a main function: https://realpython.com/python-main-function/
def main():
    # [Stan] Directions and postions should be stored more neatly
    LEFT = 180
    RIGHT = 0
    DirectionSpeed = 40

    ev3 = robot.Robot()

    ev3.initMotors()
    ev3.setMotorControls()

    ev3.initSensors()

    ev3.initRobot()

    while True:
        ev3.robotCycle(LEFT, RIGHT, DirectionSpeed)

if __name__ == "__main__":
    main()