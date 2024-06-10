import threading
import socket
from Constants import *
import Infrastructure.ClientConnection as ClientConnection
import Services.Interfaces.CommunicatorService

class ServerCommunicatorService(Services.Interfaces.CommunicatorService.CommunicatorService):
    def __init__(self, presenter):
        self._presenter = presenter
        self._listenLock = threading.Lock()
        self.receiveLock = threading.Lock()

        self._connections = {}

        try:
            self.HOST = socket.gethostbyname(socket.gethostname())
            self.HOST = '127.0.0.1'
            self._presenter.reportStatusMessage('Your local IP address is: ' + self.HOST)

            self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._listen_socket.bind((self.HOST, DEFAULT_PORT))

            self._presenter.reportStatusMessage('Socket bound to port: ' + str(DEFAULT_PORT))

            self._listen_socket.listen(5)

            self._presenter.isConnected = True

            t1 = threading.Thread(target = self.listenLoop, daemon=True)

            t1.start()

        except:
            self._presenter.reportStatusMessage('Failed to run server.')
            raise


    def listenLoop(self):
        while True:
            (conn, addr) = self._listen_socket.accept()
            self._presenter.reportStatusMessage('New connection from: ' + addr[0])
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
        self._presenter.msg_received(data)

    def sendMessage(self, data):
        self._listenLock.acquire()
        for ip, clientconnection in self._connections.items():
            clientconnection.addToSend(data)
        self._listenLock.release()

    def connectionTerminated(self, address):
        del self._connections[address[0]]
        self._presenter.connectionTerminated(address[0])
        data = {
            CHAT_MSG_NICK_KEY : address[0],
            CHAT_MSG_MESSAGE_KEY : '',
            CHAT_MSG_STATUS_KEY : STATUS_NOK
        }
        encryptedData = self._presenter.getEncryptor().encrypt(data)

        self.updateAllClients(address, encryptedData)