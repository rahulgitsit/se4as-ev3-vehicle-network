#!/usr/bin/env pybricks-micropython


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Color
from pybricks.media.ev3dev import Font
from MAPE import Communication, Knowledgebase, Moniter, Analysis, Planner, Executer

    

class Servomotors:#setup motor with port number of brick
    def __init__(self,porta=Port.B,portb=Port.C):
        self.left_motor = Motor(porta)
        self.right_motor = Motor(portb)



if __name__=="__main__":
    ev3=EV3Brick()
    comm=Communication.Communication()
    motor=Servomotors()
    knowledge=Knowledgebase.Knowledgebase(motor)
    moniter=Moniter.Moniter(knowledge)
    analyser=Analysis.Analysis(moniter,knowledge,comm)
    planner=Planner.Planner(knowledge)
    executer=Executer.Executer(knowledge,ev3,comm)  
    ev3.screen.set_font(knowledge.big_font)
    ev3.screen.draw_text(60,50,"EMERG")
    comm.connect_server()
    while True: 
        comm.read_all_values()
        rgb,reflection,color,distance,touch= moniter.sensor_reader()
        if touch == True:
        if knowledge.emergency==0:
             t=analyser.emerg_alert()

        if t in [10,12]:
            y=analyser.direction_decider()
            planner.emerg_situation(y,t)
            executer.emerg_movement(color)
            t=False
        if knowledge.emergency==1:
            planner.speedcontrol(distance)
            p=analyser.park_spot_det(rgb)
            if p:
                x=planner.park_planner(y)
                executer.parker(x)
                planner.post_parking()
            d=analyser.obstacle_detection(distance)
            if d:
                planner.uturn_planning()
                executer.vehicle_detection()
            executer.impact_det(touch)
            robo=planner.robotmovement(reflection)
            executer.robotaction(robo)
            
            
            







            







            







            






