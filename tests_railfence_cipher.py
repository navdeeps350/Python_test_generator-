from unittest import TestCase
from benchmark.railfence_cipher import raildecrypt
from benchmark.railfence_cipher import railencrypt

class Test_example(TestCase):
	def test_raildecrypt_1(self):
		y = raildecrypt('ttimebrwig', 2)
		assert y == 'tbtriwmieg'
	def test_railencrypt_2(self):
		y = railencrypt('hxtcjxisf', 5)
		assert y == 'hfxsticxj'
