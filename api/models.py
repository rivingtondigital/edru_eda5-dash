#from django.db import models
import json
import re
import time
import calendar
from pymongo import MongoClient
from bson.objectid import ObjectId
from copy import deepcopy
import logging


logger = logging.getLogger('eda5.api.models')
client = MongoClient('mongodb')

class EdaModel(object):
	def __init__(self, **kwargs):
		self._id = None
		self.created_on = calendar.timegm(time.gmtime())
		self.deleted_on = None

		for (arg, value) in kwargs.items():
			self.__dict__[arg] = value

	def tobson(self):
		ret = deepcopy(self.__dict__)
		for (key, value) in ret.items():
			if type(value) == list and len(value) > 0:
				one = value[0]
				if 'tobson' in dir(one):
					ret_list = [x.tobson() for x in value]
					ret[key] = ret_list
			elif 'tobson' in dir(value):
				ret[key] = value.tobson()
			else:
				try:
					ret[key] = value.decode('utf-8', 'ignore') if value != None and len(value) > 0 else value
				except:
					pass
		if '_id' in ret.keys():
			ret['_id'] = ObjectId(ret['_id'])
		return ret

	@classmethod
	def _unbson(cls, chunk):
		for (key, value) in chunk.items():
			if type(value) == dict:
				chunk[key] = unbson(value)
			if type(value) in [list,tuple]:
				chunk[key] = [unbson(x) for x in value]
			if key == '_id':
				chunk[key] = str(value)
		return chunk

	def tojson(self):
		ret = self.tobson()
		ret = self._unbson(ret)
		return json.dumps(ret)


	@classmethod
	def fromstore(cls, js):
		ret = cls()
		for key in js.keys():
			if hasattr(ret, key):
				it = js[key]
				if type(it) == str:
					it.replace("','", ' ')
				setattr(ret, key, js[key])
		if hasattr(ret, '_id'):
			ret._id = ObjectId()
		return ret

	@classmethod
	def frombson(cls, bson):
		ret = cls()
		for key in bson.keys():
			if hasattr(ret, key):
				attr = getattr(ret, key)
				if 'frombson' in dir(attr):
					setattr(ret, key, attr.__class__.frombson(bson[key]))
				else:
					setattr(ret, key, bson[key])

		if '_id' in bson and bson['_id'] != None:
			ret._id = str(bson['_id'])
		return ret



class Version(EdaModel):
	def __init__(self, **kwargs):
		self.shortname = None
		self.description = None
		self.major = None
		self.minor = None

		super(Version, self).__init__(**kwargs)

	def getUrlName(self):
		url_name = re.sub('\s+', '_', self.shortname.lower())
		return url_name

	urlname = property(getUrlName)

class Trigger(EdaModel):
	def __init__(self, **kwargs):
		self.identifier = None
		self.value = True
		super(Trigger, self).__init__(**kwargs)
		if type(self.value) == str and self.value.strip().lower() == 'true':
			self.value = True
		if type(self.value) == str and self.value.strip().lower() == 'false':
			self.value = False




# 	def fromstore(cls, js):
# 		ret = super(Answer, cls).fromstore(js)
# 		if 'value' in cls:
# 			'value', cls['value']
# 			if cls['value'].strip().lowercase() == 'true':
# 				value = True
# 			if cls['value'].strip().lowercase() == 'false':
# 				value = False



class Answer(EdaModel):
	def __init__(self, **kwargs):
		self.answer_id = None
		self.identity = None
		self.description = None
		self.question_id = None
		self.triggers = []
		super(Answer, self).__init__(**kwargs)

	@classmethod
	def fromstore(cls, js):
		ret = super(Answer, cls).fromstore(js)
		ret.answer_id = js['id']
		if 'triggers' in js:
			print 'found triggers', js['triggers']
			ret.triggers = [Trigger(identifier=x.left.to_ecma(), value=x.right.to_ecma()) for x in js['triggers'].children()]
		return ret

	@classmethod
	def frombson(cls, bson):
		ret = super(Answer, cls).frombson(bson)
		if 'triggers' in bson:
			ret.triggers = [Trigger.frombson(a) for a in bson['triggers']]
		return ret

