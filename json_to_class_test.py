#! usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from api_openfoodfacts.api_connection import APIInformation


class NewAPIInformation:
    """
    Constants necessary in order to use the OpenFoodFacts's API
    """
    PRODUCTS_LINK = "https://fr.openfoodfacts.org/cgi/search.pl?"
    PARAMETERS = {
        "search_simple": '1',
        "action": 'process',
        "tagtype_0": 'categories',
        "tag_contains_0": 'contains',
        "page": 1,
        "page_size": 10000,
        "json": '1',
    }
    PAGE_MIN = 1
    PAGE_MAX = 20


class Categories(object):
    id = ""
    name = ""


class Products(object):
    id = ""
    name = ""
    id_category = ""
    brands = ""
    nutriscore = ""
    link = ""
    store = ""


class Favorites(object):
    id = ""
    name_source_product = ""
    nutriscore_source_product = ""
    name_alternative_product = ""
    nutriscore_alternative_product = ""
    store_alternative_product = ""
    link_alternative_product = ""


def insert_data_to_products(jsondata):
    p = Products()
    p.__dict__.update(jsondata)
    return p


def insert_data_to_categories(jsondata):
    c = Categories()
    c.__dict__.update(jsondata)
    return c


def insert_data_to_favorites(jsondata):
    f = Favorites()
    f.__dict__.update(jsondata)
    return f


def new_get_products():
    """
    Get a list of products with a request via the API.
    """

    for page in range(NewAPIInformation.PAGE_MIN, NewAPIInformation.PAGE_MAX):
        NewAPIInformation.PARAMETERS['page'] = page
        # Make the request via the API.

        # <class 'requests.models.Response'>
        # response n'a pas t'attribut read
        products_request = requests.get(NewAPIInformation.PRODUCTS_LINK,
                                        params=NewAPIInformation.PARAMETERS)

        # <class 'dict'>
        products = products_request.json()
        # sort needed information
        for element in products['products']:
            if not all(tag in element for tag in (
                    "product_name", "brands", "nutrition_grade_fr", "url", "stores",
                    "categories")):
                pass
            else:
                # convert python dict to str
                print(type(products)) # dict
                json_products = json.dumps(products) # str
                ins = json.loads(json_products, object_hook=insert_data_to_products)
                ins.get('product_name', 'brands', 'nutrition_grade_fr', 'url', 'stores',
                        ""       'categories')
                # AttributeError: 'Products' object has no attribute 'get'
        page += 1


new_get_products()
# print(Products.id)
