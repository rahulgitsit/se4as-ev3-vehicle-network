#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port, Color

class Moniter:
    def __init__(self,obj_know, porta=Port.S3,portb=Port.S4,portc=Port.S1):
        self.obj_know=obj_know
        self.line_sensor = ColorSensor(porta)
        self.obstacle_sensor = UltrasonicSensor(portb)
        self.touch_sensor = TouchSensor(portc)
    
    def sensor_reader(self):
        self.obj_know.rgb=self.line_sensor.rgb()
        self.obj_know.reflection=self.line_sensor.reflection()
        self.obj_know.color=self.line_sensor.color()
        self.obj_know.distance=self.obstacle_sensor.distance()
        self.obj_know.touch= self.touch_sensor.pressed()

