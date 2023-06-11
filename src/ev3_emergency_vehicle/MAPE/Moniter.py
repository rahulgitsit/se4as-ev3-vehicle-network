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
        rgb=self.line_sensor.rgb()
        reflection=self.line_sensor.reflection()
        color=self.line_sensor.color()
        distance=self.obstacle_sensor.distance()
        touch= self.touch_sensor.pressed()
        return rgb,reflection,color,distance, touch

