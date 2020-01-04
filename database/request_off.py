#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from PyQt5.QtWidgets import QMessageBox


class Request:
    def __init__(self, cursor, database):
        self.msg = QMessageBox()
        self.user_cursor = cursor
        self.user_database = database

        # connexion avec la base de données
        self.running = False
        # from which row to start
        self.offset = 0

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()

    def display(self, request):
        """
        display results for the different menus
        """
        self.running = True
        while self.running:
            # make request
            self.user_cursor.execute(request)
            for result in self.user_cursor.fetchall():
                count = 0
                while count < len(result):
                    self.msg.setText(result[count])
                    count += 1

    def show_categories(self, table, limit):
        self.running = True
        while self.running:
            name_table = list(table.keys())
            category = name_table[0]

            # counting items in the table Category
            self.user_cursor.execute("SELECT COUNT(*) FROM {};".format(category))
            for num in self.user_cursor.fetchone():
                total = num

            request = ("SELECT * FROM %s ORDER BY id LIMIT {}\
                            OFFSET {};".format(category, limit, self.offset))






