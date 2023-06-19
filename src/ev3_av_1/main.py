#!/usr/bin/env pybricks-micropython
from mape.knowledge import KnowledgeBase
from mape.comms import Comms
from mape.monitor import Monitor
from mape.analyser import Analyser
from mape.planner import Planner
from mape.executor import Executer

from pybricks.parameters import Port

# import random

if __name__ == "__main__":
    kbase = KnowledgeBase()
    comms = Comms(kbase, id_=1)
    monitor = Monitor(kbase, Port.S3, Port.S4, Port.S1)
    analyser = Analyser(kbase)
    planner = Planner(kbase)
    executer = Executer(kbase, comms)
    # emergency = False

    comms.connect("C8:E2:65:CD:69:86")
    while True:
        # parking = False
        # emergency_flag = random.randint(1, 170)

        # if emergency_flag == 73 and not emergency:
        #     print("Emergency activated! - Rand Gen")
        #     emergency = 10

        kbase.start_time()
        reflection, color, rgb, distance, crash = monitor.read_sensor_values()
        parking, emergency = comms.monitor_messages()
        comms.send_messages(parking, emergency)
        analysis = analyser.analyse(
            reflection,
            color,
            rgb,
            distance,
            crash,
        )
        plan = planner.derive_plan(analysis)
        executer.execute(plan)
