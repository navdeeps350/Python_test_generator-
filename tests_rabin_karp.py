from unittest import TestCase
from benchmark.rabin_karp import rabin_karp_search

class Test_example(TestCase):
	def test_rabin_karp_search_1(self):
		y = rabin_karp_search('ngl', 'opb')
		assert y == []
	def test_rabin_karp_search_2(self):
		y = rabin_karp_search('', '')
		assert y == []
	def test_rabin_karp_search_3(self):
		y = rabin_karp_search('xm', 'sms')
		assert y == []
	def test_rabin_karp_search_4(self):
		y = rabin_karp_search('cdlybwb', 'ramsgcg')
		assert y == []
