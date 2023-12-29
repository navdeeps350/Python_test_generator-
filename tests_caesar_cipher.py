from unittest import TestCase
from benchmark.caesar_cipher import decrypt
from benchmark.caesar_cipher import encrypt

class Test_example(TestCase):
	def test_decrypt_1(self):
		y = decrypt('wfkenlpgh', 8)
		assert y == 'o^c]fdh_`'
	def test_encrypt_2(self):
		y = encrypt('jkaonbueo', 5)
		assert y == 'opftsgzjt'
