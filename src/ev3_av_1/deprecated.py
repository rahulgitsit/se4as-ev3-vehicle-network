#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait
from pybricks.messaging import BluetoothMailboxClient, NumericMailbox


# Sensor module
class Sensor:
    """Sensor class. Contains initialisation of all sensors"""

    def __init__(
        self,
        color_sensor_port=Port.S3,
        ultra_sensor_port=Port.S4,
        touch_sensor_port=Port.S1,
    ):
        self.color_sensor = ColorSensor(color_sensor_port)
        self.ultra_sonic_sensor = UltrasonicSensor(ultra_sensor_port)
        self.touch_sensor = TouchSensor(touch_sensor_port)
        print("---------Sensors initialised-----------")

    def get_sensor_data(self, sensor):
        if sensor == "color":
            return (
                self.color_sensor.reflection(),
                self.color_sensor.color(),
                self.color_sensor.rgb(),
            )
        elif sensor == "ultrasonic":
            return self.ultra_sonic_sensor.distance()
        elif sensor == "touch":
            return self.touch_sensor.pressed()


# Motor module
class ServoMotors:
    """Motor class. Used to initialise the 2 motors of the vehicle"""

    def __init__(self, left_motor_port=Port.B, right_motor_port=Port.C):
        self.left_motor = Motor(left_motor_port)
        self.right_motor = Motor(right_motor_port)
        print("---------Motors initialised-----------")


# Controller Module
class KnowledgeBase:
    """Knowledgebase class. All the variables and config details are part of this class."""

    def __init__(
        self,
        drive_speed=70,
    ):
        self.av_id = 0
        # Current speed, normal speed, maximum speed, and minimum speed
        self.DRIVE_SPEED = drive_speed
        self.NORMAL_SPEED = drive_speed
        self.MAX_SPEED = drive_speed + 30
        self.MIN_SPEED = drive_speed - 10

        # Calculate the light threshold. Choose values based on your measurements.
        self.BLACK = 10
        self.WHITE = 65
        self.threshold = (self.BLACK + self.WHITE) / 2

        # Set the gain of the PID controller.

        self.PROPORTIONAL_GAIN = 0.4
        self.INTEGRAL_GAIN = 0.1
        self.DERIVATIVE_GAIN = 0.5

        # Variables an flags
        self.deviation = 0.0
        self.derivative = 0.0
        self.integral = 0.0
        self.last_deviation = 0.0
        self.turn_rate = 0.0

        self.park_flag = 0

        self.step = 0

        self.time = 0

        # Time that state changed previously
        self.previousStateChangedTime = 0
        # Time that robot has stopped
        self.stop_time = 0
        # The flag to control robot stop or not
        self.stopping = False
        # The flags for emergency vehicle to arrive
        self.sos = False
        self.alert_mode = False

        # Color Codes
        self.STOP = Color.RED
        self.INTERSECTION = "GREEN"  # TODO: To be changed
        self.PARKING_AV = "BLUE"  # BLUE
        self.PARKING_SPCL = "YELLOW"  # YELLOW

        # Sensor Readings
        self.reflection = 0
        self.color = None
        self.rgb = (0, 0, 0)
        self.distance = 0
        self.crash = False

        # Mailbox messages
        self.mbox_parking = 0
        # from server
        self.mbox_emergency = 0
        # from server
        self.mbox_crash = 0
        self.mbox_server_ack = 0

    def update_vars(
        self,
        step,
        integral,
        derivative,
        stopping,
        time,
        previousStateChangedTime,
        stop_time,
        alert_mode,
    ):
        self.step = step
        self.integral = integral
        self.derivative = derivative
        self.stopping = stopping
        self.time = time
        self.previousStateChangedTime = previousStateChangedTime
        self.stop_time = stop_time
        self.alert_mode = alert_mode

    def configure_colors(self, stop, parking_av, parking_spcl):
        """Function to configure the colour codes"""
        self.STOP = stop
        self.PARKING_AV = parking_av
        self.PARKING_SPCL = parking_spcl

    def update_readings(self, reflection, color, rgb, distance, crash):
        self.reflection = reflection
        self.color = color
        self.rgb = rgb
        self.distance = distance
        self.crash = crash

    def update_mboxes(self, parking, emergency, crash, ack):
        self.mbox_parking = parking
        self.mbox_emergency = emergency
        self.mbox_crash = crash
        self.mbox_server_ack = ack


