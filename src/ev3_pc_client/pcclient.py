#!/usr/bin/env python3
from pybricks.messaging import BluetoothMailboxClient, NumericMailbox


# This demo makes your PC talk to an EV3 over Bluetooth.
#
# This is identical to the EV3 client example in ../bluetooth_client
#
# The only difference is that it runs in Python3 on your computer, thanks to
# the Python3 implementation of the messaging module that is included here.
# As far as the EV3 is concerned, it thinks it just talks to an EV3 client.
#
# So, the EV3 server example needs no further modifications. The connection
# procedure is also the same as documented in the messaging module docs:
# https://docs.pybricks.com/en/latest/messaging.html
#
# So, turn Bluetooth on on your PC and the EV3. You may need to make Bluetooth
# visible on the EV3. You can skip pairing if you already know the EV3 address.

# This is the address of the server EV3 we are connecting to.


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
client = BluetoothMailboxClient()
mbox_id = NumericMailbox("admin", client)
mbox_command = NumericMailbox("cmd", client)


SERVER = "C8:E2:65:CD:69:86"
print("establishing connection...")
client.connect(SERVER)
print("server connected!")

cmd = 0
mbox_command.send(cmd)
while True:
    command = int(
        input(
            "Enter your command:: \n 1. Park AV1  \n 2. Park AV2 \n 3. Park Both  \n 4. Emergency in Lane 1  \n 5. Emergency in Lane 2 \n 6. Emergency Over\n 7. Return to track - AV1 \n 8. Return to track - AV2 \n 9. Return to track - Both AVs \n"
        )
    )
    print("NOTE: Please reset command by sending '0' to resend the previous command.")
    print("=======================================")

    if command == 1:
        cmd = 11
        print("Parking command send to vehicle 1.")

    elif command == 2:
        cmd = 21
        print("Parking command send to vehicle 2.")

    elif command == 3:
        cmd = 31
        print("Parking command send to both vehicle.")

    elif command == 4:
        cmd = 41
        print("Emergency in Lane 1. Swtich to Lane 2.")

    elif command == 5:
        cmd = 42
        print("Emergency in Lane 2. Swtich to Lane 1.")

    elif command == 6:
        cmd = 51
        print("Emergency Over. Swtich to Normal Mode.")

    elif command == 7:
        cmd = 10
        print("Requested AV1 to return to lane.")

    elif command == 8:
        cmd = 20
        print("Requested AV2 to return to lane.")

    elif command == 9:
        cmd = 30
        print("Requested both vehicle to return to lane.")

    elif command == 0:
        cmd = 0

    else:
        print("Please enter a valid commmand (1-9)")

    mbox_command.send(cmd)

    print("=======================================")
