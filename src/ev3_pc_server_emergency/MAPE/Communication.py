from pybricks.messaging import BluetoothMailboxServer, NumericMailbox, LogicMailbox


class Communication:
    def __init__(self):
        self.server = BluetoothMailboxServer()

        print("Waiting for  clients")
        self.server.wait_for_connection(3)
        print("All device connected!")

        #pc_client mail box
        self.admin_id=NumericMailbox('admin',self.server)
        self.admin_command=NumericMailbox('cmd',self.server)

        # first normal vehicle mailbox
        self.mbox1_id = NumericMailbox('id1', self.server)
        self.mbox1_time = NumericMailbox('time1', self.server)
        self.mbox1_lane = NumericMailbox('lane1', self.server)
        self.mbox1_speed = NumericMailbox('speed1', self.server)
        self.mbox1_distance = NumericMailbox('distance1', self.server)
        self.mbox1_parking= NumericMailbox('parking1',self.server)
        self.mbox1_emergency=NumericMailbox('emergency1',self.server)
        self.mbox1_crash=NumericMailbox("crash1",self.server)
        self.mbox1_server_ack=NumericMailbox('ack1',self.server)
        self.mbox1_travel=NumericMailbox('travel_distance1',self.server)
        self.mbox1_restart=LogicMailbox('restart1',self.server)
        
        # emergency vehicle mailbox
        self.embox_id = NumericMailbox("id2", self.server)
        self.embox_time = NumericMailbox("time2", self.server)
        self.embox_lane = NumericMailbox("lane2", self.server)
        self.embox_speed = NumericMailbox("speed2", self.server)
        self.embox_distance = NumericMailbox("distance2", self.server)
        self.embox_emer=NumericMailbox("emer2",self.server)
        self.embox_server_ack = NumericMailbox("ack1", self.server)
        self.embox_travel=NumericMailbox("travel_distance2",self.server)
        self.embox_emergencyover = NumericMailbox("emergency1", self.server)
        self.embox_restart=LogicMailbox('restart2',self.server)

        #read from pc_client
        self.admin_cmd=self.admin_command.read()

        #read from normal vehicle
        self.front_id = self.mbox1_id.read()
        self.front_time = self.mbox1_time.read()
        self.front_lane = self.mbox1_lane.read()
        self.front_speed = self.mbox1_speed.read()
        self.front_distance = self.mbox1_distance.read()
        self.front_parking=self.mbox1_parking.read()
        self.front_emer=self.mbox1_emergency.read()
        self.front_crash=self.mbox1_crash.read()
        self.front_ack=self.mbox1_server_ack.read()
        self.front_travel=self.mbox1_travel.read()

        #read from emergency vehicle
        self.second_id = self.embox_id.read()
        self.second_time = self.embox_time.read()
        self.second_lane = self.embox_lane.read()
        self.second_speed = self.embox_speed.read()
        self.second_distance = self.embox_distance.read()
        self.second_emer=self.embox_emer.read()
        self.second_emerover=self.embox_emergencyover.read()
        self.second_ack=self.embox_server_ack.read()
        self.second_travel=self.embox_travel.read()
