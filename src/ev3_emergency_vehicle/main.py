#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait
from pybricks.messaging import BluetoothMailboxClient, NumericMailbox
from pybricks.media.ev3dev import Font, SoundFile
import random

#monitor
class Servomotors:#setup motor with port number of brick
    def __init__(self,porta=Port.B,portb=Port.C):
        self.left_motor = Motor(porta)
        self.right_motor = Motor(portb)

#moniter class
class Moniter:
    def __init__(self,obj_know):
        self.obj_know=obj_know
    def read_all_values(self):# read all values from brick
        self.obj_know.emerg=self.obj_know.embox_emer.read()
        self.obj_know.v_speed=self.obj_know.embox_speed.read()
        self.obj_know.v_lane=self.obj_know.embox_lane.read()
        self.obj_know.v_distance=self.obj_know.embox_distance.read()
        self.obj_know.v_time=self.obj_know.embox_time.read()
    def get_rgb(self): # collect rgb values from color sensor
        return self.obj_know.line_sensor.rgb()
    def get_reflection(self): # collect reflection values from color sensor
        return self.obj_know.line_sensor.reflection()
    def get_real_color(self): # collect color detected by color sensor
        return self.obj_know.line_sensor.color()
    def get_obstacle_distance(self): # uv sensor value
        return self.obj_know.obstacle_sensor.distance()
    # below are box readings
    def get_embox_id(self):
        return(self.obj_know.embox_id.read())
    def get_embox_lane(self):
        return(self.obj_know.embox_lane.read())
    def get_embox_speed(self):
        return(self.obj_know.embox_speed.read())
    def get_embox_distance(self):
        return(self.obj_know.embox_distance.read())
    def get_embox_emer(self):
        return(self.obj_know.embox_emer.read())
    def send_embox_emer(self,value):
        self.obj_know.embox_emer.send(value)

    #connecting to server, and verifying id
    def connect_server(self,SERVER = 'C8:E2:65:CD:69:86'):
        print('establishing connection...')
        self.obj_know.client.connect(SERVER)
        print('server connected!')
        while True:
            msg_id = self.obj_know.embox_id.read()
            if msg_id != None:
                break

class Analysis:
    def __init__(self,obj_moniter,obj_know):
        self.obj_moniter=obj_moniter
        self.obj_know=obj_know
    
    def detectable_colors(self): # issue with color sensor, rectified by adjusting RGB values with RGB values obtained from material we used as signals
        # check for blue
        rgb=self.obj_moniter.get_rgb()
        if rgb[2] >= 65:
            if rgb[0] <= 15:
                if rgb[1] <= 30:
                    return "BLUE"
         # check for yellow

        elif rgb[0] >= 45 and rgb[0] <= 60:
            if rgb[1] >= 25 and rgb[1] <= 42:
                if rgb[2] >= 10 and rgb[2] <= 25: # was 8 for av1
                        return "YELLOW"
        # check for green
        elif rgb[1] >= 25:
            if rgb[0] <= 10:
                if rgb[2] <= 17:
                    return "GREEN"
    #when emergency alert received from server
    def emerg_alert(self):
        if self.obj_know.emerg==10 or self.obj_know.emerg==12:
            self.obj_know.time = self.obj_know.watch.time()
            return True
    # park coming from accident spot.
    def park_alert(self):
        x=self.detectable_colors()
        if x=="GREEN" and self.obj_know.emersit==1:
            return True
    #accident spot reached. Assuming that track is free from all other vehicles and only accident vehicle on track.
    def obstacle_alert(self):
        x=self.obj_moniter.get_obstacle_distance()
        if x<180 and self.obj_know.emergency==1:
            return True
