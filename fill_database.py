import mysql.connector as mariadb
from mysql.connector import Error
from database.db_connection import DatabaseInformation
from api_openfoodfacts import api_request

database = mariadb.connect(user=DatabaseInformation.USER, password=DatabaseInformation.PASSWORD,
                           host=DatabaseInformation.HOST, database=DatabaseInformation.DATABASE,
                           buffered=True, use_unicode=True, use_pure=True)

cursor = database.cursor()

api_access = api_request.Api(cursor)


def fetch_products():
    """
    Call function to get products from the api and check
    for errors
    """
    try:
        api_access.get_products()
        print("Getting products from the Api")
    except Error as e:
        print("{}".format(e))


def keep_only_one_category():
    """
    Call function to keep one category per product and
    check for errors
    """
    try:
        api_access.delete_superfluous_categories()
        print("Keeping just one category per product")
    except Error as e:
        print("{}".format(e))


def sort_categories():
    """
    Call function to sort categories and check for errors
    """
    try:
        api_access.sort_categories()
        print("Sorting categories")
    except Error as e:
        print("{}".format(e))


def insert_categories():
    """
    Call function to insert categories in the database and
    check for errors
    """
    try:
        api_access.insert_categories(database)
        print("Inserting categories into the database")
    except Error as e:
        print("{}".format(e))


def insert_products():
    """
    Call function to insert products in the database and
    check for errors
    """
    try:
        api_access.insert_products(database)
        print("Database filled")
    except Error as e:
        print("{}".format(e))


def check_if_database_is_empty():
    """
    Check if the database is already filled or not.
    If not, it will call the data in order to fill it.
    """
    request_categories = "SELECT * FROM Categories"
    request_products = "SELECT * FROM Products"
    cursor.execute(request_categories)
    data_cat = cursor.fetchone()
    cursor.execute(request_products)
    data_prod = cursor.fetchone()
    if not data_cat and not data_prod:
        fetch_products()
        keep_only_one_category()
        sort_categories()
        insert_categories()
        insert_products()
    else:
        print("Your tables are already filled.")


check_if_database_is_empty()

