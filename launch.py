#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector

from database import db_connection, request_off, database
from database.db_connection import *
from api_openfoodfacts import api_off
from mysql.connector import errorcode
from PyQt5 import QtWidgets
import sys
import interface.fooditem_menu
import interface.categories_menu
import interface.products_menu
import interface.saved_products
import interface.mainwindow
from interface.mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from database.request_off import list_categories, list_products, user_category_choice
app = QtWidgets.QApplication(sys.argv)

message_list = list()


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
            self.db = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST,
                                              buffered=True, use_unicode=True)
            message_list.append("Connection to the database successfully established")
            self.display_message()
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message_list.append("User name or password incorrect")
                self.display_message()
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                message_list.append("Database does not seem to exist")
                self.display_message()
            else:
                message_list.append(("Connection failed with following error : {}".format(error)))
                self.display_message()
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
        message_list.append("Getting products from the Api")
        self.display_message()

        self.api_access.delete_superfluous_categories()
        message_list.append("Keeping just one category per product")
        self.display_message()

        self.api_access.sort_categories()
        message_list.append("Sorting categories")
        self.display_message()

        self.api_access.insert_categories(self.db)
        message_list.append("Inserting categories into the database")
        self.display_message()
        self.api_access.insert_products(self.db)
        message_list.append("Database ready")
        #self.main_menu(message_list)
        self.display_message()

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def display_message(self):
        self.main_menu(message_list)
        for message in message_list:
            return message

    def main_loop(self):
        try:
            self.database_access.user_cursor.execute("USE {};".format(db_connection.DATABASE))
            message_list.append("Trying to use database")
            self.display_message()

            self.cursor.execute("USE {};".format(db_connection.DATABASE))
            message_list.append("Using database")
            self.display_message()
            # ! à appeler si les tables n'existent pas
            #self.init_db()
            self.get_data()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                # if database doesn't exist
                #self.init_db()
                self.get_data()

    # program interfaces

    def main_menu(self, *kwargs):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.status_bar = self.ui.textBrowser
        self.status_bar.setText(str(kwargs))
        self.display_categories_button = self.ui.pushButton
        self.display_products_button = self.ui.pushButton_2
        self.display_food_item_button = self.ui.pushButton_3
        self.display_saved_products = self.ui.pushButton_4
        self.quit_button = self.ui.pushButton_5

        self.display_categories_button.clicked.connect(self.categories_section)
        self.display_products_button.clicked.connect(self.products_section)
        self.display_food_item_button.clicked.connect(self.find_substitute_item_menu)
        self.display_saved_products.clicked.connect(self.saved_products_menu)
        self.quit_button.clicked.connect(quit)

    def categories_section(self):
        ## appelle le fichier request_off et sa fonction pour montrer les différentes catégories
        self.request_access.show_categories(db_connection.TABLES, 100, 0)
        self.ui_categories = interface.categories_menu.Ui_MainWindow()
        self.ui_categories.setupUi(self)
        self.back_button = self.ui_categories.pushButton_5
        self.back_button.clicked.connect(self.main_menu)
        self.list_cat = self.ui_categories.textBrowser
        self.list_cat.setText(str(list_categories))
        self.quit_button = self.ui_categories.pushButton
        self.quit_button.clicked.connect(quit)

    def products_section(self):
        self.request_access.show_products(db_connection.TABLES, 100, 0)
        self.ui_products = interface.products_menu.Ui_MainWindow()
        self.ui_products.setupUi(self)
        self.back_button2 = self.ui_products.pushButton_5
        self.back_button2.clicked.connect(self.main_menu)
        self.list_prod = self.ui_products.textBrowser
        self.list_prod.setText(str(list_products))
        self.quit_button2 = self.ui_products.pushButton
        self.quit_button2.clicked.connect(quit)

    def find_substitute_item_menu(self):
        self.ui_fooditem = interface.fooditem_menu.Ui_MainWindow()
        self.ui_fooditem.setupUi(self)
        self.send_category = self.ui_fooditem.pushButton_3
        self.category_choice = self.ui_fooditem.lineEdit
        self.product_choice = self.ui_fooditem.lineEdit_2

        self.get_input_category = self.ui_fooditem.pushButton_3
        self.get_input_category.clicked.connect(self.get_category_input)
        self.get_input_product = self.ui_fooditem.pushButton_4
        # connect

        # test
        self.voir_produits_cat = self.ui_fooditem.pushButton_6
        self.voir_produits_cat.clicked.connect(self.request_access.find_products_for_a_given_category)

        self.back_button3 = self.ui_fooditem.pushButton_5
        self.back_button3.clicked.connect(self.main_menu)
        self.quit_button3 = self.ui_fooditem.pushButton
        self.quit_button3.clicked.connect(quit)

    def get_category_input(self):
        # ici il considère que user_category_choice est différente
        # mais qu'elle porte le même nom
        user_category_choice = self.category_choice.text()
        self.msg.setText(str(user_category_choice))
        self.show_dialog()


    def saved_products_menu(self):
        self.ui_savedproducts = interface.saved_products.Ui_MainWindow()
        self.ui_savedproducts.setupUi(self)
        self.back_button4 = self.ui_savedproducts.pushButton_5
        self.back_button4.clicked.connect(self.main_menu)
        self.quit_button4 = self.ui_savedproducts.pushButton
        self.quit_button4.clicked.connect(quit)


if __name__ == "__main__":
    widget = Main()
    widget.show()
    widget.main_loop()
    sys.exit(app.exec_())

