from unittest import TestCase
from benchmark.gcd import gcd

class Test_example(TestCase):
	def test_gcd_1(self):
		y = gcd(2, 8)
		assert y == 2
