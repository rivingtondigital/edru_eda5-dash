import json
import re
from datetime import datetime
import sys
from pymongo import MongoClient

import slimit
from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast
from slimit.visitors.nodevisitor import ASTVisitor

# sys.path.append('/home/eda5/public/eda5_org/eda5_manage')
# STORE_PATH = '/home/eda5/public/eda5_org/eda5/app/store/'

sys.path.append('/var/www/eda5-dashboard/eda5_manage')
STORE_PATH = '/var/www/eda5/default/app/store/'

from api.models import *

client = MongoClient('mongodb')


def extract():
    instrument = Instrument.from_store(STORE_PATH + 'instrumentstore.js')[0]
    questions = Question.from_store(STORE_PATH + 'questionstore.js')
    answers = Answer.from_store(STORE_PATH + 'answerstore.js')
    for question in questions:
        question.answers = filter(lambda x: x.question_id == question.question_id, answers)
    instrument.questions = questions
    instrument.version = 1.0
    return instrument


def clear_questionnaire():
    questionnaires = client.dsm.questionnaires
    questionnaires.remove()
    return questionnaires.count()


def get_current():
    q = client.dsm.questionnaires
    beda = q.find_one()
    eda5 = Instrument.frombson(beda)
    return eda5


def obj2dict(objs):
    def shit2str(shit):
        if re.search('join', shit):
            one = re.sub('\'\,\'', ' ', shit)
            two = re.sub(r'\[(.*?)\](\.join\(.*?\))+', r'\1', one, re.M)
            return shit2str(two)
        else:
            return shit.strip('\'\"')

    ret = []
    for obj in objs:
        q = {}
        for attr in obj:
            if len(attr.children()) != 2:
                return
            (ident, value) = attr.children()
            ident = ident.to_ecma()
            if type(value) == slimit.ast.FunctionCall:
                value = shit2str(value.to_ecma())
            if type(value) in [slimit.ast.Number, slimit.ast.String, slimit.ast.Boolean]:
                value = value.to_ecma().strip('\'\"')
            if type(value) == slimit.ast.Array:
                value = obj2dict(value)

            q[ident] = value

        ret.append(q)
    return ret


def get_data(filename):
    store = ''
    with file(filename, 'r') as store_file:
        store = store_file.read()

    parser = Parser()
    tree = parser.parse(store)
    data = tree.children()[1] \
        .children()[0] \
        .children()[2] \
        .children()[2] \
        .children()[1] \
        .children()[2] \
        .children()[1] \
        .children()

    ret = obj2dict(data)
    return ret


def read_stores():
    parser = Parser()

    with file(STORE_PATH + 'AnswerStore.js', 'r') as answers_file:
        answers_store = answers_file.read()

    answers_tree = parser.parse(answers_store)

    answers_data = \
    answers_tree.children()[0].children()[0].children()[2].children()[1].children()[1].children()[2].children()[1]
    answers = obj2dict(answers_data)

    with file(STORE_PATH + 'QuestionStore.js', 'r') as questions_file:
        questions_store = questions_file.read()

    questions_tree = parser.parse(questions_store)
    questions_data = questions_tree.children()[1] \
        .children()[0] \
        .children()[2] \
        .children()[2] \
        .children()[1] \
        .children()[2] \
        .children()[1] \
        .children()
    questions = obj2dict(questions_data)

    with file(STORE_PATH + '/InstrumentStore.js', 'r') as istore_file:
        istore = istore_file.read()
    istore_tree = parser.parse(istore)
    istore_data = \
    istore_tree.children()[1].children()[0].children()[2].children()[2].children()[1].children()[2].children()[1]
    instruments = obj2dict(istore_data)
    instrument = Instrument.fromstore(instruments[0])

    questions = [Question.fromstore(x) for x in questions]
    answers = [Answer.fromstore(x) for x in answers]

    for question in questions:
        question.answers = [x for x in answers if
                            x.question_id == question.question_id]  # filter(lambda x: x.question_id == question.question_id, answers)

    instrument.questions = questions
    version = Version()
    version.shortname = 'General'
    version.description = 'general version of the EDA-5'
    version.major = 1
    version.minor = 0
    instrument.version = version
    return instrument


def extract_save():
    questionnaires = client.dsm.questionnaires
    questionnaires.remove()

    eda5 = read_stores()
    eda5.urlname = 'eda5'
    eda5_bson = eda5.tobson()
    questionnaires.remove()
    questionnaires.save(eda5_bson)
    eda5_saved = questionnaires.find_one()
    return eda5_saved

# eda5 = extract_save()
# eda5 = Instrument.frombson(eda5)
# eda5 = extract_save()
