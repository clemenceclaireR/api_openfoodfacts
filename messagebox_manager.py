#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets


class Message:
    def __init__(self):
        self.msg = QMessageBox()

    def show_dialog(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.exec_()