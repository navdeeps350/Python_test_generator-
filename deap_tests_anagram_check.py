from unittest import TestCase
from benchmark.anagram_check import anagram_check

class Test_example(TestCase):
	def test_anagram_check_1(self):
		y = anagram_check('w7i`K8%?4', 'D"a')
		assert y == 