import socket
from Constants import *
import Infrastructure.ClientConnection as ClientConnection
import Services.Interfaces.CommunicatorService

class ClientCommunicatorService(Services.Interfaces.CommunicatorService.CommunicatorService):
    def __init__(self, presenter, ip):
        self._presenter = presenter

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self._socket.connect((ip, DEFAULT_PORT))
            self._presenter.isConnected = True
            self._presenter.reportStatusMessage('Succesfully connected to: ' + ip + ' on port: ' + str(DEFAULT_PORT))
        except:
            self._presenter.reportStatusMessage(ip + ' refused to connect on port: ' + str(DEFAULT_PORT))
            raise
        self._connection = ClientConnection.ClientConnection(self._socket, ip, self, None)

    def msg_received(self, address, data):
        self._presenter.msg_received(data)

    def sendMessage(self, data):
        self._connection.addToSend(data)

    def connectionTerminated(self, address):
        self._presenter.connectionTerminated(address)
        self._presenter.isConnected = False