class Planner:
    def __init__(self,obj_know):
        self.obj_know=obj_know
    def rescue_planner(self):# update knowledge base values and 
        if self.obj_know.emerg_occur==0:
            self.obj_know.park=0
            self.obj_know.direction=0
            self.obj_know.robot.reset()
            self.obj_know.emergency=1
            self.obj_know.stopping = False
            self.obj_know.watch.reset()
            self.starttime=self.obj_know.watch.time()
            self.obj_know.DRIVE_SPEED = 60
            self.obj_know.lane=self.obj_know.emerg%10
            self.obj_know.turnangle=1

    def parking_planner(self): # update turn angle, flags and  other knowledge base values
        self.obj_know.turnangle=-1
        if self.obj_know.direction==1:
            self.obj_know.turnangle=1
        self.obj_know.emerg=0
        self.obj_know.emer_sit=0
        self.obj_know.emerg_occur=0

    def deviation_planner(self):# decide robot motion based on distance covered and update other knowledge values
        self.obj_know.emersit=1
        self.obj_know.DRIVE_SPEED=self.obj_know.MINIMUM_SPEED
        if (self.obj_know.robot.distance()<2500):
            self.obj_know.direction=1
            if self.obj_know.lane==1:
                self.obj_know.turnangle=-1
            else:
                self.obj_know.turnangle=1
            if self.obj_know.step==0:
                self.obj_know.step=2
            else:
                self.obj_know.step=0

    def lane_switching(self): # It follows when robot moving from one lane to another
        t=self.obj_know.line_sensor.reflection()
        if self.obj_know.step==1:
            if t>45 and self.obj_know.time>=self.obj_know.previousStateChangedTime+2000:
                self.obj_know.integral=0.0
                self.obj_know.derivative=0.0
                self.obj_know.step=2
                self.obj_know.previousStateChangedTime=self.obj_know.time
        if self.obj_know.step==3:
            if t>50 and self.obj_know.time>=self.obj_know.previousStateChangedTime+2000:
                self.obj_know.integral=0.0
                self.obj_know.derivative=0.0
                self.obj_know.step=0
                self.obj_know.previousStateChangedTime=self.obj_know.time

    def speedcontrol(self): # control speed based on obstacle presence, emergency situtation etc
        distance=self.obj_know.obstacle_sensor.distance()
        if self.obj_know.step == 1 or self.obj_know.step == 3:
            self.obj_know.DRIVE_SPEED=self.obj_know.MINIMUM_SPEED
        elif self.obj_know.emergency==1 and (self.obj_know.watch.time()-self.starttime)>10000:
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

    def robotmovement(self): # update constant values, calculate turn rate..!!
        color=self.obj_know.line_sensor.reflection()
        if not self.obj_know.stopping and self.obj_know.emergency==1 and self.obj_know.park==0:
            self.obj_know.deviation = color-self.obj_know.thresold
            if self.obj_know.deviation>-10 and self.obj_know.deviation<10:
                self.obj_know.integral=0
            elif self.obj_know.deviation*self.obj_know.last_deviation<0:
                self.obj_know.integral=0
            else:
                self.obj_know.integral=self.obj_know.integral+self.obj_know.deviation
            self.obj_know.deviation=self.obj_know.deviation-self.obj_know.last_deviation

            self.obj_know.turn_rate = (self.obj_know.PROPORTIONAL_GAIN * self.obj_know.deviation) + (self.obj_know.INTEGRAL_GAIN * self.obj_know.integral) + (self.obj_know.DERIVATIVE_GAIN * self.obj_know.derivative)

            if self.obj_know.step==1:
                self.obj_know.turn_rate=12
            elif self.obj_know.step==2:
                self.obj_know.turn_rate=-1*self.obj_know.turn_rate
            elif self.obj_know.step==3:
                self.obj_know.turn_rate=-14
            
            self.obj_know.last_deviation=self.obj_know.deviation
            return True
        else:
            return False

        



class Executer:
    def __init__(self,obj_know,obj_ev3):
        self.obj_know=obj_know 
        self.obj_ev3=obj_ev3
    def startemerv(self):# move robot after getting alert, send communication to server, move robot from parking to track.
        if self.obj_know.emerg_occur==0:
            self.obj_know.emerg_occur=1
            self.obj_know.embox_emer.send(100)
            self.obj_know.embox_emer.send(100)
            self.obj_know.embox_emer.send(100)
            self.obj_know.embox_emer.send(100)
            self.obj_know.embox_emer.send(100)
            self.obj_know.embox_emer.send(100)
            self.obj_ev3.speaker.play_file(SoundFile.MOTOR_START)
            self.obj_know.robot.turn(90 * self.obj_know.turnangle)
            if self.obj_know.lane==0:
                while self.obj_know.line_sensor.color()!=Color.BLACK:
                    self.obj_know.robot.drive(self.obj_know.DRIVE_SPEED, 0)
                self.obj_know.robot.straight(50)
                self.obj_know.robot.turn(-80*self.obj_know.turnangle)
                self.obj_know.step=self.obj_know.lane
            else:
                while self.obj_know.line_sensor.color()!=Color.BLACK:
                    self.obj_know.robot.drive(self.obj_know.DRIVE_SPEED, 0)
                self.obj_know.robot.straight(200)
                self.obj_know.robot.turn(-90*self.obj_know.turnangle)
                self.obj_know.step=self.obj_know.lane
    def parkemerv(self): # park when green color detected in track, move robot to outerside of track.
        self.obj_know.robot.turn(90*self.obj_know.turnangle)
        if self.obj_know.lane==2:
            self.obj_know.robot.straight(400)
        else:
            self.obj_know.robot.straight(200)
        self.obj_know.robot.turn(90)
        self.obj_know.step=4
        self.obj_know.stopping = True
        self.obj_know.DRIVE_SPEED = 0
        self.obj_know.park=1
        self.obj_know.embox_emergencyover.send(0)
        ss=self.obj_know.embox_emergencyover.read()
        while ss!=200:
            self.obj_know.embox_emergencyover.send(0)
            ss=self.obj_know.embox_emergencyover.read()
    def lightcontrol(self):# change light when there is emergency sitution
        if self.obj_know.emergency==1:
            self.obj_ev3.light.on(Color.YELLOW)
        # else:
        #     self.obj_ev3.light.off()
    def vehicle_detection(self):#go straight if robot traveled more and take deviation if it travel less compare to half of track perimeter
        self.obj_know.robot.stop()
        wait(5000)
        if (self.obj_know.direction==1):
            self.obj_know.robot.turn(180*self.obj_know.turnangle)
    def robotaction(self,a): # movement of robot
        if a==True:
            self.obj_know.robot.drive(self.obj_know.DRIVE_SPEED, self.obj_know.turn_rate)
        else:
            self.obj_know.robot.stop() 
        self.obj_know.end_time=self.obj_know.watch.time()
           

