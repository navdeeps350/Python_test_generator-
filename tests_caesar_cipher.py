from unittest import TestCase
from benchmark.caesar_cipher import decrypt
from benchmark.caesar_cipher import encrypt

class Test_example(TestCase):
	def test_decrypt_1(self):
		y = decrypt('fc', 73)
		assert y == '|y'
	def test_encrypt_2(self):
		y = encrypt('skfc', 91)
		assert y == 'ogb_'
