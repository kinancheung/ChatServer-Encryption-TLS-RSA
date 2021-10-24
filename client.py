import select
import socket
import sys
import signal
import argparse
import threading
import ssl

from utility import *
import MainActivity

SERVER_HOST = 'localhost'

stop_thread = False

def get_and_send(client):
    while not stop_thread:
        data = sys.stdin.readline().strip()
        if data:
            send(client.sock, data)


class ChatClient():
    clientInstance = None

    """ A command line chat client using select """
    def __init__(self, host=SERVER_HOST):
        if ChatClient.clientInstance == None:
            ChatClient.clientInstance = self
            self.connected = False
            self.host = host
            self.friendsList = []
            self.groupChats = []
            self.groupChats = None
            self.singleConnected = False
            self.groupConnected = False

    @staticmethod
    def getInstance():
        if ChatClient.clientInstance == None:
            ChatClient()
        return ChatClient.clientInstance

    def setConnection(self, port, host, nickName):
        self.port = port
        self.host = host
        self.name = nickName
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

        # Initial prompt
        self.prompt = f'[{self.name}@{socket.gethostname()}]> '
        
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = self.context.wrap_socket(
                self.sock, server_hostname=host)

            self.sock.connect((self.host, self.port))
            print(f'Now connected to chat server@ port {self.port}')
            self.connected = True
            
            # Send my name...
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)

            # Contains client address, set it
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[' + '@'.join((self.name, addr)) + ']> '
            MainActivity.MainActivity.startClientActivity(self.mainWindow)
            try:
                threading.Thread(target=self.run).start()
            except Exception as e:
                print(e)
            
        except socket.error as e:
            print(f'Failed to connect to chat server @ port {self.port}')
            sys.exit(1)

    def cleanup(self):
        """Close the connection and wait for the thread to terminate."""
        self.sock.close()

    def run(self):
        """ Chat client main loop """
        while self.connected:
            try:
                # Wait for input from stdin and socket
                readable, writeable, exceptional = select.select(
                    [self.sock], [], [])

                for sock in readable:
                    if sock == self.sock:
                        data = receive(self.sock)
                        print(data)
                        if data[0] == "FRIENDSLIST":
                            self.calculateClients(data)
                            self.currentScreen.setFriendsList(self.friendsList)
                        elif data[0] == "RECEIVESINGLEMESSAGE":
                            if(self.singleConnected == True):
                                self.currentScreen.addToChatList(self.singleFriend, data[1])
                        elif data[0] == "SENDGROUPMESSAGE":
                            self.currentScreen.setGroupMessage(data[1], data[2])
                        elif data[0] == "SETGCNAME":
                            self.currentGroup = data[1]
                        elif data[0] == "CURRENTGROUPNAME":
                            self.currentScreen.setGroupName(data[1])
                        elif data[0] == "ADDEDGCLIST":
                            if(self.groupConnected == False):
                                self.currentScreen.updateGCList(data[1::])
                        elif data[0] == "MEMBERNAMES":
                            self.currentScreen.setAddedMembers(data[1::])
                        elif data[0] == "INVITABLE":
                            self.currentScreen.addConnectedMembers(data[1::])
                        elif data[0] == "RECEIVEINVITE":
                            self.mainWindow.sentInvite(data[1])
                        elif data[0] == "CSINGLE":
                            self.singleConnected = True
            except KeyboardInterrupt:
                print(" Client interrupted. """)
                self.cleanup()
                break
    
    def calculateClients(self, data):
        self.friendsList.clear()
        for client in data:
            if not client in self.friendsList:
                self.friendsList.append(client)

    def setCurrentScreen(self, screen):
        self.currentScreen = screen
    
    def getCurrentScreen(self):
        return self.currentScreen

    def setMainWindow(self, window):
        self.mainWindow = window
    
    def setGroupConnect(self):
        self.groupConnected = True

    def removeGroupConnect(self):
        self.groupConnected = False

    def returnName(self):
        return self.name
    
    def removeFromFriendsList(self):
        send(self.sock, ["DISCONNECT", self.name])

    def setOneFriend(self, person):
        self.singleFriend = person
        self.singleConnected = True

    def getOneFriend(self):
        return self.singleFriend

    def removeOneFriend(self):
        self.singleFriend = None

    def removeMyself(self):
        self.singleConnected = False

    def sendSingleMessage(self, msg):
        if(self.singleConnected == True):
            self.currentScreen.addToChatList(self.name, msg)
        if(self.singleFriend != None):
            send(self.sock, ["SINGLEMESSAGE", self.singleFriend, msg])

    def createChatRoom(self, name):
        send(self.sock, ["CREATECHATROOM", name])

    def addToGroupChat(self, groupName):
        send(self.sock, ["ADDTOGROUPCHAT", groupName, self.name])

    def sendGroupMessage(self, groupChat, msg):
        send(self.sock, ["GROUPMESSAGE", groupChat, msg, self.name])

    def removeFromGroupChat(self, groupName):
        send(self.sock, ["REMOVEME", groupName])

    def updateChatRooms(self):
        send(self.sock, ["UPDATECHATROOMS"])

    def reinstateFriends(self):
        send(self.sock, ["REINSTATEFRIENDS"])

    def getGroupName(self):
        send(self.sock, ["GETGROUPNAME", self.currentGroup])

    def getAllMembers(self):
        send(self.sock, ["GETALLMEMBERS", self.currentGroup])

    def getConnectedClients(self):
        send(self.sock, ["GETCONNECTEDCLIENTS", self.currentGroup])

    def inviteFriend(self, friend):
        send(self.sock, ["INVITEFRIEND", friend, self.currentGroup])

    def getInvitee(self):
        return self.invitee



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()

    port = given_args.port
    name = given_args.name

    client = ChatClient(name=name, port=port)