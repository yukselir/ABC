def SetDegreeOfFreedoms(nodes):
    M = 0

    for id, node in nodes.items():
        if node.rest[0] == 0:
            node.dof[0] = M
            M = M + 1

        if node.rest[1] == 0:
            node.dof[1] = M
            M = M + 1

    N = M  # N Refers to number of unknowns

    for id, node in nodes.items():
        if node.rest[0] == 1:
            node.dof[0] = M
            M = M + 1

        if node.rest[1] == 1:
            node.dof[1] = M
            M = M + 1

    return N, M