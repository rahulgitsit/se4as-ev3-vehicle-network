#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.media.ev3dev import Font, SoundFile


class Executer:
    def __init__(
        self, knowledge_base, comms, left_motor_port=Port.B, right_motor_port=Port.C
    ):
        self.kbase = knowledge_base
        self.comms = comms
        self.left_motor = Motor(left_motor_port)
        self.right_motor = Motor(right_motor_port)
        self.robot = DriveBase(
            self.left_motor, self.right_motor, wheel_diameter=55.5, axle_track=118
        )
        self.ev3 = EV3Brick()
        self.big_font = Font(size=100, bold=True)
        self.ev3.screen.set_font(self.big_font)

    def execute(self, plan):
        self.ev3.screen.draw_text(60, 50, "AV" + str(self.kbase.id_))
        if plan == "P0-crash":
            self.robot.stop()
            self.kbase.travelled_distance = self.robot.distance()
            # self.ev3.speaker.beep()
            print("Travelled distance: ", self.kbase.travelled_distance)
            self.comms.wait_for_ack(self.kbase.travelled_distance)
            while not self.comms.restart_vehicle():
                self.ev3.light.on(Color.YELLOW)
                wait(1000)
                self.ev3.light.on(Color.RED)
                wait(1000)
                print("======== Waiting for Emergency Vehicle ========")

            print("======== Vehicle restarted! ========")

        elif plan == "P1-stop":
            self.ev3.light.on(self.kbase.av_light)
            self.robot.stop()

        elif plan == "P2-check":
            print(" ======= Checking the parking lot! =======")
            self.robot.stop()
            self.robot.turn(self.kbase.angle * 90)
            wait(2000)

        elif plan == "P2-drive":
            print(" ====== Returning to track to look for another track ======")
            self.robot.turn(-self.kbase.angle * 90)
            self.robot.straight(100)

        elif plan == "P2-park":
            print(" ====== Vehicle is Parked ======")
            self.robot.straight(self.kbase.park_lot_distance)
            self.robot.turn(-self.kbase.angle * 90)
            self.robot.straight(300)
            self.ev3.speaker.play_file(SoundFile.MOTOR_STOP)
            self.comms.mbox_parking.send(self.kbase.park_ack)

        elif plan == "P2-return":
            print("======== Vehicle exited the parking lot =======")
            # ev3.speaker.play_file(SoundFile.MOTOR_START)
            self.robot.straight(-300)
            self.robot.turn(-self.kbase.angle * 90)
            self.robot.straight(self.kbase.park_lot_distance)
            self.robot.turn(self.kbase.angle * 90)

        elif plan == "P3-move":
            self.robot.straight(50)

        elif plan == "P4-drive":
            self.ev3.light.on(self.kbase.av_light)
            print("===== keep going =====")
            self.robot.drive(self.kbase.DRIVE_SPEED, self.kbase.turn_rate)

        else:
            self.robot.stop()

        # if plan != "P0-crash":
        #     plan = None
        #     self.kbase.plan = plan CHANGED FOR RESTART

        self.kbase.plan = None

        if self.kbase.reset_distance:
            print("Distance reset in robot!")
            self.ev3.speaker.beep()
            self.robot.reset()
