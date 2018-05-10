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
edited = []

#initialize distance matrix and calculate minimum distance
for i in range(len(my_df) - 1):
	for j in range(i + 1, len(my_df)):
		#can try different distance measures
		distanceMatrix.loc[i][j] = calcDistanceManhattan(numToPoint[i], numToPoint[j])
		if(firstDist):
			minDist = distanceMatrix.loc[i][j]
			minI = i
			minJ = j
			firstDist = 0
		if(distanceMatrix.loc[i][j] < minDist):
			minDist = distanceMatrix.loc[i][j]
			minI = i
			minJ = j

#combine the clusters
print(distanceMatrix)
totalLen = len(listNums)
for t in range(0, totalLen - 1):
	print(minI, minJ)
	biggerIndex = max(minI, minJ)
	smallerIndex = min(minI, minJ)
	savedRow = distanceMatrix.loc[biggerIndex]
	savedCol = distanceMatrix.loc[:][biggerIndex]
	listNums.remove(biggerIndex)

	#used for end dendogram
	edited.append(smallerIndex)
	
	#dependent on distance formula
	#using complete link for this implementation
	i = 0
	while listNums[i] != smallerIndex:
		curMax = max(distanceMatrix.loc[listNums[i]][smallerIndex], distanceMatrix.loc[listNums[i]][biggerIndex])
		distanceMatrix.loc[listNums[i]][smallerIndex] = curMax
		i += 1
	i += 1 
	while i < len(listNums):
		num1 = distanceMatrix.loc[smallerIndex][listNums[i]]
		num2 = -1
		if biggerIndex > listNums[i]:
			num2 = distanceMatrix.loc[listNums[i]][biggerIndex]
		else:
			num2 = distanceMatrix.loc[biggerIndex][listNums[i]]
		curMax = max(num1, num2)
		distanceMatrix.loc[smallerIndex][listNums[i]] = curMax
		i += 1

	#remove old rows and columns from matrix
	distanceMatrix = distanceMatrix.loc[listNums, listNums]

	print(distanceMatrix)
	#calculate new minimum distance
	i = 0
	j = 0
	firstDist = 1
	while i < len(listNums) - 1:
		j = i + 1
		while j < len(listNums):
			if(firstDist):
				minI = listNums[i]
				minJ = listNums[j]
				minDist = distanceMatrix.loc[minI][minJ]
				firstDist = 0
			if(distanceMatrix.loc[listNums[i]][listNums[j]] < minDist):
				minI = listNums[i]
				minJ = listNums[j]
				minDist = distanceMatrix.loc[minI][minJ]
			j += 1
		i += 1



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

