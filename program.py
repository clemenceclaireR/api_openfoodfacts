#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector

import api_off
import db_connection
from db_connection import *
from mysql.connector import errorcode
import request_off
import database
from PyQt5 import QtWidgets
from mainwindow import Ui_MainWindow
import sys
import food_item
import categories_menu
import products_menu
import saved_products
from PyQt5.QtWidgets import QMessageBox


class Main(QtWidgets.QMainWindow):
    """
    Main program which will interacts with the API and the database
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.main_menu()

        # connection to the database
        try:
            self.db = mysql.connector.connect(
                user=USER,
                password=PASSWORD,
                host=HOST)
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("User name or password incorrect")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not seem to exist")
            else:
                print("Connection failed with following error : {}".format(error))
        else:
            # creating cursor
            self.cursor = self.db.cursor()

        self.database_access = database.Database(self.cursor)

    def init_db(self):
        """
        Create the database and its tables
        """
        self.database_access.use_db(db_connection.DATABASE)
        self.database_access.create_tables(db_connection.TABLES, self.db)

    def get_data(self):
        """
            calls the api class of api_off.py file
        """
        pass

    def main_loop(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        try:
            self.database_access.user_cursor.execute("USE {};".format(db_connection.DATABASE))
            msg.setText("Trying to use database")
            self.cursor.execute("USE {};".format(db_connection.DATABASE))
            msg.setText("Using database")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                # if database doesn't exist
                self.init_db()
                self.get_data()
        else:
            pass

    # program interfaces
    def main_menu(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.display_categories_button = self.ui.pushButton
        self.display_products_button = self.ui.pushButton_2
        self.display_food_item_button = self.ui.pushButton_3
        self.display_saved_products = self.ui.pushButton_4
        self.quit_button = self.ui.pushButton_5

        self.display_categories_button.clicked.connect(self.categories_section)
        self.display_products_button.clicked.connect(self.products_section)
        self.display_food_item_button.clicked.connect(self.food_item_menu)
        self.display_saved_products.clicked.connect(self.saved_products_menu)
        self.quit_button.clicked.connect(quit)

    def categories_section(self):
        self.ui_categories = categories_menu.Ui_MainWindow()
        self.ui_categories.setupUi(self)
        self.back_button = self.ui_categories.pushButton_5
        self.back_button.clicked.connect(self.main_menu)
        self.quit_button = self.ui_categories.pushButton
        self.quit_button.clicked.connect(quit)

    def products_section(self):
        self.ui_products = products_menu.Ui_MainWindow()
        self.ui_products.setupUi(self)
        self.back_button2 = self.ui_products.pushButton_5
        self.back_button2.clicked.connect(self.main_menu)
        self.quit_button2 = self.ui_products.pushButton
        self.quit_button2.clicked.connect(quit)

    def food_item_menu(self):
        self.ui_fooditem = food_item.Ui_MainWindow()
        self.ui_fooditem.setupUi(self)
        self.back_button3 = self.ui_fooditem.pushButton_5
        self.back_button3.clicked.connect(self.main_menu)
        self.quit_button3 = self.ui_fooditem.pushButton
        self.quit_button3.clicked.connect(quit)

    def saved_products_menu(self):
        self.ui_savedproducts = saved_products.Ui_MainWindow()
        self.ui_savedproducts.setupUi(self)
        self.back_button4 = self.ui_savedproducts.pushButton_5
        self.back_button4.clicked.connect(self.main_menu)
        self.quit_button4 = self.ui_savedproducts.pushButton
        self.quit_button4.clicked.connect(quit)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Main()
    widget.show()
    widget.main_loop()
    sys.exit(app.exec_())

