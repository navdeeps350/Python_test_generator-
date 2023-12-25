from unittest import TestCase
from benchmark.caesar_cipher import decrypt
from benchmark.caesar_cipher import encrypt

class Test_example(TestCase):

	def test_decrypt_1(self):
		y = decrypt('elrgh', 32)
		assert y == '&-3()'
	def test_encrypt_2(self):
		y = encrypt('elrgh', 32)
		assert y == '&-3()'