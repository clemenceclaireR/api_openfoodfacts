#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from PyQt5.QtWidgets import QMessageBox


class Variables:
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


class Request:
    def __init__(self, cursor, database):
        self.msg = QMessageBox()
        self.user_cursor = cursor
        self.database = database

        # from which row to start
        self.offset = 0

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def display_categories(self, request):
        """
        display results for the different menus
        """
        self.user_cursor.execute(request)
        for result in self.user_cursor.fetchall():
            count = 0
            Variables.list_categories.append(str(result))
            count += 1

    def display_products(self, request):
        self.user_cursor.execute(request)
        for result in self.user_cursor.fetchall():
            count = 0
            Variables.list_products.append(str(result))
            count += 1

    def display_products_for_given_categories(self, request):
        self.user_cursor.execute(request)
        for result in self.user_cursor.fetchall():
            count = 0
            Variables.list_products_for_given_category.append(str(result))
            count += 1
            for products in Variables.list_products_for_given_category:
                self.msg.setText(products)
                self.msg.exec()

    def display_substitute(self, request, category, nutriscore):
        self.user_cursor.execute(request, (category, nutriscore))
        result = self.user_cursor.fetchall()
        Variables.substitute.append(result)

    def display_saved_products(self, request):
        self.user_cursor.execute(request)
        result = self.user_cursor.fetchall()
        Variables.list_saved_products.append(result)

    def show_saved_products(self):
        request = "SELECT * FROM Favorites"
        self.display_saved_products(request)

    def show_categories(self, table, limit, off):
        self.offset = off

        name_table = list(table.keys())
        category = name_table[0]

        # counting items in the table Categories
        self.user_cursor.execute("SELECT COUNT(*) FROM %s;" % category)

        request = ("SELECT * FROM %s ORDER BY id LIMIT %s OFFSET %s;" %
                   (category, limit, self.offset))

        self.display_categories(request)

    def show_products(self, table, limit, off):
        self.offset = off

        name_table = list(table.keys())
        category = name_table[1]

        self.user_cursor.execute("SELECT COUNT(*) FROM %s;" % category)

        request = ("SELECT id, name, brands FROM %s ORDER BY id LIMIT %s OFFSET %s;"
                   % (category, limit, self.offset))

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
                   ORDER BY OFFProducts.id;" % Variables.user_category_choice)

        self.display_products_for_given_categories(request)

    def find_healthier_substitute(self, category, product):
        """
        :param category: category associated by the product selected by the user
        :param product:  product to substitute selected by the user
        """
        # save product into a variable
        self.user_cursor.execute("SELECT * FROM Products \
                                WHERE Products.id = " + product)
        Variables.information = self.user_cursor.fetchone()
        Variables.nutriscore = str(Variables.information[4])
        Variables.product_name = str(Variables.information[1])


        # show products with a higher nutriscore
        request = ("SELECT Products.id, Products.name, Products.nutriscore, \
                   Products.store, Products.brands, Products.link \
                   FROM Products INNER JOIN Categories \
                   ON Products.id_category = Categories.id \
                   WHERE Categories.id = %s \
                   AND Products.nutriscore < %s \
                   ORDER BY Products.nutriscore")

        self.display_substitute(request, category, Variables.nutriscore)

    def save_product(self, prodtosave):
        # Get the product and save it into a variable
        self.msg.setText(prodtosave)
        self.msg.exec()
        self.user_cursor.execute("SELECT * FROM Products WHERE Products.id = %s;" % prodtosave) # OK
        information = self.user_cursor.fetchone()
        sub_name = information[1] # nouveau nom
        new_nutriscore = information[4] # nouveau nutriscore
        new_link = information[5] # nouveau lien
        new_store = information[6]
        source_product_name = Variables.product_name
        source_product_nutriscore = Variables.nutriscore

        # Insert the product into the table "Saved"
        self.user_cursor.execute("INSERT INTO Favorites \
                                (name_source_product, nutriscore_source_product, name_alternative_product, \
                                nutriscore_alternative_product, store_alternative_product, link_alternative_product) \
                                 VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" # quotes for str
                                 % (source_product_name, source_product_nutriscore, sub_name, new_nutriscore, new_store, new_link))

        # Save changement
        self.database.commit()
