from unittest import TestCase
from benchmark.check_armstrong import check_armstrong

class Test_example(TestCase):
	def test_check_armstrong_1(self):
		y = check_armstrong(41,)
		assert y == False
