#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from PyQt5.QtWidgets import QMessageBox


class Variables:
    list_categories = list()
    list_products = list()
    list_products_for_given_category = list()
    user_category_choice = int
    user_product_choice = int
    substitute = list()


class Request:
    def __init__(self, cursor):
        self.msg = QMessageBox()
        self.user_cursor = cursor

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
        Variables.substitute.append(str(result))

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
        information = self.user_cursor.fetchone() # tuple
        nutriscore = str(information[4]) # attention, ici parfois à 3

        # show products with a higher nutriscore
        request = ("SELECT Products.id, Products.name, Products.nutriscore, \
                   Products.store, Products.brands, Products.link \
                   FROM Products INNER JOIN Categories \
                   ON Products.id_category = Categories.id \
                   WHERE Categories.id = %s \
                   AND Products.nutriscore <= %s \
                   ORDER BY Products.nutriscore")
                   #ORDER BY Products.nutriscore" % (category, nutriscore))

        self.display_substitute(request, category, nutriscore) # request est un tuple


        # proposer de sauvegarder en bb
