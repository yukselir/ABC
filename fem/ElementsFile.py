import numpy as np
from NodesFile import nodes

elements = dict()


class TrussElement2D:
    def __init__(self, id, ni, nj, EA):
        self.id = id
        self.ni = ni
        self.nj = nj
        self.EA = EA

        elements[id] = self

    @property  # Descriptor
    def Lx(self):
        nodei = nodes[self.ni]
        nodej = nodes[self.nj]
        return nodej.X - nodei.X

    @property
    def Ly(self):
        nodei = nodes[self.ni]
        nodej = nodes[self.nj]
        return nodej.Y - nodei.Y

    @property
    def L(self):
        Lx = self.Lx
        Ly = self.Ly
        return (Lx**2 + Ly**2)**0.5

    @property
    def K(self):
        EA = self.EA
        Lx = self.Lx
        Ly = self.Ly
        L = self.L
        c = Lx / L
        s = Ly / L
        cc = c * c
        ss = s * s
        cs = c * s
        return EA/L * np.asarray([[cc, cs, -cc, -cs],
                                  [cs, ss, -cs, -ss],
                                  [-cc, -cs, cc, cs],
                                  [-cs, -ss, cs, ss]])

    @property
    def code(self):
        nodei = nodes[self.ni]
        nodej = nodes[self.nj]
        return nodei.dof + nodej.dof
