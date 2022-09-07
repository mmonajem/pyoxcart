"""
This is file contains tools for mass calibration process.
"""

from pyccapt.calibration.calibration_tools import variables


def onselect(eclick, erelease):
    "eclick and erelease are matplotlib events at press and release."

    variables.selected_x_fdm = eclick.xdata + (erelease.xdata - eclick.xdata) / 2
    variables.selected_y_fdm = eclick.ydata + (erelease.ydata - eclick.ydata) / 2
    variables.roi_fdm = min(erelease.xdata - eclick.xdata, erelease.ydata - eclick.ydata) / 2


def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    # print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
    # print(" The button you used were: %s %s" % (eclick.button, erelease.button))

    variables.selected_x1 = x1
    variables.selected_x2 = x2


def toggle_selector(event):
    # print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        # print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        # print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)