# Monitor Module
class Monitor:
    def __init__(self, knowledge, vehicle_id=1):
        self.sensor = Sensor()
        self.knowledge = knowledge
        self.knowledge.av_id = vehicle_id
        self.watch = 0

        # initialise the mailboxes and bluetooth client for the vehicle
        self.client = BluetoothMailboxClient()
        self.mbox_id = NumericMailbox("id" + str(vehicle_id), self.client)
        self.mbox_time = NumericMailbox("time" + str(vehicle_id), self.client)
        self.mbox_lane = NumericMailbox("lane" + str(vehicle_id), self.client)
        self.mbox_speed = NumericMailbox("speed" + str(vehicle_id), self.client)
        self.mbox_distance = NumericMailbox("distance" + str(vehicle_id), self.client)
        self.mbox_parking = NumericMailbox(
            "parking" + str(vehicle_id), self.client
        )  # from server
        self.mbox_emergency = NumericMailbox(
            "emergency" + str(vehicle_id), self.client
        )  # from server
        self.mbox_crash = NumericMailbox("crash" + str(vehicle_id), self.client)
        self.mbox_server_ack = NumericMailbox("ack" + str(vehicle_id), self.client)
        print("---------Mailboxes initialised-----------")
        print("---------Monitor UP and running----------")

        self.connect()
        self.start_timer()

    def connect(self, server="C8:E2:65:CD:69:86"):
        print("establishing connection...")
        self.client.connect(server)
        print("server connected!")

        while True:
            msg_id = self.mbox_id.read()
            if msg_id != None:
                break
        self.watch = StopWatch()
        self.watch.reset()

    def start_timer(self):
        self.knowledge.time = self.watch.time()

    def get_mailbox(self, mailbox):
        if mailbox == "id":
            return self.mbox_id
        elif mailbox == "time":
            return self.mbox_time
        elif mailbox == "lane":
            return self.mbox_lane
        elif mailbox == "speed":
            return self.mbox_speed
        elif mailbox == "distance":
            return self.mbox_distance
        elif mailbox == "parking":
            return self.mbox_parking
        elif mailbox == "crash":
            return self.mbox_crash
        elif mailbox == "server_ack":
            return self.mbox_server_ack
        elif mailbox == "emergency":
            return self.mbox_emergency

    def read_sensor_data(self, sensor_name):
        return self.sensor.get_sensor_data(sensor_name)

    # Read messages from the SERVER
    def read_from_server(self):
        park_command = self.mbox_parking.read()
        emergency = self.mbox_emergency.read()

        return park_command, emergency


# TODO: A lot! honestly


class Analyse:
    def __init__(self, knowledge):
        self.knowledge = knowledge
        self.alerted = False
        self.off_alert = False
        self.park_alert = False

    def detectable_colors(self, rgb):
        # check for blue
        if rgb[2] >= 65:
            if rgb[0] <= 15:
                if rgb[1] <= 30:
                    return "BLUE"

        # check for yellow
        elif rgb[0] >= 40 and rgb[0] <= 54:
            if rgb[1] >= 25 and rgb[1] <= 35:
                if rgb[2] >= 3 and rgb[2] <= 15:  # was 8 for av1
                    return "YELLOW"
        # check for green
        elif rgb[1] >= 25:
            if rgb[0] <= 10:
                if rgb[2] <= 17:
                    return "GREEN"

    def analyse_state(
        self, color, distance, reflection, rgb, touch, step, park, emergency
    ):
        if emergency and not self.alerted:
            self.alerted = True
            self.off_alert = False
            if emergency % 10 == 0:
                print("Emergency in Lane 1. Alert the planner")
                return "E0"
            elif emergency % 10 == 2:
                print("Emergency in Lane 1. Alert the planner")
                return "E2"

        elif not emergency and not self.off_alert:
            print("Emergency has been resolved")
            self.off_alert = True
            self.alerted = False
            return "Eoff"

        if park == 999 and not self.park_alert:
            print("Parking command recieved from the server.")
            self.park_alert = True
            return "parkACK"

        if touch:
            return "crashed"
        else:
            if color == self.knowledge.STOP:
                return "stop"

            elif (
                self.knowledge.park_flag == 200
                and not self.knowledge.stopping
                and distance > 245
            ):
                print("Looking for parking spot...")
                color = self.detectable_colors(rgb)
                print("Detected color: ", color)

                if color:
                    print("parking spot found")
                    return color
                else:
                    return "drive"

            elif not self.knowledge.stopping and (
                self.detectable_colors(rgb) == self.knowledge.PARKING_AV
                or self.detectable_colors(rgb) == self.knowledge.PARKING_SPCL
                or self.detectable_colors(rgb) == self.knowledge.INTERSECTION
            ):
                return "move"

            elif distance <= 300 and step != 4:
                print(
                    "------------------------- Obstacle Detected !! ------------------------"
                )
                return "obstacle"

            if (
                not self.knowledge.stopping
                and color != self.knowledge.STOP
                and self.knowledge.park_flag != 400
            ):
                return "drive"


