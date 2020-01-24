# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'saved_products.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(676, 320)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_5.setGeometry(QtCore.QRect(460, 210, 83, 25))
        self.pushButton_5.setObjectName("pushButton_5")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 221, 21))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(570, 210, 83, 25))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 40, 611, 151))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 676, 22))
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
        self.pushButton_5.setText(_translate("MainWindow", "Back"))
        self.label.setText(_translate("MainWindow", "Your previously saved products :"))
        self.pushButton.setText(_translate("MainWindow", "Quit"))
        self.menuAPI_OpenFoodFacts.setTitle(_translate("MainWindow", "API OpenFoodFacts"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
