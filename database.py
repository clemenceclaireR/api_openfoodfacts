#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector
from PyQt5.QtWidgets import QMessageBox
from mysql.connector import errorcode
from menu import *
from db_connection import *


class Database:

    def __init__(self, cursor):
        self.user_cursor = cursor

    def use_db(self, dbname):
        """
        Uses the database
        if the database doesn't exists, it will call the method to create the database
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        try:
            self.user_cursor.execute("USE {};".format(dbname))
        # Print the error and use the method called create_database
        except mysql.connector.Error as error:
            msg.setText("Database {} doesn't seem to exist".format(dbname))
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db(dbname)
                msg.setText("Database {} created successfully".format(dbname))
        else:
            msg.setText("Database status ok")

    def create_db(self, dbname):
        """
        Create tables if they don't exist already
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        try:
            request = ("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8';".format(dbname))
            self.make_request(request)
        except mysql.connector.Error as error:
            msg.setText("Unable to create database: {}".format(error))
            exit(1)
        else:
            msg.setText("Database created successfully.")
            self.use_db(dbname)

    def create_tables(self, tables, database):
        """ Create tables"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        for table_name in tables:
            table_description = tables[table_name]
            try:
                msg.setText("Table : {}".format(table_name))
                self.make_request(table_description)
            except mysql.connector.Error as error:
                if error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    msg.setText("Table already exists")
                else:
                    msg.setText(error.msg)
            else:
                msg.setText("Tables created successfully")
                database.commit()

    def make_request(self, request):
        """
        make SQL request
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        try:
            self.user_cursor.execute(request)
        except Exception as error:
            msg.setText("Incorrect SQL query: {} \n Error : {} ".format(request, error))
            return 0
        else:
            return 1
