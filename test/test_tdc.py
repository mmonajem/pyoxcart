#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2019 Surface Concept GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

-------------------------------------------------------------------------------

Created on Thu Sep 19 16:07:32 2019


Test of the user callbacks interface.
"""

import scTDC
# import sys
import timeit


# -----------------------------------------------------------------------------
# example 1 of deriving from sctdc_usercallbacks_pipe
# count TDC and DLD events and the number of callbacks for TDC events

class UCB1(scTDC.usercallbacks_pipe):
    def __init__(self, lib, dev_desc):
        super().__init__(lib, dev_desc)  # <-- mandatory
        self.reset_counters()

    def on_millisecond(self):
        # sys.stdout.write("MS ")
        pass

    def on_start_of_meas(self):
        # self.reset_counters()
        pass

    def on_end_of_meas(self):
        print("\nend of measurement")
        print("tdc events : ", self.tdc_event_count)
        print("tdc callbacks : ", self.tdc_cb_count)
        print("dld events : ", self.dld_event_count)

    def on_tdc_event(self, tdc_events, nr_tdc_events):
        self.tdc_event_count += nr_tdc_events
        self.tdc_cb_count += 1
        # sys.stdout.write("T ")

    def on_dld_event(self, dld_events, nr_dld_events):
        self.dld_event_count += nr_dld_events
        # sys.stdout.write("D ")

    def reset_counters(self):
        self.tdc_event_count = 0
        self.tdc_cb_count = 0
        self.dld_event_count = 0


# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# example 2 of deriving from sctdc_usercallbacks_pipe
# evaluate minimum and maximum values for times, x and y coordinates

class UCB2(scTDC.usercallbacks_pipe):
    def __init__(self, lib, dev_desc):
        super().__init__(lib, dev_desc)  # <-- mandatory
        self.reset_min_max()
        self.counter_tdc = 0
        self.counter_dld = 0

    def on_millisecond(self):
        pass  # do nothing (one could also skip this function definition altogether)

    def on_start_of_meas(self):
        # self.reset_min_max() # reset at every start of a measurement
        pass  # do nothing

    def on_end_of_meas(self):
        # pass
        print("end of measurement")
        print("minimum time TDC : ", self.min_time_tdc)
        print("maximum time TDC : ", self.max_time_tdc)
        print("minimum time DLD : ", self.min_time_dld)
        print("maximum time DLD : ", self.max_time_dld)
        print("minimum x : ", self.min_x)
        print("maximum x : ", self.max_x)
        print("minimum y : ", self.min_y)
        print("maximum y : ", self.max_y)

        print('dld counter', self.counter_dld)
        print('tdc counter', self.counter_tdc)

    def on_tdc_event(self, tdc_events, nr_tdc_events):
        print('event tdc')
        for i in range(nr_tdc_events):  # iterate through tdc_events
            # see class tdc_event_t in scTDC.py for all accessible fields
            t = tdc_events[i].time_data
            ch = tdc_events[i].channel
            sign_counter = tdc_events[i].sign_counter
            subdevice = tdc_events[i].subdevice
            time_tag = tdc_events[i].time_tag

            print('event tdc:', subdevice, ch, t, sign_counter, time_tag)
            self.min_time_tdc = min(self.min_time_tdc, t)
            self.max_time_tdc = max(self.max_time_tdc, t)
            self.counter_tdc += 1

    def on_dld_event(self, dld_events, nr_dld_events):
        print('event dld')
        for i in range(nr_dld_events):  # iterate through dld_events
            # see class dld_event_t in scTDC.py for all accessible fields
            t = dld_events[i].sum
            x = dld_events[i].dif1
            y = dld_events[i].dif2
            master_counter = dld_events[i].master_rst_counter
            start_counter = dld_events[i].start_counter
            print('event dld:', x, y, t, start_counter, master_counter)
            self.min_time_dld = min(self.min_time_dld, t)
            self.max_time_dld = max(self.max_time_dld, t)
            self.min_x = min(self.min_x, dld_events[i].dif1)
            self.max_x = max(self.max_x, dld_events[i].dif1)
            self.min_y = min(self.min_y, dld_events[i].dif2)
            self.max_y = max(self.max_y, dld_events[i].dif2)

            self.counter_dld += 1

    def reset_min_max(self):
        self.min_x = 1 << 40
        self.max_x = -1
        self.min_y = 1 << 40
        self.max_y = -1
        self.min_time_tdc = 1 << 40
        self.max_time_tdc = -1
        self.min_time_dld = 1 << 40
        self.max_time_dld = -1


# -----------------------------------------------------------------------------


def test1():
    device = scTDC.Device(autoinit=False)

    # initialize TDC --- and check for error!
    retcode, errmsg = device.initialize()
    if retcode < 0:
        print("error during init:", retcode, errmsg)
        return 0
    else:
        print("succesfully initialized")

    # use example 1 :
    # ucb = UCB1(lib, dev_desc) # opens a user callbacks pipe
    # or use example 2:
    ucb = UCB2(device.lib, device.dev_desc)  # opens a user callbacks pipe
    start = timeit.default_timer()
    for i in range(20):  # number of measurements
        ucb.do_measurement(100)
    end = timeit.default_timer()
    print("\ntime elapsed : ", end - start, "s")
    ucb.close()  # closes the user callbacks pipe, method inherited from base class
    device.deinitialize()


if __name__ == "__main__":
    test1()
