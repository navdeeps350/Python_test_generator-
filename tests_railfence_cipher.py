from unittest import TestCase
from benchmark.railfence_cipher import raildecrypt
from benchmark.railfence_cipher import railencrypt

class Test_example(TestCase):
	def test_raildecrypt_1(self):
		y = raildecrypt('ifeeovs', 3)
		assert y == 'ievefos'
	def test_railencrypt_2(self):
		y = railencrypt('oifwwer', 7)
		assert y == 'oifwwer'
	def test_railencrypt_3(self):
		y = railencrypt('nlcght', 2)
		assert y == 'nchlgt'
