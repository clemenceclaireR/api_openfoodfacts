#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

import mysql.connector
from menu import *
from db_connection import *
from mysql.connector import errorcode
from database import *

# TODO : creer un fichier py pour creer la liste des categories et des produits d'OFF
# TODO: creer un fichier.py qui creera la base de donnee


class Main:
    """
    Main program which will interacts with the API and the database
    """
    def __init__(self):
        # Connection with the database
        try:
            self.db = mysql.connector.connect(
                user=USER,
                password=PASSWORD,
                host=HOST)
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("User name or password incorrect")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not seem to exist")
            else:
                print("Connection failed with following error : {}".format(error))
        else:
            # creating cursor
            self.cursor = self.db.cursor()

    def menu(self):
        """
        Display menu and submenus
        """
        while 1:
            print(MAIN_MENU_TEXT)
            try :
                choice=int(input())
                if choice == 1:
                    # show categories
                    pass
                elif choice == 2:
                    # shows products
                    pass
                elif choice == 3:
                    # show substiute menu
                    pass
                elif choice == 4:
                    # show recorded products
                    pass
                elif choice == 5:
                    quit()
            except ValueError:
                print("Please enter a number between 1 and 5.")


def display_menu():
    print(MAIN_MENU_TEXT)

display_menu()
