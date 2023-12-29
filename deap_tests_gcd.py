from unittest import TestCase
from benchmark.gcd import gcd

class Test_example(TestCase):

	def test_gcd_1(self):
		y = gcd(5, 5)
		assert y == 5

	def test_gcd_2(self):
		y = gcd(3, 9)
		assert y == 3

	def test_gcd_3(self):
		y = gcd(7, 5)
		assert y == 1

	def test_gcd_4(self):
		y = gcd(5, 1)
		assert y == 1
