from pybricks.messaging import BluetoothMailboxServer, NumericMailbox, TextMailbox
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
        self.mbox1_sensor=TextMailbox("sensor1",self.server)
        

        # second normal vehicle mailbox
        self.mbox2_id = NumericMailbox('id2', self.server)
        self.mbox2_time = NumericMailbox('time2', self.server)
        self.mbox2_lane = NumericMailbox('lane2', self.server)
        self.mbox2_speed = NumericMailbox('speed2', self.server)
        self.mbox2_distance = NumericMailbox('distance2', self.server)
        self.mbox2_parking= NumericMailbox('parking2',self.server)
        self.mbox2_emergency=NumericMailbox('emergency2',self.server)
        self.mbox2_crash=NumericMailbox("crash2",self.server)
        self.mbox2_server_ack=NumericMailbox('ack2',self.server)
        self.mbox2_travel=NumericMailbox('travel_distance2',self.server)
        self.mbox2_sensor=TextMailbox("sensor2",self.server)

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
        self.front_sensor=self.mbox1_sensor.read()


        #read from normal vehicle
        self.second_id = self.mbox2_id.read()
        self.second_time = self.mbox2_time.read()
        self.second_lane = self.mbox2_lane.read()
        self.second_speed = self.mbox2_speed.read()
        self.second_distance = self.mbox2_distance.read()
        self.second_parking=self.mbox2_parking.read()
        self.second_emer=self.mbox2_emergency.read()
        self.second_crash=self.mbox2_crash.read()
        self.second_ack=self.mbox2_server_ack.read()
        self.second_travel=self.mbox2_travel.read()
        self.second_sensor=self.mbox2_sensor.read()
