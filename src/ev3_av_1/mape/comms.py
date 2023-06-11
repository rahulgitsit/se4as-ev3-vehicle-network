#!/usr/bin/env pybricks-micropython
from pybricks.tools import DataLog, StopWatch, wait
from pybricks.messaging import BluetoothMailboxClient, NumericMailbox, LogicMailbox


class Comms:
    def __init__(self, knowledge_base, id_=1):
        self.id_ = id_
        self.kbase = knowledge_base
        self.kbase.id_ = id_
        self.client = BluetoothMailboxClient()
        self.mbox_id = NumericMailbox("id" + str(id_), self.client)
        self.mbox_time = NumericMailbox("time" + str(id_), self.client)
        self.mbox_lane = NumericMailbox("lane" + str(id_), self.client)
        self.mbox_speed = NumericMailbox("speed" + str(id_), self.client)
        self.mbox_distance = NumericMailbox("distance" + str(id_), self.client)
        self.mbox_parking = NumericMailbox(
            "parking" + str(id_), self.client
        )  # from server
        self.mbox_emergency = NumericMailbox(
            "emergency" + str(id_), self.client
        )  # from server
        self.mbox_crash = NumericMailbox("crash" + str(id_), self.client)
        self.mbox_travelled_distance = NumericMailbox(
            "travel_distance" + str(id_), self.client
        )
        self.mbox_server_ack = NumericMailbox("ack" + str(id_), self.client)
        self.mbox_restart = LogicMailbox("restart" + str(id_), self.client)

    def connect(self, server="C8:E2:65:CD:69:86"):
        print("establishing connection...")
        self.client.connect(server)
        print("server connected!")

        while True:
            if self.mbox_id.read() != None:
                break

    def send_messages(self, park, emergency):
        self.mbox_id.send(self.id_)
        self.mbox_time.send(self.kbase.time)
        self.mbox_lane.send(self.kbase.step)
        self.mbox_speed.send(self.kbase.DRIVE_SPEED)
        self.mbox_distance.send(self.kbase.distance)
        # self.mbox_parking.send(self.kbase.park_ack)
        # self.mbox_emergency.send(emergency)
        self.mbox_crash.send(self.kbase.crash)
        self.mbox_server_ack.send(0)  # check

        if emergency == 10 or emergency == 12:
            self.kbase.emergency = emergency
            self.mbox_emergency.send(100)
            print("==== Emergency message recieved. ====")
            print("----- Emergency in lane: ", emergency % 10, "-----")
        elif emergency == 5:
            print("==== Emergency OVER message recieved ====")
            self.kbase.emergency = False
            self.kbase.alert_mode = False
            # self.kbase.av_light = Color.GREEN
            self.mbox_emergency.send(300)

        if park == 901 and self.kbase.park_ack != 301:
            self.kbase.park_ack = 301
            self.mbox_parking.send(self.kbase.park_ack)
            print("==== Parking command recieved .LOT 1====")
        elif park == 902 and self.kbase.park_ack != 302:
            self.kbase.park_ack = 302
            self.mbox_parking.send(self.kbase.park_ack)
            print("==== Parking command recieved .LOT 2====")

        elif park == 666 and self.kbase.park_ack:
            print("==== Return from parking command recieved ====")
            self.kbase.park_ack = 222
            self.mbox_parking.send(222)

    def monitor_messages(
        self,
    ):
        park_command = self.mbox_parking.read()  # park 888 or 999 => code 1,2
        emergency = self.mbox_emergency.read()
        restart = self.mbox_restart.read()
        ack = self.mbox_server_ack.read()

        print("Restart???? ", restart)

        return park_command, emergency

    def wait_for_ack(self, distance):
        while self.mbox_server_ack.read() != 200:
            self.mbox_crash.send(10 + self.kbase.step)
            self.mbox_travelled_distance.send(int(distance))
            print("SOS! Requesting for emergency vehicle")

    def restart_vehicle(self):
        restart = self.mbox_restart.read()
        print("Low impact incident? ", restart)
        return restart
