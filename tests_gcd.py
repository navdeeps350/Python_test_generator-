from unittest import TestCase
from benchmark.gcd import gcd

class Test_example(TestCase):
	def test_gcd_1(self):
		y = gcd(5, 5)
		assert y == 5
	def test_gcd_2(self):
		y = gcd(20, 6)
		assert y == 2
