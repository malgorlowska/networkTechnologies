import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx import bidirectional_shortest_path
from copy import deepcopy


# generating good graph
def generateEdges(G):
    numberOfEdges = 0
    connectedNodes = []
    connectedNodes.append(1)
    notConnectedNodes = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    while numberOfEdges < 29:
        while len(notConnectedNodes) != 0:
            node1 = random.choice(connectedNodes)
            node2 = random.choice(notConnectedNodes)
            G.add_edge(*(node1, node2))
            numberOfEdges += 1
            notConnectedNodes.remove(node2)
            connectedNodes.append(node2)

        node1 = random.choice(connectedNodes)
        node2 = random.choice(connectedNodes)
        if node1 != node2 & G.has_edge(node1, node2) == False:
            G.add_edge(*(node1, node2))
            numberOfEdges += 1

    print(G.nodes())  # returns a list
    print(G.edges())  # returns a list
    print(numberOfEdges)
    print(nx.is_connected(G))


def generateIntensityMatrix(a, b):
    intensityMatrix = np.zeros((20, 20))
    for i in range(0, 20):
        for j in range(0, 20):
            if i != j:
                intensityMatrix[i][j] = random.randint(a, b)

    print(intensityMatrix)
    return intensityMatrix


def generatePacketFlowMatrix(G, intensityMatrix):
    packetFlowMatrix = np.zeros((20, 20))
    for i in range(0, 20):
        for j in range(0, 20):
            if i != j:
                intensity = intensityMatrix[i][j]
                path = bidirectional_shortest_path(G, i + 1, j + 1)
                # print("between ",i+1," and ", j+1)
                # print("shortest path: ",path)
                for k in range(len(path) - 1):
                    packetFlowMatrix[path[k] - 1][path[k + 1] - 1] += intensity
    # sprawdzić czy nie za duży przepływ
    # print(packetFlowMatrix)
    return packetFlowMatrix


def addingCapacity(G, packetFlowMatrix, s, m):
    flows = []
    for i in G.edges:
        node1 = i[0] - 1
        node2 = i[1] - 1
        flows.append(packetFlowMatrix[node1][node2])

    maximum = max(flows)
    capacity = maximum * s * m
    print(capacity)
    return capacity


def calculateMediumPackageDelay(G, intensityMatrix, packetFlowMatrix, capacity, mediumPackageSize):
    sumOfIntensity = 0
    sum = 0
    for i in range(0, 20):
        for j in range(0, 20):
            if i != j:
                sumOfIntensity += intensityMatrix[i][j]

    edgeNumber = 0
    for k in G.edges:
        sum += packetFlowMatrix[k[0] - 1][k[1] - 1] / (
                (capacity / mediumPackageSize) - packetFlowMatrix[k[0] - 1][k[1] - 1])
        edgeNumber += 1

    return sum / sumOfIntensity


def networkReliability(G, N, c, m, n, tMax, p):  # p zawodność łącza
    s = 0  # succes number
    for i in range(n):
        graph = deepcopy(G)
        for j in graph.edges:
            r = random.uniform(0.0, 1.0)
            if r > p:
                # print("remove ", j)
                graph.remove_edge(*j)

        if nx.is_connected(graph):
            packetFlowMatrix = generatePacketFlowMatrix(graph, N)

            flowOk = True
            for j in graph.edges:
                node1 = j[0] - 1
                node2 = j[1] - 1
                if (c / m) < packetFlowMatrix[node1][node2]:
                    print("flow i s not ok")
                    flowOk = False
                    break

            if flowOk:
                if calculateMediumPackageDelay(graph, N, packetFlowMatrix, c, m) < tMax:
                    s += 1
                else:
                    print("time is over")

            #if i % 1000 == 0:
             #   print(i)

    return s / n

