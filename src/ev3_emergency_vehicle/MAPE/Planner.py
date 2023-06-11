#!/usr/bin/env pybricks-micropython

class Planner:
    def __init__(self,obj_know):
        self.obj_know=obj_know


    def emerg_situation(self,dir,x):
        knowledge.time=knowledge.watch.time()
        self.obj_know.lane=x
        if self.obj_know.emerg_det==0:
            self.obj_know.istouch=0
            self.obj_know.robot.reset()
            self.obj_know.emergency=1
            self.obj_know.park=0
            self.obj_know.emerg_det=1
            self.obj_know.DRIVE_SPEED=60
            self.obj_know.stopping=False
            self.obj_know.watch.reset()
            self.obj_know.cotime=self.obj_know.watch.time()
            if dir =="left":
                self.obj_know.turning=-1
                if self.obj_know.lane==10:
                    self.obj_know.step=0
                else:
                    self.obj_know.step=2
            elif dir == "right":
                self.obj_know.turning=1
                if self.obj_know.lane==10:
                    self.obj_know.step=2
                else:
                    self.obj_know.step=0
    def park_planner(self,y):
        if y=="left":
            self.obj_know.turning=1

        if y=="right":
            self.obj_know.turning=-1
        if self.obj_know.lane==10:
            return 200
        else:
            return 400



    

    def lane_swtiching(self):
        t=self.obj_know.line_sensor.reflection()
        if self.obj_know.step==1:
            if t>65 and self.obj_know.cotime>=self.obj_know.previousStateChangedTime+2000:
                self.obj_know.integral=0.0
                self.obj_know.derivative=0.0
                self.obj_know.step=2
                self.obj_know.previousStateChangedTime=self.obj_know.cotime
        elif self.obj_know.step==3:
            if t>65 and self.obj_know.cotime>=self.obj_know.previousStateChangedTime+2000:
                self.obj_know.integral=0.0
                self.obj_know.derivative=0.0
                self.obj_know.step=0
                self.obj_know.previousStateChangedTime=self.obj_know.cotime
    
    def speedcontrol(self,dis): # control speed based on obstacle presence, emergency situtation etc
        distance=dis
        if self.obj_know.step == 1 or self.obj_know.step == 3:
            self.obj_know.DRIVE_SPEED=self.obj_know.MINIMUM_SPEED
        elif self.obj_know.emergency==1 and (self.obj_know.watch.time()-self.obj_know.cotime)>10000:
            if self.obj_know.DRIVE_SPEED< self.obj_know.MAXIMUM_SPEED:
                self.obj_know.DRIVE_SPEED=self.obj_know.DRIVE_SPEED+0.3
        elif distance>600:
            if self.obj_know.DRIVE_SPEED< self.obj_know.MAXIMUM_SPEED:
                self.obj_know.DRIVE_SPEED=self.obj_know.DRIVE_SPEED+0.3
        elif distance >550 and distance <=600:
            self.obj_know.DRIVE_SPEED=self.obj_know.NORMAL_SPEED
        elif distance >500 and distance <=550:
            if self.obj_know.DRIVE_SPEED>self.obj_know.MINIMUM_SPEED:
                self.obj_know.DRIVE_SPEED=self.obj_know.DRIVE_SPEED-1
        else:
            self.obj_know.DRIVE_SPEED=self.obj_know.MINIMUM_SPEED
    

    def robotmovement(self,rel): # update constant values, calculate turn rate..!!
        color=rel
        if not self.obj_know.stopping and self.obj_know.emergency==1 and self.obj_know.park==0:
            self.obj_know.deviation = color - self.obj_know.threshold
            if self.obj_know.deviation > -10 and self.obj_know.deviation < 10:
                self.obj_know.integral = 0
            elif self.obj_know.deviation * self.obj_know.last_deviation < 0:
                self.obj_know.integral = 0
            else:
                self.obj_know.integral = self.obj_know.integral + self.obj_know.deviation
            self.obj_know.derivative = self.obj_know.deviation - self.obj_know.last_deviation

            self.obj_know.turn_rate = (self.obj_know.PROPORTIONAL_GAIN * self.obj_know.deviation) + (self.obj_know.INTEGRAL_GAIN * self.obj_know.integral) + (self.obj_know.DERIVATIVE_GAIN * self.obj_know.derivative)

            if self.obj_know.step == 1:
                self.obj_know.turn_rate = 12
            elif self.obj_know.step == 2:
                self.obj_know.turn_rate = -1*self.obj_know.turn_rate
            elif self.obj_know.step == 3:
                self.obj_know.turn_rate = -14
            
            return True
        else:
            return False
    def post_parking(self):
        self.obj_know.step=0
        self.obj_know.stopping=False
        self.obj_know.DRIVE_SPEED=0
        self.obj_know.park=1
        self.obj_know.emergency=0
        self.obj_know.back_from_emerg=0
        self.obj_know.emerg_det=0

    
    def uturn_planning(self):
        self.obj_know.back_from_emerg=1
        self.obj_know.DRIVE_SPEED=self.obj_know.MINIMUM_SPEED
        if self.obj_know.step==0:
            self.obj_know.step=2
        else:
            self.obj_know.step=0