class Knowledgebase: # all robot bluetooth box, sensors are declared here, flags are updated here, and constant values also.
    def __init__(self,obj_motor,drive_speed=60, normal_speed=60,porta=Port.S3,portb=Port.S4):
        self.obj_motor=obj_motor
        self.robot = DriveBase(obj_motor.left_motor, obj_motor.right_motor, wheel_diameter=55.5, axle_track=118)
        self.watch=StopWatch()
        self.line_sensor = ColorSensor(porta)
        self.obstacle_sensor = UltrasonicSensor(portb)
        self.client = BluetoothMailboxClient()
        self.embox_id = NumericMailbox('id2', self.client)
        self.embox_time = NumericMailbox('time2', self.client)
        self.embox_lane = NumericMailbox('lane2', self.client)
        self.embox_speed = NumericMailbox('speed2', self.client)
        self.embox_distance = NumericMailbox('distance2', self.client)
        self.embox_emer=NumericMailbox("emer2",self.client)
        self.embox_emergencyover = NumericMailbox("emergency1", self.client)
        self.emerg=self.embox_emer.read()
        self.v_speed=self.embox_speed.read()
        self.v_lane=self.embox_lane.read()
        self.v_distance=self.embox_distance.read()
        self.v_time=self.embox_time.read()

        self.emersit=0
        self.time=0
        self.direction=0

        self.emerg_occur=0
        self.turnangle=1
        self.starttime=0

        self.big_font=Font(size=100,bold=True)

        # self.data = DataLog("time", "step", "color","reflection")
        self.NORMAL_SPEED=normal_speed
        self.DRIVE_SPEED=drive_speed
        self.MAXIMUM_SPEED=self.DRIVE_SPEED+40
        self.MINIMUM_SPEED=self.NORMAL_SPEED-20
        # Calculate the light threshold. Choose values based on your measurements.
        self.BLACK=5
        self.WHITE=50
        self.thresold=(self.BLACK+self.WHITE)/2
        # Set the gain of the PID controller.
        self.PROPORTIONAL_GAIN = 0.4
        self.INTEGRAL_GAIN = 0.1
        self.DERIVATIVE_GAIN = 0.5
        # Intialize variables related to PID controller.
        self.deviation = 0.0
        self.derivative = 0.0
        self.integral = 0.0
        self.last_deviation = 0.0
        self.turn_rate = 0.0
        self.step=0
        self.stopping=  False
        self.previousStateChangedTime = 0
        self.park=0
        self.stop_time=0
        self.lane=0
        self.end_time=0
        self.emergency=0
    # def datalog(self):
    #     self.data.log(self.obj_moniter.watch.time(), self.step,self.obj_moniter.get_real_color(), self.obj_moniter.get_reflection())

if __name__ == '__main__':
    ev3=EV3Brick()
    motor=Servomotors()
    knowledge=Knowledgebase(motor)
    moniter=Moniter(knowledge)
    analyser=Analysis(moniter,knowledge)
    planner=Planner(knowledge)
    executer=Executer(knowledge,ev3)   
    moniter.connect_server()
    ev3.screen.set_font(knowledge.big_font)
    while True:
        ev3.screen.draw_text(60,50,"EMERG")
        moniter.read_all_values()
        emergency=analyser.emerg_alert()
        if emergency:
            planner.rescue_planner()
            executer.startemerv()
        park=analyser.park_alert()
        if park:
            planner.parking_planner()
            executer.parkemerv()
        planner.lane_switching()
        planner.speedcontrol()
        obs=analyser.obstacle_alert()
        if obs:
            planner.deviation_planner()
            executer.vehicle_detection() #no planner involved
        robo=planner.robotmovement()
        executer.robotaction(robo)
        executer.lightcontrol()
        # knowledge.datalog()
