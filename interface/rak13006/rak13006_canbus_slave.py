#!/usr/bin/env python3

# import the library
import can
import sys

# create a bus instance
# many other interfaces are supported as well (see documentation)
# The CAN bus bit rate for RAK13006 is 125 kb/s
try:
    bus = can.Bus(interface='socketcan',
                  channel='can0',
                  bitrate=125000,
                  receive_own_messages=True)

except Exception as e:
    print("ERROR: could not find the module. \n"
          "Make sure the CAN bus is UP by running \"ip addr | grep can\" \n" 
          "If not, please run the following command to bring it up:\n"
          "sudo modprobe can;sudo modprobe can_raw\n"
          "sudo ip link set can0 type can bitrate 125000 restart-ms 100\n"
          "sudo ip link set up can0\n")
    sys.exit()

# send a message
# message = can.Message(arbitration_id=123, is_extended_id=True, data=[0x11, 0x22, 0x33])
# bus.send(message, timeout=0.2)

# iterate over received messages
for msg in bus:
    print(f"{msg.arbitration_id:X}: {msg.data}")

# or use an asynchronous notifier
notifier = can.Notifier(bus, [can.Logger("recorded.log"), can.Printer()])
