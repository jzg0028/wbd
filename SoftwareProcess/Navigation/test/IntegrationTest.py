"""
    September 25th 2016

    author: Jesse Gamez
"""

import unittest

from Navigation.prod.TCurve import TCurve

class IntegrationTest(unittest.TestCase):
    
    def test_integration(self):
        def f(u, n):
            return u
        def g(u, n):
            return u**2
        t = TCurve(2)
        self.assertAlmostEqual(t.integrate(1, 0, f), 1.0/2.0, 3)
        self.assertAlmostEqual(t.integrate(1, 0, g), 1.0/3.0, 3)
