from unittest import TestCase
from benchmark.longest_substring import longest_sorted_substr

class Test_example(TestCase):

	def test_longest_sorted_substr_1(self):
		y = longest_sorted_substr(':UhV1 q.*',)
		assert y == ':Uh'
