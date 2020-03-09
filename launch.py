#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector as mariadb
from mysql.connector import Error
from database.db_connection import DatabaseInformation
from api_openfoodfacts import api_off
from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QMessageBox
from database.request_off import ProgramStatus, SubstituteManager, UserInput
from interface.mainwindow import Ui_MainWindow
from database import request_off, database
from database.models import Store
import operator
from peewee import *
from database.models import Categories, Products


def find_products_per_category():
    products_per_category_query = \
        Products.select(Products.id, Products.name, Products.brands, Products.nutriscore) \
        .join(Categories, on=(Products.id_category == Categories.id)).where(
         Categories.id == str(UserInput.user_category_choice)).order_by(Products.id)

    list_products_per_category_query = list(products_per_category_query)

    Store.l_products_per_cat = [
        [products.id, products.name, products.brands, products.nutriscore]
        for products in list_products_per_category_query]
    Store.l_products_per_cat.sort(key=operator.itemgetter(0))


def find_healthier_substitute():
    nutriscore = Products.select(Products.nutriscore).where(Products.id == str(UserInput.user_product_choice))
    SubstituteManager.nutriscore = str(nutriscore)
    product_name = Products.select(Products.name).where(Products.name == str(UserInput.user_product_choice))
    SubstituteManager.product_name = str(product_name)
    id_category = Products.select(Products.id_category).where(Products.id == str(UserInput.user_product_choice))

    substitute_query = Products.select(Products.id, Products.name, Products.nutriscore, Products.store,
                                       Products.brands, Products.link) \
        .join(Categories, on=Categories.id == Products.id_category).where(Categories.id == id_category,
                                                                          Products.nutriscore < nutriscore) \
        .order_by(Products.nutriscore)

    list_substitute_query = list(substitute_query)

    Store.l_substitute = [[products.id, products.name, products.nutriscore] for products in list_substitute_query]
    Store.l_substitute.sort(key=operator.itemgetter(0))


def save_product():
    substitute_product_name = Products.select(Products.name).where(Products.id == str(UserInput.product_to_register))
    substitute_product_nutriscore = Products.select(Products.nutriscore)\
                                                            .where(Products.id == str(UserInput.product_to_register))
    substitute_product_link = Products.select(Products.link).where(Products.id == str(UserInput.product_to_register))
    substitute_product_store = Products.select(Products.store).where(Products.id == str(UserInput.product_to_register))
    # source prod name (SubstituteManager.product_name)
    # source prod nutriscore (SubstituteManager.nutriscore)

    # requete insertion via ORM

def format_list(list):
    """
    Performs line break on a given list
    """
    for elem in list:
        msg = '\n'.join(elem)
        return msg


