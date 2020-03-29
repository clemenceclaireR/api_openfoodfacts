#! usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mariadb
from database.db_connection import DatabaseInformation
from .models import Categories, Products, Favorites
from api_openfoodfacts.api_request import ProgramStatus


class UserInput:
    """
    Holds data the user sent to the program
    """
    PRODUCT_TO_REGISTER = int
    USER_CATEGORY_CHOICE = int
    USER_PRODUCT_CHOICE = int


class RequestData:
    """
    Store the data obtained by requests method in order to display it
    in the graphical interface
    """
    ALL_CATEGORIES = []
    ALL_PRODUCTS = []
    PRODUCTS_PER_CATEGORY = []
    SAVED_PRODUCTS = []
    SUBSTITUTES_PRODUCTS = []
    MAX_ID = None


class SubstituteProductInformation:
    """
    Store data obtained by request for substitute product, in order to use it
    for the save function and to check if a user wants to record a product
    without a source product
    """
    SOURCE_PRODUCT = []
    SOURCE_PRODUCT_NAME = ""
    SOURCE_PRODUCT_NUTRISCORE = ""


class QuerySet:
    """
    This class will handle the queries to the database
    """

    def __init__(self):
        self.database = mariadb.connect(user=DatabaseInformation.USER, password=DatabaseInformation.PASSWORD,
                                        host=DatabaseInformation.HOST, database=DatabaseInformation.DATABASE,
                                        buffered=True, use_unicode=True, use_pure=True)

        self.cursor = self.database.cursor()

        self.categories_table = "Categories"
        self.products_table = "Products"
        self.favorites_table = "Favorites"

    def use_db(self, dbname):
        """
        Uses the database
        if the database doesn't exists, it will raise an error.
        """
        try:
            self.cursor.execute("USE %s;" % dbname)
        except mariadb.Error:
            ProgramStatus.MESSAGE_LIST.append("Database %s doesn't seem to exist" % dbname)
        else:
            ProgramStatus.MESSAGE_LIST.append("Database status ok")

    def display_categories(self, categories_table):
        """
        display the list of categories from the database
        """
        request = ('SELECT * FROM %s ORDER BY id;' % categories_table)
        self.cursor.execute(request)
        categories = []
        print(type(self.database))
        for result in self.cursor.fetchall():
            count = 0
            category = Categories
            category.id = str(result[0])
            category.name = str(result[1])
            RequestData.ALL_CATEGORIES.append("{} - {}".format(category.id, category.name))

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
            RequestData.ALL_PRODUCTS.append("{} - {}, {}".format(product.id, product.name, product.brand))
            count += 1

    def display_products_for_given_categories(self, products_table, categories_table):
        """
        display the products associated to a given category
        """
        request = ("SELECT OffProducts.id, OffProducts.name, brands, nutriscore \
                   FROM %s as OffProducts INNER JOIN %s \
                   ON OffProducts.id_category = Categories.id \
                   WHERE Categories.id = %s \
                   ORDER BY OffProducts.id;" % (products_table, categories_table, UserInput.USER_CATEGORY_CHOICE))
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            product = Products
            product.id = str(result[0])
            product.name = str(result[1])
            product.brand = str(result[2])
            product.nutriscore = str(result[3])
            RequestData.PRODUCTS_PER_CATEGORY.append("{} - {}, {} ({})".format(product.id, product.name,
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
            RequestData.SAVED_PRODUCTS.append("Your alternative product :"
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
        """
        display products with a higher nutriscore from the one selected before
        """
        request = ("SELECT * FROM Products \
                                        WHERE Products.id = " + product_to_trade)
        self.cursor.execute(request)
        SubstituteProductInformation.SOURCE_PRODUCT = Products
        SubstituteProductInformation.SOURCE_PRODUCT.results = self.cursor.fetchone()
        SubstituteProductInformation.SOURCE_PRODUCT_NAME = str(SubstituteProductInformation.SOURCE_PRODUCT.results[1])
        SubstituteProductInformation.SOURCE_PRODUCT_NUTRISCORE = str(
            SubstituteProductInformation.SOURCE_PRODUCT.results[4])
        SubstituteProductInformation.SOURCE_PRODUCT.category_id = str(
            SubstituteProductInformation.SOURCE_PRODUCT.results[2])

        request2 = ("SELECT Products.id, Products.name, Products.nutriscore, \
                   Products.store, Products.brands, Products.link \
                   FROM Products INNER JOIN Categories \
                   ON Products.id_category = Categories.id \
                   WHERE Categories.id = %s \
                   AND Products.nutriscore < %s \
                   ORDER BY Products.nutriscore")
        self.cursor.execute(request2, (SubstituteProductInformation.SOURCE_PRODUCT.category_id,
                                       SubstituteProductInformation.SOURCE_PRODUCT_NUTRISCORE))

        for result in self.cursor.fetchall():
            count = 0
            products = Products
            products.id = str(result[0])
            products.name = str(result[1])
            products.nutriscore = str(result[2])
            products.brand = str(result[4])
            RequestData.SUBSTITUTES_PRODUCTS.append("{} - {}, {} ({})".format(products.id, products.name,
                                                                              products.brand, products.nutriscore))
            count += 1

    def select_product_to_save(self, prod_to_save):
        """
        Get the user's choice product to record and insert it into the database
        """
        request = ("SELECT * FROM Products WHERE Products.id = %s " % prod_to_save)
        self.cursor.execute(request)
        product_to_save = Products
        product_to_save.result = self.cursor.fetchone()
        product_to_save.name = str(product_to_save.result[1])
        product_to_save.nutriscore = str(product_to_save.result[4])

        request = ("INSERT INTO Favorites (name_source_product, nutriscore_source_product, \
                   name_alternative_product, nutriscore_alternative_product) \
                   VALUES (%s, %s, %s, %s);")

        self.cursor.execute(request, (SubstituteProductInformation.SOURCE_PRODUCT_NAME,
                                      SubstituteProductInformation.SOURCE_PRODUCT_NUTRISCORE,
                                      product_to_save.name, product_to_save.nutriscore))
        # Save changes
        self.database.commit()

    def verify_max_id(self):
        """
        Check if the user entered a category id which is too big
        """
        request = 'SELECT max(id) FROM Categories'
        self.cursor.execute(request)
        RequestData.MAX_ID = self.cursor.fetchone()[0]

