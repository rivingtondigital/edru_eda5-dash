import json
import re
from datetime import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from copy import deepcopy
from api.models import *


def unbson(chunk):
	for (key, value) in chunk.items():
		if type(value) == dict:
			chunk[key] = unbson(value)
		if type(value) in [list,tuple]:
			chunk[key] = [unbson(x) for x in value]
		if key == '_id':
			chunk[key] = str(value)
	return chunk

client = MongoClient('mongo')

def get_current_questionnaire(urlname):
	questionnaires = client.dsm.questionnaires

	quest_bson = questionnaires.find_one({
											 'urlname':  urlname,
											 'version.major': 1,
											 'deleted_on': None
											 }, sort=[("version.minor", DESCENDING)])


	if quest_bson != None:
		quest = unbson(quest_bson)
	return quest




def get_specific_version(major_number, questionnaire):
	questionnaires = client.dsm.questionnaires

	quest_bson = questionnaires.find_one({
									'urlname': questionnaire,
									'version.major': int(major_number),
									'deleted_on': None
								}, sort=[('version.minor', DESCENDING)])

	if quest_bson != None:
		return unbson(quest_bson)
	else:
		return None


def get_all_versions():
	questionnaires = client.dsm.questionnaires
	versions = questionnaires.aggregate([
									{'$match':{'deleted_on': None}},
									 {'$group':{
														 '_id': '$instrument_id',
														 'instrument_id': {'$first': '$instrument_id'},
														 'name': {'$first': '$name'},
														 'urlname': {'$first': '$urlname'},
														 'versions': {'$addToSet': {'_id': '$_id', 'version': '$version', 'short': '$shortname'}},
														 }
									},
							])['result']

	versions = [unbson(x) for x in versions]
	return versions


def get_all_versions_flat():

	questionnaires = client.dsm.questionnaires
	versions = questionnaires.aggregate([
							{'$match': {'deleted_on':None}},
							{'$project': {'name': 1,
														'_id': 1,
														'instrument_id': 1,
														'description': 1,
#														'version.major': 1,
#														'version.minor': 1,
#														'version.shortname': 1,
#														'version.description': 1
													}
							}
						])['result']
	versions = [unbson(x) for x in versions]
	return versions

get_all_versions_flat()


def soft_delete_version(instrument_id):
	questionnaires = client.dsm.questionnaires
	questionnaires.update(
												{'_id': ObjectId(instrument_id)},
												{
												 	'$set': {'deleted_on': datetime.now().strftime('%s')}
												}
	)



def update_minor_versions(major, minor):
	print '************************'
	print 'downgrading version: ', major
	print 'except version: ', minor
	print '************************'

	questionnaires = client.dsm.questionnaires
	questionnaires.update(
								{
									'version.major': int(major),
									'deleted_on': None,
									'version.minor':{'$ne': int(minor)}
								},
								{
									'$set':{'deleted_on': datetime.now().strftime('%s')}
								},
								multi=True
	)






# def get_all_versions():
# 	questionnaires = MongoClient().dsm.questionnaires
# 	instruments = questionnaires.aggregate([
# 									{'$match':{'deleted_on': None}},
# 									{
# 									 '$group':{
# 																'_id': {
# 																				'instrument_id': '$instrument_id',
# 																				'version_major': '$version.major',
# 																			 },
# 																'instrument_id': {'$first': '$instrument_id'},
# 																'name': {'$first': '$name'},
# 																'urlname': {'$first': '$urlname'},
# 																'last_minor': {'$max': '$version.minor'},
# 																'versions': {
# 																	'$addToSet': '$version'
# 																}
# 														}
# 									},

# 							])['result']

# 	for instrument in instruments:
# 		instrument['version'] = filter(lambda x: x['minor'] == instrument['last_minor'], instrument['versions'])[0]
# 		del instrument['versions']

# 	return [unbson(x) for x in instruments]

