from unittest import TestCase
from benchmark.exponentiation import exponentiation

class Test_example(TestCase):

	def test_exponentiation_1(self):
		y = exponentiation(9, 10)
		assert y == 3486784401