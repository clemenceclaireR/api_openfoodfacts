#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector

from database import db_connection, request_off, database
from database.db_connection import *
from api_openfoodfacts import api_off
from mysql.connector import errorcode
from PyQt5 import QtWidgets
from interface.mainwindow import Ui_MainWindow
import sys
import interface.food_item
import interface.categories_menu
import interface.products_menu
import interface.saved_products
from interface.mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox


class Main(QtWidgets.QMainWindow):
    """
    Main program which will interacts with the API and the database
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.msg = QMessageBox()
        self.main_menu()

        # connection to the database
        try:
            self.db = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, buffered=True, use_unicode=True)
            self.msg.setText("Connection to the database successfully established")
            self.show_dialog()
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.msg.setText("User name or password incorrect")
                self.show_dialog()
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                self.msg.setText("Database does not seem to exist")
                self.show_dialog()
            else:
                self.msg.setText("Connection failed with following error : {}".format(error))
                self.show_dialog()
        else:
            # creating cursor
            self.cursor = self.db.cursor()

        self.database_access = database.Database(self.cursor)
        self.request_access = request_off.Request(self.cursor)
        self.api_access = api_off.Api(self.cursor)

    def init_db(self):
        """
        Create the database and its tables
        """
        self.database_access.use_db(db_connection.DATABASE)
        self.database_access.create_tables(db_connection.TABLES, self.db)

    def get_data(self):
        """
        calls the api_openfoodfacts class of api_off.py file
        """

        self.api_access.get_products()
        self.msg.setText("Getting products from the Api")
        self.show_dialog()

        self.api_access.delete_superfluous_categories()
        self.msg.setText("Keeping just one category per product")
        self.show_dialog()

        self.api_access.sort_categories()
        self.msg.setText("Sorting categories")
        self.show_dialog()

        self.api_access.insert_categories(self.db)
        self.msg.setText("Inserting categories into the database")

        self.api_access.insert_products(self.db)
        self.msg.setText("Database ready")
        self.show_dialog()

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def main_loop(self):
        try:
            self.database_access.user_cursor.execute("USE {};".format(db_connection.DATABASE))
            self.msg.setText("Trying to use database")
            self.show_dialog()

            self.cursor.execute("USE {};".format(db_connection.DATABASE))
            self.msg.setText("Using database")
            self.show_dialog()
            # ! à appeler si les tables n'existent pas
            self.init_db()
            self.get_data()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                # if database doesn't exist
                #self.init_db()
                self.get_data()

    # program interfaces
    def main_menu(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.display_categories_button = self.ui.pushButton
        self.display_products_button = self.ui.pushButton_2
        self.display_food_item_button = self.ui.pushButton_3
        self.display_saved_products = self.ui.pushButton_4
        self.quit_button = self.ui.pushButton_5
        #self.label_info = self.ui.label_3

        self.display_categories_button.clicked.connect(self.categories_section)
        self.display_products_button.clicked.connect(self.products_section)
        self.display_food_item_button.clicked.connect(self.find_substitute_item_menu)
        self.display_saved_products.clicked.connect(self.saved_products_menu)
        self.quit_button.clicked.connect(quit)

    def categories_section(self):
        ## appelle le fichier request_off et sa fonction pour montrer les différentes catégories
        self.request_access.show_categories(db_connection.TABLES, 10, 0)
        self.ui_categories = interface.categories_menu.Ui_MainWindow()
        self.ui_categories.setupUi(self)
        self.back_button = self.ui_categories.pushButton_5
        self.back_button.clicked.connect(self.main_menu)
        self.quit_button = self.ui_categories.pushButton
        self.list_cat = self.ui_categories.listView
        self.quit_button.clicked.connect(quit)

    def products_section(self):
        self.ui_products = interface.products_menu.Ui_MainWindow()
        self.ui_products.setupUi(self)
        self.back_button2 = self.ui_products.pushButton_5
        self.back_button2.clicked.connect(self.main_menu)
        self.quit_button2 = self.ui_products.pushButton
        self.quit_button2.clicked.connect(quit)

    def find_substitute_item_menu(self):
        ## Proposera de choisir une catégorie, puis un produit.
        ## Renverra un substitut pour le produit avec ses informations.
        ## Ensuite, proposera d'enregistrer le produit.
        self.ui_fooditem = interface.food_item.Ui_MainWindow()
        self.ui_fooditem.setupUi(self)
        self.back_button3 = self.ui_fooditem.pushButton_5
        self.back_button3.clicked.connect(self.main_menu)
        self.quit_button3 = self.ui_fooditem.pushButton
        self.quit_button3.clicked.connect(quit)

    def saved_products_menu(self):
        self.ui_savedproducts = interface.saved_products.Ui_MainWindow()
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

