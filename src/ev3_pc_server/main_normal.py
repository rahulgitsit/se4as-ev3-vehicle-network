#!/usr/bin/env pybricks-micropython

from pybricks.messaging import BluetoothMailboxServer, NumericMailbox
import random
import time

# Initialize Bluetooth server.
server = BluetoothMailboxServer()
admin_id=NumericMailbox('admin',server)
admin_command=NumericMailbox('cmd',server)
# Initialize mailboxes 
mbox1_id = NumericMailbox('id1', server)
mbox1_time = NumericMailbox('time1', server)
mbox1_lane = NumericMailbox('lane1', server)
mbox1_speed = NumericMailbox('speed1', server)
mbox1_distance = NumericMailbox('distance1', server)
mbox1_parking= NumericMailbox('parking1',server)
mbox1_emergency=NumericMailbox('emergency1',server)
mbox1_crash=NumericMailbox("crash1",server)
mbox1_server_ack=NumericMailbox('ack1',server)


mbox2_id = NumericMailbox('id2', server)
mbox2_time = NumericMailbox('time2', server)
mbox2_lane = NumericMailbox('lane2', server)
mbox2_speed = NumericMailbox('speed2', server)
mbox2_distance = NumericMailbox('distance2', server)
mbox2_parking= NumericMailbox('parking2',server)
mbox2_emergency=NumericMailbox('emergency2',server)
mbox2_crash=NumericMailbox("crash2",server)
mbox2_server_ack=NumericMailbox('ack2',server)


print("Waiting for clients.........")
server.wait_for_connection(3)
print("connected!")

# Send robot id to leader and follower.
admin_id.send(0)
mbox1_id.send(1)
mbox2_id.send(2)
# embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)
mbox2_id.send(2)
# embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)
mbox2_id.send(2)
# embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)
mbox2_id.send(2)
# embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)
mbox2_id.send(2)
# embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)
mbox2_id.send(2)
# embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)
mbox2_id.send(2)
# embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)
mbox2_id.send(2)
# embox_id.send(3)
ii=0

