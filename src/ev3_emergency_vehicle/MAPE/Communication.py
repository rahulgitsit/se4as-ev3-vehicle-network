#!/usr/bin/env pybricks-micropython
from pybricks.messaging import BluetoothMailboxClient, NumericMailbox, LogicMailbox,TextMailbox
class Communication:
    def __init__(self):
        self.SERVER = 'C8:E2:65:CD:69:86'
        self.client = BluetoothMailboxClient()
        self.embox_id = NumericMailbox('id2', self.client)
        self.embox_time = NumericMailbox('time2', self.client)
        self.embox_lane = NumericMailbox('lane2', self.client)
        self.embox_speed = NumericMailbox('speed2', self.client)
        self.embox_distance = NumericMailbox('distance2', self.client)
        self.embox_emer=NumericMailbox("emer2",self.client)
        self.embox_emergencyover = NumericMailbox("emergency1", self.client)
        self.embox_traveldistance= NumericMailbox("travel_distance2",self.client)
        self.embox_restart= LogicMailbox("restart2",self.client)
        self.embox_sensor=TextMailbox("sensor2",self.client)

    def connect_server(self):
        print('establishing connection...')
        self.client.connect(self.SERVER)
        print('server connected!')
        while True:
            msg_id = self.embox_id.read()
            if msg_id != None:
                break
    
    def read_all_values(self):# read all values from brick
        self.emerg=self.embox_emer.read()
        self.v_speed=self.embox_speed.read()
        self.v_lane=self.embox_lane.read()
        self.v_time=self.embox_time.read()
        self.v_travel=self.embox_traveldistance.read()
