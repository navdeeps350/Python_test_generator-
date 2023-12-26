from unittest import TestCase
from benchmark.caesar_cipher import decrypt
from benchmark.caesar_cipher import encrypt

class Test_example(TestCase):
	def test_decrypt_1(self):
		y = decrypt('vde', 2)
		assert y == 'tbc'
	def test_encrypt_2(self):
		y = encrypt('byj', 40)
		assert y == '+B3'
