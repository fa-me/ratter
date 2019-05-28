import unittest
from ratter.material import Material
from ratter.stack import Layer, Layerstack


class LayerstackTests(unittest.TestCase):

    def test_init_layerstack(self):
        l1 = Layer("layer1", Material("air"))
        l2 = Layer("layer2", Material("water"))
        layerstack = Layerstack([l1, l2])
        assert layerstack.layers is not None
