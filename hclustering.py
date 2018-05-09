import numpy as np
import pandas as pd
import sys
import read_file as rf

#uses manhattan distance
def calcDistanceManhattan(first, second):
	tot = 0
	for i in range(len(first)):
		tot += abs(first[i] - second[i])
	return tot
	
my_df = rf.read_csv()

#create a dictionary to remember data for points
numToPoint = {}
for i in range(0, len(my_df)):
	curRow = my_df.loc[i]
	curList = []
	for j in range(len(curRow)):
		curList.append(curRow.loc[j])
	numToPoint[i] = curList

listNums = list(range(len(my_df)))
distanceMatrix = pd.DataFrame(0, index=np.arange(len(my_df)), columns = listNums)
minDist = 0
minI = -1
minJ = -1
firstDist = 1

#initialize distance matrix and calculate minimum distance
for i in range(len(my_df) - 1):
	for j in range(i + 1, len(my_df)):
		#can try different distance measures
		distanceMatrix.loc[i][j] = calcDistanceManhattan(numToPoint[i], numToPoint[j])
		if(firstDist):
			minDist = distanceMatrix.loc[i][j]
			minI = i
			minJ = j
		if(distanceMatrix.loc[i][j] < minDist):
			minDist = distanceMatrix.loc[i][j]
			minI = i
			minJ = j


print(distanceMatrix)
#combine the clusters
for t in range(0, 1):
	biggerIndex = max(minI, minJ)
	smallerIndex = min(minI, minJ)
	savedRow = distanceMatrix.loc[biggerIndex]
	saveCol = distanceMatrix.loc[:][biggerIndex]
	listNums.remove(biggerIndex)
	distanceMatrix = distanceMatrix.loc[listNums, listNums]
	print(distanceMatrix)


class Leaf:
	def __init__(self, height, data):
		self.height = height
		self.data = data

class Node:
	def __init__(self, height):
		self.height = height

class Tree:
	def __init__(self, height):
		self.height = height

