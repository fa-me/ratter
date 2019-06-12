import unittest
import sympy as sp
import numpy as np
from numpy.testing import assert_array_equal, \
    assert_array_almost_equal
from tmm import coh_tmm

from ratter.expressions import as_function_of
from ratter.stack import Layerstack
from ratter.layer import Layer
from ratter.material import Material
from ratter.symbols import LAMBDA_VAC


class TestExpressions(unittest.TestCase):

    def test_as_function_of(self):
        a, b = sp.symbols('a b')

        expr = a/b

        fn = as_function_of(expr, [b, a])

        self.assertEqual(fn(1, 2), 2.0)
        self.assertEqual(fn(2, 1), 0.5)

        num_arr1 = np.random.rand(10)
        num_arr2 = np.random.rand(10)

        assert_array_equal(fn(num_arr2, num_arr1), num_arr1/num_arr2)

    def test_stack_reflection_as_function(self):
        n_air = 1
        n_glass = 1.5168 + 9.7525e-9j
        wavelength = 600e-9

        mat1 = Material('air', 1)
        mat2 = Material('glass', 1.5168 + 9.7525e-9j)

        thickness = sp.Symbol('d')

        l1 = Layer('space', mat1, sp.oo)
        l2 = Layer('plate', mat2, thickness)
        l3 = Layer('space', mat1, sp.oo)

        stack = Layerstack([l1, l2, l3])

        r = stack.reflectance_amplitude().subs(LAMBDA_VAC, wavelength)
        r_fn = as_function_of(r, [thickness])

        test_thicknesses = [340e-9, 1000e-9, 1e-6, 200e-6, 1e-3]

        def r_fn_coh(d):
            coh_res = coh_tmm('s',
                              [n_air, n_glass, n_air],
                              [np.inf, d, np.inf],
                              0,
                              wavelength)
            return coh_res['r']

        results = r_fn(np.array(test_thicknesses))
        expected = np.array([r_fn_coh(d) for d in test_thicknesses])

        assert_array_almost_equal(expected, results)
