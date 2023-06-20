#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Color
from pybricks.tools import DataLog, StopWatch, wait


class KnowledgeBase:
    DRIVE_SPEED = 70
    NORMAL_SPEED = 70
    MAX_SPEED = 100
    MIN_SPEED = 60

    # Calculate the light threshold. Choose values based on your measurements.
    BLACK = 10
    WHITE = 65

    # Set the gain of the PID controssller.
    PROPORTIONAL_GAIN = 0.4
    INTEGRAL_GAIN = 0.1
    DERIVATIVE_GAIN = 0.5

    # Colour codes
    STOP_COLOR = Color.RED
    INTERSECTION = "GREEN"  # TODO: To be changed
    PARKING_AV = "BLUE"  # BLUE
    PARKING_SPCL = "GREEN"  # YELLOW

    def __init__(
        self,
    ):
        self.id_ = 0
        self.deviation = 0.0
        self.derivative = 0.0
        self.integral = 0.0
        self.last_deviation = 0.0
        self.turn_rate = 0.0
        self.threshold = (self.BLACK + self.WHITE) / 2
        self.step = 0
        self.angle = 0
        self.travelled_distance = 0
        self.reset_distance = False
        # Time that state changed previously
        self.previousStateChangedTime = 0
        # Time that robot has stopped
        self.stop_time = 0
        # The flag to control robot stop or not
        self.stopping = False
        self.breakdown = False
        # The flag for emergency vehicle to arrive
        self.av_light = Color.GREEN
        self.sos = False
        self.crash = False
        self.emergency = False
        self.park_ack = 0
        self.alert_mode = False
        self.park_analysis_required = False
        self.analysis = "lane-follow"
        self.plan = None
        self.park_lot_distance = 0

        # sensor readings
        self.reflection = 0.0
        self.color = None
        self.rgb = (0, 0, 0)
        self.distance = 0.0
        self.crash = False

        self.watch = StopWatch()
        self.watch.reset()

    def start_time(
        self,
    ):
        self.time = self.watch.time()
        return self.time