class Planner:
    def __init__(self, knowledge_base, monitor):
        self.knowledge_base = (
            knowledge_base  # pass the knowledge_base instance here maybe
        )
        self.alerted = False
        self.monitor = monitor

    def prepare_plan(self, analysis):
        step = self.knowledge_base.step
        integral = self.knowledge_base.integral
        derivative = self.knowledge_base.derivative
        stopping = self.knowledge_base.stopping
        time = self.knowledge_base.time
        previousStateChangedTime = self.knowledge_base.previousStateChangedTime
        stop_time = self.knowledge_base.stop_time
        alert_mode = self.knowledge_base.alert_mode

        if analysis in ["E0", "E2"] and not self.alerted:
            print("Emergency alert. Switch the lane if required. Alert executor.")
            self.alerted = True
            alert_mode = True
            return analysis
        elif analysis == "Eoff":
            self.alerted = False
            self.knowledge_base.alert_mode = False
            return analysis

        elif analysis == "parkACK":
            return analysis
        # Case:1
        if analysis == "crashed":
            self.knowledge_base.stopping = True
            self.knowledge_base.speed = 0
            self.knowledge_base.step += 10
            self.knowledge_base.sos = True
            return "sos"
        else:
            if step == 1:
                if (
                    reflection > 55
                    or color == Color.WHITE
                    or color == Color.YELLOW  # was WHITE
                ) and time >= previousStateChangedTime + 2000:  # time run inside
                    integral = 0.0
                    derivative = 0.0
                    step = 2
                    previousStateChangedTime = time
            elif step == 3 and time >= previousStateChangedTime + 2000:
                if reflection > 55 or color == Color.WHITE or color == Color.YELLOW:
                    integral = 0.0
                    derivative = 0.0
                    step = 0
                    previousStateChangedTime = time
            knowledge_base.update_vars(
                step,
                integral,
                derivative,
                stopping,
                time,
                previousStateChangedTime,
                stop_time,
                alert_mode,
            )
            # Case:2
            if analysis == "stop":
                # add config changes if required
                print("STOP the vehicle")
                return analysis
            # Case:3
            elif analysis in ["E0", "E2"] and not alert_mode:
                if (
                    not stopping
                    and time >= stop_time + 1000
                    and step != 1
                    and step != 3
                ):
                    stopping = True
                    stop_time = time
                else:
                    if time >= stop_time + 1000:
                        # if step == 0 or step == 2:
                        if step == int(analysis[-1]):
                            print(
                                "\n################# Going into Alert Mode ##################\n"
                            )
                            step = step + 1
                            previousStateChangedTime = time
                        alert_mode = True
                        integral = 0.0
                        derivative = 0.0
                        stopping = False
                        stop_time = time

                # stopping = False
                # stop_time = time

            elif analysis == knowledge_base.PARKING_AV:
                print(
                    "+++++++++++++++++++++++Parking spot detected++++++++++++++++++++++++"
                )
                return "park"
            elif analysis == "move":
                return analysis
            elif analysis == "obstacle":
                return analysis
            if step == 1 or step == 3:
                self.knowledge_base.DRIVE_SPEED = self.knowledge_base.MIN_SPEED
            elif distance > 600:
                if self.knowledge_base.DRIVE_SPEED < self.knowledge_base.MAX_SPEED:
                    self.knowledge_base.DRIVE_SPEED = (
                        self.knowledge_base.DRIVE_SPEED + 0.5
                    )
            elif distance > 550 and distance <= 600:
                self.knowledge_base.DRIVE_SPEED = self.knowledge_base.NORMAL_SPEED
            elif distance > 500 and distance <= 550:
                if self.knowledge_base.DRIVE_SPEED > self.knowledge_base.MIN_SPEED:
                    self.knowledge_base.DRIVE_SPEED = (
                        self.knowledge_base.DRIVE_SPEED - 1
                    )
            else:
                self.knowledge_base.DRIVE_SPEED = self.knowledge_base.MIN_SPEED

            if analysis == "drive":
                # Calculate the deviation from the threshold.
                reflection, _, _ = self.monitor.read_sensor_data("color")
                self.knowledge_base.deviation = (
                    reflection - self.knowledge_base.threshold
                )
                # Calculate the integral.
                # if (
                #     detectable_colors(rgb) == INTERSECTION
                #     or detectable_colors(rgb) == PARKING_AV
                #     and not park
                # ):
                #     # robot.settings(DRIVE_SPEED, 0,0,0)
                #     robot.straight(50)

                if (
                    self.knowledge_base.deviation > -10
                    and self.knowledge_base.deviation < 10
                ):
                    self.knowledge_base.integral = 0
                elif (
                    self.knowledge_base.deviation * self.knowledge_base.last_deviation
                    < 0
                ):
                    self.knowledge_base.integral = 0
                else:
                    self.knowledge_base.integral = (
                        self.knowledge_base.integral + self.knowledge_base.deviation
                    )
                # Calculate the derivative.
                self.knowledge_base.derivative = (
                    self.knowledge_base.deviation - self.knowledge_base.last_deviation
                )

                # Calculate the turn rate.
                self.knowledge_base.turn_rate = (
                    (
                        self.knowledge_base.PROPORTIONAL_GAIN
                        * self.knowledge_base.deviation
                    )
                    + (self.knowledge_base.INTEGRAL_GAIN * self.knowledge_base.integral)
                    + (
                        self.knowledge_base.DERIVATIVE_GAIN
                        * self.knowledge_base.derivative
                    )
                )

                # step 0: use the calculated turn_rate
                # step 1: robot is turning right
                # step 2: use the opposite calculated turn_rate
                # step 3: robot is turning left
                if self.knowledge_base.step == 1:
                    self.knowledge_base.turn_rate = 12
                elif self.knowledge_base.step == 2:
                    self.knowledge_base.turn_rate = -1 * self.knowledge_base.turn_rate
                elif self.knowledge_base.step == 3:
                    self.knowledge_base.turn_rate = -14

                return analysis

        knowledge_base.update_vars(
            step,
            integral,
            derivative,
            stopping,
            time,
            previousStateChangedTime,
            stop_time,
            alert_mode,
        )


