#!/usr/bin/python3

from Recursos.DeviceManagerAPI import DeviceManager
import time

DM = DeviceManager("Test", "172.17.0.4")

devices = DM.get_devices()

for android in devices:
	DM.start_app(android, "com.example.renan.kotlinmpos/.MainActivity")

print("Connecting to cloudlet...")
time.sleep(3)

for android in devices:
	DM.exec_activity( android, 
    "com.example.renan.kotlinmpos.EXTRAS", 
    "--es 'operation' 'mul' --ei 'size' 500", 5 )
