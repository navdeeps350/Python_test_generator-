from unittest import TestCase
from benchmark.railfence_cipher import raildecrypt
from benchmark.railfence_cipher import railencrypt

class Test_example(TestCase):
	def test_raildecrypt_1(self):
		y = raildecrypt('pchskiyyxr', 9)
		assert y == 'pchskiyyrx'
	def test_railencrypt_2(self):
		y = railencrypt('m', 10)
		assert y == 'm'
	def test_railencrypt_3(self):
		y = railencrypt('uuxetbdytn', 8)
		assert y == 'uuxetbndty'
