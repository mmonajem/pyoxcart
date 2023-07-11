


def onselect(eclick, erelease, variables):
    """
    Callback function for the selection event.

    Args:
        eclick (MouseEvent): Event object representing the click event.
        erelease (MouseEvent): Event object representing the release event.
        variables (object): Object containing the variables.

    """
    variables.selected_x_fdm = eclick.xdata + (erelease.xdata - eclick.xdata) / 2
    variables.selected_y_fdm = eclick.ydata + (erelease.ydata - eclick.ydata) / 2
    variables.roi_fdm = min(erelease.xdata - eclick.xdata, erelease.ydata - eclick.ydata) / 2

def line_select_callback(eclick, erelease, variables):
    """
    Callback function for line selection event.

    Args:
        eclick (MouseEvent): Event object representing the press event.
        erelease (MouseEvent): Event object representing the release event.
        variables (object): Object containing the variables.

    """
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    variables.selected_x1 = x1
    variables.selected_x2 = x2
    variables.selected_y1 = y1
    variables.selected_y2 = y2
    variables.selected_calculated = False


def toggle_selector(event):
    """
    Toggles the rectangle selector based on the key press event.

    Args:
        event (KeyEvent): Event object representing the key press event.

    """
    try:
        if event.key in ['Q', 'q'] and toggle_selector.RS.active:
            toggle_selector.RS.set_active(False)
        if event.key in ['A', 'a'] and not toggle_selector.RS.active:
            toggle_selector.RS.set_active(True)
    except:
        pass
