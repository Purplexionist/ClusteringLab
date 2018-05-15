"""
#DBSCAN

Two things: Are there enough datapoints in the neighborhood? NumPoints
			Are the points sufficiently close to each other? epislon

1. Pick point x in the dataset D
2. Let D_x'_epsilon = {x in D | dist(x,x') <= epsilon}
3. if |D_x'_epsilon| >= numPoints then create a cluster

Three types of points:

	1. Core point - a point x' that satisfies the if statement in #3

	2. Boundary point - a point x where |D_x_epsilon| < NumPoints but x is in an epsilon neighborhood of a core point

	3. outlier point - x where |D_x_epsilon| < NumPoints and no core point contains x in its epsilon neighborhood

*** DBScan is very good at handling outliers and removing them from consideration***
Weakness: identifying different clusters where one is really bunched together and other is more sparse

Combination of Breadth first search (using queue data structure)

Algorithm:

Pick x in D, put x in Queue

x' <- Dequeue(Queue)
if x' is a core point
"""



#RUN WITH:
#python dbscan.py file.csv epsilon minPts

#How to get 4 clusters with a little noise:
#python dbscan 4clusters.csv 5 2
import sys
import pandas as pd

close_points = {}
cluster = {}

def distance(d1,d2):
	return (((d2-d1)**2).sum())**0.5

def find_close_points(df, d, epsilon):
	close_points = []
	for i in df.index:
		d_prime = df.loc[i,:]
		dist = distance(d,d_prime)
		if dist < epsilon:
			close_points.append(i)
	return close_points

def density_connected(df,ind,core,currentCluster):
	N_epsilon_point = close_points[ind]
	for d in N_epsilon_point:
		
		if cluster[d] != -1:
			continue
		cluster[d] = currentCluster
		if d in core:
			density_connected(df,d,core,currentCluster)
	return

def find_points_in_cluster(cluster,k):
	cluster_k = []
	for c in cluster:
		if cluster[c] == k:
			cluster_k.append(c)
	return(cluster_k)



def dbscan(df,epsilon,numPoints):
	core = []
	#find core points
	for ind in df.index:
		#This line could be a future problem
		i = ind
		d = df.loc[i,:]
		N_epsilon_d = find_close_points(df.drop(i), d, epsilon)
		close_points[i] = N_epsilon_d
		cluster[i] = -1
		if(len(N_epsilon_d) >= numPoints):
			core.append(i)

	currentCluster = 0

	for c in core:
		if cluster[c] == -1:
			currentCluster += 1
			cluster[c] = currentCluster
			density_connected(df,c,core,currentCluster)
	
	clusterList = []


	for k in range(1,currentCluster+1):
		clusterList.append(find_points_in_cluster(cluster,k))

	noise = find_points_in_cluster(cluster,-1)



	print("List of Clusters:")
	for i in range(len(clusterList)):
		clust = clusterList[i]
		df_clust = df.loc[clust,:]
		centroid = df_clust.mean()
		print("\tCluster " + str(i+1) +": " + str(clust))
		print("\t\tNumber of points: " + str(len(clust)))
		print("\t\tCentroid: (" + str(centroid[0].round(2)) + "," + str(centroid[1].round(2)) + ")")

	print("Noise:")
	print(noise)
	all_points = list(df.index)
	border = [item for item in all_points if item not in noise and item not in core]
	print("Border:")
	print(border)

		
	
	

def main():
	file_path = sys.argv[1]
	epsilon = float(sys.argv[2])
	numPoints = int(sys.argv[3])

	binary_vector = pd.read_csv(file_path,header=None,nrows=1).values.tolist()[0]
	df = pd.read_csv(file_path,skiprows=1,header=None)
	for i in range(len(binary_vector)-1,-1,-1):
		val = binary_vector[i]
		if val == 0:
			if i == 0:
				df = df.set_index(0)
			else:
				df = df.drop(i,axis=1)

	dbscan(df,epsilon,numPoints)




if __name__ == "__main__":
	main()
