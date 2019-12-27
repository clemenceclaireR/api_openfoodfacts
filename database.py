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

    def use_db(self, dbname):
        """
            This method uses the database and if
            the database doesn't exists, this method will
            use the method create_method to create the
            database.
        """
        # Try to use the database
        try:
            self.user_cursor.execute("USE {};".format(dbname))
        # Print the error and use the method called create_database
        except mysql.connector.Error as error:
            # mettre une messagebox ici
            print("Database {} does not exists".format(dbname))
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db(dbname)
                # mettre une messagebox ici
                print("Database {} created successfully".format(dbname))
        else:
            # mettre une messagebox ici
            print("\t Ok")

    def create_table(self, dbname):
        pass

