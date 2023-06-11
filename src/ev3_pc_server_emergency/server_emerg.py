
from MAPE import  Communication, Moniter, Analysis,Planner,Executer,Knowledge



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
        m=analyser.emerg_over_analyser()
        if t=="emergency":
            l=planner.emergency_planner()
            executer.send_emergency(l)
        elif t=="parking":
            list1=planner.park_planner()
            executer.send_park(list1)
        if m:
            xx=planner.emerg_over_planner()
            executer.send_emergency(xx)
