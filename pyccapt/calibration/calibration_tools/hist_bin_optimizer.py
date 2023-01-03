#######################################################################################################################
#Author   : Dr. Arun B Ayyar
#
#Based on : Shimazaki H. and Shinomoto S., A method for selecting the bin size of a time histogram Neural Computation (2007)
#	   Vol. 19(6), 1503-1527
#
#Data     : The duration for eruptions of the Old Faithful geyser in Yellowstone National Park (in minutes)
#	   or normal distribuition.
#	   given at http://176.32.89.45/~hideaki/res/histogram.html
#
#Comments : Implements a faster version than using hist from matplotlib and histogram from numpy libraries
#           Also implements the shifts for the bin edges
#
########################################################################################################################


import numpy as np
from numpy.random import normal
from matplotlib import rcParams
from numpy import array, arange, sum, mean, var, size, zeros
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure,  plot, xlabel, ylabel, title, savefig


def bin_width_optimizer_1d(data):
	data_max = max(data) #lower end of data
	data_min = min(data) #upper end of data
	n_min = 2   #Minimum number of bins Ideal value = 2
	n_max = 200  #Maximum number of bins  Ideal value =200
	n_shift = 30     #number of shifts Ideal value = 30
	N = np.array(range(n_min, n_max))
	D = float(data_max-data_min) / N    #Bin width vector
	Cs = np.zeros((len(D), n_shift)) #Cost function vector
	#Computation of the cost function
	for i in range(np.size(N)):
		shift = np.linspace(0,D[i],n_shift)
		for j in range(n_shift):
			edges = np.linspace(data_min+shift[j]-D[i]/2,data_max+shift[j]-D[i]/2,N[i]+1) # shift the Bin edges
			binindex = np.digitize(data,edges) #Find binindex of each data point
			ki=np.bincount(binindex)[1:N[i]+1] #Find number of points in each bin
			k = np.mean(ki) #Mean of event count
			v = sum((ki-k)**2)/N[i] #Variance of event count
			Cs[i,j]+= (2*k-v)/((D[i])**2) #The cost Function
	C=Cs.mean(1)

	#Optimal Bin Size Selection
	loc = np.argwhere(Cs==Cs.min())[0]
	cmin = C.min()
	idx  = np.where(C==cmin)
	idx = idx[0][0]
	optD = D[idx]
	print ('Optimal Bin Number :', N[idx])
	print ('Optimal Bin Width :', optD)

	if plot:
		#Plot
		edges = np.linspace(data_min+shift[loc[1]]-D[idx]/2,data_max+shift[loc[1]]-D[idx]/2,N[idx]+1)
		rcParams.update({'figure.autolayout': True})
		fig = figure()
		ax = fig.add_subplot(111)
		ax.hist(data, edges)
		title(u"Histogram")
		ylabel(u"Frequency")
		xlabel(u"Value")
		plt.draw()
		# savefig('Hist.png')
		fig = figure()
		plot(N,C, '.b', N[idx],cmin, '*r')
		xlabel('Number of bins')
		ylabel('Cobj')
		# savefig('Fobj.png')
		plt.show()

	return N[idx], optD

