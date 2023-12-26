from unittest import TestCase
from benchmark.zellers_birthday import zeller

class Test_example(TestCase):
	def test_zeller_1(self):
		y = zeller(14, 96, -28)
		assert y == 'Saturday'
