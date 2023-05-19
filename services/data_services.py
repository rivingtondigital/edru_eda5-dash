import json
import re
from datetime import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
from copy import deepcopy
from api.models import *
import logging

logger = logging.getLogger('eda5.dataservices')

def unbson(chunk):
    for (key, value) in chunk.items():
        if type(value) == dict:
            chunk[key] = unbson(value)
        if type(value) in [list, tuple]:
            chunk[key] = [unbson(x) for x in value]
        if key == '_id':
            chunk[key] = str(value)
    return chunk


client = MongoClient('mongodb')


def get_current_questionnaire(urlname):
    questionnaires = client.dsm.questionnaires

    quest_bson = questionnaires.find_one({
        'urlname': urlname,
        'deleted_on': None
    }, sort=[("version.minor", DESCENDING)])

    if quest_bson != None:
        quest = unbson(quest_bson)
    return quest


def get_specific_version(urlname, major, minor):
    logger.debug('Requesting {}: version {}.{}'.format(urlname, major, minor))
    questionnaires = client.dsm.questionnaires
    if minor == 'current':
        quest_bson = questionnaires.find({
            'urlname': urlname,
            'version.major': int(major),
            'deleted_on': None
        }, sort=[("version.minor", DESCENDING)]).next()

    else:
        quest_bson = questionnaires.find({
            'urlname': urlname,
            'version.major': int(major),
            'version.minor': int(minor),
            'deleted_on': None
        }).next()
    logger.info(quest_bson['version'])
    logger.info("LANGUAGE: {}".format(quest_bson.get('language')))
    if quest_bson != None:
        if 'language' not in quest_bson:
            quest_bson['language'] = {'id': 'en'}
        return unbson(quest_bson)
    else:
        return None


def get_all_versions():
    questionnaires = client.dsm.questionnaires

    versions = questionnaires.aggregate([
                {'$match': {'deleted_on': None}},
                {'$sort': {'version.major': 1, 'version.minor': -1}},
                {'$group': {
                    '_id': '$version.major',
                    'instrument_id': {'$first': '$instrument_id'},
                    'name': {'$first': '$name'},
                    'urlname': {'$first': '$urlname'},
                    'minor': {'$first': '$version.minor'},
                    'major': {'$first': '$version.major'},
                    'shortname': {'$first': '$version.shortname'},
                    'created_by': {'$first': '$created_by'},
                    'created_on': {'$first': '$created_on'}

                }},
                {'$sort': {'created_on': 1}},
                {'$group':{
                    '_id': '$instrument_id',
                    'instrument_id': {'$first': '$instrument_id'},
                    'name': {'$first': '$name'},
                    'urlname': {'$first': '$urlname'},
                    'versions': {'$addToSet': {
                        'version': {
                            'created_by': '$created_by',
                            'created_on': '$created_on',
                            'shortname': '$shortname',
                            'major': '$major',
                            'minor': '$minor'
                        }
                    }},
                 }},

        ])

    versions = [unbson(x) for x in versions]
    return versions


def soft_delete_version(id, major, minor):
    logger.info("Soft deleting {}->{}:{}".format(id, major, minor))
    questionnaires = client.dsm.questionnaires
    resp = questionnaires.update(
            {
                'instrument_id': id,
                'version.major': int(major),
                'version.minor': int(minor)
            },
            {
                '$set': {'deleted_on': datetime.now().strftime('%s')}
            }
    )
    return resp

