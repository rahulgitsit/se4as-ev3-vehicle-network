class Planner:
    def __init__(self,obj_comm,obj_know) -> None:
        self.obj_comm=obj_comm
        self.obj_know=obj_know
    def park_planner(self):
        if self.obj_know.park_flag==0 and self.obj_comm.admin_cmd%10 ==1 :
            self.obj_know.parkcount=self.obj_know.parkcount+1
            if self.obj_know.parkcount==2:
                self.obj_know.park_flag=1
            vehicle=int(str(self.obj_comm.admin_cmd)[0])
            msg=self.obj_know.parkcmd+self.obj_know.parkcount
            return vehicle,msg
        if self.obj_know.parkcount>0 and self.obj_comm.admin_cmd%10 ==0:
            self.obj_know.parkcount=self.obj_know.parkcount-1
            if self.obj_know.parkcount==0:
                self.obj_know.park_flag=0
            vehicle=int(str(self.obj_comm.admin_cmd)[0])
            msg=666
            return vehicle,msg

    
    def emergency_planner(self):
        x=self.obj_comm.front_crash
        y=self.obj_comm.second_crash
        z=self.obj_comm.admin_cmd
        if z==41 or x ==10 or y == 10:
            return 10
        if z ==42 or x==12 or y ==12:
            return 12
        if z==51:
            return 0