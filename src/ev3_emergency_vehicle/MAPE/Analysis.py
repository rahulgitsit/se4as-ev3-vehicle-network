#!/usr/bin/env pybricks-micropython

class Analysis:
    def __init__(self,obj_know,obj_comm):
        self.obj_know=obj_know
        self.obj_comm=obj_comm

    # issue with color sensor, rectified by adjusting RGB values with RGB values obtained from material we used as signals
    def detectable_colors(self,y): 
        
        # check for blue
        rgb=y
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
                if rgb[2] <= 25:
                    return "GREEN"
    
    #random generation of emergency
    def emerg_alert(self):
        x=self.obj_comm.embox_emer.read()
        if x in [10,12]:
            return x
        else:
            return False

    #distance from starting
    def direction_decider(self):
        x=self.obj_comm.embox_traveldistance.read()
        while not isinstance(x,float):
                    x=self.obj_comm.embox_traveldistance.read()
                    
        print(x)
        if x<2500:
            return "left"
        else:
            return "right"

    #obstacle detected
    def obstacle_detection(self):
        x=self.obj_know.distance
        if x< 180 and self.obj_know.emergency==1 and self.obj_know.back_from_emerg==0:
            return True
    
    #park color detection
    def park_spot_det(self):
        cr= self.obj_know.rgb
        x=self.detectable_colors(cr)
        if x=="GREEN" and self.obj_know.back_from_emerg==1:
            return True
