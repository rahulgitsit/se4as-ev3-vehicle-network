#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Color


class Planner:
    def __init__(self, knowledge_base):
        self.kbase = knowledge_base

    def derive_plan(self, analysis):
        plan = "P4-drive"
        if analysis == "sos":
            self.kbase.av_light = Color.RED
            self.kbase.stopping = True
            self.kbase.breakdown = True
            plan = "P0-crash"

        elif analysis == "lane2":
            print("========= Switched to lane 2 =====")
            self.kbase.integral = 0.0
            self.kbase.derivative = 0.0
            self.kbase.step = 2
            self.kbase.previousStateChangedTime = self.kbase.time

        elif analysis == "lane1":
            print("========= Switched to lane 1 =====")
            self.kbase.integral = 0.0
            self.kbase.derivative = 0.0
            self.kbase.step = 0
            self.kbase.previousStateChangedTime = self.kbase.time

        elif analysis == "stop":
            self.kbase.av_light = Color.YELLOW
            plan = "P1-stop"

        elif analysis == "emerg-ON":
            if (
                not self.kbase.stopping
                and self.kbase.time >= self.kbase.stop_time + 1000
                and self.kbase.step != 1
                and self.kbase.step != 3
            ):
                self.kbase.stopping = True
                self.kbase.stop_time = self.kbase.time
            else:
                if self.kbase.time >= self.kbase.stop_time + 1000:
                    if self.kbase.step == self.kbase.emergency % 10:
                        print(
                            "\n################# Going into Alert Mode ##################\n"
                        )
                        self.kbase.step = self.kbase.step + 1
                        self.kbase.previousStateChangedTime = self.kbase.time
                    self.kbase.alert_mode = True
                    self.kbase.integral = 0.0
                    self.kbase.derivative = 0.0
                    self.kbase.stopping = False
                    self.kbase.stop_time = self.kbase.time
                    self.kbase.av_light = Color.RED

        elif analysis == "park-ON":
            print(
                "======Setting the angle. Further analysis of parking lot required======="
            )
            if self.kbase.step == 0:
                self.kbase.angle = -1
            elif self.kbase.step == 2:
                self.kbase.angle = 1

            self.kbase.park_analysis_required = True
            plan = "P2-check"

        elif analysis == "lot-occupied":
            print("===== The lot is already occupied. Look for another spot ======")
            self.kbase.park_analysis_required = False
            plan = "P2-drive"

        elif "lot-available" in analysis:
            print("===== The lot is empty. Proceed to park ======")
            self.kbase.stopping = True
            self.kbase.step += 4
            self.kbase.park_ack = 200
            self.kbase.DRIVE_SPEED = 0
            self.kbase.park_analysis_required = False

            if analysis[-1] == "1":
                self.kbase.park_lot_distance = 200

            else:
                self.kbase.park_lot_distance = 400

            plan = "P2-park"

        elif analysis == "ignore":
            self.kbase.distance = 0
            plan = "P3-move"

        elif analysis == "park-OFF":
            print(" ===== Returning from the parking spot... =====")
            self.kbase.park_ack = 0
            self.kbase.step -= 4
            if self.kbase.step == 0:
                self.kbase.angle = -1
            elif self.kbase.step == 2:
                self.kbase.angle = 1
            self.kbase.stopping = False
            self.kbase.DRIVE_SPEED = self.kbase.MIN_SPEED
            plan = "P2-return"

        elif analysis == "switch-lane":
            self.kbase.av_light = Color.YELLOW
            print(
                "------------------------- Obstacle Detected !! ------------------------"
            )
            if (
                not self.kbase.stopping
                and self.kbase.time >= self.kbase.stop_time + 1000
                and self.kbase.step != 1
                and self.kbase.step != 3
            ):
                self.kbase.stopping = True
                self.kbase.stop_time = self.kbase.time
            else:
                if self.kbase.time >= self.kbase.stop_time + 1000:
                    if self.kbase.step == 0 or self.kbase.step == 2:
                        self.kbase.step = self.kbase.step + 1
                        self.kbase.previousStateChangedTime = self.kbase.time
                    self.kbase.integral = 0.0
                    self.kbase.derivative = 0.0
                    self.kbase.stopping = False
                    self.kbase.stop_time = self.kbase.time

        elif analysis == "lane-follow":
            self.kbase.stopping = False
            self.kbase.stop_time = self.kbase.time

        if (
            self.kbase.step == 1
            or self.kbase.step == 3
            or self.kbase.color == self.kbase.STOP_COLOR
        ):
            self.kbase.DRIVE_SPEED = self.kbase.MIN_SPEED
        elif self.kbase.distance > 600:
            if self.kbase.DRIVE_SPEED < self.kbase.MAX_SPEED:
                self.kbase.DRIVE_SPEED = self.kbase.DRIVE_SPEED + 0.5
        elif self.kbase.distance > 550 and self.kbase.distance <= 600:
            self.kbase.DRIVE_SPEED = self.kbase.NORMAL_SPEED
        elif self.kbase.distance > 500 and self.kbase.distance <= 550:
            if self.kbase.DRIVE_SPEED > self.kbase.MIN_SPEED:
                self.kbase.DRIVE_SPEED = self.kbase.DRIVE_SPEED - 1
        else:
            self.kbase.DRIVE_SPEED = self.kbase.MIN_SPEED

        if analysis in ["deviate", "switch-lane", "emerg-ON", "lane2", "lane1"]:
            self.kbase.deviation = self.kbase.reflection - self.kbase.threshold
            print("Calculated deviation: ", self.kbase.deviation)
            if self.kbase.deviation > -10 and self.kbase.deviation < 10:
                self.kbase.integral = 0
            elif self.kbase.deviation * self.kbase.last_deviation < 0:
                self.kbase.integral = 0
            else:
                self.kbase.integral = self.kbase.integral + self.kbase.deviation
            # Calculate the derivative.
            self.kbase.derivative = self.kbase.deviation - self.kbase.last_deviation

            # Calculate the turn rate.
            self.kbase.turn_rate = (
                (self.kbase.PROPORTIONAL_GAIN * self.kbase.deviation)
                + (self.kbase.INTEGRAL_GAIN * self.kbase.integral)
                + (self.kbase.DERIVATIVE_GAIN * self.kbase.derivative)
            )
            print("Calculated turn rate: ", self.kbase.turn_rate)
            self.kbase.last_deviation = self.kbase.deviation

            if self.kbase.step == 1:
                self.kbase.turn_rate = 12
            elif self.kbase.step == 2:
                self.kbase.turn_rate = -1 * self.kbase.turn_rate
            elif self.kbase.step == 3:
                self.kbase.turn_rate = -14

            plan = "P4-drive"

        if self.kbase.reset_distance:
            self.kbase.travelled_distance = 0
            print("Distance reset to 0 in KnowledgeBase")

        # Setting the lights
        if self.kbase.emergency > 9 or self.kbase.analysis == "stop":
            self.kbase.av_light = Color.RED
        elif self.kbase.analysis in "switch-lane":
            self.kbase.av_light = Color.YELLOW
        else:
            self.kbase.alert_mode = False
            self.kbase.av_light = Color.GREEN

        # if analysis != "sos":
        # analysis = None CHANGED FOR RESTART
        analysis = None
        self.kbase.analysis = analysis
        self.kbase.plan = plan
        print("############### The plan is ==> ", plan, " ###############")
        return plan
