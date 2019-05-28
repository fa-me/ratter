import sympy as sp
from .symbols import LAMBDA_VAC


def fresnel_r(n1, n2):
    return (n1-n2)/(n1+n2)


def fresnel_t(n1, n2):
    return 2*n1/(n1+n2)


class Layerstack(object):
    delta = sp.IndexedBase("delta")
    r = sp.IndexedBase("r")
    t = sp.IndexedBase("t")

    def __init__(self, layers):
        self.layers = layers

    def _layercount(self):
        return len(self.layers)

    def _M_list(self, n):
        return sp.Mul(sp.Matrix([[sp.exp(-sp.I*self.delta[n]), 0],
                                 [0, sp.exp(sp.I*self.delta[n])]]) *
                      sp.Matrix([[1, self.r[n, n+1]],
                                 [self.r[n, n+1], 1]]))*1 / self.t[n, n+1]

    def transfer_matrix(self):
        subs = self.substitutions

        def tm(i):
            return self._M_list(i).subs(subs)
        return reduce(lambda a, b: a*b, [tm(i) for i in range(0, self._layercount()-1)])

    @property
    def substitutions(self):
        subst = []

        N = self._layercount()

        # r and t substitutions
        for i in range(N-1):
            n1_l = self.layers[i].material.n_symbol
            n2_l = self.layers[i+1].material.n_symbol
            subst.append((self.r[i, i+1], fresnel_r(n1_l, n2_l)))
            subst.append((self.t[i, i+1], fresnel_t(n1_l, n2_l)))
        subst.append((self.r[N-1, N], 0))
        subst.append((self.t[N-1, N], 1))

        # delta and d substitutions
        for i, layer in enumerate(self.layers):
            if i == 0:
                subst.append((self.delta[i], sp.pi))
            elif i == N-1:
                subst.append((self.delta[i], 0))
            else:
                n_l = layer.material.n_symbol
                d_l = layer.thickness_symbol

                subst.append((self.delta[i], 2*sp.pi*n_l*d_l/LAMBDA_VAC))

            # n substitutions
            subst += layer.substitutions

        return subst

    def reflectance_amplitude(self):
        transm = self.transfer_matrix()
        return transm[1, 0] / transm[0, 0]

    def transmittance_amplitude(self):
        transm = self.transfer_matrix()
        return 1 / transm[0, 0]


class Layer(object):
    def __init__(self, name, material, thickness_value=None):
        """
        name
        material
        thickness can be a formula
        """
        self.name = name
        self.material = material
        self.thickness_symbol = sp.Symbol("d_"+name, real=True)
        self.thickness_value = thickness_value

    @property
    def substitutions(self):
        if self.thickness_value is None:
            res = []
        else:
            res = [(self.thickness_symbol, self.thickness_value)]

        return res + self.material.substitutions
