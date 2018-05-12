import numpy as np
import pandas as pd
import sys
import read_file as rf
from lxml import etree as ET
import time

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

def difFast(listNums, tes2d):
	minDist = 9999999999
	ans = 0
	minIN = -1
	minJN = -1
	for i in range(0, len(listNums) - 1):
		for j in range(i + 1, len(listNums)):
			ans = tes2d[i][j]
			if(ans < minDist):
				minIN = i
				minJN = j
				minDist = ans
	return minIN, minJN, minDist


def recurseTree(curNode, myXML, existNode, nodeList, k):
	if(curNode.l1 != None):
		leaf = ET.Element("leaf")
		leaf.set("height", "0")
		leaf.set("data", str(curNode.l1.data)[1:-1]) 
		myXML.append(leaf)
		if(existNode != None):
			existNode.append(str(curNode.l1.data)[1:-1])
	else:
		node = ET.Element("node")
		node.set("height", "{:.4f}".format(curNode.n1.height))
		myXML.append(node)
		if(existNode != None):
			recurseTree(curNode.n1, node, existNode, nodeList, k)
		elif(curNode.n1.height < k):
			innerList = []
			nodeList.append(innerList)
			recurseTree(curNode.n1, node, innerList, nodeList, k)
		else:
			recurseTree(curNode.n1, node, None, nodeList, k)
	if(curNode.l2 != None):
		leaf = ET.Element("leaf")
		leaf.set("height", "0")
		leaf.set("data", str(curNode.l2.data)[1:-1]) 
		myXML.append(leaf)
		if(existNode != None):
			existNode.append(str(curNode.l2.data)[1:-1])
	else:
		node = ET.Element("node")
		node.set("height", "{:.4f}".format(curNode.n2.height))
		myXML.append(node)
		if(existNode != None):
			recurseTree(curNode.n2, node, existNode, nodeList, k)
		elif(curNode.n2.height < k):
			innerList = []
			nodeList.append(innerList)
			recurseTree(curNode.n2, node, innerList, nodeList, k)
		else:
			recurseTree(curNode.n2, node, None, nodeList, k)

k = -1
if(len(sys.argv) > 2):
	k = float(sys.argv[2])
if(len(sys.argv) == 1 or len(sys.argv) > 3):
	print("Usage: py hclustering.py <dataset.csv> [thresh]")
	exit()
my_df = rf.read_csv()
#create a dictionary to remember data for points
numToPoint = {}
for i in range(0, len(my_df)):
	curRow = my_df.loc[i]
	curList = []
	for j in range(len(curRow)):
		if(curRow.iloc[j] != ' '):
			curList.append(curRow.iloc[j])
	numToPoint[i] = curList
listNums = list(range(len(my_df)))
minDist = 0
minI = -1
minJ = -1
firstDist = 1
edited = {}
finTree = Tree(-1)
tes2d = np.zeros((len(my_df), len(my_df)))

#initialize distance matrix and calculate minimum distance
for i in range(len(my_df) - 1):
	for j in range(i + 1, len(my_df)):
		#can try different distance measures
		thisAns = calcDistanceManhattan(numToPoint[i], numToPoint[j])
		tes2d[i][j] = thisAns
		if(firstDist):
			minDist = thisAns
			minI = i
			minJ = j
			firstDist = 0
		if(thisAns < minDist):
			minDist = thisAns
			minI = i
			minJ = j

#combine the clusters
totalLen = len(listNums)
for t in range(0, totalLen - 1):
	bigger = max(minI, minJ)
	smaller = min(minI, minJ)
	biggerIndex = listNums[bigger]
	smallerIndex = listNums[smaller]
	del listNums[bigger]

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
	biggerIndex = bigger
	smallerIndex = smaller
	i = 0
	while i != smallerIndex:
		curMax = max(tes2d[i][smallerIndex], tes2d[i][biggerIndex])
		tes2d[i][smallerIndex] = curMax
		i += 1
	i += 1 
	while i < len(listNums):
		num1 = tes2d[smallerIndex][i]
		num2 = -1
		if biggerIndex > i:
			num2 = tes2d[i][biggerIndex]
		else:
			num2 = tes2d[biggerIndex][i]
		curMax = max(num1, num2)
		tes2d[smallerIndex][i] = curMax
		i += 1

	#remove old rows and columns from matrix
	tes2d = np.delete(tes2d, biggerIndex, 0)
	tes2d = np.delete(tes2d, biggerIndex, 1)

	#calculate new minimum distance
	if(len(listNums) > 1):
		minI, minJ, minDist = difFast(listNums, tes2d)

#iterate through my tree and make a csv file

nodeList = []
nodeExist = 0
root = ET.Element("tree")
root.set("height", str(finTree.height))
if(finTree.height < k):
	innerList = []
	nodeList.append(innerList)
	nodeExist = 1
if(finTree.l1 != None):
	leaf1 = ET.Element("leaf")
	leaf1.set("height", "0")
	leaf1.set("data", str(finTree.l1.data)[1:-1])
	root.append(leaf1)
	if(nodeExist):
		nodeList[0].append(str(finTree.l1.data)[1:-1])
else:
	node = ET.Element("node")
	node.set("height", "{:.4f}".format(finTree.n1.height))
	root.append(node)
	if(nodeExist):
		recurseTree(finTree.n1, node, nodeList[0], nodeList, k)
	elif(finTree.n1.height < k):
		newInner = []
		nodeList.append(newInner)
		recurseTree(finTree.n1, node, newInner, nodeList, k)
	else:
		recurseTree(finTree.n1, node, None, nodeList, k)
if(finTree.l2 != None):
	leaf2 = ET.Element("leaf")
	leaf2.set("height", "0")
	leaf2.set("data", str(finTree.l2.data)[1:-1])
	root.append(leaf2)
	if(nodeExist):
		nodeList[0].append(str(finTree.l2.data)[1:-1])
else:
	node = ET.Element("node")
	node.set("height", "{:.4f}".format(finTree.n2.height))
	root.append(node)
	if(nodeExist):
		recurseTree(finTree.n2, node, nodeList[0], nodeList, k)
	elif(finTree.n2.height < k):
		newInner = []
		nodeList.append(newInner)
		recurseTree(finTree.n2, node, newInner, nodeList, k)
	else:
		recurseTree(finTree.n2, node, None, nodeList, k)
answerString = ET.tostring(root, pretty_print = True).decode()
f = open("answerXML.xml", "w")
f.write(answerString)
f.close()
print(nodeList)