def bin_width_optimizer_2d(x, y, plot=False):

	x_max = max(x)
	x_min = min(x)

	y_max = max(y)
	y_min = min(y)

	Nx_MIN = 1  # Minimum number of bins in x (integer)
	Nx_MAX = 100  # Maximum number of bins in x (integer)

	Ny_MIN = 1  # Minimum number of bins in y (integer)
	Ny_MAX = 100  # Maximum number of bins in y (integer)

	Nx = arange(Nx_MIN, Nx_MAX)  # #of Bins
	Ny = arange(Ny_MIN, Ny_MAX)  # #of Bins

	Dx = (x_max - x_min) / Nx  # Bin size vector
	Dy = (y_max - y_min) / Ny  # Bin size vector

	Dxy = []
	for i in Dx:  # Bin size vector
		a = []
		for j in Dy:  # Bin size vector
			a.append((i, j))
		Dxy.append(a)
	Dxy = array(Dxy, dtype=[('x', float), ('y', float)])  # matrix of bin size vector

	Cxy = zeros(np.shape(Dxy))

	Cxy__Dxy_plot = []  # save data to plot in scatterplot x,y,z

	# Computation of the cost function to x and y
	for i in range(size(Nx)):
		for j in range(size(Ny)):
			ki = np.histogram2d(x, y, bins=(Nx[i], Ny[j]))
			ki = ki[
				0]  # The mean and the variance are simply computed from the event counts in all the bins of the 2-dimensional histogram.
			k = mean(ki)  # Mean of event count
			v = var(ki)  # Variance of event count
			Cxy[i, j] = (2 * k - v) / ((Dxy[i, j][0] * Dxy[i, j][1]) ** 2)  # The cost Function

			# (Cxy      , Dx          ,  Dy)
			Cxy__Dxy_plot.append((Cxy[i, j], Dxy[i, j][0], Dxy[i, j][1]))  # Save result of cost function to scatterplot

	Cxy__Dxy_plot = np.array(Cxy__Dxy_plot, dtype=[('Cxy', float), ('Dx', float),
												   ('Dy', float)])  # Save result of cost function to scatterplot

	# Optimal Bin Size Selection

	# combination of i and j that produces the minimum cost function
	idx_min_Cxy = np.where(Cxy == np.min(Cxy))  # get the index of the min Cxy

	Cxymin = Cxy[idx_min_Cxy[0][0], idx_min_Cxy[1][0]]  # value of the min Cxy

	print(sum(Cxy == Cxymin)) # check if there is only one min value

	optDxy = Dxy[
		idx_min_Cxy[0][0], idx_min_Cxy[1][0]]  # get the bins size pairs that produces the minimum cost function

	optDx = optDxy[0]
	optDy = optDxy[1]

	idx_Nx = idx_min_Cxy[0][0]  # get the index in x that produces the minimum cost function
	idx_Ny = idx_min_Cxy[1][0]  # get the index in y that produces the minimum cost function

	print('#', Cxymin, Nx[idx_Nx], optDx)

	print('#', Cxymin, Ny[idx_Ny], optDy)

	if plot:
		# PLOTS

		# plot histogram2d
		fig = plt.figure()
		H, xedges, yedges = np.histogram2d(x, y, bins=[Nx[idx_Nx], Ny[idx_Ny]])
		Hmasked = np.ma.masked_where(H == 0, H)
		plt.imshow(Hmasked.T, extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], interpolation='nearest',
				   origin='lower', aspect='auto', cmap=plt.cm.Spectral)
		plt.ylabel("y")
		plt.xlabel("x")
		plt.colorbar().set_label('z')
		plt.show()

		# plot scatterplot3d to Dx,Dy and Cxy
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		x = Cxy__Dxy_plot['Dx']
		y = Cxy__Dxy_plot['Dy']
		z = Cxy__Dxy_plot['Cxy']
		ax.scatter(x, y, z, c=z, marker='o')

		ax.set_xlabel('Dx')
		ax.set_ylabel('Dy')
		ax.set_zlabel('Cxy')
		plt.draw()

		ax.scatter([optDx], [optDy], [Cxymin], marker='v', s=150, c="red")
		ax.text(optDx, optDy, Cxymin, "Cxy min", color='red')
		plt.draw()
		plt.show()

	return Nx[idx_Nx], Ny[idx_Ny]


if __name__ == "__main__":
	data = normal(0, 1, 100000)
	bin_width_optimizer_1d(data)

	x = normal(0, 100, 10000)  # Generate n pseudo-random numbers whit(mu,sigma,n)
	y = normal(0, 100, 10000)  # Generate n pseudo-random numbers whit(mu,sigma,n)
	bin_width_optimizer_2d(x, y)