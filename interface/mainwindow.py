#! usr/bin/env python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Substitute Finder")
        MainWindow.resize(1296, 650)
        MainWindow.setAutoFillBackground(False)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_5.setGeometry(QtCore.QRect(1200, 550, 83, 25))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(480, 470, 141, 16))
        self.label_2.setObjectName("label_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setGeometry(QtCore.QRect(480, 490, 381, 81))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(480, 50, 361, 161))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(480, 270, 361, 181))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 421, 17))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 71, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 50, 51, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser_4.setGeometry(QtCore.QRect(20, 110, 401, 131))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(20, 260, 341, 17))
        self.label_4.setObjectName("label_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 290, 71, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_6.setGeometry(QtCore.QRect(100, 290, 51, 25))
        self.pushButton_6.setObjectName("pushButton_6")
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(20, 330, 141, 17))
        self.label_5.setObjectName("label_5")
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser_5.setGeometry(QtCore.QRect(20, 360, 411, 121))
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(20, 510, 411, 17))
        self.label.setObjectName("label")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(20, 540, 71, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_7.setGeometry(QtCore.QRect(100, 540, 131, 25))
        self.pushButton_7.setObjectName("pushButton_7")
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(20, 90, 64, 17))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(880, 20, 191, 21))
        self.label_7.setObjectName("label_7")
        self.textBrowser_6 = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser_6.setGeometry(QtCore.QRect(880, 50, 381, 401))
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.label_8 = QtWidgets.QLabel(self.centralWidget)
        self.label_8.setGeometry(QtCore.QRect(480, 20, 81, 17))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralWidget)
        self.label_9.setGeometry(QtCore.QRect(480, 240, 64, 17))
        self.label_9.setObjectName("label_9")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1296, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuAPI_OpenFoodFacts = QtWidgets.QMenu(self.menuBar)
        self.menuAPI_OpenFoodFacts.setObjectName("menuAPI_OpenFoodFacts")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuAPI_OpenFoodFacts.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_5.setText(_translate("MainWindow", "Quit"))
        self.label_2.setText(_translate("MainWindow", "Connection status"))
        self.label_3.setText(_translate("MainWindow", "Enter the category\'s id of the product you would like to trade :"))
        self.pushButton_3.setText(_translate("MainWindow", "Send"))
        self.label_4.setText(_translate("MainWindow", "Enter the id of the product you would like to trade :"))
        self.pushButton_6.setText(_translate("MainWindow", "Send"))
        self.label_5.setText(_translate("MainWindow", "Substitute proposal :"))
        self.label.setText(_translate("MainWindow", "Enter the id of the altenative product you would like to save :"))
        self.pushButton_7.setText(_translate("MainWindow", "Save this product"))
        self.label_6.setText(_translate("MainWindow", "Products"))
        self.label_7.setText(_translate("MainWindow", "Previously saved products :"))
        self.label_8.setText(_translate("MainWindow", "Categories"))
        self.label_9.setText(_translate("MainWindow", "Products"))
        self.menuAPI_OpenFoodFacts.setTitle(_translate("MainWindow", "API OpenFoodFacts"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
