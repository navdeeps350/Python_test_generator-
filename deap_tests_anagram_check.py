from unittest import TestCase
from benchmark.anagram_check import anagram_check

class Test_example(TestCase):

	def test_anagram_check_1(self):
		y = anagram_check('#j5fBwN', 'U$I$y=W')
		assert y == False

	def test_anagram_check_2(self):
		y = anagram_check('8in', 'GF&{h+,&1u')
		assert y == False

	def test_anagram_check_3(self):
		y = anagram_check(',', '$1+V')
		assert y == False
