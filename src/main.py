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

import os
import json
import tornado.ioloop
import tornado.web
import logging
import base64

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

import database
import response
import crypto

class MainHandler(tornado.web.RequestHandler):

	def post(self):
		"""
		API handler
		"""
		request = Request(self.request.body)

		if not request.is_valid():
			logging.info("REQUEST from " + anonymize_ip(self.request.remote_ip) + " - Result: " + str(request.error))
			self.write(request.error)

		else:
			logging.info("REQUEST from " + anonymize_ip(self.request.remote_ip) + " - Result: " + str(request.response))
			self.write(request.response)

class PubKeyHandler(tornado.web.RequestHandler):
	"""
	If someone sends a post or get request to /pk -> return Public Key
	"""

	def post(self):

		logging.info("REQUEST from " + anonymize_ip(self.request.remote_ip) + " - Result: Returned server's public key")
		self.write(crypto.pubKey_string)

	def get(self):

		logging.info("REQUEST from " + anonymize_ip(self.request.remote_ip) + " - Result: Returned server's public key")
		self.write(crypto.pubKey_string)

class Request:

	def __init__(self, raw_data):
		self.raw_data = raw_data
		self.error = None
		self.response = None

	def is_valid(self):
		"""
		Check if the sent request is valid.
		
		If valid -> return True
		If invalid -> return False
		"""
		try:
			self.parsed = json.loads(self.raw_data.decode("utf-8"))
			self.action = self.parsed["action"]
		except:
			self.error = response.error_invalid_request
			return False

		if not isinstance(self.action, int) or (not self.action in (1, 2, 3, 4, 5)):
			self.error = response.error_invalid_request
			return False

		"""
		Everything fine so far.
		User sent a valid JSON object with valid action number.
		So we can execute it and look if everything else is fine too.
		
		Occurs an error while execution -> the request is not valid.
		If everything works fine, get the response from the `ProcessRequest` 
		object.
		"""

		execute = ProcessRequest(self.parsed)

		if self.action == 1:
			try:
				execute.action_1()
				self.response = execute.response
			except Exception as error:
				self.error = str(error)

		if self.action == 2:
			try:
				execute.action_2()
				self.response = execute.response
			except Exception as error:
				self.error = str(error)

		if self.action == 3:
			try:
				execute.action_3()
				self.response = execute.response
			except Exception as error:
				self.error = str(error)

		if self.action == 4:
			try:
				execute.action_4()
				self.response = execute.response
			except Exception as error:
				self.error = str(error)

		if self.action == 5:
			try:
				execute.action_5()
				self.response = execute.response
			except Exception as error:
				self.error = str(error)

		if self.error:
			return False
		else:
			return True

