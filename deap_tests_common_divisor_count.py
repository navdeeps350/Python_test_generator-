from unittest import TestCase
from benchmark.common_divisor_count import cd_count

class Test_example(TestCase):

	def test_cd_count_1(self):
		y = cd_count(9, 4)
		assert y == 1
