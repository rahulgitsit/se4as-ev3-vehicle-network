

from MAPE import Communication, Moniter,Analysis,Planner,Executer,Knowledge





if __name__=='__main__':
    comm=Communication.Communication()
    know=Knowledge.Knowledge()
    moniter=Moniter.Moniter(comm)
    analyser=Analysis.Analysis(comm,know)
    planner=Planner.Planner(comm,know)
    executer=Executer.Executer(comm,know)
    executer.send_id()
    while True:
        moniter.read_mailbox()
        t=analyser.admin_cmd_analyser()
        if t in [1,2,3]:
            l=planner.emergency_planner()
            executer.send_emergency(l,t)
        elif t=="parking":
            veh,msg=planner.park_planner()
            executer.send_park(veh,msg)
