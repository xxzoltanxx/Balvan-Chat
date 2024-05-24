import threading
import socket
from Constants import *
import ClientConnection
import BaseClasses.BaseCommunicator as BaseCommunicator

class ClientCommunicator(BaseCommunicator.Communicator):
    def __init__(self, controller, ip):
        self._controller = controller

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self._socket.connect((ip, DEFAULT_PORT))
            self._controller.isConnected = True
            self._controller.reportStatusMessage('Succesfully connected to: ' + ip + ' on port: ' + str(DEFAULT_PORT))
        except:
            self._controller.reportStatusMessage(ip + ' refused to connect on port: ' + str(DEFAULT_PORT))
            raise
        self._connection = ClientConnection.ClientConnection(self._socket, ip, self, None)

    def msg_received(self, address, data):
        self._controller.msg_received(address, data)

    def sendMessage(self, data):
        self._connection.addToSend(data)

    def connectionTerminated(self, address):
        self._controller.connectionTerminated(address)
        self._controller.isConnected = False