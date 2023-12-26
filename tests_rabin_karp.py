from unittest import TestCase
from benchmark.rabin_karp import rabin_karp_search

class Test_example(TestCase):
	def test_rabin_karp_search_1(self):
		y = rabin_karp_search('fot', 'ausw')
		assert y == []
	def test_rabin_karp_search_2(self):
		y = rabin_karp_search('fktfl', 'ycdjd')
		assert y == []
