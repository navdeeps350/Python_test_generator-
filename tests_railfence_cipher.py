from unittest import TestCase
from benchmark.railfence_cipher import raildecrypt
from benchmark.railfence_cipher import railencrypt

class Test_example(TestCase):
	def test_raildecrypt_1(self):
		y = raildecrypt('orlbd', 9)
		assert y == 'orlbd'
	def test_raildecrypt_2(self):
		y = raildecrypt('cvkyqjvjn', 2)
		assert y == 'cjvvkjynq'
	def test_railencrypt_3(self):
		y = railencrypt('daaxuw', 5)
		assert y == 'daaxwu'
