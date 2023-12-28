from unittest import TestCase
from benchmark.gcd import gcd

class Test_example(TestCase):

	def test_gcd_1(self):
		y = gcd(9, 3)
		assert y == 3


	def test_gcd_2(self):
		y = gcd(8, 9)
		assert y == 1
