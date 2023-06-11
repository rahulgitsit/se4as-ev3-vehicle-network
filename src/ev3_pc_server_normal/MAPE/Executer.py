class Executer:
    def __init__(self,obj_comm,obj_knw):
        self.obj_knw=obj_knw
        self.obj_comm=obj_comm
    def send_id(self):
        n=0
        while n<6:
            self.obj_comm.mbox2_id.send(3)
            self.obj_comm.admin_id.send(0)
            self.obj_comm.mbox1_id.send(1)
            n=n+1
    
    def send_park(self,veh,msg):
        if veh ==1:
            x=self.obj_comm.mbox1_parking
        else:
            x=self.obj_comm.mbox2_parking
        if (msg==901 or msg==902):
            print()
            print()
            print()
            print("***********************************")
            print(f"Parking request to vehicle {veh}")
            print("***********************************")
            print()
            print()
            print()
            x.send(msg)
            y=x.read()
            while y!=300+self.obj_knw.parkcount:
                x.send(msg)
                y=x.read()
        if (msg==666):
            print()
            print()
            print()
            print("***********************************")
            print(f"back to track request to vehicle {veh}")
            print("***********************************")
            print()
            print()
            print()
            x.send(msg)
            y=x.read()
            while y!=222:
                x.send(msg)
                y=x.read()
        
    def send_emergency(self,lane,value):
        if lane ==0 and self.obj_knw.emerg==1:
            self.obj_knw.emerg=0
            print("***********************************")
            print("Emergency over")
            print("***********************************")
            self.obj_comm.mbox1_emergency.send(self.obj_knw.emergover)
            self.obj_comm.mbox2_emergency.send(self.obj_knw.emergover)
            self.obj_comm.front_emer=self.obj_comm.mbox1_emergency.read()
            self.obj_comm.second_emer=self.obj_comm.mbox1_emergency.read()
            while self.obj_comm.front_emer!=300 and self.obj_comm.second_emer!=300:
                self.obj_comm.mbox1_emergency.send(self.obj_knw.emergover)
                self.obj_comm.mbox2_emergency.send(self.obj_knw.emergover)
                self.obj_comm.front_emer=self.obj_comm.mbox1_emergency.read()
                self.obj_comm.second_emer=self.obj_comm.mbox1_emergency.read()
        elif lane in [10,12] and self.obj_knw.emerg==0:
            self.obj_knw.emerg=1
            if lane ==10:
                code=10
                lane=1
            elif lane == 12:
                code=12
                lane=2
            print()
            print()
            print()
            print("***********************************")
            print(f"Emergency in lane {lane}")
            print("***********************************")
            print()
            print()
            print()
            if value==2:
                p= self.obj_comm.mbox1_server_ack
                s= self.obj_comm.mbox2_emergency
            elif value==3:
                p= self.obj_comm.mbox2_server_ack
                s= self.obj_comm.mbox1_emergency
            if value ==1:
                self.obj_comm.mbox1_emergency.send(code)
                self.obj_comm.mbox2_emergency.send(code)
                self.obj_comm.front_emer=self.obj_comm.mbox1_emergency.read()
                self.obj_comm.second_emer=self.obj_comm.mbox1_emergency.read()
                while self.obj_comm.second_emer!=100 and self.obj_comm.front_emer!=100:
                    self.obj_comm.mbox1_emergency.send(code)
                    self.obj_comm.mbox2_emergency.send(code)
                    self.obj_comm.front_emer=self.obj_comm.mbox1_emergency.read()
                    self.obj_comm.second_emer=self.obj_comm.mbox1_emergency.read()
            elif value in [3,2]:
                q=0
                while q<6:
                    p.send(self.obj_knw.ack)
                    q=q+1
                print("Ack sent")
                s.send(code)
                recv=s.read()
                while recv!=100:
                    s.send(code)
                    recv=s.read()
                print("Alert sent", code)
            
            



