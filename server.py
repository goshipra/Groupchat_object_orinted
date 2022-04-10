import socket  # Importing for server connection
import json   # Importing json
import _thread    # Importing Thread


class ServerConnection:
    """
    Starting the server to establish the connection between users
    """

    def __init__(self):
        self.host = 'localhost'
        self.port = 5000
        self.clients = []
        self.clients_name = []
        self.message ={}

    def establishing_connection(self):
        """ Establishing server connection
        """
        print("Establishing connection method")
        server_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_obj.bind((self.host, self.port))
        server_obj.listen(10)
        while True:
            try:
                c, ad = server_obj.accept()
                print('Connection Established On Server',c,ad)
                self.clients.append(c)
                _thread.start_new_thread(self.connectnewclient,(c,))
            except Exception as e:
                # print("Exception Occured: ",e)
                continue

    def sendtoall(self,msg):
        """ send to all method which send message to everyone on the chat
        """
        print("sendtoall method")
        for client in self.clients:
            client.send(msg.encode('utf-8'))

    def connectnewclient(self,c):
        """ connect new clients to the chat window and update them in the active users list"""
        print("connectnewclient method")
        while True:
            try:
                # Receiving Data from Clients:
                self.message = c.recv(2048).decode('utf-8')
                j = self.message.replace("'","\"")
                d = json.loads(j)
                print("this is d:",d)

                # Alerting If The Client Is Online Or Offline
                if d['alert'] == 'Online':
                    self.clients_name.append(d['username'])
                elif d['alert'] == 'Offline':
                    self.clients_name.pop(self.clients_name.index(d['username']))
                    self.clients.pop(self.clients.index(c))

                # Private Message to Selected receiver
                if 'receiver' in d:
                    # Find right socket
                    index = self.clients_name.index(d['receiver'])
                    receiverSocket = self.clients[index]
                    receiverPrivateMessage = str({'isPrivate': 'true', 'user_list':self.clients_name,'alert': d['alert'],'message': d['message'],'username':d['username']})
                    receiverSocket.send(receiverPrivateMessage.encode('utf-8'))
                    senderPrivateMessage = str({'isPrivate': 'true', 'user_list':self.clients_name,'alert': d['alert'],'message': d['message'],'receiver':d['receiver']})
                    c.send(senderPrivateMessage.encode('utf-8'))
                else:
                    to_send_dict = str({'isPrivate': 'false','user_list':self.clients_name,'alert': d['alert'],'message': d['message'],'username':d['username']})
                    self.sendtoall(to_send_dict)
            except Exception as e:
                # print("Error occured: ",e)
                pass


# Driver Code
print("Driver Code")
server = ServerConnection()
server.establishing_connection()
