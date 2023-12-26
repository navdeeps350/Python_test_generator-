from unittest import TestCase
from benchmark.exponentiation import exponentiation

class Test_example(TestCase):

	def test_exponentiation_1(self):
		y = exponentiation(6, 9)
		assert y == 10077696