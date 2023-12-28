from unittest import TestCase
from benchmark.caesar_cipher import decrypt
from benchmark.caesar_cipher import encrypt

class Test_example(TestCase):

	def test_decrypt_1(self):
		y = decrypt('wpxgrdju', 2)
		assert y == 'unvepbhs'
	def test_encrypt_2(self):
		y = encrypt('wpxgrdju', 2)
		assert y == 'yrzitflw'