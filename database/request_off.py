#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from PyQt5.QtWidgets import QMessageBox, QInputDialog


list_categories = list()
list_products = list()
list_products_for_given_category = list()
user_category_choice = ""


class Request:
    def __init__(self, cursor):
        self.msg = QMessageBox()
        self.user_cursor = cursor

        # from which row to start
        self.offset = 0

        # store user_input
        self.user_input = ""


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
            global list_categories
            list_categories.append(str(result))
            count += 1

    def display_products(self, request):
        self.user_cursor.execute(request)
        for result in self.user_cursor.fetchall():
            count = 0
            global list_products
            list_products.append(str(result))
            count += 1

    def display_products_for_given_categories(self, request):
        self.user_cursor.execute(request)
        for result in self.user_cursor.fetchall():
            count = 0
            global list_products_for_given_category
            list_products_for_given_category.append(str(result))
            count += 1

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

    def find_products_for_a_given_category(self):
        """
        Get products for a given category
        """
        # get the name of the selected category
        global user_category_choice
        self.user_cursor.execute("SELECT name FROM Categories WHERE id = %s;" # ne trouve pas valeur à user_cat
                                 % user_category_choice)

        for name in self.user_cursor.fetchone():
            self.msg.setText(name)
            self.show_dialog()

            # show the products for the chosen category
            request = ("SELECT Products.id, Products.name, brands,\
                            nutriscore FROM Products INNER JOIN Categories\
                            ON Products.id_category = Categories.id\
                            WHERE Categories.id = %s\
                            ORDER BY Products.id;" % user_category_choice)

            self.display_products_for_given_categories(request)

    def find_healthier_substitute(self, category, product):
        """
        :param category: category associated by the product selected by the user
        :param product:  product to substitute selected by the user
        """
        # save product into a variable
        self.user_cursor.execute("SELECT * FROM Products\
                        WHERE Products.id = " + product)
        information = self.user_cursor.fetchone()
        product_name = str(information[1])
        nutriscore = str(information[4])

        # show products with a higher nutriscore
        self.user_cursor.execute("SELECT Products.id, Products.name, Products.nutriscore,\
                        Products.shop, Products.brands, Products.link\
                        FROM Products INNER JOIN Categories \
                        ON Products.id_category = Categories.id\
                        WHERE Categories.id = %s \
                        AND Products.nutriscore <= %s \
                        ORDER BY Products.nutriscore", category, product_name, nutriscore)

        # This loop will display the index and the information related to
        for substitute in self.user_cursor.fetchall():
            count = 0
            x = 0
            while count < len(substitute):
                self.msg.setText(str(x))
                count += 1
                x += 1

        pass



        #  programme propose un substitut, sa description, un magasin ou l'acheter
        #  (le cas échéant) et un lien vers la page d'Open Food Facts concernant cet aliment.
        # proposer de sauvegarder en bb
