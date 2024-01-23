from copy import copy

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors, rcParams


def sdm(particles, bin_size, variables=None, normalize=False, reference_point=None, reference_point_shift=False,
        box_dimensions=None, plot_mode='bar', plot=False, save=False, figure_size=(6, 6), figname='sdm',
        histogram_type='1d', axes=None):
    """
	Computes 1D or 2D histograms for a set of particle coordinates.

	Parameters
	----------
	particles : (N, 3) np.array
		Set of particle coordinates for which to compute the SDM.
	bin_size : float
		Bin size for each histogram.
	variables : variables object
	normalize : bool, optional
		Option to normalize the histograms. If True, the histogram values are normalized.
	reference_point : (3,) np.array or list, optional
		The center of the box. If left as None, there is no data cropping, and calculate the SDM for the whole data.
	reference_point_shift : bool, optional
		Option to shift the relative positions by the reference point. If True, the relative positions are shifted.
	box_dimensions : (3,) np.array or list, optional
		The dimensions of the box. If left as None, the box dimensions will be inferred from the particles.
	plot_mode : str, optional
		The plot mode for the histograms. Options are 'bar' or 'line'.
	plot : bool, optional
		Option to plot the histograms. If True, the histograms are plotted.
	save : bool, optional
		Option to save the histograms. If True, the histograms are saved.
	figure_size : (float, float), optional
		The size of the figure in inches.
	figname : str, optional
		The name of the figure.
	histogram_type : str, optional
		Type of histogram. Options are '1D' or '2D' or '3D'.
	axes : list or None, optional
		Specifies the axes for 1D or 2D histograms. For '1d', provide a list like ['x'], ['y'], or ['z'].
		For '2d', provide a list like ['x', 'y'], ['y', 'z'], or ['x', 'z'] or ['x', 'y', 'z'].

	Returns
	-------
	histograms : list of np.array
		List of 1D or 2D histograms based on user preferences.
	edges : list of np.array
		Bin edges for each histogram.
	"""

    if reference_point is not None and box_dimensions is not None:
        if box_dimensions != [0, 0, 0]:
            if isinstance(reference_point, list):
                reference_point = np.array(reference_point)
            if isinstance(box_dimensions, list):
                box_dimensions = np.array(box_dimensions)
            # Ensure box_dimensions has at least 3 components
            assert len(box_dimensions) == 3, "box_dimensions must have 3 components (x, y, z)."

            # Calculate the bounds of the box
            box_min = reference_point - 0.5 * box_dimensions
            box_max = reference_point + 0.5 * box_dimensions
            # Crop particles within the specified box
            inside_box = np.all((particles >= box_min) & (particles <= box_max), axis=1)
            particles = particles[inside_box]

    print('The number of ions is: ', len(particles))
    # Calculate relative positions based on user choices
    dx, dy, dz = None, None, None

    if 'x' in axes:
        dx = np.subtract.outer(particles[:, 0], particles[:, 0])
        if reference_point_shift and reference_point is not None and box_dimensions is not None:
            dx = dx + reference_point[0]

    if 'y' in axes:
        dy = np.subtract.outer(particles[:, 1], particles[:, 1])
        if reference_point_shift and reference_point is not None and box_dimensions is not None:
            dy = dy + reference_point[1]

    if 'z' in axes:
        dz = np.subtract.outer(particles[:, 2], particles[:, 2])
        if reference_point_shift and reference_point is not None and box_dimensions is not None:
            dz = dz + reference_point[2]
    histograms = []
    edges_list = []
    if 'x' in axes and 'y' in axes and 'z' in axes:
        edges = np.arange(min(np.min(dx), np.min(dy), np.min(dz)), max(np.max(dx), np.max(dy), np.max(dz)), bin_size)
    elif 'x' in axes and 'y' in axes:
        edges = np.arange(min(np.min(dx), np.min(dy)), max(np.max(dx), np.max(dy)), bin_size)
    elif 'y' in axes and 'z' in axes:
        edges = np.arange(min(np.min(dy), np.min(dz)), max(np.max(dy), np.max(dz)), bin_size)
    elif 'x' in axes and 'z' in axes:
        edges = np.arange(min(np.min(dx), np.min(dz)), max(np.max(dx), np.max(dz)), bin_size)
    elif 'x' in axes:
        edges = np.arange(np.min(dx), np.max(dx), bin_size)
    elif 'y' in axes:
        edges = np.arange(np.min(dy), np.max(dy), bin_size)
    elif 'z' in axes:
        edges = np.arange(np.min(dz), np.max(dz), bin_size)

    if histogram_type == '1D':
        if 'x' in axes:
            histo_dx, bins_dx = np.histogram(dx.flatten(), bins=edges)
            histograms.append(histo_dx)
            edges_list.append(bins_dx)
        elif 'y' in axes:
            histo_dy, bins_dy = np.histogram(dy.flatten(), bins=edges)
            histograms.append(histo_dy)
            edges_list.append(bins_dy)
        elif 'z' in axes:
            histo_dz, bins_dz = np.histogram(dz.flatten(), bins=edges)
            histograms.append(histo_dz)
            edges_list.append(bins_dz)
        else:
            raise ValueError("Invalid axes for 1D histogram. Choose from ['x'], ['y'], or ['z'].")
        if normalize:
            histograms[-1] = histograms[-1] / np.sum(histograms[-1])

    if histogram_type == '2D':
        if 'x' in axes and 'y' in axes:
            hist2d, x_edges, y_edges = np.histogram2d(dx.flatten(), dy.flatten(), bins=[edges, edges])
            extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]
            histograms.append(hist2d)
            edges_list.extend([x_edges, y_edges])
        elif 'y' in axes and 'z' in axes:
            hist2d, x_edges, y_edges = np.histogram2d(dy.flatten(), dz.flatten(), bins=[edges, edges])
            extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]
            histograms.append(hist2d)
            edges_list.extend([x_edges, y_edges])
        elif 'x' in axes and 'z' in axes:
            hist2d, x_edges, y_edges = np.histogram2d(dx.flatten(), dz.flatten(), bins=[edges, edges])
            extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]
            histograms.append(hist2d)
            edges_list.extend([x_edges, y_edges])
        else:
            raise ValueError("Invalid axes for 2D histogram. Choose from ['x', 'y'], ['y', 'z'], or ['x', 'z'].")

        if normalize:
            histograms[-1] = histograms[-1] / np.sum(histograms[-1])

    if histogram_type == '3D':
        if 'x' in axes and 'y' in axes and 'z' in axes:
            hist3d, edges = np.histogramdd((dx.flatten(), dy.flatten(), dz.flatten()), bins=[edges, edges, edges])
            histograms.append(hist3d)
            edges_list.extend([edges])
        if normalize:
            histograms[-1] = histograms[-1] / np.sum(histograms[-1])

    if plot or save:
        # Plot histograms
        if histogram_type == '1D':
            fig, ax = plt.subplots(figsize=figure_size)
            for i, hist in enumerate(histograms):
                if plot_mode == 'bar':
                    ax.bar(edges[:-1], hist, width=bin_size, align='edge')
                    ax.set_ylabel('Counts')
                    ax.set_xlabel(f'{axes[i]} (nm)')
                elif plot_mode == 'line':
                    ax.plot(edges[:-1], hist)
                    ax.set_ylabel('Counts')
                    ax.set_xlabel(f'{axes[i]} (nm)')
        elif histogram_type == '2D':
            fig, ax = plt.subplots(figsize=figure_size)
            img = ax.imshow(histograms[-1].T, origin='lower', extent=extent, aspect="auto")
            ax.set_ylabel(f'{axes[1]} (nm)')
            ax.set_xlabel(f'{axes[0]} (nm)')
            cmap = copy(plt.cm.plasma)
            cmap.set_bad(cmap(0))
            pcm = ax.pcolormesh(x_edges, y_edges, histograms[-1].T, cmap=cmap, norm=colors.LogNorm(), rasterized=True)
            cbar = fig.colorbar(pcm, ax=ax, pad=0)
            cbar.set_label('Counts', fontsize=10)
        elif histogram_type == '3D':
            pass

        if save and variables is not None:
            # Enable rendering for text elements
            rcParams['svg.fonttype'] = 'none'
            plt.savefig(variables.result_path + '\\sdm_{fn}.png'.format(fn=figname), format="png", dpi=600)
            plt.savefig(variables.result_path + '\\sdm_{fn}.svg'.format(fn=figname), format="svg", dpi=600)

        if plot:
            plt.show()

    return histograms, edges_list
