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
        for result in self.user_cursor.fetchall():
            count = 0
            self.msg.setText(str(result))
            self.show_dialog()
            count += 1

    def show_categories(self, table, limit, off):
        self.offset = off

        name_table = list(table.keys())
        category = name_table[0]

        # counting items in the table Categories
        self.user_cursor.execute("SELECT COUNT(*) FROM %s;" % category)

        request = ("SELECT * FROM %s ORDER BY id LIMIT %s OFFSET %s;" %
                   (category, limit, self.offset))

        self.display(request)

    def show_products(self, table, limit, off):
        self.offset = off

        name_table = list(table.keys())
        category = name_table[1]

        self.user_cursor.execute("SELECT COUNT(*) FROM %s;" % category)

        request = ("SELECT id, name, brands FROM %s ORDER BY id LIMIT %s OFFSET %s;"
                   % (category, limit, self.offset))

        self.display(request)
