import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget

import MainActivity
from client import ChatClient
from datetime import datetime

class GroupChatActivity(QWidget):

    def __init__(self, mainWindow, parent=None):
        super(GroupChatActivity, self).__init__(parent)
        self.mainWindow = mainWindow
        self.clientInstance = ChatClient.getInstance()
        self.clientInstance.setCurrentScreen(self)
        self.initUI()
        self.clientInstance.getGroupName()
        self.clientInstance.getAllMembers()

    def initUI(self):
        hBox = QHBoxLayout()
        vBox = QVBoxLayout()
        vBoxInv = self.createInvDetails()

        chatBox = self.createChatBox()
        vBox.addLayout(chatBox)
        sendBox = self.createSendBox()
        vBox.addLayout(sendBox)


        hBox.addLayout(vBox)
        hBox.addLayout(vBoxInv)
        self.setLayout(hBox)

    def createInvDetails(self):
        vBoxInv = QVBoxLayout()
        memberLabel = QLabel("Members")
        vBoxInv.addWidget(memberLabel)

        self.memberList = QListWidget()
        vBoxInv.addWidget(self.memberList)

        invBtn = QPushButton("Invite")
        invBtn.clicked.connect(self.setInvButton)
        vBoxInv.addWidget(invBtn)

        return vBoxInv

    def createChatBox(self):
        infoChatBox = QVBoxLayout()
        self.singleLabel = QLabel(self)
        infoChatBox.addWidget(self.singleLabel)

        self.chatList = QListWidget()
        infoChatBox.addWidget(self.chatList)

        return infoChatBox

    def createSendBox(self):
        sendBox = QVBoxLayout()
        detailSendBox = self.createDetailSendBox()
        sendBox.addLayout(detailSendBox)
        closeBtn = QPushButton("Close")
        closeBtn.clicked.connect(self.setCloseButton)
        sendBox.addWidget(closeBtn)
        
        return sendBox

    def createDetailSendBox(self):
        sendMessageBox = QHBoxLayout()
        self.messageBox = QLineEdit()
        sendMessageBox.addWidget(self.messageBox)

        self.sendBtn = QPushButton("Send")
        self.sendBtn.clicked.connect(self.sendGroupMessage)
        sendMessageBox.addWidget(self.sendBtn)

        return sendMessageBox

    def setGroupName(self, name):
        self.singleLabel.setText(name)

    def setCloseButton(self):
        groupName = self.singleLabel.text()
        self.clientInstance.removeGroupConnect()
        self.clientInstance.removeFromGroupChat(groupName)
        MainActivity.MainActivity.startClientActivity(self.mainWindow)
    
    def setInvButton(self):
        MainActivity.MainActivity.startInviteActivity(self.mainWindow)

    def sendGroupMessage(self):
        msg = self.messageBox.text()
        self.messageBox.clear()
        groupName = self.singleLabel.text()
        self.clientInstance.sendGroupMessage(groupName, msg)

    def setGroupMessage(self, msg, name):
        now = datetime.now()
        currentTime = now.strftime("%H:%M")
        formatMsg = name + "(" + currentTime + "): " + msg
        self.chatList.addItem(formatMsg)

    def setAddedMembers(self, members):
        self.memberList.clear()
        for member in members:
            if member == self.clientInstance.returnName():
                myName = member + " (Me)"
                self.memberList.addItem(myName)
            else:
                self.memberList.addItem(member)
