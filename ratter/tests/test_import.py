import unittest

from ratter import *

class WildImportTest(unittest.TestCase):
    def test_wild_import(self):
        m1 = Material('mat1')
        m2 = Material('mat2')
        l1 = Layer('l1', m1)
        l2 = Layer('l2', m1)
        ls = Layerstack([l1,l2])

        lv = LAMBDA_VAC

        a_fn_of = as_function_of
