#!/usr/bin/python3

from Recursos.DeviceManagerAPI import DeviceManager
import time

dm = DeviceManager("t", "192.168.2.111")

devices = dm.get_devices()

for android in devices:
	dm.start_app(android, "br.ufc.mdcc.benchimage2/.MainActivity")

print("Connecting....")
time.sleep(5)

for android in devices:
	dm.exec_activity(android, "benchimage2.EXTRAS", "--ei size 4 --ei filter 2 --ei local 1", 20)
