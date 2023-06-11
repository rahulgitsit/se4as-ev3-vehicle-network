#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Color


class Analyser:
    def __init__(self, knowledge_base):
        self.kbase = knowledge_base

    # Colour analysis function used inside analysis section
    def detectable_colors(self, rgb):
        if not rgb:
            rgb = self.kbase.rgb
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
        elif rgb[1] >= 17:
            if rgb[0] <= 10:
                if rgb[2] <= 20:
                    return "GREEN"

    def analyse(self, reflection, color, rgb, distance, crash):
        analysis = None
        # TODO: ADDED FOR TESTING
        # self.kbase.emergency = emergency

        # if crash or self.kbase.breakdown:
        # analysis = "sos" CHANGED FOR RESTART

        stop_cases = [
            "park-ON",
            "park-OFF",
            "switch-lane",
            "lane2",
            "lane1",
            "emerg-ON",
            "lane-follow",
        ]

        deviate_cases = ["park-ON", "switch-lane", "lane2", "lane1", "emerg-ON"]

        if crash:
            analysis = "sos"
        elif self.kbase.park_analysis_required:
            if distance < 200:
                analysis = "lot-occupied"
            elif self.kbase.park_ack == 301:
                analysis = "lot-available1"
            elif self.kbase.park_ack == 302:
                analysis = "lot-available2"

        else:
            if self.kbase.step == 1:
                if (
                    reflection > 55
                    or color == Color.WHITE
                    or color == Color.YELLOW  # was WHITE
                ) and self.kbase.time >= self.kbase.previousStateChangedTime + 2000:
                    analysis = "lane2"
            elif (
                self.kbase.step == 3
                and self.kbase.time >= self.kbase.previousStateChangedTime + 2000
            ):
                if reflection > 55 or color == Color.WHITE or color == Color.YELLOW:
                    analysis = "lane1"

            # Case 3  Stop sign detected
            if color == self.kbase.STOP_COLOR:
                print("RED COLOR DETECTED")
                analysis = "stop"

            # Case 4 - Emergency situation
            elif self.kbase.emergency and not self.kbase.alert_mode:
                analysis = "emerg-ON"

            # Case 5-a - Parking
            elif (
                self.kbase.park_ack > 300
                and not self.kbase.stopping
                and self.kbase.distance > 245
            ):
                if (self.detectable_colors(rgb)) == self.kbase.PARKING_AV:
                    print(
                        "+++++++++++++++++++++++Parking spot detected++++++++++++++++++++++++"
                    )
                    analysis = "park-ON"
                elif (
                    self.detectable_colors(rgb) == self.kbase.INTERSECTION
                    or self.detectable_colors(rgb) == self.kbase.PARKING_SPCL
                ):
                    analysis = "ignore"

            # Case 5-b - Return from parking
            elif self.kbase.park_ack == 222:
                print(
                    "+++++++++++++++++++++++Exit from Parking++++++++++++++++++++++++"
                )
                analysis = "park-OFF"

            elif not self.kbase.stopping and (
                self.detectable_colors(rgb) == self.kbase.PARKING_AV
                or self.detectable_colors(rgb) == self.kbase.PARKING_SPCL
                or self.detectable_colors(rgb) == self.kbase.INTERSECTION
            ):
                print("+++++++++++++++++++Hello?++++++++++++++++")
                analysis = "ignore"

            # Case 6 - Obstacle detected
            elif (
                distance <= 300
                and self.kbase.step < 4
                and analysis not in ["lane2", "lane1"]
            ):
                analysis = "switch-lane"

            # Case 7 - Follow the lane
            elif not self.kbase.park_ack and analysis not in ["lane2", "lane1"]:
                analysis = "lane-follow"

            if (
                not self.kbase.stopping
                and color != self.kbase.STOP_COLOR
                and analysis not in deviate_cases
            ):
                analysis = "deviate"

            elif analysis not in stop_cases:
                print("==== stop the vehicle ====")
                analysis = "stop"

        if self.detectable_colors(rgb) == self.kbase.PARKING_SPCL:
            self.kbase.reset_distance = True
            print("Reset variable set!")
        else:
            self.kbase.reset_distance = False

        self.kbase.analysis = analysis
        print("############### The analysis is ==> ", analysis, " ###############")
        return analysis
