#!/usr/bin/env pybricks-micropython
from pybricks.media.ev3dev import  SoundFile
from pybricks.parameters import Port, Color
from pybricks.tools import DataLog, StopWatch, wait

class Executer:
    def __init__(self,obj_know,obj_ev3,obj_comm):
        self.obj_know=obj_know 
        self.obj_ev3=obj_ev3
        self.obj_comm=obj_comm
    
    def emerg_movement(self):
        
        p=0
        while p<6:
            self.obj_comm.embox_emer.send(100)
            p=p+1
        self.obj_ev3.speaker.play_file(SoundFile.MOTOR_START)
        self.obj_know.robot.turn(90)
        if self.obj_know.lane==10:
            self.obj_know.robot.straight(150)
            self.obj_know.robot.turn(80*self.obj_know.turning)
            self.obj_know.robot.stop()
        else:
            self.obj_know.robot.straight(300)
            self.obj_know.robot.turn(90*self.obj_know.turning)
            self.obj_know.robot.stop()
        self.obj_ev3.light.on(Color.RED)
    def parker(self,dis):
        self.obj_know.robot.stop()
        self.obj_know.robot.turn(90*self.obj_know.turning)
        self.obj_know.robot.straight(dis)
        self.obj_know.robot.turn(90)
        self.obj_comm.embox_emergencyover.send(0)
        ss=self.obj_comm.embox_emer.read()
        while ss!=200:
            self.obj_comm.embox_emergencyover.send(0)
            ss=self.obj_comm.embox_emer.read()
        self.obj_ev3.light.on(Color.GREEN)
        self.obj_comm.embox_restart.send(False)
    
    def vehicle_detection(self):#go straight if robot traveled more and take deviation if it travel less compare to half of track perimeter
        self.obj_know.robot.stop()
        wait(5000)
        self.obj_know.robot.straight(-50)
        self.obj_know.robot.turn(180)
    
    def impact_det(self):
        touch=self.obj_know.touch
        if touch == True and self.obj_know.istouch==0 and self.obj_know.back_from_emerg==1:
            self.obj_know.istouch=1
            co=0
            while co<7:
                self.obj_comm.embox_restart.send(True)
                co=co+1
            self.obj_ev3.speaker.beep()
            
            



    def robotaction(self,a,distance,color,reflection,rgb): # movement of robot
        distance=self.obj_know.distance
        color=self.obj_know.color
        reflection=self.obj_know.reflection
        rgb=self.obj_know.rgb
        if color!=None and reflection!=None and rgb!=None:
            s=str(color)+";"+str(reflection)+";"+str(rgb)
            self.obj_comm.embox_sensor.send(s)
        self.obj_comm.embox_distance.send(distance)
        self.obj_comm.embox_speed.send(self.obj_know.DRIVE_SPEED)
        self.obj_comm.embox_lane.send(self.obj_know.lane)
        if a==True:
            self.obj_know.robot.drive(self.obj_know.DRIVE_SPEED, self.obj_know.turn_rate)
            self.obj_know.last_deviation=self.obj_know.deviation
        else:
            self.obj_know.robot.stop() 
        self.obj_know.end_time=self.obj_know.watch.time()
