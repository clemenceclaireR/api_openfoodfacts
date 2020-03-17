#! usr/bin/env python3
# -*- coding: utf-8 -*-


from . import querysets


class Base:
    def __init__(self, cursor):
        self.cursor = cursor
        self.categories_table = "Categories"
        self.products_table = "Products"
        self.favorites_table = "Favorites"

        self.queryset = querysets.QuerySet()


class Categories(Base):
    """
    This class represents the table Categories and its columns
    with its associated function
    """
    id = int
    name = str

    def select_all_categories(self):
        """
        request to display all the categories in the database
        """
        return self.queryset.display_categories(self.categories_table)

    def select_products_per_category(self):
        """
        request to display all the products associated to a given category
        """
        return self.queryset.display_products_for_given_categories(self.products_table, self.categories_table)


class Favorites(Base):
    """
    This class represents the table Favorites and its columns
    with its associated function
    """
    id = int
    name_alt = str
    nutriscore_alt = str
    name_source = str
    nutriscore_source = str

    def select_saved_products(self):
        """
        request to display all the previously saved products
        """
        return self.queryset.display_saved_products(self.favorites_table, self.products_table)


class Products(Base):
    """
    This class represents the table Products and its columns
    with its associated function
    """
    id = int
    name = str
    id_category = str
    brand = str
    nutriscore = str
    store = str
    link = str

    def select_all_products(self):
        """
        request to display all the products from the database
        """
        return self.queryset.display_products(self.products_table)

    def select_substitute_products(self):
        """
        request to display all the substitutes of a given product
        """
        return self.queryset.display_substitute_products(querysets.UserInput.user_product_choice)

