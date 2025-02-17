import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics import silhouette_score




if __name__ == "__main__":
	# Assuming 'data' is your 15 million x, y, z positions
	# Example data with random values (replace this with your actual data)
	np.random.seed(42)
	data = np.random.rand(15000, 3)

	# Define a range of possible cluster numbers
	possible_k_values = range(2, 21)

	silhouette_scores = []
	for k in possible_k_values:
		kmeans = KMeans(n_clusters=k, random_state=42, n_init=1, max_iter=10)
		cluster_labels = kmeans.fit_predict(data)
		silhouette_scores.append(silhouette_score(data, cluster_labels))

	# Find the index of the maximum Silhouette Score
	optimal_k_index = np.argmax(silhouette_scores)

	# Get the optimal k
	optimal_k = possible_k_values[optimal_k_index]

	print(f"Optimal number of clusters (k): {optimal_k}")

	# Plot the Silhouette Score curve
	plt.figure(figsize=(10, 6))
	plt.plot(possible_k_values, silhouette_scores, marker='o')
	plt.xlabel('Number of Clusters (k)')
	plt.ylabel('Silhouette Score')
	plt.title('Silhouette Score for Optimal k')
	plt.show()

	# Create and fit the MiniBatchKMeans model
	kmeans = MiniBatchKMeans(n_clusters=optimal_k, batch_size=1000)
	cluster_labels = kmeans.fit_predict(data)

	# Create a 3D scatter plot
	fig = plt.figure(figsize=(10, 8))
	ax = fig.add_subplot(111, projection='3d')

	# Scatter plot each cluster with a different color
	for cluster_label in range(optimal_k):
		cluster_data = data[cluster_labels == cluster_label]
		ax.scatter(cluster_data[:, 0], cluster_data[:, 1], cluster_data[:, 2], label=f'Cluster {cluster_label}')

	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	ax.set_title('3D Clustering Visualization')
	ax.legend()
	plt.show()
