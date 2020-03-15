#! usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mariadb
from database.db_connection import DatabaseInformation
from .models import Categories, Products, Favorites


class UserInput:
    product_to_register = int
    user_category_choice = int
    user_product_choice = int


class List:
    all_categories = []
    all_products = []
    products_per_category = []
    saved_products = []
    substitutes_products = []
    max_id = None
    source_product = []
    source_product_name = ""
    source_product_nutriscore = ""


class QuerySet:
    """
    This class will handle the queries to the database
    """

    def __init__(self):
        self.database = mariadb.connect(user=DatabaseInformation.USER, password=DatabaseInformation.PASSWORD,
                                            host=DatabaseInformation.HOST, database=DatabaseInformation.DATABASE,
                                            buffered=True, use_unicode=True, use_pure=True)

        #self.connect_db() # renvoie une erreur car self.database existe pas
        self.cursor = self.database.cursor()

        self.categories_table = "Categories"
        self.products_table = "Products"
        self.favorites_table = "Favorites"

    def display_categories(self, table_name):
        """
        display the list of categories from the database
        """
        request = ('SELECT * FROM %s ORDER BY id;' % table_name)
        self.cursor.execute(request)
        categories = []
        print(type(self.database))
        for result in self.cursor.fetchall():
            count = 0
            category = Categories
            category.id = str(result[0])
            category.name = str(result[1])
            List.all_categories.append("{} - {}".format(category.id, category.name))

            count += 1
        return categories

    def display_products(self, products_table):
        """
        display the list of products from the database
        """
        request = ("SELECT id, name, brands FROM %s ORDER BY id;" % products_table)
        self.cursor.execute(request)
        products = []
        for result in self.cursor.fetchall():
            count = 0
            product = Products
            product.name = str(result[1])
            product.id = str(result[0])
            product.brand = str(result[2])
            List.all_products.append("{} - {}, {}".format(product.id, product.name, product.brand))
            count += 1

    def display_products_for_given_categories(self, products_table, category_table):
        """
        display the products associated to a given category
        """
        request = ("SELECT OFFProducts.id, OFFProducts.name, brands, nutriscore \
                   FROM %s as OFFProducts INNER JOIN %s \
                   ON OFFProducts.id_category = Categories.id \
                   WHERE Categories.id = %s \
                   ORDER BY OFFProducts.id;" % (products_table, category_table, UserInput.user_category_choice))
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            product = Products
            product.id = str(result[0])
            product.name = str(result[1])
            product.brand = str(result[2])
            product.nutriscore = str(result[3])
            List.products_per_category.append("{} - {}, {} : {}".format(product.id, product.name,
                                                                        product.brand, product.nutriscore))
            count += 1

    def display_saved_products(self, favorites_table, products_table):
        """
        display previously saved products
        """
        request = "SELECT Favorites.id, Favorites.name_alternative_product, Favorites.nutriscore_alternative_product, \
                   Favorites.name_source_product, Favorites.nutriscore_source_product, \
                   Products.link, Products.store FROM %s LEFT JOIN %s ON  \
                   Favorites.name_alternative_product = Products.name" % (favorites_table, products_table)
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            favorites = Favorites
            products = Products
            favorites.id = str(result[0])
            favorites.name_alt = str(result[1])
            favorites.nutriscore_alt = str(result[2])
            favorites.name_source = str(result[3])
            favorites.nutriscore_source = str(result[4])
            products.link = str(result[5])
            products.store = str(result[6])
            List.saved_products.append("Your alternative product :"
                                       "\n {} - {} ({})"
                                       "\nYour source product :"
                                       "\n {} ({})"
                                       "\nWhere to find :"
                                       "\n {} - {}"
                                       "\n"
                                       .format(favorites.id, favorites.name_alt, favorites.nutriscore_alt,
                                               favorites.name_source, favorites.nutriscore_source,
                                               products.store, products.link))
            count += 1

    def display_substitute_products(self, product_to_trade):
        request = ("SELECT * FROM Products \
                                        WHERE Products.id = " + product_to_trade)
        self.cursor.execute(request)
        List.source_product = Products
        List.source_product.results = self.cursor.fetchone()
        List.source_product_name = str(List.source_product.results[1])
        List.source_product_nutriscore = str(List.source_product.results[4])
        List.source_product.category_id = str(List.source_product.results[2])

        request2 = ("SELECT Products.id, Products.name, Products.nutriscore, \
                   Products.store, Products.brands, Products.link \
                   FROM Products INNER JOIN Categories \
                   ON Products.id_category = Categories.id \
                   WHERE Categories.id = %s \
                   AND Products.nutriscore < %s \
                   ORDER BY Products.nutriscore")
        self.cursor.execute(request2, (List.source_product.category_id, List.source_product_nutriscore))

        for result in self.cursor.fetchall():
            count = 0
            products = Products
            products.id = str(result[0])
            products.name = str(result[1])
            products.nutriscore = str(result[2])
            # products.store = str(results[3])
            products.brand = str(result[4])
            # products.link = str(results[5])
            List.substitutes_products.append("{} - {}, {} ({})".format(products.id, products.name,
                                                                       products.brand, products.nutriscore))
            count += 1

    def select_product_to_save(self, prod_to_save):
        request = ("SELECT * FROM Products WHERE Products.id = %s " % prod_to_save)
        self.cursor.execute(request)
        product_to_save = Products
        product_to_save.result = self.cursor.fetchone()
        product_to_save.name = str(product_to_save.result[1])
        product_to_save.nutriscore = str(product_to_save.result[4])

        request = ("INSERT INTO Favorites (name_source_product, nutriscore_source_product, \
                   name_alternative_product, nutriscore_alternative_product) \
                   VALUES (%s, %s, %s, %s);")

        self.cursor.execute(request, (List.source_product_name, List.source_product_nutriscore,
                                      product_to_save.name, product_to_save.nutriscore))
        # Save changes
        self.database.commit()

    def verify_max_id(self):
        request = 'SELECT max(id) FROM Categories'
        self.cursor.execute(request)
        List.max_id = self.cursor.fetchone()[0]

    def connect_db(self):
        if self.database.is_connected():
            return
        else:
            self.database = mariadb.connect(user=DatabaseInformation.USER, password=DatabaseInformation.PASSWORD,
                                            host=DatabaseInformation.HOST, database=DatabaseInformation.DATABASE,
                                            buffered=True, use_unicode=True, use_pure=True)

