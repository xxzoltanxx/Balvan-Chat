import Encryptor
import BalvanChatApp
import Server.ServerCommunicator
import Client.ClientCommunicator
import Constants
import threading
import queue
import json

class Controller:
    def __init__(self):
        self._text = ''
        self._password = '1'
        self._encryptor = None
        self._name = ''
        self._communicator = None
        self.isConnected = False
        self._messageLock = threading.Lock()
        self._messageQueue = queue.Queue()
        self.shouldExit = False


    def getEncryptor(self):
        return self._encryptor

    def getName(self):
        return self._name

    def send(self, text):
        data = {
            "name" : self._name,
            "message" : text,
            "status" : Constants.STATUS_OK
        }

        encryptedMessage = self._encryptor.encrypt(data)
        self._communicator.sendMessage(encryptedMessage)

    def connect(self, ip, password, name, salt):
        self._password = password
        self._encryptor = Encryptor.Encryptor(self._password, salt)
        self._name = name
        try:
            self._communicator = Client.ClientCommunicator.ClientCommunicator(self, ip)
        except:
            pass

    def runServer(self, password, name, salt):
        self._name = name
        self._password = password
        self._encryptor = Encryptor.Encryptor(self._password, salt)
        try:
            self._communicator = Server.ServerCommunicator.ServerCommunicator(self)
        except:
            pass


    def msg_received(self, address, data):
        try:
            decrypted_json = self._encryptor.decrypt(data)
            name = decrypted_json['name']
            msg = decrypted_json['message']
            status = decrypted_json['status']

            if (status == Constants.STATUS_NOK):
                self._messageLock.acquire()
                self._messageQueue.put((name + 'has disconnected.', 'status'))
                self._messageLock.release()
            else:
                self._messageLock.acquire()
                self._messageQueue.put((name + ":" + msg, 'other'))
                self._messageLock.release()
        except:
            self.reportStatusMessage('Received malformed message. Passphrase mismatch.')

    def reportStatusMessage(self, text):
        self._messageLock.acquire()
        self._messageQueue.put((text, 'status'))
        self._messageLock.release()
    
    def connectionTerminated(self, address):
        self._messageLock.acquire()
        self._messageQueue.put((address + ' has disconnected.', 'status'))
        self._messageLock.release()

    def pollStatusMessage(self):
        try:
            self._messageLock.acquire()
            nextItem = self._messageQueue.get(block=False)
            self._messageLock.release()
            return nextItem
        except:
            self._messageLock.release()
            return None
