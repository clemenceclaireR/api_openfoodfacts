#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector
from PyQt5.QtWidgets import QMessageBox
from mysql.connector import errorcode
from database.request_off import StoredData


class Database:
    """
    Selection and requests for a given database
    """

    def __init__(self, cursor):
        self.cursor = cursor
        self.msg = QMessageBox()

    def show_dialog(self): # DRY
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def use_db(self, dbname):
        """
        Uses the database
        if the database doesn't exists, it will raise an error.
        """
        try:
            self.cursor.execute("USE {};".format(dbname))
        except mysql.connector.Error:
            StoredData.message_list.append("Database {} doesn't seem to exist".format(dbname))
        else:
            StoredData.message_list.append("Database status ok")

    def make_request(self, request):
        """
        make SQL request
        """
        try:
            self.cursor.execute(request)
        except Exception as error:
            self.msg.setText("Incorrect SQL query: {} \n Error : {} ".format(request, error))
            self.show_dialog()
            return 0
        else:
            return 1

