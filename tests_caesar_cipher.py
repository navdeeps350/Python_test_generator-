from unittest import TestCase
from benchmark.caesar_cipher import decrypt
from benchmark.caesar_cipher import encrypt

class Test_example(TestCase):
	def test_decrypt_1(self):
		y = decrypt('ymljlgyvc', 84)
		assert y == '%xwuwr%"n'
	def test_encrypt_2(self):
		y = encrypt('gswewjvbmn', 56)
		assert y == '@LP>PCO;FG'
