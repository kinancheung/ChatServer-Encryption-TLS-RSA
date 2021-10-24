import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QPushButton,  QVBoxLayout

import MainActivity
from client import ChatClient

class SentInviteDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.clientInstance = ChatClient.getInstance()
        self.parent = parent

        self.setWindowTitle("INVITED!!!")

        self.okBtn = QPushButton("Accept")
        self.noBtn = QPushButton("Reject")
        self.okBtn.clicked.connect(self.accept)
        self.noBtn.clicked.connect(self.reject)
        self.vBox = QVBoxLayout()
        self.inviteMessage = QLabel(self)

        self.buttonBox = QHBoxLayout()
        self.buttonBox.addSpacing(1)
        self.buttonBox.addWidget(self.okBtn)
        self.buttonBox.addWidget(self.noBtn)
        self.buttonBox.addSpacing(1)

        self.vBox.addWidget(self.inviteMessage)
        self.vBox.addLayout(self.buttonBox)
        self.setLayout(self.vBox)



    def accept(self):
        connected = self.clientInstance.getOneFriend()
        if(connected != None):
            client = self.clientInstance.getCurrentScreen()
            client.sendLeaveMessage()
        self.clientInstance.removeOneFriend()
        self.clientInstance.removeMyself()
        self.clientInstance.setGroupConnect()
        self.clientInstance.addToGroupChat(self.groupName)
        MainActivity.MainActivity.startGroupChatActivity(self.parent)
        self.done(1)

    def reject(self):
        self.done(1)

    def setMessage(self, groupName):
        self.groupName = groupName
        self.inviteMessage.setText("You have been invited to join " + groupName)