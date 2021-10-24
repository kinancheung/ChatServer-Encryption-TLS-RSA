import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget
from ClientActivity import ClientActivity

import MainActivity
from client import ChatClient
from datetime import datetime


class ChatActivity(QWidget):

    def __init__(self, mainWindow, parent=None):
        super(ChatActivity, self).__init__(parent)
        self.mainWindow = mainWindow
        self.clientInstance = ChatClient.getInstance()
        self.clientInstance.setCurrentScreen(self)
        self.initUI()
        self.sendJoinMessage()

    def initUI(self):
        vBox = QVBoxLayout()
        chatBox = self.createChatBox()
        vBox.addLayout(chatBox)
        sendBox = self.createSendBox()
        vBox.addLayout(sendBox)
        self.setLayout(vBox)

    def createChatBox(self):
        infoChatBox = QVBoxLayout()
        # insert a name here
        singleLabel = QLabel("Chat with " + self.clientInstance.getOneFriend())
        singleLabel.font().setPointSize(20)
        infoChatBox.addWidget(singleLabel)

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
        self.sendBtn.clicked.connect(self.sendMessage)
        sendMessageBox.addWidget(self.sendBtn)

        return sendMessageBox

    def setCloseButton(self):
        self.clientInstance.removeMyself()
        self.clientInstance.removeGroupConnect()
        self.sendLeaveMessage()
        self.clientInstance.removeOneFriend()
        MainActivity.MainActivity.startClientActivity(self.mainWindow)

    def sendMessage(self):
        msg = self.messageBox.text()
        self.messageBox.clear()
        self.clientInstance.sendSingleMessage(msg)

    def sendJoinMessage(self):
        msg = "User has Joined the Chat"
        self.clientInstance.sendSingleMessage(msg)

    def sendLeaveMessage(self):
        msg = "User has Left the Chat"
        self.clientInstance.sendSingleMessage(msg)

    def addToChatList(self, name, msg):
        now = datetime.now()
        currentTime = now.strftime("%H:%M")
        formatMsg = name + "(" + currentTime + "): " + msg
        self.chatList.addItem(formatMsg)