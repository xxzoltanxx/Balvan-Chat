import socket
from Constants import *
import Infrastructure.ClientConnection as ClientConnection
import Services.Interfaces.CommunicatorService

class ClientCommunicatorService(Services.Interfaces.CommunicatorService.CommunicatorService):
    def __init__(self, provider, ip):
        self._provider = provider

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self._socket.connect((ip, DEFAULT_PORT))
            self._provider.isConnected = True
            self._provider.reportStatusMessage('Succesfully connected to: ' + ip + ' on port: ' + str(DEFAULT_PORT))
        except:
            self._provider.reportStatusMessage(ip + ' refused to connect on port: ' + str(DEFAULT_PORT))
            raise
        self._connection = ClientConnection.ClientConnection(self._socket, ip, self, None)

    def msg_received(self, address, data):
        self._provider.msg_received(data)

    def sendMessage(self, data):
        self._connection.addToSend(data)

    def connectionTerminated(self, address):
        self._provider.connectionTerminated(address)
        self._provider.isConnected = False