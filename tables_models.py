#! usr/bin/env python3
# -*- coding: utf-8 -*-

import peewee
from peewee import *

database = MySQLDatabase('openfoodfacts', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT',
                                             'use_unicode': True, 'user': 'user', 'passwd': 'off2019'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Categories(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = 'categories'


class Products(BaseModel):
    id = PrimaryKeyField(null=False)
    brands = CharField(null=True)
    id_category = ForeignKeyField(column_name='id_category', field='id', model=Categories)
    link = CharField(null=True)
    name = CharField(null=True, unique=True)
    nutriscore = CharField(null=True)
    store = CharField(null=True)

    class Meta:
        table_name = 'products'


class Favorites(BaseModel):
    #link_alternative_product = CharField(null=True)
    name_alternative_product = ForeignKeyField(column_name='name_alternative_product',
                                               field='name', model=Products, null=True)
    name_source_product = ForeignKeyField(backref='products_name_source_product_set',
                                          column_name='name_source_product', field='name',
                                          model=Products, null=True)
    nutriscore_alternative_product = CharField(null=True)
    nutriscore_source_product = CharField(null=True)
    #store_alternative_product = CharField(null=True)

    class Meta:
        table_name = 'favorites'


# connection to the database

database.connect() # ok



products_query = Products.select(Products.id, Products.name)
list_products_query = list(products_query)
#categories_query = Categories.select()
#favorites_query = Favorites.select()


#l_products = [[products.id, products.name] for products in list_products_query]

#id_products = [products.id for products in products_query]
#print(l_products)


