import math

import matplotlib.pyplot as plt


class AnnoteFinder(object):
    """
    Callback for matplotlib to display an annotation when points are left clicked on
    and deselect when right click on with mouse.
    The point which is closest to the click and within xtol and ytol is identified.

    Register this function like this:

    scatter(xdata, ydata)
    af = AnnoteFinder(xdata, ydata, annotes)
    connect('button_press_event', af)
    """

    def __init__(self, xdata, ydata, annotes, variables, ax=None, xtol=None, ytol=None):
        """
        Initialize the AnnoteFinder object.

        Args:
            xdata (list): X-coordinates of the data points.
            ydata (list): Y-coordinates of the data points.
            annotes (list): List of annotations corresponding to the data points.
            variables (list): List of variables corresponding to the data points.
            ax (Axes, optional): The matplotlib Axes instance. Defaults to None.
            xtol (float, optional): The tolerance value in the x-direction. Defaults to None.
            ytol (float, optional): The tolerance value in the y-direction. Defaults to None.
        """
        self.data = list(zip(xdata, ydata, annotes))
        if xtol is None:
            xtol = ((max(xdata) - min(xdata)) / float(len(xdata))) / 2
        if ytol is None:
            ytol = ((max(ydata) - min(ydata)) / float(len(ydata))) / 2
        self.xtol = xtol
        self.ytol = ytol
        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax
        self.drawnAnnotations = {}
        self.links = []
        self.variables = variables

    def annotates_plotter(self, event):
        """
        Callback function to handle button press event.

        Args:
            event (Event): The matplotlib event object.
        """
        if event.inaxes:
            clickX = event.xdata
            clickY = event.ydata
            if (self.ax is None) or (self.ax is event.inaxes):
                annotes = []
                for x, y, a in self.data:
                    if ((clickX - self.xtol < x < clickX + self.xtol) and
                            (clickY - self.ytol < y < clickY + self.ytol)):
                        annotes.append(
                            (distances(x, clickX, y, clickY), x, y, a))
                if annotes:
                    annotes.sort()
                    distance, x, y, annote = annotes[0]
                    if event.button == 3:  # right-click
                        # Call deselectPoint method on right-click
                        self.deselectPoint(event.inaxes, x, y, annote)
                    else:
                        # Call drawAnnote method on left-click
                        self.drawAnnote(event.inaxes, x, y, annote)
                    for l in self.links:
                        l.drawSpecificAnnote(annote)




    def drawAnnote(self, ax, x, y, annote):
        """
        Draw the annotation on the plot.

        Args:
            ax (Axes): The matplotlib Axes instance.
            x (float): X-coordinate of the annotation.
            y (float): Y-coordinate of the annotation.
            annote (str): The annotation text.
        """

        if (x, y) in self.drawnAnnotations:
            return
        else:
            # Calculate an offset to move the annotation to the left of the peak_x
            x_offset = - 1.2
            # Draw the annotation without the dash "-"
            t = ax.text(x + x_offset, y, str(annote), ha='right', va='center')

            m = ax.scatter([x], [y], marker='H', c='r', zorder=100)
            self.drawnAnnotations[(x, y)] = (t, m)
            self.ax.figure.canvas.draw_idle()

        self.variables.peaks_idx.append(int(annote) - 1)
        self.variables.peaks_idx.sort()

    def deselectPoint(self, ax, x, y, annote):
        """
        Draw the annotation on the plot.

        Args:
            ax (Axes): The matplotlib Axes instance.
            x (float): X-coordinate of the annotation.
            y (float): Y-coordinate of the annotation.
            annote (str): The annotation text.
        """

        if (x, y) in self.drawnAnnotations:
            markers = self.drawnAnnotations[(x, y)]
            for m in markers:
                m.set_visible(not m.get_visible())
            self.ax.figure.canvas.draw_idle()

        # Remove the deselected peak_x index from peaks_idx
        self.variables.peaks_idx.remove(int(annote) - 1)
        self.variables.peaks_idx.sort()

    def drawSpecificAnnote(self, annote):
        """
        Draw specific annotation on the plot.

        Args:
            annote (str): The annotation to be drawn.
        """
        annotesToDraw = [(x, y, a) for x, y, a in self.data if a == annote]
        for x, y, a in annotesToDraw:
            self.drawAnnote(self.ax, x, y, a)


def distances(x1, x2, y1, y2):
    """
    Calculate the Euclidean distance between two points.

    Args:
        x1 (float): X-coordinate of the first point.
        x2 (float): X-coordinate of the second point.
        y1 (float): Y-coordinate of the first point.
        y2 (float): Y-coordinate of the second point.

    Returns:
        float: The Euclidean distance between the two points.
    """
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