class ProcessRequest:

	def __init__(self, parsed_request):
		self.parsed_request = parsed_request

	def action_1(self):
		"""
		`action_1` -> Lookup
		
		If everything works fine -> create self.response
		If something goes wrong -> raise Exception
		"""
		if len(self.parsed_request) != 2:
			raise Exception(response.error_invalid_request)

		try:
			name = str(self.parsed_request["name"]).upper()
		except:
			raise Exception(response.error_invalid_request)

		lookup_result = database.lookup(name)

		if lookup_result:
				self.response = {"success_action_1": "Lookup has been successful.",
				                 "id": lookup_result}
		else:
			raise Exception(response.error_lookup)

	def action_2(self):
		"""
		`action_2` -> Reverse-Lookup
		
		If everything works fine -> create self.response
		If something goes wrong -> raise Exception
		"""
		if len(self.parsed_request) != 2:
			raise Exception(response.error_invalid_request)

		try:
			pk = self.parsed_request["pk"]

			if invalid_pk(pk):
				raise
		except:
			raise Exception(response.error_invalid_request)

		reverse_lookup_result = database.reverse_lookup(pk)

		if reverse_lookup_result:
			self.response = {"success_action_2": "Reverse lookup has been successful.",
			                 "name": reverse_lookup_result}
		else:
			raise Exception(response.error_reverse_lookup)

	def action_3(self):
		"""
		`action_3` -> Registration
		
		If everything works fine -> create self.response
		If something goes wrong -> raise Exception
		"""
		if len(self.parsed_request) != 4:
			raise Exception(response.error_invalid_request)

		try:
			pk = self.parsed_request["pk"]

			if invalid_pk(pk):
				raise

			nonce = nacl.encoding.Base64Encoder.decode(self.parsed_request["nonce"].encode("utf-8"))

			payload_encrypted = self.parsed_request["encrypted"].encode("utf-8")
			payload_encrypted = nacl.encoding.Base64Encoder.decode(payload_encrypted)

			pk_byte = pk.encode("utf-8")
			client_pk = PublicKey(pk_byte, nacl.encoding.HexEncoder)

			payload_decrypted = crypto.decrypt_request(crypto.secKey, client_pk, payload_encrypted, nonce)
			payload_decrypted = json.loads(payload_decrypted.decode("utf-8"))

			if len(payload_decrypted) != 2:
				raise

			tox_id = payload_decrypted["tox_id"]
			name = str(payload_decrypted["name"]).upper()

			if len(tox_id) != 76:
				raise

			if not pk == tox_id[:64]:
				raise

			# Check if checksum of Tox ID that will be registered is correct
			if not tox_id[72:] == crypto.compute_checksum(tox_id[:64], tox_id[64:72]):
				raise
		except:
			raise Exception(response.error_invalid_request)

		if len(name) < 1 or len(name) > 60:
			raise Exception(response.error_namelength)

		if database.lookup(name):
			raise Exception(response.error_name_used)
		if database.reverse_lookup(pk):
			raise Exception(response.error_pk_registered)

		database.registration(tox_id, name)

		self.response = {"success_action_3": "The username has been registered."}

	def action_4(self):
		"""
		`action_4` -> Update
		
		If everything works finde -> create self.response
		If something goes wrong -> raise Exception
		"""
		if len(self.parsed_request) != 4:
			raise Exception(response.error_invalid_request)

		try:
			pk = self.parsed_request["pk"]

			if invalid_pk(pk):
				raise

			nonce = nacl.encoding.Base64Encoder.decode(self.parsed_request["nonce"].encode("utf-8"))
		except:
			raise Exception(response.error_invalid_request)

		if not database.reverse_lookup(pk):
			raise Exception(response.error_update)

		try:
			payload_encrypted = self.parsed_request["encrypted"].encode("utf-8")
			payload_encrypted = nacl.encoding.Base64Encoder.decode(payload_encrypted)

			pk_byte = pk.encode("utf-8")
			client_pk = PublicKey(pk_byte, nacl.encoding.HexEncoder)

			payload_decrypted = crypto.decrypt_request(crypto.secKey, client_pk, payload_encrypted, nonce)

			new_toxid = payload_decrypted.decode("utf-8")

			if len(new_toxid) != 76:
				raise

			if not pk == new_toxid[:64]:
				raise

			if crypto.compute_checksum(new_toxid[:64], new_toxid[64:72]) != new_toxid[72:]:
				raise
		except:
			raise Exception(response.error_invalid_request)

		database.update(new_toxid)

		self.response = {"success_action_4": "The username has been updated."}

	def action_5(self):
		"""
		`action_5` -> Deletion
		
		If everything works finde -> create self.response
		If something goes wrong -> raise Exception
		"""
		if len(self.parsed_request) != 4:
			raise Exception(response.error_invalid_request)

		try:
			pk = self.parsed_request["pk"]

			if invalid_pk(pk):
				raise

			nonce = nacl.encoding.Base64Encoder.decode(self.parsed_request["nonce"].encode("utf-8"))
		except:
			raise Exception(response.error_invalid_request)

		if not database.reverse_lookup(pk):
			raise Exception(response.error_deletion)

		try:
			payload_encrypted = self.parsed_request["encrypted"].encode("utf-8")
			payload_encrypted = nacl.encoding.Base64Encoder.decode(payload_encrypted)
		except:
			raise Exception(response.error_deletion)

		if not pk == payload_encrypted:
			raise Exception(response.error_invalid_request)

		database.deletion_pk(pk)

		self.response = deletion_successful = {"success_action_5": "The username has been deleted."}

### Functions for automation:

def invalid_pk(pk):
	"""
	Just a simple function that should roughly check if the Public Key is valid
	
	If invalid -> return True
	If valid -> return False
	"""

	if len(pk) != 64:
		return True

	try:
		int(pk, 16)
		pk.encode("utf-8")
	except:
		return True

	return False

def anonymize_ip(ip_address):

	anonymize = True

	if anonymize:
		if "." in ip_address:
			ip = ip_address.split(".")
			return (ip[0] + "." + ip[1] + ".XXX.XXX")
		if ":" in ip_address:
			ip = ip_address.split(":")
			return (ip[0] + ":" + ip[1] + ":XXX:XXX")
	if not anonymize:
		return ip_address

if __name__ == "__main__":

	logging.basicConfig(filename="server.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
	logging.getLogger("tornado.access").disabled = True
	logging.getLogger("tornado.application").disabled = True

	database = database.Database()
	crypto = crypto.Crypto()

	application = tornado.web.Application([
		(r"/api", MainHandler),
		(r"/pk", PubKeyHandler)
		])

	# Because server should run behind a proxy -> xheaders=True
	application.listen(8888, xheaders=True)

	try:
		logging.info("Start server ...")
		tornado.ioloop.IOLoop.current().start()
	finally:
		logging.info("Server has been stopped!")
