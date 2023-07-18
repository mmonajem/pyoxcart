import matplotlib.pyplot as plt
import numpy as np


class VerticalLineManager:
    def __init__(self, ax, x, y):
        self.ax = ax
        self.fig = ax.figure
        self.lines = []
        self.active_line = None
        self.x = x
        self.y = y
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid_button_press = self.fig.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.cid_scroll = self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)

        self.is_zooming = False
        self.zoom_factor = 1.1
        if len(x) > 0:
            self.ax.set_xlim(np.min(x), np.max(x))
        self.ax.set_yscale('log')  # Set y-axis to logarithmic scale

        self.original_xlim = (np.min(x), np.max(x)) if len(x) > 0 else (
        0, 1)  # Store the original x-axis limits as a tuple
        self.original_ylim = (np.min(y), np.max(y)) if len(y) > 0 else (
        0, 1)  # Store the original y-axis limits as a tuple

    def on_press(self, event):
        if event.button == 1:
            self.add_line(event.xdata)

    def on_release(self, event):
        if event.button == 3:
            self.remove_line(event.xdata)

    def on_motion(self, event):
        if self.active_line is not None:
            self.update_line(event.xdata)

    def on_key_press(self, event):
        if event.key == 'h':
            self.reset_view()

    def on_scroll(self, event):
        if event.button == 'up':
            self.zoom(event.xdata, self.zoom_factor)
        elif event.button == 'down':
            self.zoom(event.xdata, 1 / self.zoom_factor)
        self.ax.figure.canvas.draw_idle()

    def zoom(self, x, zoom_factor=1.1):
        x_range = self.ax.get_xlim()[1] - self.ax.get_xlim()[0]
        x_new_range = x_range / zoom_factor

        x_left = x - (x - self.ax.get_xlim()[0]) / zoom_factor
        self.ax.set_xlim(x_left, x_left + x_new_range)

    def reset_view(self):
        self.ax.set_xlim(*self.original_xlim)
        self.ax.set_ylim(*self.original_ylim)
        self.fig.canvas.draw_idle()

    def add_line(self, x):
        line = plt.Line2D([x, x], [self.ax.get_ylim()[0], self.ax.get_ylim()[1]], color='r', linestyle='--',
                          linewidth=2)
        self.ax.add_line(line)
        self.lines.append(line)
        self.active_line = line

    def remove_line(self, x):
        for line in self.lines:
            if np.isclose(line.get_xdata()[0], x):
                line.remove()
                self.lines.remove(line)
                break
        self.fig.canvas.draw_idle()

    def remove_line_under_cursor(self, x, y):
        line = self.get_line_under_cursor(x, y)
        if line is not None:
            self.lines.remove(line)
            line.remove()
            self.fig.canvas.draw()

    def on_button_press(self, event):
        if event.button == 3:  # Right click to remove the line
            self.remove_line_under_cursor(event.xdata, event.ydata)

    def update_line(self, x):
        if self.active_line is not None:
            self.active_line.set_data([x, x], [self.ax.get_ylim()[0], self.ax.get_ylim()[1]])
            self.fig.canvas.draw_idle()

    def get_line_positions(self):
        return [line.get_xdata()[0] for line in self.lines]

    def get_line_under_cursor(self, x, y, tolerance=100):
        for line in self.lines:
            line_x = line.get_xdata()
            line_y = line.get_ydata()
            distance = np.sqrt((line_x - x) ** 2 + (line_y - y) ** 2)
            if np.any(distance < tolerance):
                return line
        return None
