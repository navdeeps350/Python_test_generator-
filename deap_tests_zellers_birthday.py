from unittest import TestCase
from benchmark.zellers_birthday import zeller

class Test_example(TestCase):

	def test_zeller_1(self):
		y = zeller(9, 10, 4)
		assert y == 'Saturday'

	def test_zeller_2(self):
		y = zeller(10, 10, 26)
		assert y == 'Sunday'
