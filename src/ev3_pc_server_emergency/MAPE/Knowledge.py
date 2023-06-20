import openpyxl
from openpyxl import Workbook
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
        self.columnname2=["Time","Emergency vehicle speed","Emergency vehicle lane","Color from emerg vehicle","Reflection from emerg vehicle","RGB from emerg vehicle"]
        with open('normalav.csv', 'w', encoding='UTF8',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.columnname1)
        with open('emergav.csv', 'w', encoding='UTF8',newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.columnname2)

    def write_normalav_log(self,var_list:list):
        with open('normalav.csv', 'a', newline='') as p:
                writer = csv.writer(p)
                writer.writerow(var_list)
    
    def write_emergav_log(self,var_list:list):
        with open('emergav.csv', 'a', newline='') as p:
                writer = csv.writer(p)
                writer.writerow(var_list)



        
    
