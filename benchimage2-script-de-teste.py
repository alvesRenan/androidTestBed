#!/usr/bin/python3

import time

from Recursos.DeviceManagerAPI import DeviceManager

dm = DeviceManager( "Test", "172.17.0.4" )

devices = dm.get_devices()

for android in devices:
	dm.start_app( android, "br.ufc.mdcc.benchimage2/.MainActivity" )

print("Connecting....")
time.sleep(5)

for android in devices:
	dm.exec_activity( android, "benchimage2.EXTRAS", "--ei size 4 --ei filter 2 --ei local 1", 3 )
