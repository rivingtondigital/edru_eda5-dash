import pymongo
import logging
import json
import re

from bson.objectid import ObjectId
import base64
from api.models import DJ_Instrument, Instrument
from api_auth.models import InstrumentAuth
from django.contrib.auth.models import User
import data_services as ds


SUBS = {'BMI:BMI': 'BMI:BMI',
 'BMI:Height': 'BMI:HEIGHT',
 'BMI:RecentHeight': 'BMI:RECENT_HEIGHT',
 'BMI:RecentLowBMI': 'BMI:RECENT_LOW_BMI',
 'BMI:RecentWeight': 'BMI:RECENT_WEIGHT',
 'BMI:Weight': 'BMI:WEIGHT',
 'BingeEating:OBEs per month': 'Binge Eating:OBES_PER_MONTH',
 'BingeEating:OBEs per week': 'Binge Eating:OBES_PER_WEEK',
 'BingeEating:SBEs per month': 'Binge Eating:SBES_PER_MONTH',
 'BingeEating:SBEs per week': 'Binge Eating:SBES_PER_WEEK',
 'Diuretics:Average_number_per_month': 'DIURETICS:AVERAGE_NO_MONTH',
 'Diuretics:Average_number_per_week': 'DIURETICS:AVERAGE_NO_WEEK',
 'Exercise:Average_number_episodes_per_month': 'EXERCISE:AVERAGE_PER_MONTH',
 'Exercise:Average_number_episodes_per_week': 'EXERCISE:AVERAGE_PER_WEEK',
 'Exercise:Average_number_mins_per_episode': 'EXERCISE:AVERAGE_MINUTES_PER',
 'Exercise:Type': 'EXERCISE:TYPE',
 'Interview:Date:date': 'INTERVIEW:DATE:date',
 'Interview:InterviewerID': 'INTERVIEW:INTERVIEW_ID',
 'Interview:SubjectAge:number': 'INTERVIEW:SUBJECT_AGE:number',
 'Interview:SubjectID': 'INTERVIEW:SUBJECT_ID',
 'Laxatives:Average_number_per_month': 'LAXATIVES:AVERAGE_NO_MONTH',
 'Laxatives:Average_number_per_week': 'LAXATIVES:AVERAGE_NO_WEEK',
 'OtherMethod:Average_number_per_month': 'OTHER_METHOD:AVERAGE_NO_MONTH',
 'OtherMethod:Average_number_per_week': 'OTHER_METHOD:AVERAGE_NO_WEEK',
 'OtherMethod:Name': 'OTHER_METHOD:NAME',
 'Vomiting:Average_number_per_month': 'VOMITING:AVERAGE_NO_MONTH',
 'Vomiting:Average_number_per_week': 'VOMITING:AVERAGE_NO_WEEK'}


def find_all_questionnaires():
###
# find all distinct questionnaires by major_version
# and return their major version and shortname
###
    client = pymongo.MongoClient('mongodb')
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
                {'$sort': {'name': 1}}
            ])
    return versions.next()


def do_sub(txt):
    for m, sb in SUBS.items():
        if txt and m in txt:
            print("Found a match: {}".format(m))
            txt = re.sub(m, sb, txt)
            print("Fixed: {}".format(txt.encode("utf-8")))
    return txt


def make_url(version, debug=True):
    params = {
        'q': version['urlname'],
        'major': version['major'],
        minor: version['minor'],
        debug: debug
    }
    ret = base64.b64encode(params)
    return ret


def parse_doc(questionnaire):
    for q in questionnaire.get('questions', []):
        q['probe_text'] = do_sub(q.get('probe_text', ""))
    return questionnaire


def correct_version(major):
    q = ds.get_specific_version('eda5', major, 'current')
    print("Latest: {}".format(q['version']))
    q = parse_doc(q)
    ins = Instrument.frombson(q)
    ins.save('minor')
    nxt = ds.get_specific_version('eda5', major, 'current')
    print("Latest: {}".format(nxt['version']))


def bulk_permissions(user):
    client = pymongo.MongoClient('mongodb')
    questionnaires = client.dsm.questionnaires

    for q in questionnaires.find():
        eda5 = Instrument.frombson(q)
        if InstrumentAuth.objects.filter(user=user,
                                         instrument__instrument_id=eda5.instrument_id,
                                         instrument__major_version=eda5.version.major).exists():
            continue

        instrument, is_saved = DJ_Instrument.objects.get_or_create(
            name=eda5.name,
            instrument_id=eda5.instrument_id,
            major_version=eda5.version.major,
            shortname=eda5.version.shortname
        )

        ia = InstrumentAuth()
        ia.instrument = instrument
        ia.user = user
        ia.owner = True
        ia.write = True
        ia.read = True
        ia.save()
