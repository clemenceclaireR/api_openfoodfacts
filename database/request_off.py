#! usr/bin/env python3
# -*- Coding: UTF-8 -*-


class ProgramStatus:
    message_list = list()


class UserInput:
    product_to_register = int
    user_category_choice = int
    user_product_choice = int


class ListProducts:
    list_categories = list()
    list_products = list()
    list_products_for_given_category = list()
    list_saved_products = list()
    substitute = list()


class SubstituteManager:
    nutriscore = ""
    product_name = ""


class Request:
    """
    This class contains the methods which will interact
    with the database in order to get and display informations
    """

    def __init__(self, cursor, database):
        self.cursor = cursor
        self.database = database

    def display_categories(self, request):
        """
        display the list of categories from the database
        """
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            ListProducts.list_categories.append(str(result))
            count += 1

    def display_products(self, request):
        """
        display the list of products from the database
        """
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            ListProducts.list_products.append(str(result))
            count += 1

    def display_products_for_given_categories(self, request):
        """
        display the products associated to a given category
        """
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            ListProducts.list_products_for_given_category.append(str(result))
            count += 1

    def display_substitute(self, request, category, nutriscore):
        """
        display substitutes for a given product
        """
        self.cursor.execute(request, (category, nutriscore))
        for result in self.cursor.fetchall():
            count = 0
            ListProducts.substitute.append(str(result))
            count += 1

    def display_saved_products(self, request):
        """
        display previously saved products
        """
        self.cursor.execute(request)
        for result in self.cursor.fetchall():
            count = 0
            ListProducts.list_saved_products.append(str(result))
            count += 1

    def show_saved_products(self):
        """
        Ask the database for all the entries from the Favorite table
        and display it
        """
        request = "SELECT * FROM Favorites"
        self.display_saved_products(request)

    def show_categories(self, table):
        """
        Get the keys from a given table in order to get
        its name and ask the database for its entries,
        then display it
        """
        name_table = list(table.keys())
        category = name_table[0]

        # counting items in the table Categories
        self.cursor.execute("SELECT COUNT(*) FROM %s;" % category)

        request = ("SELECT * FROM %s ORDER BY id;" %
                   category)

        self.display_categories(request)

    def show_products(self, table):
        """
        Get the keys from a given tame in order to get
        its name and ask the database for its entries,
        then display it
        """
        name_table = list(table.keys())
        category = name_table[1]

        self.cursor.execute("SELECT COUNT(*) FROM %s;" % category)

        request = ("SELECT id, name, brands FROM %s ORDER BY id;"
                   % category)

        self.display_products(request)

    def find_products_for_a_given_category(self):
        """
        Ask the database for products information for a given category
        ans display it
        """
        request = ("SELECT OFFProducts.id, OFFProducts.name, brands, nutriscore \
                   FROM Products as OFFProducts \
                   INNER JOIN Categories \
                   ON OFFProducts.id_category = Categories.id \
                   WHERE Categories.id = %s \
                   ORDER BY OFFProducts.id;" % UserInput.user_category_choice)

        self.display_products_for_given_categories(request)

    #def find_healthier_substitute(self, category, product):
    def find_healthier_substitute(self,  product):
        """
        Ask the database for the products from the same
        category that the user selected, but with a higher nutriscore
        then display it
        :param category: category associated by the product selected by the user
        :param product:  product to substitute selected by the user
        """
        # save product into a variable
        self.cursor.execute("SELECT * FROM Products \
                                WHERE Products.id = " + product)
        SubstituteManager.information = self.cursor.fetchone()
        SubstituteManager.nutriscore = str(SubstituteManager.information[4])
        SubstituteManager.product_name = str(SubstituteManager.information[1])
        SubstituteManager.associated_category = str(SubstituteManager.information[2])

        request = ("SELECT Products.id, Products.name, Products.nutriscore, \
                   Products.store, Products.brands, Products.link \
                   FROM Products INNER JOIN Categories \
                   ON Products.id_category = Categories.id \
                   WHERE Categories.id = %s \
                   AND Products.nutriscore < %s \
                   ORDER BY Products.nutriscore")

        self.display_substitute(request, SubstituteManager.associated_category, SubstituteManager.nutriscore)

    def save_product(self, prodtosave):
        """
        Get from the database the needed information for the
        product selected by the user and insert it in the Favorites table
        :param prodtosave: get the id of the product to save
        """
        # Get the product and save it into a variable
        self.cursor.execute("SELECT * FROM Products WHERE Products.id = %s " % prodtosave)
        information = self.cursor.fetchone()
        sub_name = information[1]
        new_nutriscore = information[4]
        new_link = information[5]
        new_store = information[6]
        source_product_name = SubstituteManager.product_name
        source_product_nutriscore = SubstituteManager.nutriscore

        save_request = ("INSERT INTO Favorites \
                                        (name_source_product, nutriscore_source_product, name_alternative_product, \
                                        nutriscore_alternative_product, store_alternative_product, \
                                        link_alternative_product) \
                                        VALUES (%s, %s, %s, %s, %s, %s);")

        self.cursor.execute(save_request, (source_product_name, source_product_nutriscore, sub_name,
                                           new_nutriscore, new_store, new_link))
        # Save changes
        self.database.commit()
