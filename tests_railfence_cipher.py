from unittest import TestCase
from benchmark.railfence_cipher import raildecrypt
from benchmark.railfence_cipher import railencrypt

class Test_example(TestCase):
	def test_raildecrypt_1(self):
		y = raildecrypt('jnwpgtu', 8)
		assert y == 'jnwpgtu'
	def test_raildecrypt_2(self):
		y = raildecrypt('tjjxnljj', 6)
		assert y == 'tjjxljjn'
	def test_railencrypt_3(self):
		y = railencrypt('hdvhr', 5)
		assert y == 'hdvhr'
	def test_railencrypt_4(self):
		y = railencrypt('fvfqrvvrqt', 2)
		assert y == 'ffrvqvqvrt'
