from unittest import TestCase
from benchmark.gcd import gcd

class Test_example(TestCase):

	def test_gcd_1(self):
		y = gcd(4, 3)
		assert y == 1
