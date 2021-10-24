import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

import MainActivity
from client import ChatClient

class LoginActivity(QWidget):

    def __init__(self, mainWindow, parent=None):
        super(LoginActivity, self).__init__(parent)
        self.mainWindow = mainWindow
        self.clientInstance = ChatClient.getInstance()
        self.clientInstance.setCurrentScreen(self)
        self.initUI()

    def initUI(self):
        vBox = QVBoxLayout()
        loginGrid = self.createLoginFields()
        loginButtons = self.createLoginButtons()
        vBox.addLayout(loginGrid)
        vBox.addLayout(loginButtons)
        self.setLayout(vBox)

    def createLoginFields(self):
        grid = QGridLayout()
        grid.addWidget(QLabel("IP Address"), 0, 0)
        grid.addWidget(QLabel("Port"), 1, 0)
        grid.addWidget(QLabel("Nick Name"), 2, 0)

        self.connection = QLineEdit()
        self.port = QLineEdit()
        self.nickName = QLineEdit()
        grid.addWidget(self.connection, 0, 1)
        grid.addWidget(self.port, 1, 1)
        grid.addWidget(self.nickName, 2, 1)

        return grid

    def createLoginButtons(self):
        hBox = QHBoxLayout()
        connectBtn = QPushButton("Connect")
        connectBtn.clicked.connect(self.switchButtonHandler)
        cancelBtn = QPushButton("Cancel")
        cancelBtn.clicked.connect(QCoreApplication.instance().quit)

        hBox.addStretch(1)
        hBox.addWidget(connectBtn)
        hBox.addWidget(cancelBtn)
        hBox.addStretch(1)

        return hBox

    def switchButtonHandler(self):
        host = self.connection.text()
        port = int(self.port.text())
        nickName = self.nickName.text()
        
        ChatClient.setConnection(self.clientInstance, port, host, nickName)

        
        