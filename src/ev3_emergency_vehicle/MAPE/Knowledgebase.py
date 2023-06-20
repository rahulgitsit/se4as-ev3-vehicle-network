#!/usr/bin/env pybricks-micropython


from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait
from pybricks.media.ev3dev import Font

class Knowledgebase:
    def __init__(self,obj_motor,drive_speed=60, normal_speed=60):
        self.obj_motor=obj_motor
        self.robot = DriveBase(obj_motor.left_motor, obj_motor.right_motor, wheel_diameter=55.5, axle_track=118)
        # self.client = BluetoothMailboxClient()


        #speed
        self.NORMAL_SPEED=normal_speed
        self.DRIVE_SPEED=drive_speed
        self.MAXIMUM_SPEED=self.DRIVE_SPEED+40
        self.MINIMUM_SPEED=self.NORMAL_SPEED-20

        #thresold
        self.BLACK=10
        self.WHITE=65
        self.threshold = (self.BLACK + self.WHITE) / 2

        #pid controller
        self.PROPORTIONAL_GAIN = 0.4
        self.INTEGRAL_GAIN = 0.1
        self.DERIVATIVE_GAIN = 0.5

        #variables related to pid controller
        self.deviation = 0.0
        self.derivative = 0.0
        self.integral = 0.0
        self.last_deviation = 0.0
        self.turn_rate = 0.0

        # Lane change state
        # step 0: drive on the outer lane
        # step 1: change lane (from outer to inner)
        # step 2: drive on the inner lane
        # step 3: change lane (from inner to outer)
        self.step = 0


        # Time that state changed previously
        self.previousStateChangedTime = 0


        # Time that robot has stopped
        self.stop_time = 0

        # The flag to control robot stop or not
        self.stopping = False

        #flag to control emergency situation
        self.emergency=0

        #flag to control vehicle when coming back from emergency
        self.back_from_emerg=0

        #flag when emergecny detected first time
        self.emerg_det=0

        #flag for parking
        self.park=0

        #accident occured lane
        self.lane=0

        #time monitering
        self.watch = StopWatch()
        self.watch.reset()

        #for the display
        self.big_font=Font(size=100,bold=True)

        #for reading time
        self.time=0
        self.cotime=0

        #for turning
        self.turning=0

        self.istouch=0

        self.rgb=[]
        self.reflection=0
        self.color=""
        self.distance=0
        self.touch=False
