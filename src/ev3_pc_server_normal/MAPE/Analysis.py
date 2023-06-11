class Analysis:
    def __init__(self,obj_comm,obj_know):
        self.obj_comm=obj_comm
        self.obj_know=obj_know
    
    def admin_cmd_analyser(self):
        x=self.obj_comm.front_crash
        y=self.obj_comm.second_crash
        if (self.obj_comm.admin_cmd and self.obj_comm.admin_cmd>0 and self.obj_comm.admin_cmd != self.obj_know.perv_cmd) or x in [10,12] or y in [10,12]:
            if self.obj_comm.admin_cmd in [10,11,20,21] and self.obj_comm.admin_cmd != self.obj_know.perv_cmd:
                print(self.obj_comm.admin_cmd)
                self.obj_know.perv_cmd=self.obj_comm.admin_cmd
                return "parking"
            elif self.obj_comm.admin_cmd in [41,42,51] and self.obj_comm.admin_cmd != self.obj_know.perv_cmd:
                self.obj_know.perv_cmd=self.obj_comm.admin_cmd
                return 1
            elif x in [10,12]:
                return 2
            elif y in [10,12]:
                return 3
            else:
                print("No Value")
                return 0
