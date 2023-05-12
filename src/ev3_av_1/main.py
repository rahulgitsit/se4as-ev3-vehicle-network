#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port, Color
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait
from pybricks.messaging import BluetoothMailboxClient, NumericMailbox
from pybricks.media.ev3dev import Font, SoundFile


"""KnowledgeBase section of MAPE-K loop system. Consists of the variables and flags used throughout the program. Knowledgebase is accessible to Monitor, Analyser, Planner, and Executor.
"""
# Current speed, normal speed, maximum speed, and minimum speed
DRIVE_SPEED = 70
NORMAL_SPEED = 70
MAX_SPEED = 100
MIN_SPEED = 60

# Calculate the light threshold. Choose values based on your measurements.
BLACK = 10
WHITE = 65
threshold = (BLACK + WHITE) / 2

# Set the gain of the PID controssller.
PROPORTIONAL_GAIN = 0.4
INTEGRAL_GAIN = 0.1
DERIVATIVE_GAIN = 0.5

# Colour codes
STOP_COLOR = Color.RED
INTERSECTION = "GREEN"  # TODO: To be changed
PARKING_AV = "BLUE"  # BLUE
PARKING_SPCL = "YELLOW"  # YELLOW

# Intialize variables related to PID controller.
deviation = 0.0
derivative = 0.0
integral = 0.0
last_deviation = 0.0
turn_rate = 0.0

# Lane change state
# step 0: drive on the outer lane
# step 1: change lane (from outer to inner)
# step 2: drive on the inner lane
# step 3: change lane (from inner to outer)
step = 0
# Time that state changed previously
previousStateChangedTime = 0
# Time that robot has stopped
stop_time = 0
# The flag to control robot stop or not
stopping = False

# The flag for emergency vehicle to arrive
sos = False

crash = False
emergency = False
park_ack = 0
alert_mode = False
park_analysis_required = False
analysis = "lane-follow"


"""Initialise the motors and sensors of the vehicle."""
# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Initialize the color sensor.
line_sensor = ColorSensor(Port.S3)

# Initialize the ultrasonic sensor. It is used to detect
# obstacles as the robot drives around.
obstacle_sensor = UltrasonicSensor(Port.S4)

# Initialise touch sensor
crash_sensor = TouchSensor(Port.S1)


# Colour analysis function used inside analysis section
def detectable_colors(rgb):
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


# Initialize the drive base.
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=118)
ev3 = EV3Brick()

# data = DataLog('time', 'step', 'color', 'speed', 'distance', 'stop', 'deviation', 'integral', 'derivative')

# Initialize Bluetooth client and mailboxes for message passing.
client = BluetoothMailboxClient()
mbox_id = NumericMailbox("id1", client)
mbox_time = NumericMailbox("time1", client)
mbox_lane = NumericMailbox("lane1", client)
mbox_speed = NumericMailbox("speed1", client)
mbox_distance = NumericMailbox("distance1", client)
mbox_parking = NumericMailbox("parking1", client)  # from server
mbox_emergency = NumericMailbox("emergency1", client)  # from server
mbox_crash = NumericMailbox("crash1", client)
mbox_server_ack = NumericMailbox("ack1", client)  # TODO: Do we need this? #from server


# Server robot name
SERVER = "C8:E2:65:CD:69:86"
print("establishing connection...")
client.connect(SERVER)
print("server connected!")

# # Wait until receive message from the negotiator.
while True:
    msg_id = mbox_id.read()
    if msg_id != None:
        break

# Start time.
watch = StopWatch()
watch.reset()


big_font = Font(size=100, bold=True)
ev3.screen.set_font(big_font)