class Rule(EdaModel):
	def __init__(self, **kwargs):
		self.expression = None
		self.target = None
		self.question_id = None
		self.diagnosis = False
		self.diagnosisname = None
		self.endifdiagnosis = False
		self.trigger = Trigger()
		super(Rule, self).__init__(**kwargs)

	@classmethod
	def fromstore(cls, js):
		ret = super(Rule, cls).fromstore(js)
		if 'diagnosis' in js and js['diagnosis'] in ['true', 'True']:
			ret.diagnosis = True
		else:
			ret.diagnosis = False
		if 'trigger' in js:
			ret.trigger = Trigger(identifier=js['trigger'], value=True)
		return ret

class Question(EdaModel):
	def __init__(self, **kwargs):
		self.question_id = None
		self.initial = False
		self.identity = None
		self.section_label = None
		self.short_name = None
		self.probe_text = None
		self.symptom_text = None
		self.instrument_id = None
		self.answers = []
		self.rules = []
		super(Question, self).__init__(**kwargs)

	@classmethod
	def fromstore(cls, js):
		ret = super(Question, cls).fromstore(js)
		ret.question_id = js['id']
		ret.short_name = js['shortname']
		ret.section_label = js['sectionlabel']
		ret.probe_text = js['interviewprobe']
		ret.symptom_text = js['symptom']
		ret.rules = [Rule.fromstore(x) for x in js['rules']]
		return ret

	@classmethod
	def frombson(cls, bson):
		ret = super(Question, cls).frombson(bson)
		if 'answers' in bson:
			ret.answers = [Answer.frombson(a) for a in bson['answers']]
		if 'rules' in bson:
			ret.rules = [Rule.frombson(r) for r in bson['rules']]
		return ret


class Instrument(EdaModel):
	def __init__(self, **kwargs):
		self.instrument_id = None
		self.name = None
		self.urlname = None
		self.version = None
		self.description = None
		self.questions = []
		super(Instrument, self).__init__(**kwargs)

	@classmethod
	def fromstore(cls, js):
		ret = super(Instrument, cls).fromstore(js)
		ret.instrument_id = js['id']
		return ret


	@classmethod
	def frombson(cls, bson):
		ret = super(Instrument, cls).frombson(bson)
		if 'questions' in bson:
			ret.questions = [Question.frombson(q) for q in bson['questions']]
		if 'version' in bson:
			ret.version = Version.frombson(bson['version'])
		return ret

	def save(self, versiontype):
		questionnaires = client.dsm.questionnaires
		logger.info('Saving {} verson of {} -> {}'.format(versiontype, self.name, self.version.tojson()))

		bson = self.tobson()
		bson['created_on'] = calendar.timegm(time.gmtime())
		if versiontype == 'major':
			#Find the next major version
			major = questionnaires.find_one({'instrument_id': self.instrument_id}, sort=[{"version.major", -1}])['version']['major']
			logger.info('OLD MAJOR {}'.format(major))

			bson['version']['major'] = major + 1
			bson['version']['minor'] = 0

			logger.info('NEW MAJOR {}'.format(bson['version']['major']))

		else:
			#Find the next available minor version and soft delete all previous versions
			minor = questionnaires.find_one(
												{'instrument_id': self.instrument_id, 'version.major': self.version.major},
												sort=[{"version.minor", -1}]
						)['version']['minor']
			minor = minor + 1
			bson['version']['minor'] = minor

			# questionnaires.update(
			# 							{
			# 								'version.major': major,
			# 								'deleted_on': None,
			# 								'version.minor':{'$ne': minor}
			# 							},
			# 							{
			# 								'$set':{'deleted_on': datetime.now().strftime('%s')}
			# 							},
			# 							multi=True
			# )
			# old_id = self._id
			# new_copy = questionnaires.find_one({'_id': })
			# logger.info('Saved: {} -> {}'.format(old_id, self._id))
			# logger.info('Saved new version: {}'.format(self.version.tojson()))
		_id = questionnaires.save(bson)
		return Instrument.frombson(bson).version



# questionnaires.find_one({'instrument_id': '1'}, sort=[{"version.major", -1}])['version']['major']
# for q in questionnaires.find({'instrument_id': '1'}):
# 	print q['_id'], q['version']
