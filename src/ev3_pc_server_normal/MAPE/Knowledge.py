import csv
class Knowledge:
    def __init__(self):
        self.perv_cmd=0
        self.park_flag=0
        self.parkcount=0
        self.parkcmd=900
        self.emerg=0
        self.ack=200
        self.emergover=5
        self.columnname1=["Time","First vehicle lane","First vehicle speed","First vehicle parking","First Vehicle Obstacle distance","Color from first vehicle","Reflection from first vehicle","RGB from first vehicle"]
        self.columnname2=["Time","second vehicle speed","second vehicle lane","second vehicle parking","second Vehicle Obstacle distance","Color from second vehicle","Reflection from second vehicle","RGB from second vehicle"]
        with open('normal1av.csv', 'w', encoding='UTF8',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.columnname1)
        with open('normalav2av.csv', 'w', encoding='UTF8',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.columnname2)
    def write_normalav1_log(self,var_list:list):
        with open('normal1av.csv', 'a', newline='') as p:
                writer = csv.writer(p)
                writer.writerow(var_list)
    def write_normalav2_log(self,var_list:list):
        with open('normalav2av.csv', 'a', newline='') as p:
                writer = csv.writer(p)
                writer.writerow(var_list)
