from unittest import TestCase
from benchmark.exponentiation import exponentiation

class Test_example(TestCase):

	def test_exponentiation_1(self):
		y = exponentiation(-5, 5)
		assert y == -3125