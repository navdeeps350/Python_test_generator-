from unittest import TestCase
from benchmark.rabin_karp import rabin_karp_search

class Test_example(TestCase):

	def test_rabin_karp_search_1(self):
		y = rabin_karp_search('Am(7 #', 'Xq P;h.@1')
		assert y == []