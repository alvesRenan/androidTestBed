#!/usr/bin/python3
import sys
from time import sleep

from Recursos.DeviceManagerAPI import DeviceManager

dm = DeviceManager( "r", "", "on-device/json/%s" % sys.argv[1] )

devices = dm.get_devices()

# for android in devices:
#   dm.start_app( android, "com.example.italo.sourceafistest/.MainActivity" )

# sleep( 10 )

for android in devices:
  # sending a image
  # dm.exec_activity( android, "sourceAfis.EXTRAS", "--es useImage yes --es numCandidates %s" % sys.argv[1], 40 )
  # dm.exec_activity( android, "sourceAfis.EXTRAS", "--es useImage yes" % sys.argv[1], 40 )

  # sending json
  # dm.exec_activity( android, "sourceAfis.EXTRAS", "--es numCandidates %s" % sys.argv[1], 30 )
  dm.exec_activity( android, "sourceAfis.EXTRAS", "", 30 )