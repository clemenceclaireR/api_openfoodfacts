#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector
from api_openfoodfacts.api_request import ProgramStatus


class Database:
    """
    Selection for a given database
    """

    def __init__(self, cursor):
        self.cursor = cursor

    def use_db(self, dbname):
        """
        Uses the database
        if the database doesn't exists, it will raise an error.
        """
        try:
            self.cursor.execute("USE {};".format(dbname))
        except mysql.connector.Error:
            ProgramStatus.message_list.append("Database {} doesn't seem to exist".format(dbname))
        else:
            ProgramStatus.message_list.append("Database status ok")



