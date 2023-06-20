import datetime
class Moniter:
    def __init__(self,obj_comm,obj_know):
        self.obj_comm=obj_comm
        self.obj_know=obj_know
    
    def read_mailbox(self): #read all mailboxs
        self.obj_comm.admin_cmd=self.obj_comm.admin_command.read()
        self.obj_comm.front_id = self.obj_comm.mbox1_id.read()
        self.obj_comm.front_time = self.obj_comm.mbox1_time.read()
        self.obj_comm.front_lane = self.obj_comm.mbox1_lane.read()
        self.obj_comm.front_speed = self.obj_comm.mbox1_speed.read()
        self.obj_comm.front_distance = self.obj_comm.mbox1_distance.read()
        self.obj_comm.front_parking=self.obj_comm.mbox1_parking.read()
        self.obj_comm.front_emer=self.obj_comm.mbox1_emergency.read()
        self.obj_comm.front_crash=self.obj_comm.mbox1_crash.read()
        self.obj_comm.front_ack=self.obj_comm.mbox1_server_ack.read()
        self.obj_comm.front_travel=self.obj_comm.mbox1_travel.read()
        self.obj_comm.front_sensor=self.obj_comm.mbox1_sensor.read()
        self.obj_comm.front_sensor=self.obj_comm.mbox1_sensor.read()
        p=self.obj_comm.mbox1_sensor.read()
        if p!=None:
            p=p.split(";")
        else:
            p=[0,0,0]
        self.obj_comm.second_id = self.obj_comm.embox_id.read()
        self.obj_comm.second_time = self.obj_comm.embox_time.read()
        self.obj_comm.second_lane = self.obj_comm.embox_lane.read()
        self.obj_comm.second_speed = self.obj_comm.embox_speed.read()
        self.obj_comm.second_distance = self.obj_comm.embox_distance.read()
        self.obj_comm.second_emer=self.obj_comm.embox_emer.read()
        self.obj_comm.second_emerover=self.obj_comm.embox_emergencyover.read()
        self.obj_comm.second_ack=self.obj_comm.embox_server_ack.read()
        self.obj_comm.second_travel=self.obj_comm.embox_travel.read()
        self.obj_comm.second_sensor=self.obj_comm.embox_sensor.read()
        s=self.obj_comm.embox_sensor.read()
        if s !=None:
            s=s.split(";")
        else:
            s=[0,0,0]
        t=datetime.datetime.now()
        
        if self.obj_comm.front_speed!=None:
            if  self.obj_comm.front_speed>0:
                list1=[t,self.obj_comm.front_lane,self.obj_comm.front_speed,self.obj_comm.front_parking,self.obj_comm.front_distance,p[0],p[1],p[2]]
                self.obj_know.write_normalav_log(list1)
        if self.obj_comm.second_speed!=None:
            if self.obj_comm.second_speed>0:
                list2=[t,self.obj_comm.second_speed,self.obj_comm.second_lane,s[0],s[1],s[2]]
                self.obj_know.write_emergav_log(list2)
