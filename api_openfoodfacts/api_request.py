#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import requests
from .api_connection import APIInformation


class ProgramStatus:
    message_list = list()


class Api:
    """
    This class will make the connection with the OpenFoodFacts API.
    It will make the different requests needed to create a list of products and categories.
    """

    def __init__(self, cursor):
        self.categories = list()
        self.sorted_categories = list()
        self.parsed_categories = list()
        self.parsed_products = list()
        self.id_name = list()
        self.user_cursor = cursor

    def get_products(self):
        """
        Get a list of products with a request via the API.
        """

        for page in range(APIInformation.PAGE_MIN, APIInformation.PAGE_MAX):
            APIInformation.PARAMETERS['page'] = page
            # Make the request via the API.
            products_request = requests.get(APIInformation.PRODUCTS_LINK,
                                            params=APIInformation.PARAMETERS)
            products = products_request.json()
            # sort needed information
            for element in products['products']:
                if not all(tag in element for tag in (
                        "product_name", "brands", "nutrition_grade_fr", "url", "stores",
                        "categories")):
                    pass
                else:
                    self.parsed_products.append(element)
            page += 1

    def delete_superfluous_categories(self):
        """
        Delete superfluous categories associated to a product
        in order to keep just one
        """
        text = list()
        for i in self.parsed_products:
            # Splitting string
            head, mid, end = i['categories'].partition(',')
            text.append(head)

        counter = 0
        while counter < (len(text) - 1):
            for j in self.parsed_products:
                j['categories'] = text[counter]
                counter += 1

    def sort_categories(self):
        """
        Extract category from the parsed product list
        and add it to a list of categories
        """
        categories = list()
        for element in self.parsed_products:
            categories.append(element['categories'])

        self.sorted_categories = sorted(set(categories))
        ProgramStatus.message_list.append("Categories sorted successfully")
        return self.sorted_categories

    def insert_categories(self, database):
        """
        Insert the categories into the database
        """
        for element in self.sorted_categories:
            # rows with invalid data that cause the error are ignored
            self.user_cursor.execute("INSERT IGNORE INTO Categories(name) VALUES ('%s')"
                                     % element)
        database.commit()
        ProgramStatus.message_list.append("Categories inserted successfully.")

    def get_categories_name_and_ids(self):
        """
        Get the id and the name of a category in the Categories table
        and save it into a list
        """
        self.id_name = list()
        count = 0
        while count < len(self.sorted_categories):
            category = str(count + 1)
            self.user_cursor.execute("SELECT id, name FROM Categories WHERE id = %s;" % category)
            category_saved = self.user_cursor.fetchone()
            self.id_name.append(category_saved)
            count += 1
        return self.id_name

    def convert_categories_to_product_list(self):
        """
        get the name of categories and get its number
        in order to use it for the products in the
        insert_products function
        """
        self.get_categories_name_and_ids()
        ids = range(0, len(self.id_name))

        for n in ids:
            for product in self.parsed_products:
                if product['categories'] == self.id_name[n][1]:  # name
                    product['categories'] = self.id_name[n][0]  # ID

        return self.parsed_products

    def insert_products(self, database):
        """
        Get products and save them into database
        """
        self.convert_categories_to_product_list()
        for element in self.parsed_products:
            self.user_cursor.execute("INSERT IGNORE INTO Products(\
                name, id_category, brands, nutriscore, link, store) VALUES(\
                %s, %s, %s, %s, %s, %s)", (
                element['product_name'], element['categories'],
                element['brands'], element['nutrition_grade_fr'],
                element['url'], element['stores']))

        ProgramStatus.message_list.append("Products inserted successfully in the database.")
        database.commit()
