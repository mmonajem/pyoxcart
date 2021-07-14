"""
This is the main script for reading TDC.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""
import scTDC


class UCB2(scTDC.usercallbacks_pipe):
    """
    TDC class for DLD and TDC events
    """
    def __init__(self, lib, dev_desc, queue_x, queue_y, queue_t,
                 queue_dld_start_counter, queue_channel, queue_time_data,
                 queue_tdc_start_counter):
        super().__init__(lib, dev_desc)  # <-- mandatory
        # The queues that share the data between this and main process
        self.queue_x = queue_x
        self.queue_y = queue_y
        self.queue_t = queue_t
        self.queue_dld_start_counter = queue_dld_start_counter
        self.queue_channel = queue_channel
        self.queue_time_data = queue_time_data
        self.queue_tdc_start_counter = queue_tdc_start_counter

    def on_millisecond(self):
        pass  # do nothing (one could also skip this function definition altogether)

    def on_start_of_meas(self):
        pass  # do nothing

    def on_end_of_meas(self):
        pass

    def on_tdc_event(self, tdc_events, nr_tdc_events):
        for i in range(nr_tdc_events):  # iterate through tdc_events
            # see class tdc_event_t in scTDC.py for all accessible fields
            # save TDC events in queues
            self.queue_time_data.put(tdc_events[i].time_data)
            self.queue_channel.put(tdc_events[i].channel)
            self.queue_tdc_start_counter.put(tdc_events[i].start_counter)

    def on_dld_event(self, dld_events, nr_dld_events):
        for i in range(nr_dld_events):  # iterate through dld_events
            # see class dld_event_t in scTDC.py for all accessible fields
            # save DLD events in queues
            self.queue_x.put(dld_events[i].dif1)
            self.queue_y.put(dld_events[i].dif2)
            self.queue_t.put(dld_events[i].sum)
            self.queue_dld_start_counter.put(dld_events[i].start_counter)


# Initializing the TDC
def initialize_tdc():
    """
    Initialize the TDC
    """
    device = scTDC.Device(autoinit=False)
    retcode, errmsg = device.initialize()
    if retcode < 0:
        print("Error during initialization : ({}) {}".format(errmsg, retcode))
        return 0

    return device


# This function is called from main control loop in a separate process
def experiment_measure(queue_x, queue_y, queue_t, queue_dld_start_counter, queue_channel,
                       queue_time_data, queue_tdc_start_counter,
                       queue_start_measurement, queue_stop_mesurment):
    """
    measurement function
    """
    device_tdc = initialize_tdc()
    ucb = UCB2(device_tdc.lib, device_tdc.dev_desc,
               queue_x, queue_y, queue_t, queue_dld_start_counter, queue_channel,
               queue_time_data, queue_tdc_start_counter)  # opens a user callbacks pipe

    ucb.close()  # closes the user callbacks pipe, method inherited from base class

    device_tdc.deinitialize()

    device_tdc = initialize_tdc()
    ucb = UCB2(device_tdc.lib, device_tdc.dev_desc,
               queue_x, queue_y, queue_t, queue_dld_start_counter, queue_channel,
               queue_time_data, queue_tdc_start_counter)  # opens a user callbacks pipe

    # print('The TDC process is ready for measurement')
    while True:
        # Do the measurment for a long time
        # The measurement is terminate if the main process terminate this process
        # ucb.do_measurement(86400000)
        # Do the measurement for 5 second
        ucb.do_measurement(5000)
        # The while loop breaks if the main process send stop flag
        if not queue_stop_mesurment.empty():
            print('TDC loop is break in child process')
            break

    # The code not comes to the below lines.
    ucb.close()  # closes the user callbacks pipe, method inherited from base class

    device_tdc.deinitialize()
