import select
import socket
import sys
import signal
import argparse
import ssl

from utility import *

SERVER_HOST = 'localhost'


class ChatServer(object):
    """ An example chat server using select """

    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.clientNames = ["FRIENDSLIST"]
        self.groupChats = []
        self.outputs = []  # list output sockets

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem")
        self.context.load_verify_locations('cert.pem')
        self.context.set_ciphers('AES128-SHA')

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.server.listen(backlog)
        self.server = self.context.wrap_socket(self.server, server_side=True)
        # Catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

        print(f'Server listening to port: {port} ...')

    def sighandler(self, signum, frame):
        """ Clean up client outputs"""
        print('Shutting down server...')

        # Close existing client sockets
        for output in self.outputs:
            output.close()

        self.server.close()

    def get_client_name(self, client):
        """ Return the name of the client """
        info = self.clientmap[client]
        name = info[1]
        return name

    def run(self):
        # inputs = [self.server, sys.stdin]
        inputs = [self.server]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(
                    inputs, self.outputs, [])
            except select.error as e:
                break

            for sock in readable:
                sys.stdout.flush()
                if sock == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print(
                        f'Chat server: got connection {client.fileno()} from {address}')
                    # Read the login name
                    cname = receive(client).split('NAME: ')[1]

                    # Compute client name and send back
                    self.clients += 1
                    send(client, f'CLIENT: {str(address[0])}')
                    inputs.append(client)

                    self.clientmap[client] = (address, cname)
                    self.clientNames.append(cname)
                    # send(client, self.clientNames)

                    # Send joining information to other clients
                    for output in self.outputs:
                        send(output, self.clientNames)
                    self.outputs.append(client)
                else:
                    # handle all other sockets
                    try:
                        data = receive(sock)
                        if data[0] == "DISCONNECT":
                            self.clientNames.remove(data[1])
                            print(self.clientNames)
                            for output in self.outputs:
                                if output != sock:
                                    send(output, self.clientNames)
                            self.clients -= 1
                            # remove from client names when they leave
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)
                        elif data[0] == "SINGLEMESSAGE":
                            for client in self.clientmap:
                                if data[1] == self.get_client_name(client):
                                    send(client, ["RECEIVESINGLEMESSAGE", data[2]])
                        elif data[0] == "CREATECHATROOM":
                            groupChat = ["ChatRoom by " + data[1], sock]
                            send(sock, ["SETGCNAME", groupChat[0]])
                            self.groupChats.append(groupChat)
                            for output in self.outputs:
                                if output != sock:
                                    gcList = ["ADDEDGCLIST"]
                                    for chats in self.groupChats:
                                        gcList.append(chats[0])
                                        send(output, gcList)
                        elif data[0] == "ADDTOGROUPCHAT":
                            for client in self.clientmap:
                                if data[2] == self.get_client_name(client):
                                    for chats in self.groupChats:
                                        if chats[0] == data[1]:
                                            chats.append(sock)
                                            send(sock, ["SETGCNAME", data[1]])
                        elif data[0] == "GROUPMESSAGE":
                            for chats in self.groupChats:
                                if chats[0] == data[1]:
                                    for client in chats[1::]:
                                        send(client, ["SENDGROUPMESSAGE", data[2], data[3]])
                        elif data[0] == "REMOVEME":
                            for chats in self.groupChats:
                                if chats[0] == data[1]:
                                    chats.remove(sock)
                                    print(chats)
                                    for clients in chats[1::]:
                                        names = ["MEMBERNAMES"]
                                        for people in chats[1::]:
                                            names.append(self.get_client_name(people))
                                        send(clients, names)
                        elif data[0] == "UPDATECHATROOMS":
                            gcList = ["ADDEDGCLIST"]
                            for chats in self.groupChats:
                                gcList.append(chats[0])
                            send(sock, gcList)
                        elif data[0] == "REINSTATEFRIENDS":
                            send(sock, self.clientNames)
                        elif data[0] == "GETGROUPNAME":
                            send(sock, ["CURRENTGROUPNAME", data[1]])
                        elif data[0] == "GETALLMEMBERS":
                            for chats in self.groupChats:
                                if chats[0] == data[1]:
                                    for present in chats[1::]:
                                        names = ["MEMBERNAMES"]
                                        for clients in chats[1::]:
                                            names.append(self.get_client_name(clients))
                                        print(names)
                                        send(present, names)
                        elif data[0] == "GETCONNECTEDCLIENTS":
                            for chats in self.groupChats:
                                if chats[0] == data[1]:
                                    connectedClients = ["INVITABLE"]
                                    presentClients = []
                                    for people in chats[1::]:
                                        presentClients.append(self.get_client_name(people))
                                    for client in self.clientNames[1::]:
                                        if client not in presentClients:
                                            connectedClients.append(client)
                                    send(sock, connectedClients)
                        elif data[0] == "INVITEFRIEND":
                            for client in self.clientmap:
                                if data[1] == self.get_client_name(client):
                                    send(client, ["RECEIVEINVITE", data[2]])
                    except socket.error as e:
                        # Remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)
                        
        self.server.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Socket Server Example with Select')
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    name = given_args.name

    server = ChatServer(port)
    server.run()