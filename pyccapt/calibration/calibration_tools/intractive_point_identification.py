import math

import matplotlib.pyplot as plt

from pyccapt.calibration.calibration_tools import share_variables


class AnnoteFinder(object):
    """
    Callback for matplotlib to display an annotation when points are clicked on.
    The point which is closest to the click and within xtol and ytol is identified.

    Register this function like this:

    scatter(xdata, ydata)
    af = AnnoteFinder(xdata, ydata, annotes)
    connect('button_press_event', af)
    """

    def __init__(self, xdata, ydata, annotes, ax=None, xtol=None, ytol=None):
        """
        Initialize the AnnoteFinder object.

        Args:
            xdata (list): X-coordinates of the data points.
            ydata (list): Y-coordinates of the data points.
            annotes (list): List of annotations corresponding to the data points.
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

    def distance(self, x1, x2, y1, y2):
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

    def __call__(self, event):
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
                            (self.distance(x, clickX, y, clickY), x, y, a))
                if annotes:
                    annotes.sort()
                    distance, x, y, annote = annotes[0]
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
            markers = self.drawnAnnotations[(x, y)]
            for m in markers:
                m.set_visible(not m.get_visible())
            self.ax.figure.canvas.draw_idle()
        else:
            t = ax.text(x, y, " - %s" % (annote))
            m = ax.scatter([x], [y], marker='d', c='r', zorder=100)
            self.drawnAnnotations[(x, y)] = (t, m)
            self.ax.figure.canvas.draw_idle()

        variables.peaks_idx.append(int(annote) - 1)

    def drawSpecificAnnote(self, annote):
        """
        Draw specific annotation on the plot.

        Args:
            annote (str): The annotation to be drawn.
        """
        annotesToDraw = [(x, y, a) for x, y, a in self.data if a == annote]
        for x, y, a in annotesToDraw:
            self.drawAnnote(self.ax, x, y, a)
