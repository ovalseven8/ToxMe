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
import sys
import sqlite3
import logging

import response

"""
Database structure:

* toxdns.db *

Table `users`
- name (text)
- pubkey (text)
- nospam (text)
- checksum (text)
"""

class Database:
	def __init__(self):
		"""
		Initialize.
		Connect to database and if there is no database yet, create one!
		"""
		self.path = "./toxdns.db"
		
		if not os.path.exists(self.path):
			try:
				self.conn = sqlite3.connect(self.path)
				self.c = self.conn.cursor()
				self.c.execute("""CREATE TABLE users
				          (name text, pubkey text, nospam text, checksum text)""")
				self.conn.commit()
			except Exception:
				logging.exception("Could not create database!")
				sys.exit(1)
		else:
			try:
				self.conn = sqlite3.connect(self.path)
				self.c = self.conn.cursor()
			except:
				logging.exception("Could not connect to database!")
				sys.exit(1)
			
	
	def lookup(self, name):
		
		try:
			name_lookup = (name,)
			self.c.execute("SELECT pubkey, nospam, checksum FROM users WHERE name=?", name_lookup)
		except Exception:
			logging.exception("Lookup failed because of intern error:")
			raise Exception(response.error_intern)
		
		result = self.c.fetchall()
		if len(result) != 1:
			return None
		else:
			return result[0][0] + result[0][1] + result[0][2]
	
	def reverse_lookup(self, pk):
		
		try:
			pubkey = (pk,)
			self.c.execute("SELECT name FROM users WHERE pubkey=?", pubkey)
		except Exception:
			logging.exception("Reverse lookup failed because of intern error:")
			raise Exception(response.error_intern)
		
		result = self.c.fetchall()
		if len(result) != 1:
			return None
		else:
			return result[0][0]
	
	def registration(self, toxid, username):
		
		try:
			register = (username, toxid[:64], toxid[64:72], toxid[72:])
			self.c.execute("INSERT INTO users VALUES (?,?,?,?)", register)
			self.conn.commit()
		except:
			logging.exception("Registration failed because of intern error:")
			raise Exception(response.error_intern)
	
	def update(self, toxid):
		
		try:
			pubkey = (toxid[:64],)
			self.c.execute("SELECT nospam FROM users WHERE pubkey=?", pubkey)
			result = self.c.fetchall()
		except:
			logging.exception("Update failed because of intern error:")
			raise Exception(response.error_intern)
			
		if result[0][0] == toxid[64:72]:
			raise Exception(response.error_update_nochange)
		
		try:
			self.c.execute("UPDATE users SET nospam=?, checksum=? WHERE pubkey=?", (toxid[64:72], toxid[72:], toxid[:64]))
			self.conn.commit()
		except:
			logging.exception("Update failed because of intern error:")
			raise Exception(response.error_intern)
	
	def deletion_pk(self, pk):
		
		try:
			self.c.execute("DELETE FROM users WHERE pubkey=?", (pk,))
			self.conn.commit()
		except:
			logging.exception("Deletion failed because of intern error:")
			raise Exception(response.error_intern)
