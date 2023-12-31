from unittest import TestCase
from benchmark.anagram_check import anagram_check

class Test_example(TestCase):

	def test_anagram_check_1(self):
		y = anagram_check('aIxp', '.PSq')
		assert y == False

	def test_anagram_check_2(self):
		y = anagram_check('|', 'Tqs1(;P')
		assert y == False
