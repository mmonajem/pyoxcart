from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

from mcculw import ul
from mcculw.enums import InfoType, BoardInfo, AiChanType, TcType, TempScale, TInOptions


def run_example():
    device_to_show = "USB-TC"
    board_num = 0

    # Verify board is Board 0 in InstaCal.  If not, show message...
    print("Looking for Board 0 in InstaCal to be {0} series...".format(device_to_show))

    try:
        # Get the devices name...
        board_name = ul.get_board_name(board_num)

    except Exception as e:
        if ul.ErrorCode(1):
            # No board at that number throws error
            print("\nNo board found at Board 0.")
            print(e)
            return

    else:
        if device_to_show in board_name:
            # Board 0 is the desired device...
            print("{0} found as Board number {1}.\n".format(board_name, board_num))
            ul.flash_led(board_num)

        else:
            # Board 0 is NOT desired device...
            print("\nNo {0} series found as Board 0. Please run InstaCal.".format(device_to_show))
            return

    try:
        # select a channel
        channel = 1
        # Set thermocouple type to type K
        # ul.set_config(
        #     InfoType.BOARDINFO, board_num, channel, BoardInfo.CHANTCTYPE,
        #     TcType.K)
        # # Set the temperature scale to Fahrenheit
        # ul.set_config(
        #     InfoType.BOARDINFO, board_num, channel, BoardInfo.TEMPSCALE,
        #     TempScale.CELSIUS)
        # # Set data rate to 60Hz
        # ul.set_config(
        #     InfoType.BOARDINFO, board_num, channel, BoardInfo.ADDATARATE, 60)

        # Read data from the channel:
        channel_list = ['MC_NEG', 'MC_Det', 'Mc-Top', 'MC-Gate', 'BC-Top', 'BC-Pump']
        for i in range(6):

            options = TInOptions.NOFILTER
            value_temperature = ul.t_in(board_num, i, TempScale.CELSIUS, options)
            print("Channel{:d} - {:s}:  {:.3f} Degrees.".format(i, channel_list[i], value_temperature))

    except Exception as e:
        print('\n', e)


if __name__ == '__main__':
    run_example()