#! usr/bin/env python3
# -*- Coding: UTF-8 -*-


class APIInformation:
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
