from unittest import TestCase
from benchmark.check_armstrong import check_armstrong

class Test_example(TestCase):

	def test_check_armstrong_1(self):
		y = check_armstrong(175,)
		assert y == False
	def test_check_armstrong_2(self):
		y = check_armstrong(6,)
		assert y == False