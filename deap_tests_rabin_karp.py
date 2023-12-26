from unittest import TestCase
from benchmark.rabin_karp import rabin_karp_search

class Test_example(TestCase):

	def test_rabin_karp_search_1(self):
		y = rabin_karp_search('S@4(i.', 'yu79w_')
		assert y == []
	def test_rabin_karp_search_2(self):
		y = rabin_karp_search('', 'K 4~uf*')
		assert y == []
	def test_rabin_karp_search_3(self):
		y = rabin_karp_search('`', '/CBqj>%`9g')
		assert y == [7]
	def test_rabin_karp_search_4(self):
		y = rabin_karp_search('/', 'uKL')
		assert y == []