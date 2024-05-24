import threading
import socket
from Constants import *
import ClientConnection
import BaseClasses.BaseCommunicator as BaseCommunicator
import time

class ServerCommunicator(BaseCommunicator.Communicator):
    def __init__(self, controller):
        self._controller = controller
        self._listenLock = threading.Lock()
        self.receiveLock = threading.Lock()

        self._connections = {}

        try:
            self.HOST = socket.gethostbyname(socket.gethostname())
            
            self._controller.reportStatusMessage('Your local IP address is: ' + self.HOST)

            self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._listen_socket.bind((self.HOST, DEFAULT_PORT))

            self._controller.reportStatusMessage('Socket bound to port: ' + str(DEFAULT_PORT))

            self._listen_socket.listen(5)

            self._controller.isConnected = True

            t1 = threading.Thread(target = self.listenLoop, daemon=True)

            t1.start()

        except:
            self._controller.reportStatusMessage('Failed to run server.')
            raise


    def listenLoop(self):
        while True:
            (conn, addr) = self._listen_socket.accept()
            self._controller.reportStatusMessage('New connection from: ' + addr[0])
            self._listenLock.acquire()
            self._connections[addr[0]] = ClientConnection.ClientConnection(conn, addr, self, self.receiveLock)
            self._listenLock.release()

    def updateAllClients(self, AddressDontUpdate, data):
        self._listenLock.acquire()
        for ip, clientconnection in self._connections.items():
            if (ip == AddressDontUpdate[0]):
                continue
            clientconnection.addToSend(data)
        self._listenLock.release()

    def msg_received(self, address, data):
        self.updateAllClients(address, data)
        self._controller.msg_received(address, data)

    def sendMessage(self, data):
        self._listenLock.acquire()
        for ip, clientconnection in self._connections.items():
            clientconnection.addToSend(data)
        self._listenLock.release()

    def connectionTerminated(self, address):
        del self._connections[address[0]]
        self._controller.connectionTerminated(address[0])
        data = {
            "name" : address[0],
            "message" : '',
            "status" : STATUS_NOK
        }
        encryptedData = self._controller.getEncryptor().encrypt(data)

        self.updateAllClients(self, address, encryptedData)