from unittest import TestCase
from benchmark.anagram_check import anagram_check

class Test_example(TestCase):
	def test_anagram_check_1(self):
		y = anagram_check('v', 's')
		assert y == False
