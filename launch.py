#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector

from database import db_connection, request_off, database
from database.db_connection import *
from api_openfoodfacts import api_off
from mysql.connector import errorcode
from PyQt5 import QtWidgets
import sys
import interface.mainwindow
from interface.mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from database.request_off import StoredData
app = QtWidgets.QApplication(sys.argv)


#message_list = list()


class Main(QtWidgets.QMainWindow):
    """
    Main program which will interacts with the API and the database
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.msg = QMessageBox()

        # connection to mysql database
        self.database = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST,
                                                    buffered=True, use_unicode=True)
        self.cursor = self.database.cursor()

        self.api_access = api_off.Api(self.cursor)
        self.database_access = database.Database(self.cursor)
        self.request_access = request_off.Request(self.cursor, self.database)

        self.main_menu()

    def init_db(self):
        """
        Create the database and its tables
        """
        self.database_access.use_db(db_connection.DATABASE)
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
        StoredData.message_list.append("Getting products from the Api")
        self.display_message(StoredData.message_list)

        self.api_access.delete_superfluous_categories()
        StoredData.message_list.append("Keeping just one category per product")
        self.display_message(StoredData.message_list)

        self.api_access.sort_categories()
        StoredData.message_list.append("Sorting categories")
        self.display_message(StoredData.message_list)

        self.api_access.insert_categories(self.database)
        StoredData.message_list.append("Inserting categories into the database")
        self.display_message(StoredData.message_list)

        self.api_access.insert_products(self.database)
        StoredData.message_list.append("Database ready")
        self.display_message(StoredData.message_list)

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def display_message(self, mess_list):
        self.main_menu(str(mess_list))
        self.format_list(str(mess_list))

    def main_loop(self):
        try:
            self.database_access.user_cursor.execute("USE {};".format(db_connection.DATABASE))
            StoredData.message_list.append("Trying to use database")
            self.display_message(StoredData.message_list)

            self.cursor.execute("USE {};".format(db_connection.DATABASE))
            StoredData.message_list.append("Using database")
            self.display_message(StoredData.message_list)

            self.get_data()

            self.request_access.show_categories(db_connection.TABLES)
            self.list_cat.setText(str("\n".join(StoredData.list_categories)))
            self.request_access.show_products(db_connection.TABLES)
            self.list_prod.setText(str("\n".join(StoredData.list_products)))
            self.request_access.show_saved_products()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.get_data()

    # program interface

    def main_menu(self, *kwargs):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.status_bar = self.ui.textBrowser
        self.status_bar.setText(str("\n".join(StoredData.message_list)))
        self.saved_product_field = self.ui.textBrowser_6
        self.saved_product_field.setText(str("\n".join(StoredData.list_saved_products)))
        self.quit_button = self.ui.pushButton_5
        self.list_cat = self.ui.textBrowser_2
        self.list_cat.setText(str("\n".join(StoredData.list_categories))) # vide quand 1er lancement
        self.list_prod = self.ui.textBrowser_3
        self.list_prod.setText(str("\n".join(StoredData.list_products)))
        self.send_category = self.ui.pushButton_3
        self.send_category.clicked.connect(self.request_show_products_for_given_cat)
        self.send_product = self.ui.pushButton_6
        self.send_product.clicked.connect(self.look_for_substitute)
        self.category_choice = self.ui.lineEdit
        self.product_choice = self.ui.lineEdit_2
        self.saved_product_choice = self.ui.lineEdit_3
        self.save_button = self.ui.pushButton_7
        self.save_button.clicked.connect(self.get_product_to_save)

        self.quit_button.clicked.connect(quit)

    def request_show_products_for_given_cat(self):
        StoredData.user_category_choice = self.category_choice.text()
        try:
            self.request_access.find_products_for_a_given_category()
            self.list_prod_cat = self.ui.textBrowser_4
            self.list_prod_cat.setText(str("\n".join(StoredData.list_products_for_given_category)))
        except:
            self.msg.setText("Please enter an existing number.")
            self.show_dialog()

    def get_product_to_save(self):
        StoredData.product_to_register = self.saved_product_choice.text()
        try:
            self.request_access.save_product(StoredData.product_to_register)
            self.msg.setText("Product saved")
            self.msg.exec()
            self.request_access.show_saved_products()
            self.saved_product_field.setText(str("\n".join(StoredData.list_saved_products)))
        except:
            self.msg.setText("Please enter an existing number.")
            self.show_dialog()

    def look_for_substitute(self):
        StoredData.user_product_choice = self.product_choice.text()
        try:
            self.request_access.find_healthier_substitute(StoredData.user_category_choice,
                                                          StoredData.user_product_choice)
            self.substitute = self.ui.textBrowser_5
            self.substitute.setText(str("\n".join(StoredData.substitute)))
        except:
            self.msg.setText("Please enter an existing number.")
            self.show_dialog()


if __name__ == "__main__":
    widget = Main()
    widget.show()
    widget.main_loop()
    sys.exit(app.exec_())

