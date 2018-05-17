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
#python dbscan 4clusters.csv 5.2 3
# see the issue with DBScan on 4clusters by incrementing to 5.4

import sys
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

close_points = {}
cluster = {}
taxi = False

def distance(d1,d2):
	if taxi:
		tot = 0
		for i in range(len(d1)):
			tot += abs(float(d2[i]) - float(d1[i]))
		#print(d1,d2,tot)
		return tot
		
	return (((d2-d1)**2).sum())**0.5

def find_close_points(df, d, epsilon):
	close_points = []
	for i in df.index:
		d_prime = df.loc[i,:]
		dist = distance(d,d_prime)
		#print(d,d_prime,dist)
		if dist <= epsilon:
			close_points.append(i)
	return close_points

def density_connected(df,ind,core,currentCluster):
	N_epsilon_point = close_points[ind]
	for d in N_epsilon_point:
		
		#if point has already been through density_connected and assigned a cluster, skip it or else
		# we recurse way too much
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
	for i in df.index:
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
		print("\tCluster " + str(i+1) +": ")
		print("\t\tNumber of points: " + str(len(clust)))
		centroid_str = "\t\tCentroid: ("
		for j in range(len(centroid)):
			centroid_str += str(centroid.iloc[j].round(2)) + ","
		print(centroid_str[0:-1] + ")")
		curMax = -1
		curMin = 999999
		curAvg = 0
		sse = 0
		for point in clust:
			offSet = distance(df.loc[point,:], centroid)
			sse += offSet**2
			curAvg += offSet
			if(offSet > curMax):
				curMax = offSet
			if(offSet < curMin):
				curMin = offSet
		curAvg /= len(clust)
		print("\t\t\tMax Distance from Centroid:",curMax)
		print("\t\t\tMin Distance from Centroid:",curMin)
		print("\t\t\tAvg Distance from Centroid:",curAvg)
		print("\t\t\tSSE:",sse)
		print("Points:")
		print(str(df_clust))
	print("Noise:")
	print(df.loc[noise,:])
	print("\tNumber of outliers:",len(noise))
	print("\tPercentage of dataset:",float(len(noise))/float(len(df)))
	all_points = list(df.index)
	border = [item for item in all_points if item not in noise and item not in core]
	print("Border:")
	print(df.loc[border,:])

	clusterList.append(noise)
	
	###################################################Visuals############################################

	clusterNum = 0
	if(len(clusterList) > 0):
		colors = 100//len(clusterList)
		curColor = 1
		xList = []
		yList = []
		zList = []
		cList = []
		for a in clusterList:
			
			for blah in a:
				point = df.loc[blah,:]
				if(point.size <= 3):
					xList.append(point.iloc[0])
					yList.append(point.iloc[1])
					cList.append(curColor)
					if(len(point) == 3):
						zList.append(point[2])
				elif(point.size == 3):
					xList.append(point.iloc[0])
					yList.append(point.iloc[1])
					cList.append(curColor)
				else:
					break
					
			curColor += colors
	for blah in noise:
		point = df.loc[blah,:]
		if(point.size <= 3):
			xList.append(point.iloc[0])
			yList.append(point.iloc[1])
			cList.append(curColor)
			if(len(point) == 3):
				zList.append(point[2])
			else:
				xList.append(point.iloc[0])
				yList.append(point.iloc[1])
				cList.append(curColor)


	ddd = False
	dd = True
	if len(df.loc[clusterList[0][0],:]) == 3:
		ddd = True
	if len(df.loc[clusterList[0][0],:]) == 2:
		dd = True

	if(len(clusterList) > 0 and dd):
		plt.scatter(xList, yList, c = cList)
		plt.show()
	elif(len(clusterList) > 0 and ddd):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(xList, yList, zList, c = cList)
		ax.set_xlabel('X Label')
		ax.set_ylabel('Y Label')
		ax.set_zlabel('Z Label')
		plt.show()
	else:
		print("Have a nice life")


		
	
	

def main():
	file_path = sys.argv[1]
	try:
		epsilon = float(sys.argv[2])
	except:
		split = sys.argv[2].split("/")
		epsilon = float(split[0])/float(split[1])
	numPoints = int(sys.argv[3])

	try:
		if sys.argv[4] == "1":
			taxi = True
		
	except:
		taxi = False

	binary_vector = pd.read_csv(file_path,header=None,nrows=1).values.tolist()[0]
	df = pd.read_csv(file_path,skiprows=1,header=None)

	

	if (isinstance(df.loc[0,len(df.columns)-1],str)):
		df = df.drop(len(df.columns)-1, axis = 1)
	for i in range(len(binary_vector)-1,-1,-1):
		val = binary_vector[i]
		if val == 0:
			if i == 0:
				df = df.set_index(0)
			else:
				df = df.drop(i,axis=1)
	if sys.argv[1] == "planets.csv" or sys.argv[1] == "mammal_milk.csv":
		df = (df-df.mean())/df.std()
	dbscan(df,epsilon,numPoints)




if __name__ == "__main__":
	main()
