import sys
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import ChatActivity
import GroupChatActivity
import InviteActivity
import LoginActivity
import ClientActivity
from SentInviteDialog import SentInviteDialog
from client import ChatClient


class MainActivity(QMainWindow):

    def __init__(self, parent=None):
        super(MainActivity, self).__init__(parent)
        self.startLoginActivity()
        self.clientObj = ChatClient.getInstance()
        self.clientObj.setMainWindow(self)
        self.joined = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.popUpInvite)
        self.timer.start(420)

    def popUpInvite(self):
        if self.joined:
            self.joined = False
            inviteDialog = SentInviteDialog(self)
            inviteDialog.setMessage(self.popUpRoom)
            self.popUpRoom = None
            inviteDialog.exec()
            

    def sentInvite(self, name):
        self.joined = True
        self.popUpRoom = name

    def startLoginActivity(self):
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)
        self.setWindowTitle("Login")
        self.loginStart = LoginActivity.LoginActivity(self)
        self.setCentralWidget(self.loginStart)
        self.resize(400, 300)
        self.show()

    def startClientActivity(self):
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowTitle("Chat Home")
        self.clientStart = ClientActivity.ClientActivity(self)
        self.setCentralWidget(self.clientStart)
        self.resize(800, 600)
        self.show()

    def startChatActivity(self):
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowTitle("Chat")
        self.chatStart = ChatActivity.ChatActivity(self)
        self.setCentralWidget(self.chatStart)
        self.resize(400, 600)
        self.show()

    def startGroupChatActivity(self):
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowTitle("Chat")
        self.groupChatStart = GroupChatActivity.GroupChatActivity(self)
        self.setCentralWidget(self.groupChatStart)
        self.resize(600, 600)
        self.show()

    def startInviteActivity(self):
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setWindowTitle("Invite")
        self.inviteStart = InviteActivity.InviteActivity(self)
        self.setCentralWidget(self.inviteStart)
        self.resize(300, 600)
        self.show()
        
if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = MainActivity()
    sys.exit(app.exec_())