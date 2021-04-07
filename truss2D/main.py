import numpy as np
from NodesFile import TrussNode2D, nodes
from ElementsFile import TrussElement2D, elements
from Helpers import SetDegreeOfFreedoms
import sys

# node input
node1x = float(sys.argv[1])
node1y = float(sys.argv[2])
node1rx = float(sys.argv[3])
node1ry = float(sys.argv[4])
node2x = float(sys.argv[5])
node2y = float(sys.argv[6])
node2rx = float(sys.argv[7])
node2ry = float(sys.argv[8])
node3x = float(sys.argv[9])
node3y = float(sys.argv[10])
node3rx = float(sys.argv[11])
node3ry = float(sys.argv[12])
node4x = float(sys.argv[13])
node4y = float(sys.argv[14])
node4rx = float(sys.argv[15])
node4ry = float(sys.argv[16])
node5x = float(sys.argv[17])
node5y = float(sys.argv[18])
node5rx = float(sys.argv[19])
node5ry = float(sys.argv[20])


TrussNode2D(id=1, X=node1x, Y=node1y)
TrussNode2D(id=2, X=node2x, Y=node2y)
TrussNode2D(id=3, X=node3x, Y=node3y)
TrussNode2D(id=4, X=node4x, Y=node4y)
TrussNode2D(id=5, X=node5x, Y=node5y)

#nodes[1].rest = [1, 1]
#nodes[3].rest = [0, 1]

# nodes restrictions input
nodes[1].rest[0] = node1rx
nodes[1].rest[1] = node1ry
nodes[2].rest[0] = node2rx
nodes[2].rest[1] = node2ry
nodes[3].rest[0] = node3rx
nodes[3].rest[1] = node3ry
nodes[4].rest[0] = node4rx
nodes[4].rest[1] = node4ry
nodes[5].rest[0] = node5rx
nodes[5].rest[1] = node5ry

# Applied forces
nodes[4].force = [0, -20]
nodes[5].force = [10, 0]

N, M = SetDegreeOfFreedoms(nodes)

print("N:", N)
print("M:", M)

for id, node in nodes.items():
    print("id:", id, "dof:", node.dof)

# Element input
Elm1ni = float(sys.argv[21])
Elm1nj = float(sys.argv[22])
Elm1EA = float(sys.argv[23])
Elm2ni = float(sys.argv[24])
Elm2nj = float(sys.argv[25])
Elm2EA = float(sys.argv[26])
Elm3ni = float(sys.argv[27])
Elm3nj = float(sys.argv[28])
Elm3EA = float(sys.argv[29])
Elm4ni = float(sys.argv[30])
Elm4nj = float(sys.argv[31])
Elm4EA = float(sys.argv[32])
Elm5ni = float(sys.argv[33])
Elm5nj = float(sys.argv[34])
Elm5EA = float(sys.argv[35])
Elm6ni = float(sys.argv[36])
Elm6nj = float(sys.argv[37])
Elm6EA = float(sys.argv[38])
Elm7ni = float(sys.argv[39])
Elm7nj = float(sys.argv[40])
Elm7EA = float(sys.argv[41])

'''
Elm1ni, Elm1nj, Elm1EA, Elm1Lx, Elm1Ly,
Elm2ni, Elm2nj, Elm2EA, Elm2Lx, Elm2Ly,
Elm3ni, Elm3nj, Elm3EA, Elm3Lx, Elm3Ly,
Elm4ni, Elm4nj, Elm4EA, Elm4Lx, Elm4Ly,
Elm5ni, Elm5nj, Elm5EA, Elm5Lx, Elm5Ly,
Elm6ni, Elm6nj, Elm6EA, Elm6Lx, Elm6Ly,
Elm7ni, Elm7nj, Elm7EA, Elm7Lx, Elm7Ly
'''

TrussElement2D(id=1, ni=Elm1ni, nj=Elm1nj, EA=Elm1EA)
TrussElement2D(id=2, ni=Elm2ni, nj=Elm2nj, EA=Elm2EA)
TrussElement2D(id=3, ni=Elm3ni, nj=Elm3nj, EA=Elm3EA)
TrussElement2D(id=4, ni=Elm4ni, nj=Elm4nj, EA=Elm4EA)
TrussElement2D(id=5, ni=Elm5ni, nj=Elm5nj, EA=Elm5EA)
TrussElement2D(id=6, ni=Elm6ni, nj=Elm6nj, EA=Elm6EA)
TrussElement2D(id=7, ni=Elm7ni, nj=Elm7nj, EA=Elm7EA)

for id, elm in elements.items():
    print("id:", id, "Lx:", elm.Lx, "Ly:", elm.Ly,
          "L:", elm.L)  # TrussElement2D.Lx(elm)


for id, elm in elements.items():
    print("Stiffness Matrix of element:", id)
    print(elm.K)

for id, elm in elements.items():
    print("Code vector of element:", id)
    print(elm.code)


Ks = np.zeros((M, M))
Ps = np.zeros((M, 1))

for id, elm in elements.items():
    Ke = elm.K
    cv = elm.code
    for i in range(4):  # i-> 0, 1, 2, 3
        for j in range(4):  # j-> 0, 1, 2, 3
            cv_i = cv[i]
            cv_j = cv[j]
            Ks[cv_i, cv_j] += Ks[cv_i, cv_j] + Ke[i, j]

print("System Stiffness Matrix:")
print(Ks)

for id, node in nodes.items():
    Ps[node.dof[0], 0] = node.force[0]  # Px
    Ps[node.dof[1], 0] = node.force[1]  # Py

print("System Ps")
print(Ps)

K11 = Ks[0:N, 0:N]
P1 = Ps[0:N, 0]

print("K11")
print(K11)

print("P1")
print(P1)

u1 = np.linalg.inv(K11) @ P1

print("u1")
print(u1)

us = u1.tolist() + [0] * (M-N)

print(us)

RHS = Ks @ us

print("RHS")
print(RHS)
