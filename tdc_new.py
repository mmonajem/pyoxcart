"""
This is the main new script for reading TDC.
@author: Mehrpad Monajem <mehrpad.monajem@fau.de>
"""
import scTDC
import time
import numpy as np
from queue import Queue

# define some constants to distinguish the type of element placed in the queue
QUEUE_DATA = 0
QUEUE_ENDOFMEAS = 1


class BufDataCB4(scTDC.buffered_data_callbacks_pipe):
    def __init__(self, lib, dev_desc, raw_mode, dld_events,
                 max_buffered_data_len=500000):
        if not raw_mode:
            data_field_selection = \
                scTDC.SC_DATA_FIELD_DIF1 \
                | scTDC.SC_DATA_FIELD_DIF2 \
                | scTDC.SC_DATA_FIELD_TIME \
                | scTDC.SC_DATA_FIELD_START_COUNTER
        elif raw_mode:
            data_field_selection = \
                scTDC.SC_DATA_FIELD_TIME \
                | scTDC.SC_DATA_FIELD_CHANNEL \
                | scTDC.SC_DATA_FIELD_START_COUNTER

        super().__init__(lib, dev_desc, data_field_selection,  # <-- mandatory!
                         max_buffered_data_len, dld_events)    # <-- mandatory!

        self.queue = Queue()
        self.end_of_meas = False

    def on_data(self, d):
        # make a dict that contains copies of numpy arrays in d ("deep copy")
        # start with an empty dict, insert basic values by simple assignment,
        # insert numpy arrays using the copy method of the source array
        dcopy = {}
        for k in d.keys():
            if isinstance(d[k], np.ndarray):
                dcopy[k] = d[k].copy()
            else:
                dcopy[k] = d[k]
        self.queue.put((QUEUE_DATA, dcopy))
        if self.end_of_meas:
            self.end_of_meas = False
            self.queue.put((QUEUE_ENDOFMEAS, None))

    def on_end_of_meas(self):
        self.end_of_meas = True
        # setting end_of_meas, we remember that the next on_data delivers the
        # remaining data of this measurement
        return True

# -----------------------------------------------------------------------------


def experiment_measure(raw_mode, queue_x,
                       queue_y, queue_t,
                       queue_dld_start_counter,
                       queue_channel,
                       queue_time_data,
                       queue_tdc_start_counter,
                       queue_stop_measurement):
    """
    measurement function
    Parameters
    ----------
    DLD Queues: queue
        Queues that contains DLD data
    TDC Queues: queue
        Queues that contains TDC raw data
    Stop measurement flag: queue
        Queue for stop the measurement. This queue is set to True from oxcart.py

    Returns
    -------
    None
    """

    device = scTDC.Device(autoinit=False)

    # initialize TDC --- and check for error!
    retcode, errmsg = device.initialize()
    if retcode < 0:
        print("error during init:", retcode, errmsg)
        return -1
    else:
        print("successfully initialized")

    # open a BUFFERED_DATA_CALLBACKS pipe
    bufdatacb = BufDataCB4(device.lib, device.dev_desc, raw_mode, dld_events=not raw_mode)

    # define a closure that checks return codes for errors and does clean up
    def errorcheck(retcode):
        if retcode < 0:
            print(device.lib.sc_get_err_msg(retcode))
            bufdatacb.close()
            device.deinitialize()
            return -1
        else:
            return 0


    # start a first measurement
    retcode = bufdatacb.start_measurement(300)
    if errorcheck(retcode) < 0:
        return -1

    while True:
        # start = time.time()
        eventtype, data = bufdatacb.queue.get()  # waits until element available
        if eventtype == QUEUE_DATA:
            if not raw_mode:
                queue_x.put(data["dif1"])
                queue_y.put(data["dif2"])
                queue_t.put(data["time"])
                queue_dld_start_counter.put(data["start_counter"])
            elif raw_mode:
                queue_channel.put(data["channel"])
                queue_time_data.put(data["time"])
                queue_tdc_start_counter.put(data["start_counter"])
        elif eventtype == QUEUE_ENDOFMEAS:
            if queue_stop_measurement.empty():
                retcode = bufdatacb.start_measurement(300)
                if errorcheck(retcode) < 0:
                    return -1
            else:
                print('TDC loop is break in child process')
                break
        else: # unknown event
            break # break out of the event loop
        # print('tdc process time:', time.time() - start)

    time.sleep(0.1)
    # clean up
    bufdatacb.close() # closes the user callbacks pipe, method inherited from base class
    device.deinitialize()

    return 0


