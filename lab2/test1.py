
import networkx as nx
import matplotlib.pyplot as plt
from main import generatePacketFlowMatrix, addingCapacity,calculateMediumPackageDelay, networkReliability, test1

G = nx.Graph()
nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
edges = [(1, 14), (1, 19), (1, 16), (1, 4), (1, 17), (1, 9), (1, 20), (2, 16), (2, 10), (2, 12), (3, 19), (4, 18),
         (4, 6), (4, 5), (5, 14), (7, 18), (7, 8), (7, 16), (9, 11), (11, 17), (12, 19), (13, 14), (13, 15),
         (14, 15), (14, 16), (14, 18), (16, 19), (19, 20)]
G.add_nodes_from(nodes)
G.add_edges_from(edges)

N = [[0, 8, 4, 9, 3, 3, 4, 6, 5, 5, 6, 5, 4, 6, 3, 1, 4, 3, 7, 3],
     [5, 0, 1, 2, 3, 6, 3, 4, 3, 7, 3, 4, 4, 9, 2, 9, 9, 8, 7, 1],
     [1, 4, 0, 8, 5, 9, 7, 4, 7, 3, 8, 6, 3, 7, 5, 1, 9, 1, 7, 2],
     [2, 2, 3, 0, 9, 8, 6, 7, 5, 5, 5, 6, 1, 1, 1, 8, 8, 5, 5, 9],
     [9, 4, 9, 9, 0, 9, 2, 3, 3, 2, 9, 9, 9, 5, 5, 9, 8, 9, 7, 8],
     [8, 7, 8, 1, 5, 0, 5, 6, 3, 6, 3, 8, 6, 2, 5, 9, 8, 4, 2, 5],
     [5, 1, 3, 1, 4, 7, 0, 1, 4, 9, 8, 9, 8, 6, 4, 8, 5, 2, 6, 4],
     [9, 3, 1, 2, 7, 8, 2, 0, 8, 4, 9, 3, 8, 4, 6, 4, 7, 7, 6, 7],
     [4, 8, 9, 8, 7, 5, 5, 6, 0, 1, 7, 1, 6, 8, 9, 6, 6, 4, 9, 7],
     [5, 3, 3, 8, 9, 7, 4, 6, 1, 0, 5, 6, 9, 9, 4, 7, 5, 1, 6, 6],
     [9, 4, 7, 5, 3, 7, 3, 3, 3, 9, 0, 6, 5, 3, 4, 8, 8, 7, 6, 6],
     [3, 9, 8, 1, 6, 5, 6, 1, 1, 5, 9, 0, 4, 9, 5, 3, 7, 1, 3, 1],
     [6, 8, 5, 3, 5, 6, 6, 3, 9, 3, 3, 1, 0, 3, 7, 2, 8, 4, 4, 5],
     [2, 8, 9, 1, 2, 5, 1, 2, 7, 6, 2, 9, 2, 0, 6, 4, 6, 8, 7, 9],
     [4, 6, 7, 1, 5, 2, 4, 5, 8, 4, 4, 8, 5, 6, 0, 3, 7, 9, 9, 5],
     [3, 4, 8, 3, 1, 1, 9, 8, 1, 5, 8, 2, 6, 7, 3, 0, 3, 5, 8, 1],
     [5, 4, 5, 4, 7, 6, 5, 4, 2, 2, 5, 1, 2, 9, 9, 3, 0, 9, 2, 2],
     [3, 1, 8, 9, 4, 6, 5, 2, 4, 5, 5, 2, 7, 8, 5, 3, 1, 0, 2, 2],
     [6, 9, 2, 9, 1, 1, 2, 1, 5, 2, 5, 9, 9, 1, 6, 8, 5, 9, 0, 4],
     [7, 2, 1, 9, 4, 1, 1, 4, 2, 3, 4, 2, 6, 2, 8, 5, 9, 2, 2, 0]
     ]

mediumPackageSize = 12000
reliabilityOfEdge = 0.98  # p
packageDelayMax = 0.1  # Tmax dopuszczalne opóźnienie pakietu

packetFlowMatrix = generatePacketFlowMatrix(G, N)
capacity = addingCapacity(G, packetFlowMatrix, 2, mediumPackageSize)
packageDelay = calculateMediumPackageDelay(G, N, packetFlowMatrix, capacity, mediumPackageSize)

y, x = test1(G,N,capacity,mediumPackageSize,packageDelayMax,reliabilityOfEdge)
plt.plot(x,y)
plt.xlabel('new packages')
plt.ylabel('reliability of the graph')
plt.show()
