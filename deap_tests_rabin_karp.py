from unittest import TestCase
from benchmark.rabin_karp import rabin_karp_search

class Test_example(TestCase):

	def test_rabin_karp_search_1(self):
		y = rabin_karp_search('d', 'M37 qeK')
		assert y == []

	def test_rabin_karp_search_2(self):
		y = rabin_karp_search('5', 'Y5DE&EE%')
		assert y == [1]

	def test_rabin_karp_search_3(self):
		y = rabin_karp_search(';2>', '=Xx')
		assert y == []
