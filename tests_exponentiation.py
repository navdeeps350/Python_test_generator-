from unittest import TestCase
from benchmark.exponentiation import exponentiation

class Test_example(TestCase):
	def test_exponentiation_1(self):
		y = exponentiation(2, 6)
		assert y == 64
