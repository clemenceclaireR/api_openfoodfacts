#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector
from mysql.connector import errorcode
from menu import *
from db_connection import *


class Database:
    """
    Database handling
    """
    def __init__(self, cursor):
        self.user_cursor = cursor


