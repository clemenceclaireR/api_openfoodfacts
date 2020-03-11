#! usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector as mariadb
from database.db_connection import DatabaseInformation
from .models import Category


class CategoryQuerySet:
    def __init__(self):
        self.connect_db()
        self.cursor = self.database.cursor()
        self.category_access = Category(self.cursor)

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
            category.name = str(result)
            categories.append(Category)

            count += 1
        return categories

    def connect_db(self):
        if self.database.is_connected():
            return
        else:
            self.database = mariadb.connect(user=DatabaseInformation.USER, password=DatabaseInformation.PASSWORD,
                                            host=DatabaseInformation.HOST, database=DatabaseInformation.DATABASE,
                                            buffered=True, use_unicode=True, use_pure=True)
