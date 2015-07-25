import re
from pymongo import MongoClient
import os
from services import data_services

os.path.abspath(os.curdir)


qs = MongoClient().dsm.questionnaires

qs.count()

from pprint import pprint

nonames = []
for q in qs.find():

	print q['_id']
	if 'name' in q:
		print q['name']
	else:
		nonames.append(q)
		print 'no name'


len(nonames)


