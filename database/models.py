#! usr/bin/env python3
# -*- coding: utf-8 -*-


from . import querysets


class Base:
    def __init__(self, cursor):
        self.cursor = cursor
        # self.name = name
        self.categories_table = "Categories"
        self.products_table = "Products"
        self.favorites_table = "Favorites"

        self.queryset = querysets.QuerySet()


class Categories(Base):
    id = int
    name = str

    def select_all_categories(self):
        return self.queryset.display_categories(self.categories_table)

    def select_products_per_category(self):
        return self.queryset.display_products_for_given_categories(self.products_table, self.categories_table)


class Favorites(Base):
    id = int
    name_alt = str
    nutriscore_alt = str
    name_source = str
    nutriscore_source = str

    def select_saved_products(self):
        return self.queryset.display_saved_products(self.favorites_table, self.products_table)


class Products(Base):
    id = int
    name = str
    id_category = str
    brand = str
    nutriscore = str
    store = str
    link = str

    def select_all_products(self):
        return self.queryset.display_products(self.products_table)

    def select_substitute_products(self):
        return self.queryset.display_substitute_products(querysets.UserInput.user_product_choice)

