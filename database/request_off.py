#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from PyQt5.QtWidgets import QMessageBox


class Request:
    def __init__(self, cursor):
        self.msg = QMessageBox()
        self.user_cursor = cursor

        # from which row to start
        self.offset = 0

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def display(self, request):
        """
        display results for the different menus
        """
        self.user_cursor.execute(request)
        for result in self.user_cursor.fetchall(): # liste vide
            count = 0
            self.msg.setText(result[count])
            self.show_dialog()
            count += 1

    def show_categories(self, table, limit, off):
        self.offset = off

        name_table = list(table.keys())
        category = name_table[0]

        # counting items in the table Categories

        self.user_cursor.execute("SELECT COUNT(*) FROM %s;" % category) # ici, arrive à lire les données de l'API

        request = ("SELECT * FROM %s ORDER BY id LIMIT %s OFFSET %s;" %
                   (category, limit, self.offset)) # ici, renvoie une liste vide.

        self.display(request)
