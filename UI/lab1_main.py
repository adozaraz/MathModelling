# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lab1_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(560, 10, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.currentTime = QtWidgets.QTextBrowser(self.centralwidget)
        self.currentTime.setGeometry(QtCore.QRect(660, 10, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.currentTime.setFont(font)
        self.currentTime.setObjectName("currentTime")
        self.pyplotGraph = QtWidgets.QWidget(self.centralwidget)
        self.pyplotGraph.setGeometry(QtCore.QRect(10, 10, 531, 541))
        self.pyplotGraph.setObjectName("pyplotGraph")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(620, 530, 121, 23))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.menu.setFont(font)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.newSystem = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.newSystem.setFont(font)
        self.newSystem.setObjectName("newSystem")
        self.saveSystem = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.saveSystem.setFont(font)
        self.saveSystem.setObjectName("saveSystem")
        self.openSystem = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.openSystem.setFont(font)
        self.openSystem.setObjectName("openSystem")
        self.planetParameters = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        self.planetParameters.setFont(font)
        self.planetParameters.setObjectName("planetParameters")
        self.menu.addAction(self.newSystem)
        self.menu.addAction(self.saveSystem)
        self.menu.addAction(self.openSystem)
        self.menu.addSeparator()
        self.menu.addAction(self.planetParameters)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Текущее время"))
        self.pushButton.setText(_translate("MainWindow", "Начать симуляцию"))
        self.menu.setTitle(_translate("MainWindow", "Файл"))
        self.newSystem.setText(_translate("MainWindow", "Новая система"))
        self.saveSystem.setText(_translate("MainWindow", "Сохранить"))
        self.openSystem.setText(_translate("MainWindow", "Открыть"))
        self.planetParameters.setText(_translate("MainWindow", "Параметры планет"))
