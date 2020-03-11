#! usr/bin/env python3
# -*- coding: utf-8 -*-


from database.db_connection import DatabaseInformation
from .request_off import UserInput
#from .querysets import CategoryQuerySet


class Base:
    def __init__(self, cursor):
        self.cursor = cursor
        # self.name = name
        self.categories_table = "Categories"


class Category(Base):
    # display categories fait par queryset, mais probleme import queryset
    # marcherait si c'était ici
    #def select_all_categories(self):
        #query = CategoryQuerySet
        #return query.display_categories(self.cursor, self.categories_table)
    name = str
    id = str

class Products(Base):
    pass

