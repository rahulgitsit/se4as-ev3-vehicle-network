class Planner:
    def __init__(self,obj_comm,obj_know) -> None:
        self.obj_comm=obj_comm
        self.obj_know=obj_know
        
    def park_planner(self): #
        if self.obj_know.park_flag==0 and self.obj_comm.admin_cmd%10 ==1 :
            self.obj_know.park_flag=1
            self.obj_know.parkcount=+1
            vehicle=int(str(self.obj_comm.admin_cmd)[0])
            msg=self.obj_know.parkcmd+self.obj_know.parkcount
            list1=[vehicle,msg]
            return list1
        elif self.obj_know.park_flag==1 and self.obj_comm.admin_cmd%10 ==0:
            self.obj_know.parkcount=self.obj_know.parkcount-1
            self.obj_know.park_flag=0
            vehicle=int(str(self.obj_comm.admin_cmd)[0])
            msg=666
            list2=[vehicle,msg]
            return list2
    
    def emergency_planner(self): 
        if self.obj_comm.admin_cmd in [41,42] or self.obj_comm.front_crash in [10,12]:
            if self.obj_comm.admin_cmd==41 or self.obj_comm.front_crash ==10:
                lane=10
            elif self.obj_comm.admin_cmd==42 or self.obj_comm.front_crash ==12:
                lane=12
            return lane
        elif self.obj_comm.admin_cmd==51:
            return 0
        

    def emerg_over_planner(self): 
        return 0
