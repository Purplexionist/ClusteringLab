import numpy as np
import sys

def main():

    if len(sys.argv) != 3:
        print('Usage: python k-means.py <inputFile.csv> <K>')
        sys.exit(1)

    csvPath = sys.argv[1]
    k = int(sys.argv[2])

    with open(csvPath, "r") as file:
        restrictions = []
        for i,x in enumerate(file.readline().split(",")):
            if x == '1':
                restrictions.append(i)

    data = np.genfromtxt(csvPath, delimiter=',', usecols=restrictions)[1:]

    clusters = cluster(data, k)

    for i,c in enumerate(clusters):
        print('Cluster', i+1, ':')
        for x in c:
            print(x, end=', ')
        print('\n')

def cluster(data, k):
    m = selectInitialCentroid(data,k)
    prevAssignments = [-1] * len(data)

    changeMade = True
    while changeMade:
        sums = [np.zeros(len(data[0])) for i in range(k)]
        counts = np.zeros(k)
        clusters = [[] for i in range(k)]
        curAssignments = [-1] * len(data)
        changeMade = False

        for i, x in enumerate(data):
            # get cluster to place point in
            curAssignments[i] = findMinDistance(x, m)
            # if it is different than before mark change
            if curAssignments[i] != prevAssignments[i]:
                changeMade = True

            clusters[curAssignments[i]].append(x)
            sums[curAssignments[i]] += x
            counts[curAssignments[i]] += 1

        for i in range(k):
            # if cluster has no points in it then recompute centroid
            if (counts[i] == 0): continue

            m[i] = sums[i]/counts[i]

        prevAssignments = curAssignments[:]

    return clusters

def selectInitialCentroid(data, k):
    centroids = []
    globalCentroid = centroid(data)

    centroids.append(findMaxDistance(data, [globalCentroid]))

    for i in range(k-1):
        centroids.append(findMaxDistance(data, centroids))

    return centroids

def findMaxDistance(data, points):
    maxDist = 0
    maxPoint = None
    for i in range(len(data)):
        dist = 0
        for c in points:
            dist += distance(data[i], c)
        if dist > maxDist:
            maxDist = dist
            maxPoint = data[i]
    return maxPoint

def findMinDistance(point, centroids):
    minDist = float("inf")
    minIndex = None

    for i in range(len(centroids)):
        dist = distance(point, centroids[i])
        if dist < minDist:
            minIndex = i
            minDist = dist

    return minIndex

def distance(x, y):
    return eucledian(x, y)

def eucledian(x, y):
    sum = 0
    for i in range(len(x)):
        sum += np.power(x[i] - y[i], 2)
    return np.sqrt(sum)

def centroid(data):
    sums = [0] * len(data[0])
    for i in range(len(data)):
        for j in range(len(data[i])):
            sums[j] += data[i,j]

    return np.array([s/float(len(data)) for s in sums])


def getDistances(x, m):

    return []


if __name__ == '__main__':
    main()