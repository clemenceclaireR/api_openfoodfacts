#! usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mariadb
from database.db_connection import DatabaseInformation
from .models import Category, Products


class Test:
    categories = []


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
        self.category_access = Category(self.cursor)

        self.categories_table = "Categories"

    def display_categories(self, table_name):
        """
        display the list of categories from the database
        """
        request = ('SELECT * FROM %s ORDER BY id;' % table_name)
        self.cursor.execute(request)
        categories = []
        for result in self.cursor.fetchall():
            count = 0
            category = Category
            category.id = str(result[0])
            category.name = str(result[1])
            Test.categories.append(category.id)
            Test.categories.append(category.name)

            count += 1
        return categories

    def display_products(self, table_name):
        """
        display the list of products from the database
        """
        request = ("SELECT id, name, brands FROM %s ORDER BY id;" % table_name)
        self.cursor.execute(request)
        products = []
        for result in self.cursor.fetchall():
            count = 0
            products = Products
            products.name = str(result)
            Test.products.append(products.name)
            count += 1

    def select_all_categories(self):
        self.display_categories(self.categories_table)

    def connect_db(self):
        if not self.database:
            self.database = mariadb.connect(user=DatabaseInformation.USER, password=DatabaseInformation.PASSWORD,
                                            host=DatabaseInformation.HOST, database=DatabaseInformation.DATABASE,
                                            buffered=True, use_unicode=True, use_pure=True)
        if self.database.is_connected():
            return
