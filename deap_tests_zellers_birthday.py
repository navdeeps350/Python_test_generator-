from unittest import TestCase
from benchmark.zellers_birthday import zeller

class Test_example(TestCase):

	def test_zeller_1(self):
		y = zeller(-24, -90, -5)
		assert y == 'Sunday'
	def test_zeller_2(self):
		y = zeller(73, 9, 9)
		assert y == 'Saturday'
	def test_zeller_3(self):
		y = zeller(-97, 50, 3)
		assert y == 'Wednesday'
	def test_zeller_4(self):
		y = zeller(-48, -84, -46)
		assert y == 'Friday'