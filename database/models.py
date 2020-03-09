#! usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
import peewee
from peewee import *
from database.db_connection import DatabaseInformation
from .request_off import UserInput

database = MySQLDatabase('openfoodfacts', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT',
                                             'use_unicode': True, 'user': DatabaseInformation.USER,
                                             'passwd': DatabaseInformation.PASSWORD})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Categories(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = 'Categories'


class Products(BaseModel):
    brands = CharField(null=True)
    id_category = ForeignKeyField(column_name='id_category', field='id', model=Categories)
    link = CharField(null=True)
    name = CharField(null=True, unique=True)
    nutriscore = CharField(null=True)
    store = CharField(null=True)

    class Meta:
        table_name = 'Products'


class Favorites(BaseModel):
    # name_alternative_product = ForeignKeyField(column_name='name_alternative_product',
    #                                          field='name', model=Products, null=True)
    name_alternative_product = CharField(null=True)
    name_source_product = CharField(null=True)
    # name_source_product = ForeignKeyField(column_name='name_source_product', field='name',
    #                                     model=Products, null=True)
    # backref='products_name_source_product_set',
    nutriscore_alternative_product = CharField(null=True)
    nutriscore_source_product = CharField(null=True)

    class Meta:
        table_name = 'Favorites'


# connection to the database
database.connect()

products_query = Products.select(Products.id, Products.name, Products.link, Products.store)
list_products_query = list(products_query)

categories_query = Categories.select()
list_categories_query = list(categories_query)

favorites_query = Favorites.select(Favorites.id, Favorites.name_alternative_product,
                                   Favorites.nutriscore_alternative_product,
                                   Favorites.name_source_product, Favorites.nutriscore_source_product, Products.store,
                                   Products.link) \
    .join(Products, on=(Products.name == Favorites.name_alternative_product))

list_favorites_query = list(favorites_query)

products_by_id_query = Products.select().where(Products.id == UserInput.user_product_choice)
list_products_by_id_query = list(products_by_id_query)


class Store:
    l_products = [[products.id, products.name] for products in list_products_query]
    l_products.sort(key=operator.itemgetter(0))

    l_categories = [[categories.id, categories.name] for categories in list_categories_query]
    l_categories.sort(key=operator.itemgetter(0))

    l_favorites = [
        [favorites.id, favorites.name_alternative_product, favorites.nutriscore_alternative_product,
         favorites.name_source_product, favorites.nutriscore_source_product,
         favorites.products.link, favorites.products.store] for favorites in list_favorites_query]
    l_favorites.sort(key=operator.itemgetter(0))








