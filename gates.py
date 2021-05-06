import nidaqmx
import time
from nidaqmx.constants import (
    LineGrouping)

with nidaqmx.Task() as task:
	task.do_channels.add_do_chan('Dev2/port0/line0:7')
	task.start()

	task.write([0,1,0,0,0,0,0,0])
	time.sleep(1)
	# task.write([0,8,0,0])
	# time.sleep(.002)
	# task.write([0,0,8,0])
	# time.sleep(.002)
	# task.write([0,0,0,8])
	# time.sleep(.002)