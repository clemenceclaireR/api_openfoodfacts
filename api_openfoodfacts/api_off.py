#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import requests
from . import api_connection
from PyQt5.QtWidgets import QMessageBox
from mysql.connector import Error


class Api:
    """
    This class will make the connection with the OpenFoodFacts API.
    It will make the different requests needed to create a list of products and categories.
    """
    def __init__(self, cursor):
        self.msg = QMessageBox()
        self.categories = list()
        self.sorted_categories = list()
        self.cleaned_categories = list()
        self.cleaned_products = list()
        self.id_name = list()
        self.change_pages = api_connection.PARAMETERS
        self.user_cursor = cursor

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def get_products(self):
        """
        Get a list of products with a request via the API.
        """
        # Make the request via the API.
        for page in range(1, 5):
            self.change_pages['page'] = page
            products_request = requests.get(api_connection.PRODUCTS_LINK,
                                            params=api_connection.PARAMETERS)
            products = products_request.json()
            # sort needed infos
            for element in products['products']:
                if not all(tag in element for tag in (
                        "product_name", "brands", "nutrition_grade_fr", "url",
                        "stores", "categories")):
                    continue
                self.cleaned_products.append(element)
            page += 1

            #self.msg.setText("Page(s): {} on {}".format(page, 5))
            #self.show_dialog()

    def insert_categories(self, database):
        """
        Insert the categories into the database
        """
        for element in self.sorted_categories:
            self.user_cursor.execute("INSERT IGNORE INTO Categories(name) VALUES ('{}')"
                                     .format(element))
        database.commit()
        self.msg.setText("Categories inserted successfully.")
        self.show_dialog()

    def insert_products(self, database):
        """
        Get products and save them into database
        """

        try:
            for element in self.cleaned_products:
                # probleme lors de l'insertion dans la bdd
                self.user_cursor.execute("INSERT IGNORE INTO Products(name, id_category, brands, nutriscore,"
                                         "link, store) VALUES({}, {}, {}, {}, {}, {})".format(
                                            element['product_name'], element['categories'], element['brands'],
                                            element['nutrition_grade_fr'], element['url'], element['stores']))
                self.msg.setText("Product inserted successfully in the database.")
                self.show_dialog()
        except Error:
            self.msg.setText("Errors while inserting products into the database")
            self.show_dialog()
        else:
            self.msg.setText("Products inserted successfully in the database.")
            self.show_dialog()
            database.commit()