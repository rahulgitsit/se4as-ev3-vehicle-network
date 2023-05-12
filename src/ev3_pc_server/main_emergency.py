#!/usr/bin/env pybricks-micropython


from pybricks.messaging import BluetoothMailboxServer, NumericMailbox

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


embox_id = NumericMailbox("id2", server)
embox_time = NumericMailbox("time2", server)
embox_lane = NumericMailbox("lane2", server)
embox_speed = NumericMailbox("speed2", server)
embox_distance = NumericMailbox("distance2", server)
embox_emer=NumericMailbox("emer2",server)
# embox_id = NumericMailbox("id1", server)
embox_time = NumericMailbox("time1", server)
embox_lane = NumericMailbox("lane1", server)
embox_speed = NumericMailbox("speed1", server)
embox_distance = NumericMailbox("distance1", server)
embox_step=NumericMailbox("step1",server)
embox_parking = NumericMailbox("parking1", server)  
embox_emergencyover = NumericMailbox("emergency1", server)  
embox_crash = NumericMailbox("crash1", server)
embox_server_ack = NumericMailbox("ack1", server)  # TODO: 



print("Waiting for  clients")
server.wait_for_connection(3)
print("All device connected!")

# Send robot id to leader and follower.
admin_id.send(0)
mbox1_id.send(1)

embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)

embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)

embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)

embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)

embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)

embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)

embox_id.send(3)
admin_id.send(0)
mbox1_id.send(1)

embox_id.send(3)
q=0
p=0
front_emer=300
# h=True
aq=0
emerg=0
admin_cmd=0
front_crash_flag=False
while True:
    #reading values from PC-client
    previous_cmd=admin_cmd
    admin_cmd=admin_command.read()
    #reading values from Normal AV
    front_id = mbox1_id.read()
    front_time = mbox1_time.read()
    front_lane = mbox1_lane.read()
    front_speed = mbox1_speed.read()
    front_distance = mbox1_distance.read()
    front_parking=mbox1_parking.read()
    front_emer=mbox1_emergency.read()
    front_crash=mbox1_crash.read()
    front_ack=mbox1_server_ack.read()
    #read values from Emergency AV
    second_id = embox_id.read()
    second_time = embox_time.read()
    second_lane = embox_lane.read()
    second_speed = embox_speed.read()
    second_distance = embox_distance.read()
    second_parking=embox_parking.read()
    second_emer=embox_emer.read()
    second_emerover=embox_emergencyover.read()
    second_crash=embox_crash.read()
    second_ack=embox_server_ack.read()

    
    #action taking based on PC-client request
    if admin_cmd and admin_cmd>0 and admin_cmd!=previous_cmd:
          if(admin_cmd==11) and aq==0:
                print()
                print()
                print()
                print("***********************************")
                print("Parking request to vehicle 1")
                print("***********************************")
                print()
                print()
                print()
                mbox1_parking.send(999)
                front_parking=mbox1_parking.read()
                while front_parking!=200:
                      mbox1_parking.send(999)
                      front_parking=mbox1_parking.read()
                aq=1
          if(admin_cmd==10):
                print()
                print()
                print()
                print("****************************************")
                print("back to track request to vehicle 1")
                print("****************************************")
                print()
                print()
                print()
                mbox1_parking.send(666)
                front_parking=mbox1_parking.read()
                while front_parking!=222:
                      mbox1_parking.send(666)
                      front_parking=mbox1_parking.read()
                aq=0
          if (admin_cmd==41 and emerg==0):
                print()
                print()
                print()
                print("****************************************")
                print("Emergency in lane 1")
                print("Requesting AV to switch lane to 2")
                print("****************************************")
                print()
                print()
                print()
                emerg=1
                mbox1_emergency.send(10)
                front_emer=mbox1_emergency.read()
                while front_emer!=100:
                      mbox1_emergency.send(10)
                      front_emer=mbox1_emergency.read()
                embox_emer.send(10)
                second_emer=embox_emer.read()
                while second_emer!=100:
                      embox_emer.send(10)
                      second_emer=embox_emer.read()
                      
          if (admin_cmd==42 and emerg==0):
                print()
                print()
                print()
                print("****************************************")
                print("Emergency in lane 2")
                print("Requesting AV to switch lane to 1")
                print("****************************************")
                print()
                print()
                print()
                emerg=1
                mbox1_emergency.send(12)
                front_emer=mbox1_emergency.read()
                while second_emer!=100 and front_emer!=100:
                      mbox1_emergency.send(12)
                      front_emer=mbox1_emergency.read()
                embox_emer.send(12)
                second_emer=embox_emer.read()
                while second_emer!=100:
                      embox_emer.send(12)
                      second_emer=embox_emer.read()
          if (admin_cmd==51 and emerg==1):
                emerg=0
                print("Emergency over")
                mbox1_emergency.send(0)
                front_emer=mbox1_emergency.read()
                while second_emer!=300 and front_emer!=300:
                      mbox1_emergency.send(0)
                      front_emer=mbox1_emergency.read()
    #emergency alert from normal vehicle
    front_crash=mbox1_crash.read()
    if(front_crash in [10,12] and emerg==0 and front_crash_flag==False):
          front_crash_flag=True
          mbox1_server_ack.send(200)
          mbox1_server_ack.send(200)
          mbox1_server_ack.send(200)
          mbox1_server_ack.send(200)
          mbox1_server_ack.send(200)
          mbox1_server_ack.send(200)
          emerg=1
          if front_crash==12:
                     print()
                     print()
                     print()
                     print("****************************************")
                     print("Emergency in lane 2")
                     print("Requesting AV to switch lane to 1")
                     print("****************************************")
                     print()
                     print()
                     print() 
          if front_crash==10:
                     print()
                     print()
                     print()
                     print("****************************************")
                     print("Emergency in lane 1")
                     print("Requesting AV to switch lane to 2")
                     print("****************************************")
                     print()
                     print()
                     print() 
          embox_emer.send(front_crash)
          second_emer=embox_emer.read()
          while second_emer!=100:
                  embox_emer.send(front_crash)
                  second_emer=embox_emer.read()             
    #emergency overfrom emergency av
    second_emerover=embox_emergencyover.read()
    if(second_emerover==0 and emerg==1):
            emerg=0
            embox_emergencyover.send(200)
            embox_emergencyover.send(200)
            embox_emergencyover.send(200)
            embox_emergencyover.send(200)
            embox_emergencyover.send(200)
            embox_emergencyover.send(200)
            embox_emer.send(99)
            embox_emer.send(99)
            embox_emer.send(99)
            embox_emer.send(99)
            embox_emer.send(99)
            embox_emer.send(99)
            print("***********************************")
            print("Emergency over")
            print("***********************************")

            mbox1_emergency.send(0)
            front_emer=mbox1_emergency.read()
            while second_emer!=300 and front_emer!=300:
                  mbox1_emergency.send(0)
                  front_emer=mbox1_emergency.read()
            print("exit from emer over")
                
#   