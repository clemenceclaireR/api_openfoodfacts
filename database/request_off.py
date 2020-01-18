#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from PyQt5.QtWidgets import QMessageBox, QInputDialog
from interface.categories_menu import Ui_MainWindow

list_categories = list()
list_products = list()


class Request:
    def __init__(self, cursor):
        self.msg = QMessageBox()
        self.user_cursor = cursor

        # from which row to start
        self.offset = 0

        # store user_input
        self.user_input = ''

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def display(self, request):
        """
        display results for the different menus
        """
        self.user_cursor.execute(request)
        for result in self.user_cursor.fetchall():
            count = 0
            global list_categories, list_products
            list_categories.append(str(result))
            list_products.append(str(result))
            count += 1

    def show_categories(self, table, limit, off):
        self.offset = off

        name_table = list(table.keys())
        category = name_table[0]

        # counting items in the table Categories
        self.user_cursor.execute("SELECT COUNT(*) FROM %s;" % category)

        request = ("SELECT * FROM %s ORDER BY id LIMIT %s OFFSET %s;" %
                   (category, limit, self.offset))

        self.display(request)

    def show_products(self, table, limit, off):
        self.offset = off

        name_table = list(table.keys())
        category = name_table[1]

        self.user_cursor.execute("SELECT COUNT(*) FROM %s;" % category)

        request = ("SELECT id, name, brands FROM %s ORDER BY id LIMIT %s OFFSET %s;"
                   % (category, limit, self.offset))

        self.display(request)

    def select_product_to_replace(self, table, limit, off):
        self.offset = off
        name_table = list(table.keys())
        category = name_table[0]
        self.user_cursor.execute("SELECT COUNT(*) FROM %s;" % category)
        request = ("SELECT * FROM %s ORDER BY id LIMIT %s\
                        OFFSET %s;" % (category, limit, self.offset))
        # selectionner la catégorie

        # vérifie que l'utilisateur ait bien rentré un nombre
        if self.user_input.isdigit():
            self.find_products_for_a_given_category(self.user_input)
            # rajouter elif : cas où bien numéro, mais pas de cat associée
        else:
            self.msg.setText("Please enter a number")
            self.show_dialog()

        # sélectionner l'aliment : doit appeler une fonction qui renvoie les produits
        # associés à une catégorie

    def find_products_for_a_given_category(self, limit):
        self.user_cursor.execute("SELECT name\
                        FROM Categories WHERE id = %s;" % self.user_input)
        for name in self.user_cursor.fetchone():
            self.msg.setText(name)
            self.show_dialog()

            # show the products for the chosen category
            request = ("SELECT Products.id, Products.name, brands,\
                            nutriscore FROM Products INNER JOIN Categories\
                            ON Products.id_category = Categories.id\
                            WHERE Categories.id = %s\
                            ORDER BY Products.id LIMIT %s OFFSET %s;" % (
                self.user_input, limit, self.offset))

            self.display(request)

    #def propose_better_alternative(self, category, product):
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

        # show products with a higher nutricore
        self.user_cursor.execute("SELECT Products.id, Products.name, Products.nutriscore,\
                        Products.shop, Products.brands, Products.link\
                        FROM Products INNER JOIN Categories \
                        ON Products.id_category = Categories.id\
                        WHERE Categories.id = %(id_cat)s \
                        AND Products.nutriscore <= %(code)s \
                        ORDER BY Products.nutriscore, rand() LIMIT 5", category, product_name, nutriscore)

        # This loop will display the index and the information related to
        for substitute in self.user_cursor.fetchall():
            count = 0
            x = 0
            while count < len(substitute):
                self.msg.setText(str(x))
                count += 1
                x += 1

        # register = QInputDialog().getText()

        pass



        #  programme propose un substitut, sa description, un magasin ou l'acheter
        #  (le cas échéant) et un lien vers la page d'Open Food Facts concernant cet aliment.
        # proposer de sauvegarder en bb