class Execute:
    def __init__(self, monitor, knowledgebase):
        self.monitor = monitor
        self.knowledge_base = knowledgebase
        self.motors = ServoMotors()
        # Initialize the drive base.
        self.robot = DriveBase(
            self.motors.left_motor,
            self.motors.right_motor,
            wheel_diameter=55.5,
            axle_track=118,
        )
        self.ev3 = EV3Brick()

    def inform_server(
        self,
    ):
        # Send messages to the SERVER.
        self.av_id = self.monitor.get_mailbox("id")
        self.timebox = self.monitor.get_mailbox("time")
        self.lane = self.monitor.get_mailbox("lane")
        self.speed = self.monitor.get_mailbox("speed")
        self.distancebox = self.monitor.get_mailbox("distance")
        self.parking = self.monitor.get_mailbox("parking")
        self.crash = self.monitor.get_mailbox("crash")
        self.emergency = self.monitor.get_mailbox("emergency")

        self.av_id.send(self.knowledge_base.av_id)
        self.timebox.send(self.knowledge_base.time)
        self.lane.send(self.knowledge_base.step)
        self.speed.send(self.knowledge_base.DRIVE_SPEED)
        self.distancebox.send(self.monitor.read_sensor_data("ultrasonic"))
        park, emerg = self.monitor.read_from_server()
        if park:
            self.parking.send(self.knowledge_base.park_flag)
        if emerg:
            self.emergency.send(emerg)
        self.crash.send(self.knowledge_base.sos)

    def emergency_or_park_ack(self, emergency, park_command):
        if emergency:
            self.ev3.light.on(Color.RED)
            print("//////////////////// CAUTION !!! /////////////////////")
            self.emergency.send(100)
        else:
            self.emergency.send(300)
            self.ev3.light.on(Color.GREEN)

        if park_command and self.knowledge_base.park_flag != 200:
            print("Sending ACK to server")
            self.knowledge_base.park_flag = 200
            self.parking.send(
                self.knowledge_base.park_flag
            )  # TODO: Status code for recieving parking signal
        elif park_command == 666:
            self.knowledge_base.step -= 4
            self.knowledge_base.park_flag = 222
            self.parking.send(self.knowledge_base.park_flag)

    def execute_plan(self, plan):
        reflection, color, rgb = self.monitor.read_sensor_data("color")
        step = self.knowledge_base.step
        integral = self.knowledge_base.integral
        derivative = self.knowledge_base.derivative
        stopping = self.knowledge_base.stopping
        time = self.knowledge_base.time
        previousStateChangedTime = self.knowledge_base.previousStateChangedTime
        stop_time = self.knowledge_base.stop_time
        alert_mode = self.knowledge_base.alert_mode

        # Server ACKS for emergency or parking
        if plan == "E0" or plan == "E2":
            print("Send emergency ACK to server.")
            self.emergency_or_park_ack(True, False)

        elif plan == "emergOff":
            self.emergency_or_park_ack(False, False)

        if plan == "parkACK":
            self.emergency_or_park_ack(False, True)

        # Execution of vehicle states as per the plans
        # Case:1
        if plan == "sos":
            self.robot.stop()
            self.ev3.light.on(self.knowledge_base.STOP)
            self.ev3.speaker.beep()

            while self.monitor.get_mailbox("server_ack").read() != 200:
                self.inform_server()
                print("-==-=-=-=-=-=-=-=-VEHICLE CRASHED. SOS TO SERVER=-=-=-=-=-=")

            print(
                "####################### WAITING FOR EMERGENCY VEHICLE ########################"
            )
            return

        else:
            # Case:2
            if plan == "stop":
                self.knowledge_base.DRIVE_SPEED = self.knowledge_base.MIN_SPEED
                self.robot.stop()
                return
            # Case:3:Handled in planner
            # Case:4
            elif plan == "park":
                self.robot.stop()

                if step == 0:
                    angle = -1
                elif step == 2:
                    angle = 1

                self.robot.turn(angle * 90)
                wait(2000)
                distance = self.monitor.read_sensor_data("ultrasonic")

                print("\nDistance ahead: ", distance)
                if distance < 200:  # TODO! Calibrate the values
                    print(
                        "+++++++++++Parking lot occupied. Search for another spot.+++++++++++"
                    )

                    self.robot.turn(-angle * 90)
                    self.robot.straight(100)
                else:
                    self.robot.straight(200)
                    self.robot.turn(-angle * 90)
                    print(
                        "++++++++++++++++++++++.Vehicle parked.+++++++++++++++++++++++++++++"
                    )
                    self.knowledge_base.stopping = True
                    self.knowledge_base.step += 4  # Check the impact of this. To denote parking. NEED TO STORE PREVIOUS STATE. maybe add some constant to step instead of storing the prev state
                    self.knowledge_base.park_flag = 400
                    monitor.get_mailbox("parking").send(400)
                    self.knowledge_base.DRIVE_SPEED = 0

            elif plan == "move":
                self.robot.straight(50)
            elif plan == "obstacle":
                self.ev3.light.on(Color.YELLOW)
                # robot.stop()
                print(
                    "------------------------- Obstacle Detected !! ------------------------"
                )
                if (
                    not stopping
                    and time >= stop_time + 1000
                    and step != 1
                    and step != 3
                ):
                    stopping = True
                    stop_time = time
                else:
                    if time >= stop_time + 1000:
                        if step == 0 or step == 2:
                            step = step + 1
                            previousStateChangedTime = time
                        integral = 0.0
                        derivative = 0.0
                        stopping = False
                        stop_time = time
            elif not self.knowledge_base.park_flag:
                stopping = False
                stop_time = time

            knowledge_base.update_vars(
                step,
                integral,
                derivative,
                stopping,
                time,
                previousStateChangedTime,
                stop_time,
                alert_mode,
            )

            if plan == "drive":
                self.robot.drive(
                    self.knowledge_base.DRIVE_SPEED, self.knowledge_base.turn_rate
                )

                self.knowledge_base.last_deviation = self.knowledge_base.deviation
            else:
                self.robot.stop()


################################################################################################################################################


# Start of main
if __name__ == "__main__":
    # Create the class instances
    knowledge_base = KnowledgeBase()
    monitor = Monitor(knowledge_base, 1)
    analyser = Analyse(knowledge_base)
    planner = Planner(knowledge_base, monitor)
    executor = Execute(monitor, knowledge_base)

    while True:
        # monitor all the sensors and mailboxes
        reflection, color, rgb = monitor.read_sensor_data("color")
        distance = monitor.read_sensor_data("ultrasonic")
        crash = monitor.read_sensor_data("crash")
        park, emergency = monitor.read_from_server()

        if park:
            print("Should park ??: ", park)
        # park or emergency message from the server ORDER CHANGES> CHANGE IN SERVER AS WELL
        executor.inform_server()  # informing the server of the state variables to communicate to other

        analysis = analyser.analyse_state(
            color,
            distance,
            reflection,
            rgb,
            crash,
            knowledge_base.step,
            park,
            emergency,
        )  # analyse the monitored values
        plan = planner.prepare_plan(analysis)
        executor.execute_plan(plan)
