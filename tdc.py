import multiprocessing
import time

import variables
import scTDC


class UCB2(scTDC.usercallbacks_pipe):
    def __init__(self, lib, dev_desc, queue_x, queue_y, queue_t, queue_start_counter):
        super().__init__(lib, dev_desc)  # <-- mandatory
        # self.x = []
        # self.y = []
        # self.t = []
        # self.start_counter = []
        self.queue_x = queue_x
        self.queue_y = queue_y
        self.queue_t = queue_t
        self.queue_start_counter = queue_start_counter

    def on_millisecond(self):
        pass  # do nothing (one could also skip this function definition altogether)

    def on_start_of_meas(self):
        pass  # do nothing

    def on_end_of_meas(self):
        pass
        # variables.x = self.x
        # variables.y = self.y
        # variables.t = self.t
        # variables.start_counter = self.start_counter

    def on_tdc_event(self, tdc_events, nr_tdc_events):
        pass
        # for i in range(nr_tdc_events):  # iterate through tdc_events
        #     # see class tdc_event_t in scTDC.py for all accessible fields
        #     t = tdc_events[i].time_data

    def on_dld_event(self, dld_events, nr_dld_events):
        for i in range(nr_dld_events):  # iterate through dld_events
            # see class dld_event_t in scTDC.py for all accessible fields
            # self.t.append(dld_events[i].sum)
            # self.x.append(dld_events[i].dif1)
            # self.y.append(dld_events[i].dif2)
            # self.start_counter.append(dld_events[i].start_counter)
            self.queue_x.put(dld_events[i].dif1)
            self.queue_y.put(dld_events[i].dif2)
            self.queue_t.put(dld_events[i].sum)
            self.queue_start_counter.put(dld_events[i].start_counter)


def initialize_tdc():
    device = scTDC.Device(autoinit=False)
    retcode, errmsg = device.initialize()
    if retcode < 0:
        print("Error during initialization : ({}) {}".format(errmsg, retcode))
        return 0

    return device


def experiment_measure(queue_x, queue_y, queue_t, queue_start_counter):

    device_tdc = initialize_tdc()
    ucb = UCB2(device_tdc.lib, device_tdc.dev_desc,
               queue_x, queue_y, queue_t, queue_start_counter)  # opens a user callbacks pipe
    # total_steps = variables.ex_time * variables.ex_freq
    # steps = 0
    # while steps < total_steps:
    while True:
        ucb.do_measurement(86400000)
        # ucb.do_measurement(int(1000 / variables.ex_freq))  # Time of measurement in ms
        # if variables.stop_flag:
        #     # wait for 3 second
        #     time.sleep(3)
        #     break
        # steps += 1

    ucb.close()  # closes the user callbacks pipe, method inherited from base class

    device_tdc.deinitialize()
