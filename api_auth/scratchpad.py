import sqlite3
import os
import hashlib

from django.conf import settings
settings.configure()
from django.contrib.auth.models import User


def get_rand():
	dig = hashlib.new('ripemd160')
	b = os.urandom(128)
	dig.update(b)
	dig.hexdigest()
	return dig


user = User()
user.username = 'jon@rdig.co'
