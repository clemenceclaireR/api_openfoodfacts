#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector

from database.db_connection import DatabaseInformation
from api_openfoodfacts import api_off
from mysql.connector import errorcode
from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QMessageBox
from database.request_off import StoredData
import mysql.connector
from interface.mainwindow import Ui_MainWindow
from database import request_off, database
from mysql.connector import Error


class Main(QtWidgets.QMainWindow):
    """
    Main program which will interacts with the API and the database
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.msg = QMessageBox()

        # connection to mysql database
        self.database = mysql.connector.connect(user=DatabaseInformation.USER, password=DatabaseInformation.PASSWORD,
                                                host=DatabaseInformation.HOST, buffered=True, use_unicode=True)
        self.cursor = self.database.cursor()

        self.api_access = api_off.Api(self.cursor)
        self.database_access = database.Database(self.cursor)
        self.request_access = request_off.Request(self.cursor, self.database)

        self.main_menu()

    def show_dialog(self):
        """
        open a QMessageBox
        """
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def format_list(self, list):
        """
        Performs line break on a given list
        """
        for elem in list:
            msg = '\n'.join(elem)
            return msg

    def fetch_products(self):
        """
        Call function to get products from the api and check
        for errors
        """
        try:
            self.api_access.get_products()
            StoredData.message_list.append("Getting products from the Api")
        except Error as e:
            self.msg.setText("{}".format(e))
            self.show_dialog()
        self.display_message(StoredData.message_list)

    def keep_only_one_category(self):
        """
        Call function to keep one category per product and
        check for errors
        """
        try:
            self.api_access.delete_superfluous_categories()
            StoredData.message_list.append("Keeping just one category per product")
        except Error as e:
            self.msg.setText("{}".format(e))
            self.show_dialog()
        else:
            StoredData.message_list.append("Categories parsed successfully")
        self.display_message(StoredData.message_list)

    def sort_categories(self):
        """
        Call function to sort categories and check for errors
        """
        try:
            self.api_access.sort_categories()
            StoredData.message_list.append("Sorting categories")
        except Error as e:
            self.msg.setText("{}".format(e))
            self.show_dialog()
        self.display_message(StoredData.message_list)

    def insert_categories(self):
        """
        Call function to insert categories in the database and
        check for errors
        """
        try:
            self.api_access.insert_categories(self.database)
            StoredData.message_list.append("Inserting categories into the database")
        except Error as e:
            self.msg.setText("{}".format(e))
            self.show_dialog()
        self.display_message(StoredData.message_list)

    def insert_products(self):
        """
        Call function to insert products in the database and
        check for errors
        """
        try:
            self.api_access.insert_products(self.database)
            StoredData.message_list.append("Database ready")
        except Error as e:
            self.msg.setText("{}".format(e))
            self.show_dialog()
        self.display_message(StoredData.message_list)

    def get_data(self):
        """
        Call the needed functions in order to get data from
        the api and parse it, then insert it in the database
        """
        self.fetch_products()
        self.keep_only_one_category()
        self.sort_categories()
        self.insert_categories()
        self.insert_products()

    def display_message(self, mess_list):
        """
        Actualize the data's status in the program window
        """
        self.main_menu(str(mess_list))
        self.format_list(str(mess_list))

    def main_loop(self):
        """
        Main loop of the program :
        - connection with the database
        - get the data from the api to write/actualize it in the database
        - displaying of the categories, products and saved products
        """
        try:
            self.database_access.cursor.execute("USE {};".format(DatabaseInformation.DATABASE))
            StoredData.message_list.append("Trying to use database")
            self.display_message(StoredData.message_list)

            self.cursor.execute("USE {};".format(DatabaseInformation.DATABASE))
            StoredData.message_list.append("Using database")
            self.display_message(StoredData.message_list)

            #self.get_data()

            self.request_access.show_categories(DatabaseInformation.TABLES)
            self.list_cat.setText(str("\n".join(StoredData.list_categories)))
            self.request_access.show_products(DatabaseInformation.TABLES)
            self.list_prod.setText(str("\n".join(StoredData.list_products)))
            self.request_access.show_saved_products()
            self.saved_product_field.setText(str("\n".join(StoredData.list_saved_products)))

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.get_data()

    # program interface

    def main_menu(self, *kwargs):
        """
        Initialize and put associated data in the QWidgets objects
        """
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.status_bar = self.ui.textBrowser
        self.status_bar.setText(str("\n".join(StoredData.message_list)))
        self.saved_product_field = self.ui.textBrowser_6
        self.saved_product_field.setText(str("\n".join(StoredData.list_saved_products)))
        self.quit_button = self.ui.pushButton_5
        self.list_cat = self.ui.textBrowser_2
        self.list_cat.setText(str("\n".join(StoredData.list_categories)))
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
        """
        Get user's category input and return the associated products
        """
        # refresh list when this function is called
        StoredData.list_products_for_given_category = []
        StoredData.user_category_choice = self.category_choice.text()
        # convert data to int in order to verify its value
        # if it's a text, no need to convert : pass
        try:
            StoredData.int_user_category_choice = int(self.category_choice.text())
        except ValueError:
            pass

        self.cursor.execute('SELECT max(id) FROM Categories')
        max_id = self.cursor.fetchone()[0]

        # if user input bigger than the max id, alert
        if StoredData.int_user_category_choice > max_id:
            self.msg.setText(str("This number is too big."))
            self.show_dialog()
        try:
            self.request_access.find_products_for_a_given_category()
            self.list_prod_cat = self.ui.textBrowser_4
            self.list_prod_cat.setText(str("\n".join(StoredData.list_products_for_given_category)))
        except mysql.connector.Error as error:
            self.msg.setText(str("Please enter a number. \nError : {}".format(error)))
            self.show_dialog()

    def get_product_to_save(self):
        """
        Get user's substitute choice input and save it in the database
        """
        StoredData.product_to_register = self.saved_product_choice.text()
        try:
            self.request_access.save_product(StoredData.product_to_register)
            self.msg.setText("Product saved")
            self.show_dialog()
            # raffraichit
            StoredData.list_saved_products = []
            self.request_access.show_saved_products()
            self.saved_product_field.setText(str("\n".join
                                                 (StoredData.list_saved_products)))
        except TypeError:
            self.msg.setText("Please enter an attributed number.")
            self.show_dialog()
        except mysql.connector.Error as error:
            self.msg.setText(str("Please enter a number. \nError : {}".format(error)))
            self.show_dialog()

    def look_for_substitute(self):
        """
        Get user's product choice to trade and display the alternatives
        """
        StoredData.substitute = [] # raffraichit
        StoredData.user_product_choice = self.product_choice.text()
        try:
            self.request_access.find_healthier_substitute(StoredData.user_category_choice,
                                                          StoredData.user_product_choice)
            self.substitute = self.ui.textBrowser_5
            self.substitute.setText(str("\n".join(StoredData.substitute)))
        except TypeError:
            self.msg.setText("Please enter an attributed number.")
            self.show_dialog()
        except mysql.connector.Error as error:
            self.msg.setText("Please enter a number. \nError : {}".format(error))
            self.show_dialog()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Main()
    widget.show()
    widget.main_loop()
    sys.exit(app.exec_())

