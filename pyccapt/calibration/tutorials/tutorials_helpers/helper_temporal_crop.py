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
		variables.data = data_loadcrop.crop_dataset(variables.data, variables)
		print('The crop for Min Idx:', variables.selected_x1, ' and Max Idx:', variables.selected_x2, 'is applied')


def call_plot_crop_experiment(variables):
	# Define widgets and labels for each parameter
	max_tof_widget = widgets.FloatText(value=variables.max_tof)
	max_tof_label = widgets.Label(value="Max TOF:", layout=label_layout)

	frac_widget = widgets.FloatText(value=1.0)
	frac_label = widgets.Label(value="Fraction:", layout=label_layout)

	# Modify bins_widget and figure_size_widget to be editable
	bins_x = widgets.IntText(value=1200)
	bins_y = widgets.IntText(value=800)
	bins_label = widgets.Label(value="Bins (X, Y):", layout=label_layout)

	figure_size_x = widgets.FloatText(value=7.0)
	figure_size_y = widgets.FloatText(value=3.0)
	figure_size_label = widgets.Label(value="Figure Size (X, Y):", layout=label_layout)

	draw_rect_widget = widgets.fixed(False)
	data_crop_widget = widgets.fixed(True)
	pulse_plot_widget = widgets.Dropdown(options=[('False', False), ('True', True)], value=False)
	pulse_plot_label = widgets.Label(value="Pulse Plot:", layout=label_layout)

	dc_plot_widget = widgets.Dropdown(options=[('True', True), ('False', False)], value=True)
	dc_plot_label = widgets.Label(value="DC Plot:", layout=label_layout)

	pulse_mode_widget = widgets.Dropdown(options=[('voltage', 'voltage'), ('laser', 'laser')], value='voltage')
	pulse_mode_label = widgets.Label(value="Pulse Mode:", layout=label_layout)

	save_widget = widgets.Dropdown(options=[('True', True), ('False', False)], value=False)
	save_label = widgets.Label(value="Save:", layout=label_layout)

	figname_widget = widgets.Text(value='hist_ini')
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
		data = variables.data.copy()
		variables = variables
		max_tof = max_tof_widget.value
		frac = frac_widget.value

		# Get the values from the editable widgets and create tuples
		bins = (bins_x.value, bins_y.value)
		figure_size = (figure_size_x.value, figure_size_y.value)

		draw_rect = draw_rect_widget.value
		data_crop = data_crop_widget.value
		pulse_plot = pulse_plot_widget.value
		dc_plot = dc_plot_widget.value
		pulse_mode = pulse_mode_widget.value
		save = save_widget.value
		figname = figname_widget.value

		with out:  # Capture the output within the 'out' widget
			out.clear_output()  # Clear any previous output
			# Call the actual function with the obtained values
			data_loadcrop.plot_crop_experiment_history(data, variables, max_tof, frac, bins, figure_size,
			                                           draw_rect, data_crop, pulse_plot, dc_plot,
			                                           pulse_mode, save, figname)
		# Enable the button when the code is finished
		button_plot.disabled = False

	button_plot.on_click(lambda b: on_button_click(b, variables))
	button_apply.on_click(lambda b: apply_crop(variables, out))
	button_rest.on_click(lambda b: reset(variables, out))

	widget_container = widgets.VBox([
		widgets.HBox([max_tof_label, max_tof_widget]),
		widgets.HBox([frac_label, frac_widget]),
		widgets.HBox([bins_label, widgets.HBox([bins_x, bins_y])]),
		widgets.HBox([figure_size_label, widgets.HBox([figure_size_x, figure_size_y])]),
		widgets.HBox([pulse_plot_label, pulse_plot_widget]),
		widgets.HBox([dc_plot_label, dc_plot_widget]),
		widgets.HBox([pulse_mode_label, pulse_mode_widget]),
		widgets.HBox([save_label, save_widget]),
		widgets.HBox([figname_label, figname_widget]),
		widgets.HBox([button_plot, button_apply, button_rest]),
	])
	display(widget_container)
	display(out)
