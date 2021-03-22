
nodes = dict()


class TrussNode2D:
    def __init__(self, id, X, Y):  # Constructor/Initializer
        self.id = id
        self.X = X
        self.Y = Y

        self.rest = [0, 0]
        self.dof = [-1, -1]
        self.force = [0, 0]

        nodes[id] = self
