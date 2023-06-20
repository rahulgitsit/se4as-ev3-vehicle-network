#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port


class Monitor:
    def __init__(
        self,
        knowledge_base,
        colour_sensor_port,
        ultrasonic_sensor_port,
        touch_sensor_port,
    ):
        self.kbase = knowledge_base
        # Initialize the color sensor.
        self.line_sensor = ColorSensor(colour_sensor_port)

        # Initialize the ultrasonic sensor. It is used to detect obstacles as the robot drives around.
        self.obstacle_sensor = UltrasonicSensor(ultrasonic_sensor_port)

        # Initialise touch sensor
        self.crash_sensor = TouchSensor(touch_sensor_port)

    def read_sensor_values(
        self,
    ):
        self.kbase.reflection = self.line_sensor.reflection()
        self.kbase.color = self.line_sensor.color()
        self.kbase.rgb = self.line_sensor.rgb()
        self.kbase.distance = self.obstacle_sensor.distance()
        self.kbase.crash = self.crash_sensor.pressed()

        return (
            self.kbase.reflection,
            self.kbase.color,
            self.kbase.rgb,
            self.kbase.distance,
            self.kbase.crash,
        )
