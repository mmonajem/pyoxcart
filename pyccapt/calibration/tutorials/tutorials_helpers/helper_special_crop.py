import ipywidgets as widgets
from IPython.display import display
from ipywidgets import Output

from pyccapt.calibration.data_tools import data_loadcrop

# Define a layout for labels to make them a fixed width
label_layout = widgets.Layout(width='200px')


def reset(variables, out):
    variables.data = variables.data_backup.copy()
    with out:  # Capture the output within the 'out' widget
        out.clear_output()  # Clear any previous output
        print('Reset the crop')


def apply_crop(variables, out):
    # Crop the dataset
    with out:  # Capture the output within the 'out' widget
        if variables.roi_fdm > 0:
            data_crop_spatial = data_loadcrop.crop_data_after_selection(variables.data, variables)
            print('The crop for center x:', variables.selected_x_fdm, 'center y:',
                  variables.selected_y_fdm, 'and radios:', variables.roi_fdm, 'is applied')
        else:
            print('select the data spacialy from cell below')


def call_plot_crop_fdm(variables):
    # Define widgets and labels for each parameter
    frac_widget = widgets.FloatText(value=1.0)
    frac_label = widgets.Label(value="Fraction:", layout=label_layout)

    # Modify bins_widget and figure_size_widget to be editable
    bins_x = widgets.IntText(value=256)
    bins_y = widgets.IntText(value=256)
    bins_label = widgets.Label(value="Bins (X, Y):", layout=label_layout)

    figure_size_x = widgets.FloatText(value=5.0)
    figure_size_y = widgets.FloatText(value=4.0)
    figure_size_label = widgets.Label(value="Figure Size (X, Y):", layout=label_layout)

    save_widget = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
    save_label = widgets.Label(value="Save:", layout=label_layout)

    figname_widget = widgets.Text(value='fdm_ini')
    figname_label = widgets.Label(value="Figure Name:", layout=label_layout)

    # Create a button widget to trigger the function
    button_plot = widgets.Button(description="plot")
    # Create a button widget to trigger the function
    button_apply = widgets.Button(description="apply crop")
    # Create a button widget to trigger the function
    button_rest = widgets.Button(description="reset")

    out = Output()

    def on_button_click(b, variables):
        # Disable the button while the code is running
        button_plot.disabled = True

        # Get the values from the widgets
        frac = frac_widget.value
        bins = (bins_x.value, bins_y.value)
        figure_size = (figure_size_x.value, figure_size_y.value)
        save = save_widget.value
        figname = figname_widget.value

        with out:  # Capture the output within the 'out' widget
            out.clear_output()  # Clear any previous output
            # Call the function
            data = variables.data.copy()
            data_loadcrop.plot_crop_fdm(data, bins, frac, axis_mode='normal', figure_size=figure_size,
                                        variables=variables, range_sequence=[], range_mc=[], range_detx=[],
                                        range_dety=[], range_x=[], range_y=[], range_z=[],
                                        data_crop=True, draw_circle=False, save=save, figname=figname)

        # Enable the button when the code is finished
        button_plot.disabled = False

    button_plot.on_click(lambda b: on_button_click(b, variables))
    button_apply.on_click(lambda b: apply_crop(variables, out))
    button_rest.on_click(lambda b: reset(variables, out))

    widget_container = widgets.VBox([
        widgets.HBox([frac_label, frac_widget]),
        widgets.HBox([bins_label, widgets.HBox([bins_x, bins_y])]),
        widgets.HBox([figure_size_label, widgets.HBox([figure_size_x, figure_size_y])]),
        widgets.HBox([save_label, save_widget]),
        widgets.HBox([figname_label, figname_widget]),
        widgets.HBox([button_plot, button_apply, button_rest]),
    ])
    display(widget_container)
    display(out)
