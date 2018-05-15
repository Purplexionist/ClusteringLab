import numpy as np
import sys


def main():

    normalized = False
    if len(sys.argv) == 4 and "normalized" in sys.argv:
        normalized = True
    elif len(sys.argv) != 3:
        print('Usage: python k-means.py <inputFile.csv> <K> [normalized]')
        sys.exit(1)

    csvPath = sys.argv[1]
    k = int(sys.argv[2])

    with open(csvPath, "r") as file:
        restrictions = []
        for i,x in enumerate(file.readline().split(",")):
            if x.strip() == '1':
                restrictions.append(i)

    data = np.genfromtxt(csvPath, delimiter=',', usecols=restrictions)[1:]

    print('K-means Clustering of', csvPath)
    print('k =', k)
    print("Normalized =", normalized)
    print()

    if normalized:
        data = normalize(data)

    clusters, centroids = cluster(data, k)

    def printClusters(id=False, label=False):
        """Method that prints labels, id, or full row of data in each cluster"""

        # Build dictionary mapping rows to desired output
        output = {}
        with open(csvPath, "r") as file:
            for i, line in enumerate(file.readlines()[1:]):
                if label:
                    output[tuple(data[i].tolist())] = line.strip().split(',')[-1].strip()
                elif id:
                    output[tuple(data[i].tolist())] = line.strip().split(',')[0].strip()
                else:
                    output[tuple(data[i].tolist())] = [float(x) for x in line.strip().split(',')]

        for i, c in enumerate(clusters):
            print('Cluster', i + 1, ':')
            print('Center:', centroids[i])

            if len(c) == 0:
                print("Empty Cluster\n")
                continue

            minDist, maxDist, avgDist = getDistFromCenter(c, centroids[i])
            print("Max Dist. to Center:", maxDist)
            print("Min Dist. to Center:", minDist)
            print("Avg Dist. to Center:", avgDist)
            print("SSE:", sse(c, centroids[i]))
            print(len(c), "Points:")
            for x in c:
                print(output[tuple(x.tolist())], end=',')
            print('\n')

    if csvPath == "data/iris.csv":  # only file with labels
        printClusters(label=True)
    elif 0 not in restrictions:     # if first column not used assume its an id
        printClusters(id=True)
    else:                           # else print entire row
        printClusters()

def sse(cluster, center):
    sum = 0
    for x in cluster:
        # square euclidian distance to get sse
        dist = eucledian(x, center)
        sum += np.power(dist, 2)
    return round(sum, 2)

def getDistFromCenter(cluster, center):
    minDist = float("inf")
    maxDist = 0
    sum = 0
    for x in cluster:
        dist = distance(x, center)
        if dist < minDist:
            minDist = dist
        if dist > maxDist:
            maxDist = dist
        sum += dist
    return round(minDist, 2), round(maxDist, 2), round(sum/float(len(cluster)), 2)

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
            # if cluster has no points in it then don't recompute centroid
            if (counts[i] == 0): continue
            m[i] = sums[i]/counts[i]

        prevAssignments = curAssignments[:]

    return clusters, m

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

def normalize(data):
    high = 100.0
    low = 0.0

    mins = np.min(data, axis=0)
    maxs = np.max(data, axis=0)
    rng = maxs - mins

    return high - (((high - low) * (maxs - data)) / rng)

if __name__ == '__main__':
    main()