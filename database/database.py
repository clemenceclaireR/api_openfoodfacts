#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector
from PyQt5.QtWidgets import QMessageBox
from mysql.connector import errorcode
from launch import message_list


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
            message_list.append("Database {} doesn't seem to exist".format(dbname))
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db(dbname)
                message_list.append("Database {} created successfully".format(dbname))
        else:
            message_list.append("Database status ok")

    def create_db(self, dbname):
        """
        Create tables if they don't exist already
        """
        try:
            request = ("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8';".format(dbname))
            self.make_request(request)
        except mysql.connector.Error as error:
            message_list.append("Unable to create database: {}".format(error))
            exit(1)
        else:
            message_list.append("Database created successfully.")
            self.use_db(dbname)

    def create_tables(self, tables, database):
        """ Create tables"""
        for table_name in tables:
            table_description = tables[table_name]
            try:
                message_list.append("Table : {}".format(table_name))
                self.make_request(table_description)
            except mysql.connector.Error as error:
                if error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    message_list.append("Table already exists")
                else:
                    self.msg.setText(error.msg)
                    self.show_dialog()
            else:
                message_list.append("Tables created successfully")
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

