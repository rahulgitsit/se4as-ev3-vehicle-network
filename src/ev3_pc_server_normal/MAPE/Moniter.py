class Moniter:
    def __init__(self,obj_comm):
        self.obj_comm=obj_comm
    
    def read_mailbox(self):
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

        self.obj_comm.second_id = self.obj_comm.mbox2_id.read()
        self.obj_comm.second_time = self.obj_comm.mbox2_time.read()
        self.obj_comm.second_lane = self.obj_comm.mbox2_lane.read()
        self.obj_comm.second_speed = self.obj_comm.mbox2_speed.read()
        self.obj_comm.second_distance = self.obj_comm.mbox2_distance.read()
        self.obj_comm.second_parking=self.obj_comm.mbox2_parking.read()
        self.obj_comm.second_emer=self.obj_comm.mbox2_emergency.read()
        self.obj_comm.second_crash=self.obj_comm.mbox2_crash.read()
        self.obj_comm.second_ack=self.obj_comm.mbox2_server_ack.read()
        self.obj_comm.second_travel=self.obj_comm.mbox2_travel.read()
