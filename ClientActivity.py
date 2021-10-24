import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox, QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget

import MainActivity
from client import ChatClient

class ClientActivity(QWidget):

    def __init__(self, mainWindow, parent=None):
        super(ClientActivity, self).__init__(parent)
        self.clientInstance = ChatClient.getInstance()
        self.mainWindow = mainWindow
        self.clientInstance.setCurrentScreen(self)
        self.initUI()
        self.clientInstance.updateChatRooms()
        self.clientInstance.reinstateFriends()

    def initUI(self):
        vBox = QVBoxLayout()
        connectLabel = self.createConnectLabel()
        connectedClients = self.createConnectedLayout()
        friendLabel = self.createFriendsLabel()
        chatRoomInfo = self.createChatRoomLayout()
        vBox.addWidget(connectLabel)
        vBox.addLayout(connectedClients)
        vBox.addWidget(friendLabel)
        vBox.addLayout(chatRoomInfo)
        self.setLayout(vBox)

    def createConnectLabel(self):
        connectLabel = QLabel("Connected Clients")
        connectLabel.font().setPointSize(20)
        return connectLabel

    def createConnectedLayout(self):
        friendsBox = QHBoxLayout()
        self.connectCombo = QListWidget()
        self.connectCombo.itemClicked.connect(self.oneToOneChanged)
        self.connectButton = QPushButton("1:1 Chat")
        self.connectButton.clicked.connect(self.joinSingleChat)
        friendsBox.addWidget(self.connectCombo)
        friendsBox.addWidget(self.connectButton)

        return friendsBox

    def joinSingleChat(self):
        person = self.connectCombo.currentItem()
        if person is not None:
            self.clientInstance.setGroupConnect()
            self.clientInstance.setOneFriend(person.text())
            MainActivity.MainActivity.startChatActivity(self.mainWindow)

    def oneToOneChanged(self, item):
        me = self.clientInstance
        self.selectedPerson = item.text()
        if(self.selectedPerson == me.returnName()+" (Me)"):
            self.connectButton.setDisabled(True)
        else:
            #put logic for if people are already in chat?
            self.connectButton.setDisabled(False)


    def createFriendsLabel(self):
        chatLabel = QLabel("Chat rooms (Group chat)")
        return chatLabel

    def createChatRoomLayout(self):
        roomsBox = QHBoxLayout()
        self.roomsCombo = QListWidget()
        roomsBox.addWidget(self.roomsCombo)

        btnsSelection = self.createBtnSelection()
        roomsBox.addLayout(btnsSelection)

        return roomsBox

    def createBtnSelection(self):
        btnContainer = QVBoxLayout()
        createBtn = QPushButton("Create")
        createBtn.clicked.connect(self.createChatRoom)

        joinBtn = QPushButton("Join")
        joinBtn.clicked.connect(self.joinChatRoom)

        closeBtn = QPushButton("Close")
        closeBtn.clicked.connect(self.returnToLogin)

        btnContainer.addWidget(createBtn)
        btnContainer.addWidget(joinBtn)
        btnContainer.addWidget(closeBtn)
        
        return btnContainer

    def createChatRoom(self):
        myName = self.clientInstance.returnName()
        self.clientInstance.setGroupConnect()
        self.clientInstance.createChatRoom(myName)
        MainActivity.MainActivity.startGroupChatActivity(self.mainWindow)

    def joinChatRoom(self):
        groupChat = self.roomsCombo.currentItem()
        if groupChat is not None:
            self.clientInstance.setGroupConnect()
            self.clientInstance.addToGroupChat(groupChat.text())
        MainActivity.MainActivity.startGroupChatActivity(self.mainWindow)

    
    def returnToLogin(self):
        # make sure to remove user from map here
        self.clientInstance.removeFromFriendsList()
        MainActivity.MainActivity.startLoginActivity(self.mainWindow)
    

    def setFriendsList(self, friendsList):
        me = self.clientInstance
        self.connectCombo.clear()
        for people in friendsList[1::]:
            if people == me.returnName():
                myName = people + " (Me)"
                self.connectCombo.addItem(myName)
            else:
                self.connectCombo.addItem(people)
    
    def updateGCList(self, gcList):
        self.roomsCombo.clear()
        self.roomsCombo.addItems(gcList)