from unittest import TestCase
from benchmark.anagram_check import anagram_check

class Test_example(TestCase):

	def test_anagram_check_1(self):
		y = anagram_check('3E2R\\"CY<', '&:,|fG|V.')
		assert y == False

	def test_anagram_check_2(self):
		y = anagram_check('4?$VX><n>M', '')
		assert y == False

	def test_anagram_check_3(self):
		y = anagram_check('6', '')
		assert y == False
