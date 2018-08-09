#!/usr/bin/python3

from Recursos.DeviceManagerAPI import DeviceManager
import time

DM = DeviceManager("tes2", "192.168.2.110")

devices = DM.get_devices()

for android in devices:
	DM.start_app(android, "com.example.renan.kotlinmpos/.MainActivity")

print("Connecting to cloudlet...")
time.sleep(7)

for android in devices:
	DM.exec_activity(android, "com.example.renan.kotlinmpos/.MainActivity", "--es 'operation' 'mul' --ei 'size' 1000", 5)