starttime=time.time()
q=0
p=0
rr=[259,366,478,555,919,171,629,779,815,70]
lanelist=[10,12]
star=0
lane=0
front_emer=300
h=True
random_=0
aq=0
bq=0
cq=0
emerg=0
front_crash_flag=False
second_crash_flag=False #to avoid multple ack sending
while True:


    # Read messages received from the front robot
    admin_cmd=admin_command.read()

    front_id = mbox1_id.read()
    front_time = mbox1_time.read()
    front_lane = mbox1_lane.read()
    front_speed = mbox1_speed.read()
    front_distance = mbox1_distance.read()
    front_parking=mbox1_parking.read()
    front_emer=mbox1_emergency.read()
    front_crash=mbox1_crash.read()
    front_ack=mbox1_server_ack.read()

    second_id = mbox2_id.read()
    second_time = mbox2_time.read()
    second_lane = mbox2_lane.read()
    second_speed = mbox2_speed.read()
    second_distance = mbox2_distance.read()
    second_parking=mbox2_parking.read()
    second_emer=mbox2_emergency.read()
    second_crash=mbox2_crash.read()
    second_ack=mbox2_server_ack.read()

    

    if admin_cmd and admin_cmd>0:
          if(admin_cmd==11) and aq==0:
                print("***********************************")
                print("Parking request to vehicle 1")
                print("***********************************")
                mbox1_parking.send(999)
                front_parking=mbox1_parking.read()
                while front_parking!=200:
                      mbox1_parking.send(999)
                      front_parking=mbox1_parking.read()
                aq=1
          if(admin_cmd==10) and aq==1:
                print("back to track request to vehicle 1")
                mbox1_parking.send(666)
                front_parking=mbox1_parking.read()
                while front_parking!=222:
                      mbox1_parking.send(666)
                      front_parking=mbox1_parking.read()
                aq=0
          if(admin_cmd==21) and bq==0:
                print("***********************************")
                print("Parking request to vehicle 2")
                print("***********************************")
                mbox2_parking.send(999)
                second_parking=mbox2_parking.read()
                while second_parking!=200:
                      mbox2_parking.send(999)
                      second_parking=mbox2_parking.read()
                bq=1
          if(admin_cmd==20) and bq==1:
                print("back to track request to vehicle 1")
                mbox2_parking.send(666)
                second_parking=mbox2_parking.read()
                while second_parking!=222:
                      mbox2_parking.send(666)
                      second_parking=mbox2_parking.read()
                bq=0
          if(admin_cmd==31) and cq==0:
                print("***********************************")
                print("Parking request to vehicle both")
                print("***********************************")
                mbox2_parking.send(999)
                mbox1_parking.send(999)
                second_parking=mbox2_parking.read()
                front_parking=mbox1_parking.read()
                while second_parking!=200 and front_parking!=200:
                      mbox2_parking.send(999)
                      second_parking=mbox2_parking.read()
                      mbox1_parking.send(999)
                      front_parking=mbox1_parking.read()
                cq=1
                aq=1
                bq=1
          if(admin_cmd==30) and cq==1:
                print("Back to track request to vehicle both")
                mbox2_parking.send(666)
                mbox1_parking.send(666)
                second_parking=mbox2_parking.read()
                front_parking=mbox1_parking.read()
                while second_parking!=222 and front_parking!=222:
                      mbox2_parking.send(666)
                      second_parking=mbox2_parking.read()
                      mbox1_parking.send(666)
                      front_parking=mbox1_parking.read()
                cq=0
                aq=0
                bq=0
          if (admin_cmd==41):
                print("***********************************")
                print("Emergency in lane 1")
                print("***********************************")
                emerg=1
                mbox1_emergency.send(10)
                mbox2_emergency.send(10)
                second_emer=mbox2_emergency.read()
                front_emer=mbox1_emergency.read()
                while second_emer!=100 and front_emer!=100:
                      mbox1_emergency.send(10)
                      mbox2_emergency.send(10)
                      second_emer=mbox2_emergency.read()
                      front_emer=mbox1_emergency.read()
          if (admin_cmd==42):
                print("***********************************")
                print("Emergency in lane 2")
                print("***********************************")
                emerg=1
                mbox1_emergency.send(12)
                mbox2_emergency.send(12)
                second_emer=mbox2_emergency.read()
                front_emer=mbox1_emergency.read()
                while second_emer!=100 and front_emer!=100:
                      mbox1_emergency.send(12)
                      mbox2_emergency.send(12)
                      second_emer=mbox2_emergency.read()
                      front_emer=mbox1_emergency.read()
          if (admin_cmd==51):
                print("***********************************")
                print("Emergency Over")
                print("***********************************")
                emerg=0
                mbox1_emergency.send(0)
                mbox2_emergency.send(0)
                second_emer=mbox2_emergency.read()
                front_emer=mbox1_emergency.read()
                second_crash=0
                front_crash=0
                while second_emer!=300 or front_emer!=300:
                      mbox1_emergency.send(0)
                      mbox2_emergency.send(0)
                      second_emer=mbox2_emergency.read()
                      front_emer=mbox1_emergency.read()
    second_crash=mbox2_crash.read()
    front_crash=mbox1_crash.read()
    if  second_crash in [10,12] and emerg==0:
          print("Emergency in AV2")
          emerg=1
          senderlist=[mbox2_server_ack,mbox2_lane,mbox1_emergency]
          if second_crash_flag==False:
            senderlist[0].send(200)
            senderlist[0].send(200)
            senderlist[0].send(200)
            senderlist[0].send(200)
            senderlist[2].send(senderlist[1].read()+10)
            x=senderlist[2].read()
            while x!=100:
                  senderlist[2].send(senderlist[1].read()+10)
                  x=senderlist[2].read()
            second_crash_flag=True
    if front_crash in [10,12] and emerg==0:
          print("Emergency in AV1")
          emerg=1
          senderlist=[mbox1_server_ack,mbox1_lane,mbox2_emergency]
          if front_crash_flag==False:
            senderlist[0].send(200)
            senderlist[0].send(200)
            senderlist[0].send(200)
            senderlist[0].send(200)
            senderlist[2].send(senderlist[1].read()+10)
            x=senderlist[2].read()
            while x!=100:
                  senderlist[2].send(senderlist[1].read()+10)
                  x=senderlist[2].read()
            front_crash_flag=True

      
        
            
                      
    