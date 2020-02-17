#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from PyQt5.QtWidgets import QMessageBox


class StoredData:
    list_categories = list()
    list_products = list()
    list_products_for_given_category = list()
    list_saved_products = list()
    user_category_choice = int
    user_product_choice = int
    substitute = list()
    product_to_register = int
    nutriscore = ""
    product_name = ""
    message_list = list()


class Request:
    def __init__(self, cursor, database):
        self.msg = QMessageBox()
        self.cursor = cursor
        self.database = database

    def display_categories(self, request):
        """
        display results for the different menus
        """
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            StoredData.list_categories.append(str(result))
            count += 1

    def display_products(self, request):
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            StoredData.list_products.append(str(result))
            count += 1

    def display_products_for_given_categories(self, request):
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            StoredData.list_products_for_given_category.append(str(result))
            count += 1

    def display_substitute(self, request, category, nutriscore):
        self.cursor.execute(request, (category, nutriscore))
        for result in self.cursor.fetchall():
            count = 0
            StoredData.substitute.append(str(result))
            count += 1

    def display_saved_products(self, request):
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            StoredData.list_saved_products.append(str(result))
            count += 1

    def show_saved_products(self):
        request = "SELECT * FROM Favorites"
        self.display_saved_products(request)

    def show_categories(self, table):

        name_table = list(table.keys())
        category = name_table[0]

        # counting items in the table Categories
        self.cursor.execute("SELECT COUNT(*) FROM %s;" % category)

        request = ("SELECT * FROM %s ORDER BY id;" %
                   category)

        self.display_categories(request)

    def show_products(self, table):

        name_table = list(table.keys())
        category = name_table[1]

        self.cursor.execute("SELECT COUNT(*) FROM %s;" % category)

        request = ("SELECT id, name, brands FROM %s ORDER BY id;"
                   % category)

        self.display_products(request)

    def select_category(self, table):
        """
        Select the category associated to the user input
        """
        name_table = list(table.keys())
        category = name_table[0]
        return category

    def find_products_for_a_given_category(self):
        """
        Get products for a given category
        """
        request = ("SELECT OFFProducts.id, OFFProducts.name, brands, nutriscore \
                   FROM Products as OFFProducts \
                   INNER JOIN Categories \
                   ON OFFProducts.id_category = Categories.id \
                   WHERE Categories.id = %s \
                   ORDER BY OFFProducts.id;" % StoredData.user_category_choice)

        self.display_products_for_given_categories(request)

    def find_healthier_substitute(self, category, product):
        """
        :param category: category associated by the product selected by the user
        :param product:  product to substitute selected by the user
        """
        # save product into a variable
        self.cursor.execute("SELECT * FROM Products \
                                WHERE Products.id = " + product)
        StoredData.information = self.cursor.fetchone()
        StoredData.nutriscore = str(StoredData.information[4])
        StoredData.product_name = str(StoredData.information[1])

        request = ("SELECT Products.id, Products.name, Products.nutriscore, \
                   Products.store, Products.brands, Products.link \
                   FROM Products INNER JOIN Categories \
                   ON Products.id_category = Categories.id \
                   WHERE Categories.id = %s \
                   AND Products.nutriscore < %s \
                   ORDER BY Products.nutriscore")

        self.display_substitute(request, category, StoredData.nutriscore)

    def save_product(self, prodtosave):
        # Get the product and save it into a variable
        self.cursor.execute("SELECT * FROM Products WHERE Products.id = %s;" % prodtosave)
        information = self.cursor.fetchone()
        sub_name = information[1]
        new_nutriscore = information[4]
        new_link = information[5]
        new_store = information[6]
        source_product_name = StoredData.product_name
        source_product_nutriscore = StoredData.nutriscore

        # Insert the product into the table "Saved"
        self.cursor.execute("INSERT INTO Favorites \
                                (name_source_product, nutriscore_source_product, name_alternative_product, \
                                nutriscore_alternative_product, store_alternative_product, link_alternative_product) \
                                 VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"  # quotes for str
                            % (source_product_name, source_product_nutriscore, sub_name,
                                    new_nutriscore, new_store, new_link))

        # Save changes
        self.database.commit()

    def update_database(self):
        self.cursor.execute()
