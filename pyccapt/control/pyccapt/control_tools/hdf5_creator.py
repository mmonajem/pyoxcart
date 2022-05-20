"""
This is the script for saving the hdf5 file containing the experiment data.
"""

import h5py
import logging

from pyccapt.control_tools import variables

log = logging.getLogger('hdf5_creator')
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', 
                              '%m-%d-%Y %H:%M:%S')
file_handler = logging.FileHandler('hdf5_creator.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)


def hdf_creator_oxcart(time_counter, time_ex_s, time_ex_m, time_ex_h):
    # save hdf5 file
    log.info("Function - hdf_creator_oxcart | time_counter- > {} | type - {}".format(time_counter,type(time_counter)))
    log.info("Function - hdf_creator_oxcart | time_ex_s- > {} | type - {}".format(time_ex_s,type(time_ex_s))) 
    log.info("Function - hdf_creator_oxcart | time_ex_m- > {} | type - {}".format(time_ex_m,type(time_ex_m))) 
    log.info("Function - hdf_creator_oxcart | time_ex_h- > {} | type - {}".format(time_ex_h,type(time_ex_h))) 



    with h5py.File(variables.path + '\\data_%s.h5' % variables.exp_name, "w") as f:
        f.create_dataset("apt/high_voltage", data=variables.main_v_dc, dtype='f')
        f.create_dataset("apt/pulse_voltage", data=variables.main_v_p, dtype='f')
        f.create_dataset("apt/num_events", data=variables.main_counter, dtype='i')
        f.create_dataset('apt/temperature', data=variables.main_temperature, dtype='f')
        f.create_dataset('apt/main_chamber_vacuum', data=variables.main_chamber_vacuum, dtype='f')
        f.create_dataset("apt/time_counter", data=time_counter, dtype='i')

        f.create_dataset("time/time_s", data=time_ex_s, dtype='i')
        f.create_dataset("time/time_m", data=time_ex_m, dtype='i')
        f.create_dataset("time/time_h", data=time_ex_h, dtype='i')

        if variables.counter_source == 'TDC':
            f.create_dataset("dld/x", data=variables.x, dtype='i')
            f.create_dataset("dld/y", data=variables.y, dtype='i')
            f.create_dataset("dld/t", data=variables.t, dtype='i')
            f.create_dataset("dld/start_counter", data=variables.dld_start_counter, dtype='i')
            f.create_dataset("dld/high_voltage", data=variables.main_v_dc_dld, dtype='f')
            f.create_dataset("dld/pulse_voltage", data=variables.main_v_p_dld, dtype='f')

        elif variables.counter_source == 'TDC_Raw':
            f.create_dataset("tdc/start_counter", data=variables.tdc_start_counter, dtype='i')
            f.create_dataset("tdc/channel", data=variables.channel, dtype='i')
            f.create_dataset("tdc/time_data", data=variables.time_data, dtype='i')
            f.create_dataset("tdc/high_voltage", data=variables.main_v_dc_tdc, dtype='f')
            f.create_dataset("tdc/pulse_voltage", data=variables.main_v_p_tdc, dtype='f')

        elif variables.counter_source == 'DRS':
            f.create_dataset("drs/ch0_time", data=variables.ch0_time, dtype='f')
            f.create_dataset("drs/ch0_wave", data=variables.ch0_wave, dtype='f')
            f.create_dataset("drs/ch1_time", data=variables.ch1_time, dtype='f')
            f.create_dataset("drs/ch1_wave", data=variables.ch1_wave, dtype='f')
            f.create_dataset("drs/ch2_time", data=variables.ch2_time, dtype='f')
            f.create_dataset("drs/ch2_wave", data=variables.ch2_wave, dtype='f')
            f.create_dataset("drs/ch3_time", data=variables.ch3_time, dtype='f')
            f.create_dataset("drs/ch3_wave", data=variables.ch3_wave, dtype='f')
            f.create_dataset("drs/high_voltage", data=variables.main_v_dc_drs, dtype='f')
            f.create_dataset("drs/pulse_voltage", data=variables.main_v_p_drs, dtype='f')


def hdf_creator_physic(time_counter, time_ex_s, time_ex_m, time_ex_h):

    # save hdf5 file
    with h5py.File(variables.path + '\\data_%s.h5' % variables.exp_name, "w") as f:
        f.create_dataset("apt/high_voltage", data=variables.main_v_dc, dtype='f')
        f.create_dataset("apt/num_events", data=variables.main_counter, dtype='i')
        f.create_dataset("apt/time_counter", data=time_counter, dtype='i')

        f.create_dataset("time/time_s", data=time_ex_s, dtype='i')
        f.create_dataset("time/time_m", data=time_ex_m, dtype='i')
        f.create_dataset("time/time_h", data=time_ex_h, dtype='i')

        if variables.counter_source == 'TDC':
            f.create_dataset("dld/x", data=variables.x, dtype='i')
            f.create_dataset("dld/y", data=variables.y, dtype='i')
            f.create_dataset("dld/t", data=variables.t, dtype='i')
            f.create_dataset("dld/AbsoluteTimeStamp", data=variables.dld_start_counter, dtype='i')
            f.create_dataset("dld/high_voltage", data=variables.main_v_dc_dld, dtype='f')

            f.create_dataset("tdc/ch0", data=variables.ch0, dtype='i')
            f.create_dataset("tdc/ch1", data=variables.ch1, dtype='i')
            f.create_dataset("tdc/ch2", data=variables.ch2, dtype='i')
            f.create_dataset("tdc/ch3", data=variables.ch3, dtype='i')
            f.create_dataset("tdc/ch4", data=variables.ch4, dtype='i')
            f.create_dataset("tdc/ch5", data=variables.ch5, dtype='i')
            f.create_dataset("tdc/ch6", data=variables.ch6, dtype='i')
            f.create_dataset("tdc/ch7", data=variables.ch6, dtype='i')
