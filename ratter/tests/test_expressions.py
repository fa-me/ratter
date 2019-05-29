import unittest
import sympy as sp
import numpy as np
from numpy.testing import assert_array_equal

from ratter.expressions import as_function_of


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
