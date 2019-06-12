import unittest
from ratter.material import Material
from ratter.stack import Layerstack
from ratter.layer import Layer


class LayerstackTests(unittest.TestCase):
    def setUp(self):
        l1 = Layer("layer1", Material("air"))
        l2 = Layer("layer2", Material("water"))
        self.layerstack = Layerstack([l1, l2])

    def test_layerstack_exists(self):
        assert self.layerstack.layers is not None

    def test_transfer_matrix_exists(self):
        assert self.layerstack.transfer_matrix() is not None
