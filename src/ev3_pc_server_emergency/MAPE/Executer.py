import random


class Executer:
    def __init__(self,obj_comm,obj_knw):
        self.obj_knw=obj_knw
        self.obj_comm=obj_comm
    def send_id(self):
        n=0
        while n<6:
            self.obj_comm.embox_id.send(3)
            self.obj_comm.admin_id.send(0)
            self.obj_comm.mbox1_id.send(1)
            n=n+1
    
    def send_park(self,list1=[]):
        print(int(list1[1]))
        if (int(list1[1])==901 or int(list1[1])==902):
            print()
            print()
            print()
            print("***********************************")
            print(f"Parking request to vehicle {list1[0]}")
            print("***********************************")
            print()
            print()
            print()
            self.obj_comm.mbox1_parking.send(int(list1[1]))
            self.obj_comm.front_parking=self.obj_comm.mbox1_parking.read()
            while self.obj_comm.front_parking!=300+self.obj_knw.parkcount:
                self.obj_comm.mbox1_parking.send(int(list1[1]))
                self.obj_comm.front_parking=self.obj_comm.mbox1_parking.read()
        elif int(list1[1])==666:
            print()
            print()
            print()
            print("***********************************")
            print(f"back to track request to vehicle {list1[0]}")
            print("***********************************")
            print()
            print()
            print()
            self.obj_comm.mbox1_parking.send(int(list1[1]))
            self.obj_comm.front_parking=self.obj_comm.mbox1_parking.read()
            while self.obj_comm.front_parking!=222:
                self.obj_comm.mbox1_parking.send(int(list1[1]))
                self.obj_comm.front_parking=self.obj_comm.mbox1_parking.read()
        
    def send_emergency(self,lane):
        e=self.obj_comm.embox_restart.read()
        if e == True:
                co=0
                while co<7:
                    self.obj_comm.mbox1_restart.send(True)
                    co=co+1
        if lane ==0 and self.obj_knw.emerg==1:


            print("Emergency over")
            self.obj_comm.embox_emer.send(self.obj_knw.ack)
            self.obj_comm.embox_emer.send(self.obj_knw.ack)
            self.obj_comm.embox_emer.send(self.obj_knw.ack)
            self.obj_comm.embox_emer.send(self.obj_knw.ack)
            self.obj_comm.embox_emer.send(self.obj_knw.ack)
            self.obj_comm.embox_emer.send(self.obj_knw.ack)
            self.obj_comm.mbox1_emergency.send(self.obj_knw.emergover)
            self.obj_knw.emerg=0
            self.obj_comm.front_emer=self.obj_comm.mbox1_emergency.read()
            while self.obj_comm.front_emer!=300:
                self.obj_comm.mbox1_emergency.send(self.obj_knw.emergover)
                self.obj_comm.front_emer=self.obj_comm.mbox1_emergency.read()
            self.obj_comm.mbox1_restart.send(False)
            self.obj_comm.mbox1_server_ack.send(69)
        elif lane in [10,12] and self.obj_knw.emerg==0:
            self.obj_knw.emerg=1
            cmd_index=0
            if lane ==10:
                code=10
                lane=1
            elif lane == 12:
                code=12
                lane=2
            if self.obj_comm.front_crash in [10,12]:
                cmd_index=1

            print()
            print()
            print()
            print("***********************************")
            print(f"Emergency in lane {lane}")
            print("***********************************")
            print()
            print()
            print()
            c=0
            if cmd_index==0:
                travel=random.randint(1000,5000)
                self.obj_comm.mbox1_emergency.send(code)
                self.obj_comm.front_emer=self.obj_comm.mbox1_emergency.read()
                while self.obj_comm.front_emer!=100:
                    self.obj_comm.mbox1_emergency.send(code)
                    self.obj_comm.front_emer=self.obj_comm.mbox1_emergency.read()
            elif cmd_index==1:
                travel=self.obj_comm.mbox1_travel.read()
                while not isinstance(travel,float):
                    travel=self.obj_comm.mbox1_travel.read()
                print("accident happened in real ",travel)
                p=0
                while p<6:
                    self.obj_comm.mbox1_server_ack.send(self.obj_knw.ack)
                    p=p+1
            self.obj_comm.embox_emer.send(code)
            self.obj_comm.second_emer=self.obj_comm.embox_emer.read()
            print("travel distance",travel)
            travel=int(travel)
            while c<6:
                self.obj_comm.embox_travel.send(travel)
                c=c+1
            while self.obj_comm.second_emer!=100:
                self.obj_comm.embox_emer.send(code)
                self.obj_comm.second_emer=self.obj_comm.embox_emer.read()
            e=self.obj_comm.embox_restart.read()
