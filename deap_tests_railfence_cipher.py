from unittest import TestCase
from benchmark.railfence_cipher import raildecrypt
from benchmark.railfence_cipher import railencrypt

class Test_example(TestCase):

	def test_raildecrypt_1(self):
		y = raildecrypt('ibgwmvg', 3)
		assert y == 'igvwbmg'
