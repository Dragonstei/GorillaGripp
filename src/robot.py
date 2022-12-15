# EV3 imports, documentation found at: https://pybricks.com/ev3-micropython/
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, SoundFile
from pybricks.tools import wait

# [Stan] Directions and postions should be stored more neatly
LEFT = 180
MIDDLE = 90
RIGHT = 0

ResetPos = 90
DirectionSpeed = 40

class Robot(EV3Brick):
    def __init__(self):
        super(Robot, self).__init__()

        print("Creating EV3Brick object")

    def __del__(self):
        print("EV3Brick Desctructor called")

    def initMotors(self):
        # Motors are defined with a port, their direction and a list containing the gears connected to it
        self.elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
        self.base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])
        self.gripper_motor = Motor(Port.D)

    def setMotorControls(self):
        self.elbow_motor.control.limits(speed = 100, acceleration = 120)
        self.base_motor.control.limits(speed = 100, acceleration = 120)

    def initSensors(self):
        self.base_switch = TouchSensor(Port.S1)
        self.elbow_switch = TouchSensor(Port.S3)
        self.egg_sensor = ColorSensor(Port.S4)

    def initRobot(self):
        self.elbow_motor.run_time(-30, 1000)
        self.elbow_motor.run(15)
        while not self.elbow_switch.pressed():
            wait(10)
        self.elbow_motor.reset_angle(0)
        self.elbow_motor.hold()

        self.base_motor.run(-60)
        while not self.base_switch.pressed():
            wait(10)
        self.base_motor.reset_angle(0)
        self.base_motor.hold()

        self.gripper_motor.run_until_stalled(200, then = Stop.COAST, duty_limit = 30)
        self.gripper_motor.reset_angle(0)

        while self.gripper_motor.angle() > -900:
            self.gripper_motor.run(-200)
        self.gripper_motor.hold()
        self.base_motor.hold()

        self.speaker.play_file(SoundFile.READY)
        self.speaker.say('GorillaGripper ready')

    # [Stan] Robot functions, could be a seperate class to handle all functionality
    # run_target(speed, position)

    def detection(self):
        # [Stan] rgb(0, 0, 0) can be too sensitive, (2, 2, 2) works in a light environment. reflection() adds a red light to the camera, can cause confusion with RGB detection
        # Ambient can be used to set the detection values for seperate environments. Ex. a dark ambient room where ambient() < 10 can use different detection values than ambient() > 10
        if self.egg_sensor.color():
            print("[1] Egg detected")
            self.speaker.beep()
            self.base_motor.hold()
            self.grab()
            self.drop()
            self.reset()
            return True
        else:
            return False

    def grab(self):
        print("[2] Grabbing egg")
        self.elbow_motor.run_target(60, -40)
        self.gripper_motor.run_until_stalled(200, then = Stop.HOLD, duty_limit = 60)
        self.elbow_motor.run_target(80, 0)

    def drop(self):
        self.base_motor.run_target(60, RIGHT)
        print("[3] Dropping egg")
        self.elbow_motor.run_target(60, -40)
        self.gripper_motor.run_target(200, -900)
        self.elbow_motor.run_target(80, 0)

    def reset(self):
        print("[4] Resetting position")
        self.base_motor.run_target(70, ResetPos)
        if self.base_motor.angle() == ResetPos:
            self.robotCycle(LEFT, RIGHT, DirectionSpeed)
        wait(500)

    def robotCycle(self, position, position2, direction):
        while self.base_motor.angle() != position:
            try:
                self.base_motor.run(direction)
                if self.detection():
                    break
            except:
                print("[!] Error, couldn't move robot arm")
                break
        if self.base_motor.angle() == position:
            self.base_motor.hold()
            self.robotCycle(position2, position, -direction)