"""
This is the script for testing National Instrument edge counter.
"""

try:
    import nidaqmx
except:
    print('Please install nidaqmx')

import time

if __name__ == '__main__':
    task_counter = nidaqmx.Task()
    task_counter.ci_channels.add_ci_count_edges_chan("Dev1/ctr0")

    # if you need to prescale
    # task.ci_channels[0].ci_prescaler = 8

    # reference the terminal you want to use for the counter here
    task_counter.ci_channels[0].ci_count_edges_term = "PFI0"
    task_counter.start()
    # task.read()
    i = 0
    for i in range(10):
        time.sleep(1)
        data = task_counter.read(number_of_samples_per_channel=1)
        print(data)
    task_counter.stop()
    task_counter.close()
