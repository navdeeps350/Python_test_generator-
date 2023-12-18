from unittest import TestCase
from benchmark.exponentiation import exponentiation

class Test_example(TestCase):
	def test_exponentiation_1(self):
		y = exponentiation(-11, 1)
		assert y == -11
	def test_exponentiation_2(self):
		y = exponentiation(8, 8)
		assert y == 16777216
