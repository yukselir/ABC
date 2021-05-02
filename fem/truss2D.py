import random
import json
import numpy as np
from NodesFile import TrussNode2D, nodes
from ElementsFile import TrussElement2D, elements
from Helpers import SetDegreeOfFreedoms
import sys

# node input
h = float(sys.argv[1])
dL = float(sys.argv[2])
N = int(sys.argv[3])

n = 1
for i in range(N+1):
    TrussNode2D(id=n, X=i*dL, Y=0)
    n += 1
for i in range(N):
    TrussNode2D(id=n, X=i*dL+0.5*dL, Y=h)
    n += 1

e = 1
for i in range(N):
    TrussElement2D(id=e, ni=i+1, nj=i+2, EA=2000)
    e += 1

for i in range(N):
    TrussElement2D(id=e, ni=i+1, nj=i+1+1+N, EA=2000)
    e += 1

for i in range(N):
    TrussElement2D(id=e, ni=i+1+1+N, nj=i+2, EA=2000)
    e += 1

for i in range(N-1):
    TrussElement2D(id=e, ni=i+1+1+N, nj=i+1+1+N+1, EA=2000)
    e += 1

nodes[1].rest = [1, 1]
nodes[N+1].rest = [0, 1]

for i in range(N-1):
    nodes[i+2].force = [0, -100]


N, M = SetDegreeOfFreedoms(nodes)

# print("N:", N)
# print("M:", M)

# for id, node in nodes.items():
#     print("id:", id, "dof:", node.dof)

# for id, elm in elements.items():
#     print("id:", id, "Lx:", elm.Lx, "Ly:", elm.Ly,
#           "L:", elm.L)  # TrussElement2D.Lx(elm)


# for id, elm in elements.items():
#     print("Stiffness Matrix of element:", id)
#     print(elm.K)

# for id, elm in elements.items():
#     print("Code vector of element:", id)
#     print(elm.code)


Ks = np.zeros((M, M))
Ps = np.zeros((M, 1))

for id, elm in elements.items():
    Ke = elm.K
    cv = elm.code
    for i in range(4):  # i-> 0, 1, 2, 3
        for j in range(4):  # j-> 0, 1, 2, 3
            cv_i = cv[i]
            cv_j = cv[j]
            Ks[cv_i, cv_j] += Ke[i, j]

#print("System Stiffness Matrix:")
# print(Ks)

for id, node in nodes.items():
    Ps[node.dof[0], 0] = node.force[0]  # Px
    Ps[node.dof[1], 0] = node.force[1]  # Py

# print("System Ps")
# print(Ps)

K11 = Ks[0:N, 0:N]
P1 = Ps[0:N, 0]

# print("K11")
# print(K11)

# print("P1")
# print(P1)

u1 = np.linalg.inv(K11) @ P1

# print("u1")
# print(u1)

us = u1.tolist() + [0] * (M-N)

# print(us)

RHS = Ks @ us

# print("RHS")
# print(RHS)


dictionary = {
    "nodes": {node.id: {"X": node.X, "Y": node.Y, "u": [us[node.dof[0]], us[node.dof[1]]], "p": [RHS[node.dof[0]], RHS[node.dof[1]]]} for id, node in nodes.items()},
    "elements": {elm.id: {"n1": elm.ni, "n2": elm.nj, "axialForce": random.uniform(0, 1) - 0.5} for id, elm in elements.items()},
}

# dictionary = {"a" : 1 ,"b" : 2}

json_object = json.dumps(dictionary)
print(json_object)