while True:
    time = watch.time()
    ev3.screen.draw_text(60, 50, "AV1")

    # Monitor section
    """Monitor the sensor readings as well as the messages send from the server"""
    reflection = line_sensor.reflection()
    color = line_sensor.color()
    rgb = line_sensor.rgb()
    distance = obstacle_sensor.distance()
    crash = crash_sensor.pressed()

    # Send messages to the SERVER.
    mbox_id.send(1)
    mbox_time.send(time)
    mbox_lane.send(step)
    mbox_speed.send(DRIVE_SPEED)
    mbox_distance.send(distance)
    mbox_parking.send(park_ack)

    # Monitor the messages from the SERVER
    park_command = mbox_parking.read()
    emergency = mbox_emergency.read()

    # Second ack for the messages send by the server
    if emergency:
        mbox_emergency.send(100)
    else:
        av_light = Color.GREEN
        mbox_emergency.send(300)

    if park_command == 999 and park_ack != 200:
        park_ack = 200
        mbox_parking.send(park_ack)
        print("==== Parking command recieved ====")
    elif park_command == 666 and park_ack:
        print("==== Return from parking command recieved ====")
        park_ack = 222
        mbox_parking.send(park_ack)

    # Analysis Section
    """ Analyser analyses the sensor readings and the messages from the server. The analysis is then passed to the planner section."""
    # Case 1 - Vehicle crashed
    if crash:
        analysis = "sos"
    elif park_analysis_required:
        if distance < 200:
            analysis = "lot-occupied"
        else:
            analysis = "lot-available"
    else:
        if step == 1 and emergency % 10 != 2:
            if (
                reflection > 55
                or color == Color.WHITE
                or color == Color.YELLOW  # was WHITE
            ) and time >= previousStateChangedTime + 2000:
                analysis = "lane2"
        elif (
            step == 3
            and time >= previousStateChangedTime + 2000
            and emergency % 10 != 0
        ):
            if reflection > 55 or color == Color.WHITE or color == Color.YELLOW:
                analysis = "lane1"

        # Case 3  Stop sign detected
        if color == STOP_COLOR:
            analysis = "stop"

        # Case 4 - Emergency situation
        elif emergency and not alert_mode:
            analysis = "emerg-ON"

        # Case 5-a - Parking
        elif park_ack == 200 and not stopping and distance > 245:
            if (detectable_colors(rgb)) == PARKING_AV:
                print(
                    "+++++++++++++++++++++++Parking spot detected++++++++++++++++++++++++"
                )
                analysis = "park-ON"
            elif (
                detectable_colors(rgb) == INTERSECTION
                or detectable_colors(rgb) == PARKING_SPCL
            ):
                analysis = "ignore"

        # Case 5-b - Return from parking
        elif park_ack == 222:
            print("+++++++++++++++++++++++Exit from Parking++++++++++++++++++++++++")
            analysis = "park-OFF"

        elif not stopping and (
            detectable_colors(rgb) == PARKING_AV
            or detectable_colors(rgb) == PARKING_SPCL
            or detectable_colors(rgb) == INTERSECTION
        ):
            analysis = "ignore"

        # Case 6 - Obstacle detected
        elif distance <= 300 and step < 4 and analysis not in ["lane2", "lane1"]:
            analysis = "switch-lane"

        # Case 7 - Follow the lane
        elif not park_ack and analysis not in ["lane2", "lane1"]:
            analysis = "lane-follow"
        #     stopping=False
        #     stop_time =time

        if (
            not stopping
            and color != STOP_COLOR
            and analysis not in ["park-ON", "switch-lane", "lane2", "lane1", "emerg-ON"]
        ):
            print("Is this being executed???")
            analysis = "deviate"
        elif analysis not in [
            "park-ON",
            "park-OFF",
            "switch-lane",
            "lane2",
            "lane1",
            "emerg-ON",
        ]:
            print("==== stop the vehicle ====")
            analysis = "stop"

    print("############### The analysis is ==> ", analysis, " ###############")

    # Planner Section
    """ According to the analysis the planner derives a plan of action. The variables and flags in the knowledgebase are modified to make the executor work as desired."""
    if analysis == "sos":
        av_light = Color.RED
        stopping = True
        plan = "P0-crash"

    elif analysis == "lane2":
        print("========= Switched to lane 2 =====")
        integral = 0.0
        derivative = 0.0
        step = 2
        previousStateChangedTime = time

    elif analysis == "lane1":
        print("========= Switched to lane 1 =====")
        integral = 0.0
        derivative = 0.0
        step = 0
        previousStateChangedTime = time

    elif analysis == "stop":
        av_light = Color.YELLOW
        plan = "P1-stop"

    elif analysis == "emerg-ON":
        if not stopping and time >= stop_time + 1000 and step != 1 and step != 3:
            stopping = True
            stop_time = time
        else:
            if time >= stop_time + 1000:
                if step == emergency % 10:
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
                av_light = Color.RED

    elif analysis == "park-ON":
        print(
            "======Setting the angle. Further analysis of parking lot required======="
        )
        if step == 0:
            angle = -1
        elif step == 2:
            angle = 1

        park_analysis_required = True
        plan = "P2-check"

    elif analysis == "lot-occupied":
        print("===== The lot is already occupied. Look for another spot ======")
        park_analysis_required = False
        plan = "P2-drive"

    elif analysis == "lot-available":
        print("===== The lot is empty. Proceed to park ======")
        stopping = True
        step += 4
        park_ack = 200
        DRIVE_SPEED = 0
        park_analysis_required = False
        plan = "P2-park"

    elif analysis == "ignore":
        plan = "P3-move"

    elif analysis == "park-OFF":
        print(" ===== Returning from the parking spot... =====")
        park_ack = 0
        step -= 4
        if step == 0:
            angle = -1
        elif step == 2:
            angle = 1
        stopping = False
        DRIVE_SPEED = MIN_SPEED
        plan = "P2-return"

    elif analysis == "switch-lane":
        av_light = Color.YELLOW
        print("------------------------- Obstacle Detected !! ------------------------")
        if not stopping and time >= stop_time + 1000 and step != 1 and step != 3:
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

    elif analysis == "lane-follow":
        stopping = False
        stop_time = time

    if step == 1 or step == 3 or color == STOP_COLOR:
        DRIVE_SPEED = MIN_SPEED
    elif distance > 600:
        if DRIVE_SPEED < MAX_SPEED:
            DRIVE_SPEED = DRIVE_SPEED + 0.5
    elif distance > 550 and distance <= 600:
        DRIVE_SPEED = NORMAL_SPEED
    elif distance > 500 and distance <= 550:
        if DRIVE_SPEED > MIN_SPEED:
            DRIVE_SPEED = DRIVE_SPEED - 1
    else:
        DRIVE_SPEED = MIN_SPEED

    if analysis in ["deviate", "switch-lane"]:
        deviation = reflection - threshold
        if deviation > -10 and deviation < 10:
            integral = 0
        elif deviation * last_deviation < 0:
            integral = 0
        else:
            integral = integral + deviation
        # Calculate the derivative.
        derivative = deviation - last_deviation

        # Calculate the turn rate.
        turn_rate = (
            (PROPORTIONAL_GAIN * deviation)
            + (INTEGRAL_GAIN * integral)
            + (DERIVATIVE_GAIN * derivative)
        )

        last_deviation = deviation

        # step 0: use the calculated turn_rate
        # step 1: robot is turning right
        # step 2: use the opposite calculated turn_rate
        # step 3: robot is turning left
        if step == 1:
            turn_rate = 12
        elif step == 2:
            turn_rate = -1 * turn_rate
        elif step == 3:
            turn_rate = -14

        plan = "P4-drive"

    # Setting the lights
    if emergency:
        av_light = Color.RED
    elif analysis == "stop":
        av_light = Color.YELLOW
    else:
        av_light = Color.GREEN

    analysis = None
    print("############### The plan is ==> ", plan, " ###############")

    # Executor section
    """Executor just executes the plan devised by the planner component.Thus completing the MAPE-K feedback."""

    if plan == "P0-crash":
        ev3.light.on(av_light)
        robot.stop()

        while mbox_server_ack.read() != 200:
            ev3.speaker.beep()
            mbox_id.send(1)
            mbox_time.send(time)
            mbox_lane.send(step)
            mbox_speed.send(0)
            mbox_distance.send(0)
            mbox_crash.send(10 + step)
            print("-==-=-=-=-=-=-=-=-VEHICLE CRASHED. SOS TO SERVER=-=-=-=-=-=")

        print("======== Waiting for Emergency Vehicle ========")

    elif plan == "P1-stop":
        ev3.light.on(av_light)
        robot.stop()

    elif plan == "P2-check":
        print(" ======= Checking the parking lot! =======")
        robot.stop()
        robot.turn(angle * 90)
        wait(2000)

    elif plan == "P2-drive":
        print(" ====== Returning to track to look for another track ======")
        robot.turn(-angle * 90)
        robot.straight(100)

    elif plan == "P2-park":
        print(" ====== Vehicle is Parked ======")
        robot.straight(200)
        robot.turn(-angle * 90)
        # ev3.speaker.play_file(SoundFile.MOTOR_STOP)
        mbox_parking.send(park_ack)

    elif plan == "P2-return":
        print("======== Vehicle exited the parking lot =======")
        # ev3.speaker.play_file(SoundFile.MOTOR_START)
        robot.turn(-angle * 90)
        robot.straight(200)
        robot.turn(angle * 90)

    elif plan == "P3-move":
        robot.straight(50)

    elif plan == "P4-drive":
        ev3.light.on(av_light)
        print("===== keep going =====")
        robot.drive(DRIVE_SPEED, turn_rate)

    else:
        robot.stop()
    plan = None
    print("__________________________")
    print("step: " + str(step))
    print("park: ", park_ack)
    print("emergency: ", emergency)
    print("stopping: ", stopping)
    print("color: " + str(color))
    print("reflection: " + str(reflection))
    # print("speed: " + str(DRIVE_SPEED))
    print("distance: " + str(distance))
    # print("turn rate: " + str(turn_rate))
    print("__________________________")

    end_time = watch.time()
