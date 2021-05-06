import nidaqmx
import time
from nidaqmx.constants import (
    LineGrouping)

with nidaqmx.Task() as task:
	task.do_channels.add_do_chan('Dev2/port0/line0:5')
	# task.timing.cfg_samp_clk_timing(0.1)
	task.start()


	task.write([True,False,False,False,False,False])
	time.sleep(.5)
	task.write([False,False,False,False,False,False])
	time.sleep(5)
	task.write([False, True, False, False, False, False])
	time.sleep(.5)
	task.write([False, False, False, False, False, False])
	# task.write(True)
	# time.sleep(1)
	# task.write(False)
	# time.sleep(1)
	# task.write([0,0,8,0])
	# time.sleep(.002)
	# task.write([0,0,0,8])
	# time.sleep(.002)