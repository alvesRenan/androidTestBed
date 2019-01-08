#!/usr/bin/python3

from Recursos.DeviceManagerAPI import DeviceManager
import time

dm = DeviceManager("w", "172.17.0.5")

# creates clodulet if the servers of the scenraio 
# are over the threashold
dm.use_dynamic_cloudlet("nifty_booth", 200)

devices = dm.get_devices()

for android in devices:
	dm.start_app(android, "br.ufc.mdcc.benchimage2/.MainActivity")

print("Connecting....")
time.sleep(5)

for android in devices:
	dm.exec_activity(android, "benchimage2.EXTRAS", "--ei size 4 --ei filter 2 --ei local 1", 4)
