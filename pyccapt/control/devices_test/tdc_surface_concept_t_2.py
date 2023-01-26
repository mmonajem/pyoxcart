"""
This is the main vew script for reading TDC Surface Concept .
"""

import time
import timeit
import numpy as np
from queue import Queue

# Local module and scripts
from tdc_surface_concept import scTDC

raw_mode = False
NR_OF_MEASUREMENTS = 4  # number of measurements
EXPOSURE_MS = 1000  # exposure duration in milliseconds

if not raw_mode:
    DATA_FIELD_SEL1 = \
        scTDC.SC_DATA_FIELD_DIF1 \
        | scTDC.SC_DATA_FIELD_DIF2 \
        | scTDC.SC_DATA_FIELD_TIME \
        | scTDC.SC_DATA_FIELD_CHANNEL \
        | scTDC.SC_DATA_FIELD_SUBDEVICE \
        | scTDC.SC_DATA_FIELD_START_COUNTER
elif raw_mode:
    DATA_FIELD_SEL1 = \
        scTDC.SC_DATA_FIELD_TIME \
        | scTDC.SC_DATA_FIELD_CHANNEL \
        | scTDC.SC_DATA_FIELD_SUBDEVICE \
        | scTDC.SC_DATA_FIELD_TIME_TAG \
        | scTDC.SC_DATA_FIELD_START_COUNTER
# define some constants to distinguish the type of element placed in the queue
QUEUE_DATA = 0
QUEUE_ENDOFMEAS = 1


class BufDataCB4(scTDC.buffered_data_callbacks_pipe):
    def __init__(self, lib, dev_desc, raw_mode,  dld_events,
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
                | scTDC.SC_DATA_FIELD_SUBDEVICE \
                | scTDC.SC_DATA_FIELD_START_COUNTER \
                | scTDC.SC_DATA_FIELD_TIME_TAG \

        super().__init__(lib, dev_desc, data_field_selection,  # <-- mandatory!
                         max_buffered_data_len, dld_events)  # <-- mandatory!

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


def run():
    device = scTDC.Device(autoinit=False)

    # initialize TDC --- and check for error!
    retcode, errmsg = device.initialize()
    if retcode < 0:
        print("error during init:", retcode, errmsg)
        return -1
    else:
        print("successfully initialized")

    # open a BUFFERED_DATA_CALLBACKS pipe
    bufdatacb_dld = BufDataCB4(device.lib, device.dev_desc, raw_mode=False, dld_events=True)
    # bufdatacb_tdc = BufDataCB4(device.lib, device.dev_desc, raw_mode=True, dld_events=False)

    # define a closure that checks return codes for errors and does clean up
    def errorcheck(retcode):
        if retcode < 0:
            print(device.lib.sc_get_err_msg(retcode))
            bufdatacb_dld.close()
            # bufdatacb_tdc.close()
            device.deinitialize()
            return -1
        else:
            return 0

    start = timeit.default_timer()

    # start a first measurement
    retcode = bufdatacb_dld.start_measurement(EXPOSURE_MS)
    if errorcheck(retcode) < 0:
        return -1

    meas_remaining = NR_OF_MEASUREMENTS
    while True:
        print('Number of remaining measurement',meas_remaining)
        eventtype_dld, data_dld = bufdatacb_dld.queue.get()  # waits until element available
        # eventtype_tdc, data_tdc = bufdatacb_tdc.queue.get()  # waits until element available
        if eventtype_dld == QUEUE_DATA:

            print(len(data_dld["start_counter"]))
            a_dld = np.array((data_dld["start_counter"],
                          data_dld["dif1"], data_dld["dif2"], data_dld["time"]))
            print(a_dld)
            print('+++++++++++++++++++++++++++')
        # if eventtype_tdc == QUEUE_DATA:
        #     print(len(data_tdc["start_counter"]))
        #     # a_tdc = np.array((data_tdc["channel"], data_tdc["start_counter"],
        #     #               data_tdc["time"], data_tdc["time_tag"], data_tdc["subdevice"]))
        #     print(data_tdc["time_tag"])
            # print(a_tdc)

            print('==========================')
        meas_remaining = meas_remaining - 1
        if meas_remaining > 0:
            retcode = bufdatacb_dld.start_measurement(EXPOSURE_MS)
            if errorcheck(retcode) < 0:
                return -1
            # else:
            #     break
        else:  # unknown event
            break  # break out of the event loop

    end = timeit.default_timer()
    print("\ntime elapsed : ", end - start, "s")

    time.sleep(0.1)
    # clean up
    bufdatacb_dld.close()  # closes the user callbacks pipe, method inherited from base class
    # bufdatacb_tdc.close()
    device.deinitialize()

    return 0


if __name__ == "__main__":
    run()
