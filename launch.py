#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector as mariadb
from mysql.connector import Error
from database.db_connection import DatabaseInformation
from api_openfoodfacts import api_request
from PyQt5 import QtWidgets
import sys
from PyQt5.QtWidgets import QMessageBox
from api_openfoodfacts.api_request import ProgramStatus
from interface.mainwindow import Ui_MainWindow
from database import database, querysets, models
from database.querysets import List, UserInput, SubstituteProductInformation


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

        self.api_access = api_request.Api(self.cursor)
        self.database_access = database.Database(self.cursor)
        self.queryset = querysets.QuerySet()
        self.category_access = models.Categories(self.cursor)
        self.product_access = models.Products(self.cursor)
        self.favorites_access = models.Favorites(self.cursor)

        self.main_menu()

    def show_dialog(self):
        """
        Open a QMessageBox
        """
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

################## These functions call the Api Request methods and catch errors if there are some ##################

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

#####################################################################################################################

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

    def check_if_database_is_empty(self):
        request = "SELECT * from Categories"
        self.cursor.execute(request)
        data = self.cursor.fetchone()
        if not data:
            self.get_data()
        else:
            return

    def main_loop(self):
        """
        Main loop of the program :
        - connection with the database
        - get the data from the api to write/actualize it in the database
        - displaying of the categories, products and saved products
        """
        try:
            # ici, est ce que je ne mettrais pas le contenu de database.py
            # dans queryset ?
            self.database_access.use_db(DatabaseInformation.DATABASE)
            self.display_message(ProgramStatus.message_list)

            # fonction check si tables vides : sinon, appelle get_data()
            self.check_if_database_is_empty()
            #self.get_data()
            self.category_access.select_all_categories()
            self.list_cat.setText(str("\n".join(List.all_categories)))

            self.product_access.select_all_products()
            self.list_prod.setText(str("\n".join(List.all_products)))

            self.favorites_access.select_saved_products()
            self.saved_product_field.setText(str("\n".join(List.saved_products)))

        except mariadb.Error as err:
            self.msg.setText("An error occured : %s" % err)
            self.display_message()

    def main_menu(self, *kwargs):
        """
        Initialize and put associated data in the QWidgets objects
        """
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.status_bar = self.ui.textBrowser
        self.status_bar.setText(str("\n".join(ProgramStatus.message_list)))
        self.saved_product_field = self.ui.textBrowser_6
        self.saved_product_field.setText(str("\n".join(List.saved_products)))
        self.quit_button = self.ui.pushButton_5
        self.list_cat = self.ui.textBrowser_2
        self.list_cat.setText(str("\n".join(List.all_categories)))
        self.list_prod = self.ui.textBrowser_3
        self.list_prod.setText(str("\n".join(List.all_products)))
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
        List.products_per_category = []
        UserInput.user_category_choice = self.category_choice.text()

        # convert data to int in order to verify its value
        # if it's a text, no need to convert : pass
        try:
            UserInput.int_user_category_choice = int(self.category_choice.text())
            self.queryset.verify_max_id()

            # if user input bigger than the max id, alert
            if UserInput.int_user_category_choice > List.max_id:
                self.msg.setText(str("This number is too big."))
                self.show_dialog()
            try:
                self.category_access.select_products_per_category()
                self.list_prod_cat = self.ui.textBrowser_4
                self.list_prod_cat.setText(str("\n".join(List.products_per_category)))

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
            self.queryset.select_product_to_save(UserInput.product_to_register)
            self.check_presence_source_product()
            # refresh list when a new research is saved
            List.saved_products = []
            # call to queryset instead of favorites in order to refresh correctly
            self.queryset.display_saved_products("Favorites", "Products")
            self.saved_product_field.setText(str("\n".join(List.saved_products)))
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
        if SubstituteProductInformation.source_product_name == "":
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
        List.substitutes_products = []
        UserInput.user_product_choice = self.product_choice.text()
        try:
            self.product_access.select_substitute_products()
            self.substitute = self.ui.textBrowser_5
            self.substitute.setText(str("\n".join(List.substitutes_products)))
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
