#! usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
from peewee import *
from database.db_connection import DatabaseInformation
from .request_off import UserInput


database = MySQLDatabase('openfoodfacts', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT',
                                             'use_unicode': True, 'user': DatabaseInformation.USER,
                                             'passwd': DatabaseInformation.PASSWORD})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


