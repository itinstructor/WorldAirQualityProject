# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 750)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.locationGroupBox = QGroupBox(self.centralwidget)
        self.locationGroupBox.setObjectName(u"locationGroupBox")
        self.formLayout = QFormLayout(self.locationGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.cityLabel = QLabel(self.locationGroupBox)
        self.cityLabel.setObjectName(u"cityLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.cityLabel)

        self.cityLineEdit = QLineEdit(self.locationGroupBox)
        self.cityLineEdit.setObjectName(u"cityLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cityLineEdit)

        self.stateLabel = QLabel(self.locationGroupBox)
        self.stateLabel.setObjectName(u"stateLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.stateLabel)

        self.stateLineEdit = QLineEdit(self.locationGroupBox)
        self.stateLineEdit.setObjectName(u"stateLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.stateLineEdit)

        self.countryLabel = QLabel(self.locationGroupBox)
        self.countryLabel.setObjectName(u"countryLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.countryLabel)

        self.countryLineEdit = QLineEdit(self.locationGroupBox)
        self.countryLineEdit.setObjectName(u"countryLineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.countryLineEdit)


        self.verticalLayout.addWidget(self.locationGroupBox)

        self.buttonWidget = QWidget(self.centralwidget)
        self.buttonWidget.setObjectName(u"buttonWidget")
        self.horizontalLayout = QHBoxLayout(self.buttonWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.currentAQIButton = QPushButton(self.buttonWidget)
        self.currentAQIButton.setObjectName(u"currentAQIButton")

        self.horizontalLayout.addWidget(self.currentAQIButton)

        self.aqiForecastButton = QPushButton(self.buttonWidget)
        self.aqiForecastButton.setObjectName(u"aqiForecastButton")

        self.horizontalLayout.addWidget(self.aqiForecastButton)


        self.verticalLayout.addWidget(self.buttonWidget)

        self.resultsTextEdit = QTextEdit(self.centralwidget)
        self.resultsTextEdit.setObjectName(u"resultsTextEdit")
        font = QFont()
        font.setFamilies([u"Courier New"])
        font.setPointSize(10)
        self.resultsTextEdit.setFont(font)

        self.verticalLayout.addWidget(self.resultsTextEdit)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"World Air Quality Index", None))
        self.locationGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Location Input", None))
        self.cityLabel.setText(QCoreApplication.translate("MainWindow", u"City:", None))
        self.stateLabel.setText(QCoreApplication.translate("MainWindow", u"State:", None))
        self.countryLabel.setText(QCoreApplication.translate("MainWindow", u"Country:", None))
        self.currentAQIButton.setText(QCoreApplication.translate("MainWindow", u"Get Current AQI", None))
        self.aqiForecastButton.setText(QCoreApplication.translate("MainWindow", u"Get AQI Forecast", None))
    # retranslateUi

