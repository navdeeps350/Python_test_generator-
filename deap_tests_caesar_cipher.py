from unittest import TestCase
from benchmark.caesar_cipher import decrypt
from benchmark.caesar_cipher import encrypt

class Test_example(TestCase):

	def test_decrypt_1(self):
		y = decrypt('vnamlg', 83)
		assert y == '#zmyxs'

	def test_encrypt_2(self):
		y = encrypt('cqkvcmxk', 5)
		assert y == 'hvp{hr}p'
