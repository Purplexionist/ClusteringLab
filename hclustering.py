import numpy as np
import pandas as pd
import sys
import read_file as rf
from lxml import etree as ET

class Leaf:
	def __init__(self, height, data):
		self.height = height
		self.data = data

class Node:
	def __init__(self, height):
		self.height = height
		self.l1 = None
		self.l2 = None
		self.n1 = None
		self.n2 = None

class Tree:
	def __init__(self, height):
		self.height = height
		self.l1 = None
		self.l2 = None
		self.n1 = None
		self.n2 = None

#uses manhattan distance
def calcDistanceManhattan(first, second):
	tot = 0
	for i in range(len(first)):
		tot += abs(float(first[i]) - float(second[i]))
	return tot

def recurseTree(curNode, myXML):
	if(curNode.l1 != None):
		leaf = ET.Element("leaf")
		leaf.set("height", "0")
		leaf.set("data", str(curNode.l1.data)[1:-1]) 
		myXML.append(leaf)
	else:
		node = ET.Element("node")
		node.set("height", "{:.4f}".format(curNode.n1.height))
		myXML.append(node)
		recurseTree(curNode.n1, node)
	if(curNode.l2 != None):
		leaf = ET.Element("leaf")
		leaf.set("height", "0")
		leaf.set("data", str(curNode.l2.data)[1:-1]) 
		myXML.append(leaf)
	else:
		node = ET.Element("node")
		node.set("height", "{:.4f}".format(curNode.n2.height))
		myXML.append(node)
		recurseTree(curNode.n2, node)
	
my_df = rf.read_csv()
#create a dictionary to remember data for points
numToPoint = {}
for i in range(0, len(my_df)):
	curRow = my_df.loc[i]
	curList = []
	print(curRow)
	for j in range(len(curRow)):
		if(curRow.iloc[j] != ' '):
			curList.append(curRow.iloc[j])
	numToPoint[i] = curList
listNums = list(range(len(my_df)))
distanceMatrix = pd.DataFrame(0.0, index=np.arange(len(my_df)), columns = listNums)
minDist = 0
minI = -1
minJ = -1
firstDist = 1
edited = {}
finTree = Tree(-1)

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
totalLen = len(listNums)
for t in range(0, totalLen - 1):
	print(distanceMatrix)
	biggerIndex = max(minI, minJ)
	smallerIndex = min(minI, minJ)
	savedRow = distanceMatrix.loc[biggerIndex]
	savedCol = distanceMatrix.loc[:][biggerIndex]
	listNums.remove(biggerIndex)

	#used for end dendogram
	if(len(listNums) > 1):
		tempNode = Node(minDist)
		if smallerIndex in edited:
			tempNode.n1 = edited[smallerIndex]
		else:
			tempL1 = Leaf(0, numToPoint[smallerIndex])
			tempNode.l1 = tempL1
		if biggerIndex in edited:
			tempNode.n2 = edited[biggerIndex]
		else:
			tempL2 = Leaf(0, numToPoint[biggerIndex])
			tempNode.l2 = tempL2
		edited[smallerIndex] = tempNode
	else:
		finTree.height = minDist
		if smallerIndex in edited:
			finTree.n1 = edited[smallerIndex]
		else:
			tempL1 = Leaf(0, numToPoint[smallerIndex])
			finTree.l1 = tempL1
		if biggerIndex in edited:
			finTree.n2 = edited[biggerIndex]
		else:
			tempL2 = Leaf(0, numToPoint[biggerIndex])
			finTree.l2 = tempL2

	
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

#iterate through my tree and make a csv file
root = ET.Element("tree")
root.set("height", str(finTree.height))
if(finTree.l1 != None):
	leaf1 = ET.Element("leaf")
	leaf1.set("height", "0")
	leaf1.set("data", str(finTree.l1.data)[1:-1])
	root.append(leaf1)
else:
	node = ET.Element("node")
	node.set("height", "{:.4f}".format(finTree.n1.height))
	root.append(node)
	recurseTree(finTree.n1, node)
if(finTree.l2 != None):
	leaf2 = ET.Element("leaf")
	leaf2.set("height", "0")
	leaf2.set("data", str(finTree.l2.data)[1:-1])
	root.append(leaf2)
else:
	node = ET.Element("node")
	node.set("height", "{:.4f}".format(finTree.n2.height))
	root.append(node)
	recurseTree(finTree.n2, node)
blah = ET.tostring(root, pretty_print = True).decode()
print(blah)