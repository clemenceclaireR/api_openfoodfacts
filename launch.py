#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector

from database import db_connection, request_off, database
from database.db_connection import *
from api_openfoodfacts import api_off
from mysql.connector import errorcode
from PyQt5 import QtWidgets
import sys
import interface.saved_products
import interface.mainwindow
from interface.mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from database.request_off import Variables
app = QtWidgets.QApplication(sys.argv)

# RAJOUTER BOUTON POUR RAFFRAICHIR
# Liste message statut affiche False quand Back de la section des produits sauvegardés :
# formater correctement pour cadre vide ou garder messages précédents

message_list = list()


class Main(QtWidgets.QMainWindow):
    """
    Main program which will interacts with the API and the database
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.msg = QMessageBox()
        self.main_menu()

        # connection to mysql database
        self.database = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST,
                                                    buffered=True, use_unicode=True)
        self.cursor = self.database.cursor()

        self.api_access = api_off.Api(self.cursor)
        self.database_access = database.Database(self.cursor)
        self.request_access = request_off.Request(self.cursor, self.database)

    #def init_db(self):
     #   """
      #  Create the database and its tables
       # """
        #self.database_access.use_db(db_connection.DATABASE)
        #self.database_access.create_tables(db_connection.TABLES, self.database)

    def format_list(self, list):
        for elem in list:
            msg = '\n'.join(elem)
            return msg

    def get_data(self):
        """
        calls the api_openfoodfacts class of api_off.py file
        """

        self.api_access.get_products()
        message_list.append("Getting products from the Api")
        self.display_message(message_list)

        self.api_access.delete_superfluous_categories()
        message_list.append("Keeping just one category per product")
        self.display_message(message_list)

        self.api_access.sort_categories()
        message_list.append("Sorting categories")
        self.display_message(message_list)

        self.api_access.insert_categories(self.database)
        message_list.append("Inserting categories into the database")
        self.display_message(message_list)
        self.api_access.insert_products(self.database)
        message_list.append("Database ready")
        #self.main_menu(message_list)
        self.display_message(message_list)

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def display_message(self, mess_list):
        self.main_menu(str(mess_list))
        self.format_list(str(mess_list))
        # ici avant pas de param, et message_list directement dans les self

    def main_loop(self):
        try:
            self.database_access.user_cursor.execute("USE {};".format(db_connection.DATABASE))
            message_list.append("Trying to use database")
            self.display_message(message_list)

            self.cursor.execute("USE {};".format(db_connection.DATABASE))
            message_list.append("Using database")
            self.display_message(message_list)
            # self.get_data()
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
        self.status_bar.setText(str("\n".join(message_list)))
        self.display_saved_products = self.ui.pushButton_4
        self.display_saved_products.clicked.connect(self.saved_products_menu)
        self.quit_button = self.ui.pushButton_5
        self.display_categories = self.ui.pushButton
        self.display_categories.clicked.connect(self.request_show_categories)
        self.display_products = self.ui.pushButton_2
        self.display_products.clicked.connect(self.request_show_products)
        self.send_category = self.ui.pushButton_3
        self.send_category.clicked.connect(self.request_show_products_for_given_cat)
        self.send_product = self.ui.pushButton_6
        self.send_product.clicked.connect(self.look_for_substitute)
        # RAJOUTER CAS OU IL NY A PAS DE SUBSTITUT
        self.category_choice = self.ui.lineEdit
        self.product_choice = self.ui.lineEdit_2
        self.saved_product_choice = self.ui.lineEdit_3
        self.save_button = self.ui.pushButton_7
        self.save_button.clicked.connect(self.get_product_to_save)

        self.quit_button.clicked.connect(quit)

    def request_show_categories(self):
        self.request_access.show_categories(db_connection.TABLES, 100, 0)
        self.list_cat = self.ui.textBrowser_2
        self.list_cat.setText(str("\n".join(Variables.list_categories)))

    def request_show_products(self):
        self.request_access.show_products(db_connection.TABLES, 100, 0)
        self.list_prod = self.ui.textBrowser_3
        self.list_prod.setText(str("\n".join(Variables.list_products)))

    def request_show_products_for_given_cat(self):
        Variables.user_category_choice = self.category_choice.text()
        try:
            self.request_access.find_products_for_a_given_category()
            self.list_prod_cat = self.ui.textBrowser_4
            self.list_prod_cat.setText(str("\n".join(Variables.list_products_for_given_category)))
        except:
            self.msg.setText("Please enter a number.")
            self.show_dialog()

    def get_product_to_save(self):
        Variables.product_to_register = self.saved_product_choice.text()
        try:
            self.request_access.save_product(Variables.product_to_register)
        except:
            self.msg.setText("Please enter a number.")
            self.show_dialog()

    def look_for_substitute(self):
        Variables.user_product_choice = self.product_choice.text()
        try:
            self.request_access.find_healthier_substitute(Variables.user_category_choice, Variables.user_product_choice)
            self.substitute = self.ui.textBrowser_5
            self.substitute.setText(str("\n".join(Variables.substitute)))
        except:
            self.msg.setText("Please enter a number.")
            self.show_dialog()

    def saved_products_menu(self):
        self.request_access.show_saved_products()
        self.ui_savedproducts = interface.saved_products.Ui_MainWindow()
        self.ui_savedproducts.setupUi(self)
        self.saved_product = self.ui_savedproducts.textBrowser
        self.saved_product.setText(str("\n".join(Variables.list_saved_products))) # ! format inef ici
        self.back_button4 = self.ui_savedproducts.pushButton_5
        self.back_button4.clicked.connect(self.main_menu)
        self.quit_button4 = self.ui_savedproducts.pushButton
        self.quit_button4.clicked.connect(quit)


if __name__ == "__main__":
    widget = Main()
    widget.show()
    widget.main_loop()
    sys.exit(app.exec_())

