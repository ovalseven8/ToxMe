"""
ToxMe
Copyright (C) 2016  <ovalseven8>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

import sys
import logging
import nacl.utils
from nacl.public import PrivateKey, Box

class Crypto:
	
	def __init__(self):
		"""
		Initialize crypto stuff
		"""
		
		try:
			with open("SecretKey", "rb") as SecKeyFile:
				key = SecKeyFile.read()
		except Exception:
			logging.info("No secret key yet -> Generate new one")
			key = None
		
		if key:
			self.secKey = PrivateKey(key, nacl.encoding.HexEncoder)
			self.pubKey = self.secKey.public_key
		else:
			self.secKey = PrivateKey.generate()
			self.pubKey = self.secKey.public_key
		
		self.secKey_string = self.secKey.encode(nacl.encoding.HexEncoder).upper()
		self.pubKey_string = self.pubKey.encode(nacl.encoding.HexEncoder).upper()
		
		try:
			with open("SecretKey", "wb") as SecKeyFile, open("PublicKey", "wb") as PubKeyFile:
				SecKeyFile.write(self.secKey_string)
				PubKeyFile.write(self.pubKey_string)
		except Exception:
			logging.exception("Could not save secret key!")
			sys.exit(1)
	
	@staticmethod
	def compute_checksum(pk, nospam):
		"""
		Return the checksum for the public key + NoSpam value
		"""
		checksum = [0, 0] # initializing
		
		for number, byte in enumerate(nacl.encoding.HexEncoder.decode(pk + nospam)):
			checksum[number % 2] ^= byte
		return "".join(hex(byte)[2:].zfill(2) for byte in checksum).upper()
	
	@staticmethod
	def decrypt_request(secKey, pubKey_client, ciphertext, nonce):
		"""
		Decrypt the ciphertext and return plaintext
		"""
		box = Box(secKey, pubKey_client)
		plain = box.decrypt(ciphertext, nonce)
		
		return plain