class Main(QtWidgets.QMainWindow):
    """
    Main program which will interacts with the API and the database
    """

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.msg = QMessageBox()

        # connection to mysql database
        # use_pure parameter is necessary to connection
        # in order to use C implementation that uses  MySQL C client library
        self.database = mariadb.connect(user=DatabaseInformation.USER, password=DatabaseInformation.PASSWORD,
                                        host=DatabaseInformation.HOST, database=DatabaseInformation.DATABASE,
                                        buffered=True, use_unicode=True, use_pure=True)

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

    def fetch_products(self):
        """
        Call function to get products from the api and check
        for errors
        """
        try:
            self.api_access.get_products()
            ProgramStatus.message_list.append("Getting products from the Api")
        except Error as e:
            self.msg.setText("{}".format(e))
            self.show_dialog()
        self.display_message(ProgramStatus.message_list)

    def keep_only_one_category(self):
        """
        Call function to keep one category per product and
        check for errors
        """
        try:
            self.api_access.delete_superfluous_categories()
            ProgramStatus.message_list.append("Keeping just one category per product")
        except Error as e:
            self.msg.setText("{}".format(e))
            self.show_dialog()
        else:
            ProgramStatus.message_list.append("Categories parsed successfully")
        self.display_message(ProgramStatus.message_list)

    def sort_categories(self):
        """
        Call function to sort categories and check for errors
        """
        try:
            self.api_access.sort_categories()
            ProgramStatus.message_list.append("Sorting categories")
        except Error as e:
            self.msg.setText("{}".format(e))
            self.show_dialog()
        self.display_message(ProgramStatus.message_list)

    def insert_categories(self):
        """
        Call function to insert categories in the database and
        check for errors
        """
        try:
            self.api_access.insert_categories(self.database)
            ProgramStatus.message_list.append("Inserting categories into the database")
        except Error as e:
            self.msg.setText("{}".format(e))
            self.show_dialog()
        self.display_message(ProgramStatus.message_list)

    def insert_products(self):
        """
        Call function to insert products in the database and
        check for errors
        """
        try:
            self.api_access.insert_products(self.database)
            ProgramStatus.message_list.append("Database ready")
        except Error as e:
            self.msg.setText("{}".format(e))
            self.show_dialog()
        self.display_message(ProgramStatus.message_list)

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
        format_list(str(mess_list))

    def main_loop(self):
        """
        Main loop of the program :
        - connection with the database
        - get the data from the api to write/actualize it in the database
        - displaying of the categories, products and saved products
        """
        try:
            self.database_access.cursor.execute("USE {};".format(DatabaseInformation.DATABASE))
            ProgramStatus.message_list.append("Trying to use database")
            self.display_message(ProgramStatus.message_list)

            self.cursor.execute("USE {};".format(DatabaseInformation.DATABASE))
            ProgramStatus.message_list.append("Using database")
            self.display_message(ProgramStatus.message_list)

            # self.get_data()
            self.list_cat.setText(str("\n".join(map(str, Store.l_categories))))
            self.list_prod.setText(str("\n".join(map(str, Store.l_products))))
            self.saved_product_field.setText(str("\n".join(map(str, Store.l_favorites))))

        except mariadb.Error as err:
            if err.errno:
                self.get_data()

    def main_menu(self, *kwargs):
        """
        Initialize and put associated data in the QWidgets objects
        """
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.status_bar = self.ui.textBrowser
        self.status_bar.setText(str("\n".join(ProgramStatus.message_list)))
        self.saved_product_field = self.ui.textBrowser_6
        self.saved_product_field.setText(str("\n".join(map(str, Store.l_favorites))))
        self.quit_button = self.ui.pushButton_5
        self.list_cat = self.ui.textBrowser_2
        self.list_cat.setText(str("\n".join(map(str, Store.l_categories))))
        self.list_prod = self.ui.textBrowser_3
        self.list_prod.setText(str("\n".join(map(str, Store.l_products))))
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
        #ListProducts.list_products_for_given_category = []  # à modifier
        Store.l_products_per_cat = []
        UserInput.user_category_choice = self.category_choice.text()

        # convert data to int in order to verify its value
        # if it's a text, no need to convert : pass
        try:
            UserInput.int_user_category_choice = int(self.category_choice.text())
            ################ WITH ORM ##############################
            max_id2 = Categories.select(fn.MAX(Categories.id)).scalar()
            ########################################################
            self.cursor.execute('SELECT max(id) FROM Categories')
            max_id = self.cursor.fetchone()[0]

            # if user input bigger than the max id, alert
            # if UserInput.int_user_category_choice > max_id: ######### max_id2
            if UserInput.int_user_category_choice > max_id2:  ######### max_id2
                self.msg.setText(str("This number is too big."))
                self.show_dialog()
            try:
                # self.request_access.find_products_for_a_given_category() # voir ici
                self.list_prod_cat = self.ui.textBrowser_4
                # puis changer en dessous
                # self.list_prod_cat.setText(str("\n".join(ListProducts.list_products_for_given_category)))
                find_products_per_category()
                self.list_prod_cat.setText(str("\n".join(map(str, Store.l_products_per_cat))))
                #         self.saved_product_field.setText(str("\n".join(map(str, Store.l_favorites)))
            except mariadb.Error as error:
                self.msg.setText(str("Please enter a number. \nError : {}".format(error)))
                self.show_dialog()

        except ValueError:
            self.msg.setText("Please enter a number.")
            self.show_dialog()

    def get_product_to_save(self):
        """
        Get user's substitute choice input and save it in the database
        """
        UserInput.product_to_register = self.saved_product_choice.text()
        try:
            self.request_access.save_product(UserInput.product_to_register)
            self.check_presence_source_product()
            # refresh list when a new research is saved
            #ListProducts.list_saved_products = []
            Store.l_favorites = []
            # self.request_access.show_saved_products()
            self.saved_product_field.setText(str("\n".join(map(str, Store.l_favorites))))
            # self.saved_product_field.setText(str("\n".join
            #                                    (ListProducts.list_saved_products)))
        except TypeError:
            self.msg.setText("Please enter an attributed number.")
            self.show_dialog()
        except mariadb.Error as error:
            self.msg.setText(str("Please enter a number. \nError : {}".format(error)))
            self.show_dialog()

    def check_presence_source_product(self):
        """
        Check if there is a source product when the user wants to save a product
        """
        if SubstituteManager.product_name == "":
            self.msg.setText(str("The product you just saved has no source product."))
            self.show_dialog()
        else:
            self.msg.setText("Product saved")
            self.show_dialog()

    def look_for_substitute(self):
        """
        Get user's product choice to trade and display the alternatives
        """
        # refresh list when this function is called
        #ListProducts.substitute = []
        Store.l_substitute = []
        UserInput.user_product_choice = self.product_choice.text()
        try:
            #self.request_access.find_healthier_substitute(UserInput.user_product_choice)
            find_healthier_substitute()
            self.substitute = self.ui.textBrowser_5
            #self.substitute.setText(str("\n".join(ListProducts.substitute)))
            self.substitute.setText(str("\n".join(map(str, Store.l_substitute))))
        except TypeError:
            self.msg.setText("Please enter an attributed number.")
            self.show_dialog()
        except mariadb.Error as error:
            self.msg.setText("Please enter a number. \nError : {}".format(error))
            self.show_dialog()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Main()
    widget.show()
    widget.main_loop()
    sys.exit(app.exec_())
