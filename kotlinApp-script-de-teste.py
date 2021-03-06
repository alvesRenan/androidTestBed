#!/usr/bin/python3

from time import sleep
from Recursos.DeviceManagerAPI import DeviceManager


DM = DeviceManager("r", "192.168.100.15")

devices = DM.get_devices()

for android in devices:
	DM.start_app(android, "com.example.renan.kotlinmpos/.MainActivity")

print("Connecting to cloudlet...")
sleep(5)

for android in devices:
	DM.exec_activity( android, 
    "com.example.renan.kotlinmpos.EXTRAS", 
    "--es 'operation' 'mul' --ei 'size' 500", 3 )
