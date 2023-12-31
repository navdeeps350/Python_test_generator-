from unittest import TestCase
from benchmark.caesar_cipher import decrypt
from benchmark.caesar_cipher import encrypt

class Test_example(TestCase):
	def test_decrypt_1(self):
		y = decrypt('jkibnr', 75)
		assert y == '~ }v#\''
	def test_encrypt_2(self):
		y = encrypt('ggth', 18)
		assert y == 'yy\'z'
