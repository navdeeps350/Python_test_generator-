from unittest import TestCase
from benchmark.anagram_check import anagram_check

class Test_example(TestCase):

	def test_anagram_check_1(self):
		y = anagram_check('x@~ #`zEo', '7G5_=e;&q')
		assert y == False
	def test_anagram_check_2(self):
		y = anagram_check('CVkh', 'L72a1a7{7Y')
		assert y == False
	def test_anagram_check_3(self):
		y = anagram_check('\\', '4t.')
		assert y == False