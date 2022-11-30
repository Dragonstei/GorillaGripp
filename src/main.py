#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Robot Arm Program
-----------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://education.lego.com/en-us/support/mindstorms-ev3/building-instructions#building-core
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

# Initialize the EV3 Brick
ev3 = EV3Brick()

# Configure the gripper motor on Port A with default settings.
gripper_motor = Motor(Port.D)

# Configure the elbow motor. It has an 8-teeth and a 40-teeth gear
# connected to it. We would like positive speed values to make the
# arm go upward. This corresponds to counterclockwise rotation
# of the motor.
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])

# Configure the motor that rotates the base. It has a 12-teeth and a
# 36-teeth gear connected to it. We would like positive speed values
# to make the arm go away from the Touch Sensor. This corresponds
# to counterclockwise rotation of the motor.
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])

# Limit the elbow and base accelerations. This results in
# very smooth motion. Like an industrial robot.
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Set up the Touch Sensor. It acts as an end-switch in the base
# of the robot arm. It defines the starting point of the base.
base_switch = TouchSensor(Port.S1)

# Set up the Color Sensor. This sensor detects when the elbow
# is in the starting position. This is when the sensor sees the
# white beam up close.
elbow_switch = TouchSensor(Port.S3)

ei_sensor = ColorSensor(Port.S4)

# Initialize the elbow. First make it go down for one second.
# Then make it go upwards slowly (15 degrees per second) until
# the Color Sensor detects the white beam. Then reset the motor
# angle to make this the zero point. Finally, hold the motor
# in place so it does not move.
elbow_motor.run_time(-30, 1000)
elbow_motor.run(15)
while not elbow_switch.pressed():
    wait(10)
elbow_motor.reset_angle(0)
elbow_motor.hold()

# Initialize the base. First rotate it until the Touch Sensor
# in the base is pressed. Reset the motor angle to make this
# the zero point. Then hold the motor in place so it does not move.
base_motor.run(-60)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()

# Initialize the gripper. First rotate the motor until it stalls.
# Stalling means that it cannot move any further. This position
# corresponds to the closed position. Then rotate the motor
# by 90 degrees such that the gripper is open.
gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)

gripper_motor.reset_angle(0)

def initialize_gripper():
    while gripper_motor.angle() > -900:
        gripper_motor.run(-200)
    gripper_motor.hold()
    base_motor.hold()


initialize_gripper() 

# Define the three destinations for picking up and moving the wheel stacks.
LEFT = 180
MIDDLE = 90
RIGHT = 0

ResetPos = 50
DirectionSpeed = 40

def robot_beeb(amount):
    # Play three beeps to indicate that the initialization is complete.
    for i in range(amount):
        ev3.speaker.beep()
        wait(100)

robot_beeb(3)

def robot_dropoff_position():
    base_motor.run_target(60, RIGHT)
    if base_motor.angle() == RIGHT:
        robot_drop()

def robot_grab():
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, closes the gripper, and
    # raises the elbow to pick up the object.
    print("grab")
    # Lower the arm.
    elbow_motor.run_target(60, -42)
    # Close the gripper to grab the wheel stack.
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    # Raise the arm to lift the wheel stack.
    elbow_motor.run_target(60, 0)
    robot_dropoff_position()

def robot_drop():
    # This function makes the robot base rotate to the indicated
    # position. There it lowers the elbow, opens the gripper to
    # release the object. Then it raises its arm again.
    print("drop")
    # Lower the arm to put the wheel stack on the ground.
    elbow_motor.run_target(60, -42)
    # Open the gripper to release the wheel stack.
    gripper_motor.run_target(200, -900)
    # Raise the arm.
    elbow_motor.run_target(60, 0)
    robot_reset_position()

def robot_reset_position():
    base_motor.run_target(60, ResetPos)
    if base_motor.angle() == ResetPos:
        robot_cycle(LEFT,RIGHT,DirectionSpeed)

def robot_cycle(position,position2, direction):
    #while base_motor.angle() != position or ei_sensor.reflection() > 32:
    while base_motor.angle() != position:
        try:
            #print(base_motor.angle())
            base_motor.run(direction)
            if robot_detect() == True:
                print("True")
                break
        except:
            print("error")
            break
    if base_motor.angle() == position:
        base_motor.hold()
        robot_cycle(position2,position,-direction)
    print("end")

def robot_detect():
    #print("start")
    while ei_sensor.reflection() > 0:
        #print(ei_sensor.color())
        #print(ei_sensor.rgb())
        print("ei")
        robot_beeb(1)
        base_motor.hold()
        robot_grab()
        return True
        break
    #print("end")

try:
    #robot_detect()
    robot_cycle(LEFT,RIGHT,DirectionSpeed)
except:
    print("can't start cycle")

    