def test1(G, N, c, m, tMax, p):
    iterations = 100
    step = 10
    newPackages = []
    for i in range(0,1010,10):
        newPackages.append(i)

    print("newPackages ", newPackages)

    graph = deepcopy(G)
    intensity = deepcopy(N)
    results = np.zeros(101)
    results[0] = networkReliability(graph, intensity, c, m, 1000, tMax, p)
    for j in range(99):
        print("I T E R A C J A: ", j)
        startPackage = 0
        graph = deepcopy(G)
        intensity = deepcopy(N)
        for i in range(iterations):
            findEdge = False
            while findEdge == False:
                node1 = random.randint(0, 19)
                node2 = random.randint(0, 19)
                if node1 != node2:
                    findEdge = True

            intensity[node1][node2] += step
            flow = generatePacketFlowMatrix(graph, intensity)
            results[i] += networkReliability(graph, intensity, c, m, 10, tMax, p)

    for j in range(len(results)):
        results[j] = results[j] / 100
    print(newPackages)
    print(results)
    return results, newPackages

def test2(G, N, m, tMax, p):
    step = 5*m
    capacities = []
    results = np.zeros(100)
    firstCapacity = 10*m
    for i in range(100):
        capacities.append(firstCapacity + (i*step))

    print("capacities ", capacities)

    for j in range(100):
        print("I T E R A C J A: ", j)

        for i in range(100):
            findEdge = False
            while findEdge == False:
                node1 = random.randint(0, 19)
                node2 = random.randint(0, 19)
                if node1 != node2:
                    findEdge = True

            results[i] += networkReliability(G, N, capacities[i], m, 10, tMax, p)

    for j in range(len(results)):
        results[j] = results[j] / 100
    print(capacities)
    print(results)
    return results, capacities

def test3(G, N, c, m, tMax, p):

    results = np.zeros(11)
    newEdges = []
    for i in range(11):
        newEdges.append(i)

    print("newEdges ", newEdges)

    for j in range(100):
        graph = deepcopy(G)
        print("I T E R A C J A: ", j)

        results[0] += networkReliability(graph, N, c, m, 10, tMax, p)
        for i in range(10):
            findEdge = False
            while findEdge == False:
                node1 = random.randint(0, 19)
                node2 = random.randint(0, 19)
                if node1 != node2:
                    findEdge = True
                    graph.add_edge(node1,node2)

            results[i+1] += networkReliability(graph, N, c, m, 100, tMax, p)

    for j in range(len(results)):
        results[j] = results[j] / 100
    print(newEdges)
    print(results)
    return results, newEdges

def main():
    G = nx.Graph()
    nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    edges = [(1, 14), (1, 19), (1, 16), (1, 4), (1, 17), (1, 9), (1, 20), (2, 16), (2, 10), (2, 12), (3, 19), (4, 18),
             (4, 6), (4, 5), (5, 14), (7, 18), (7, 8), (7, 16), (9, 11), (11, 17), (12, 19), (13, 14), (13, 15),
             (14, 15), (14, 16), (14, 18), (16, 19), (19, 20)]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    intensityMatrix = np.zeros((20, 20))  # N
    packetFlowMatrix = np.zeros((20, 20))  # a
    capacity = 10000000  # c przepustowość krawędzi
    reliabilityOfEdge = 0.98  # p
    mediumPackageSize = 12000  # m bity uzmiennić!!
    packageDelayMax = 1  # Tmax dopuszczalne opóźnienie pakietu

    # generateEdges()
    intensityMatrix = generateIntensityMatrix(1, 9)
    packetFlowMatrix = generatePacketFlowMatrix(G, intensityMatrix)
    capacity = addingCapacity(G, packetFlowMatrix, 2, mediumPackageSize)
    packageDelay = calculateMediumPackageDelay(G, intensityMatrix, packetFlowMatrix, capacity, mediumPackageSize)
    print("delay ", packageDelay)

    # plotting graph
    # nx.draw(G)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
    # plt.savefig(“graph.png”)

    # s = networkReliability(G, intensityMatrix, capacity, mediumPackageSize, 100000, packageDelayMax, reliabilityOfEdge)
    # print("succeses: ", s)


if __name__ == "__main__":
    main()
