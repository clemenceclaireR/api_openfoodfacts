#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector
from PyQt5.QtWidgets import QMessageBox
from mysql.connector import errorcode


class Database:

    def __init__(self, cursor):
        self.user_cursor = cursor
        self.msg = QMessageBox()

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def use_db(self, dbname):
        """
        Uses the database
        if the database doesn't exists, it will call the method to create the database
        """
        try:
            self.user_cursor.execute("USE {};".format(dbname))
        # Print the error and use the method called create_database
        except mysql.connector.Error as error:
            self.msg.setText("Database {} doesn't seem to exist".format(dbname))
            self.show_dialog()
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db(dbname)
                self.msg.setText("Database {} created successfully".format(dbname))
                self.show_dialog()
        else:
            self.msg.setText("Database status ok")
            self.show_dialog()

    def create_db(self, dbname):
        """
        Create tables if they don't exist already
        """
        try:
            request = ("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8';".format(dbname))
            self.make_request(request)
        except mysql.connector.Error as error:
            self.msg.setText("Unable to create database: {}".format(error))
            self.show_dialog()
            exit(1)
        else:
            self.msg.setText("Database created successfully.")
            self.show_dialog()
            self.use_db(dbname)

    def create_tables(self, tables, database):
        """ Create tables"""
        for table_name in tables:
            table_description = tables[table_name]
            try:
                self.msg.setText("Table : {}".format(table_name))
                self.show_dialog()
                self.make_request(table_description)
            except mysql.connector.Error as error:
                if error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    self.msg.setText("Table already exists")
                    self.show_dialog()
                else:
                    self.msg.setText(error.msg)
                    self.show_dialog()
            else:
                self.msg.setText("Tables created successfully")
                self.show_dialog()
                database.commit()

    def make_request(self, request):
        """
        make SQL request
        """
        try:
            self.user_cursor.execute(request)
        except Exception as error:
            self.msg.setText("Incorrect SQL query: {} \n Error : {} ".format(request, error))
            self.show_dialog()
            return 0
        else:
            return 1
