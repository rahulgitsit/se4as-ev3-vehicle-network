class Analysis:
    def __init__(self,obj_comm,obj_know):
        self.obj_comm=obj_comm
        self.obj_know=obj_know
    
    def admin_cmd_analyser(self): # analysis commands from pc_client and normal vehicle
        x=self.obj_comm.front_crash
        if (self.obj_comm.admin_cmd and self.obj_comm.admin_cmd>0 and self.obj_comm.admin_cmd != self.obj_know.perv_cmd) or x in [10,12]:
            self.obj_know.perv_cmd=self.obj_comm.admin_cmd
            if self.obj_comm.admin_cmd in [10,11,20,21]:
                return "parking"
            if self.obj_comm.admin_cmd in [41,42,51] or x in [10,12]:
                return "emergency"
            else:
                print("No Value")
                return 0
            


    def emerg_over_analyser(self):# analysis commands from emergency vehicle 
        self.obj_comm.second_emerover=self.obj_comm.embox_emergencyover.read()
        if self.obj_comm.second_emerover==0 and self.obj_know.emerg==1:
            return True     
