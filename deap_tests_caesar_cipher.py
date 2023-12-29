from unittest import TestCase
from benchmark.caesar_cipher import decrypt
from benchmark.caesar_cipher import encrypt

class Test_example(TestCase):

	def test_decrypt_1(self):
		y = decrypt('hyq', 3)
		assert y == 'evn'

	def test_encrypt_2(self):
		y = encrypt('hyq', 3)
		assert y == 'k|t'
