import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget

import MainActivity
from client import ChatClient

class InviteActivity(QWidget):

    def __init__(self, mainWindow, parent=None):
        super(InviteActivity, self).__init__(parent)
        self.mainWindow = mainWindow
        self.clientInstance = ChatClient.getInstance()
        self.clientInstance.setCurrentScreen(self)
        self.initUI()
        self.clientInstance.getConnectedClients()

    def initUI(self):
        vBox = self.createInviteBox()
        self.setLayout(vBox)

    def createInviteBox(self):
        invBox = QVBoxLayout()
        clientLabel = QLabel("Connected Clients")
        invBox.addWidget(clientLabel)

        self.clientList = QListWidget()
        invBox.addWidget(self.clientList)

        hBox = QHBoxLayout()
        self.invBtn = QPushButton("Invite")
        self.invBtn.clicked.connect(self.inviteMember)
        cancelBtn = QPushButton("Cancel")
        cancelBtn.clicked.connect(self.setCancel)
        hBox.addWidget(self.invBtn)
        hBox.addWidget(cancelBtn)
        
        invBox.addLayout(hBox)

        return invBox

    def setCancel(self):
        MainActivity.MainActivity.startGroupChatActivity(self.mainWindow)

    def addConnectedMembers(self, clients):
        self.clientList.clear()
        self.clientList.addItems(clients)
    
    def inviteMember(self):
        person = self.clientList.currentItem()
        if person is not None:
            self.clientInstance.inviteFriend(person.text())
        MainActivity.MainActivity.startGroupChatActivity(self.mainWindow)

        