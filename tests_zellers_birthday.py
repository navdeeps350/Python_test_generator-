from unittest import TestCase
from benchmark.zellers_birthday import zeller

class Test_example(TestCase):
	def test_zeller_1(self):
		y = zeller(67, 19, 5)
		assert y == 'Saturday'
	def test_zeller_2(self):
		y = zeller(61, 108, 41)
		assert y == 'Friday'
