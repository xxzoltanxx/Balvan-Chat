import Encryptor
import Server.ServerCommunicator
import Client.ClientCommunicator
import Constants
import threading
import queue

class Controller:
    def __init__(self):
        self._text = ''
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
            Constants.CHAT_MSG_NICK_KEY : self._name,
            Constants.CHAT_MSG_MESSAGE_KEY : text,
            Constants.CHAT_MSG_STATUS_KEY  : Constants.STATUS_OK
        }

        self._messageLock.acquire()
        self._messageQueue.put(data)
        self._messageLock.release()

        encryptedMessage = self._encryptor.encrypt(data)
        self._communicator.sendMessage(encryptedMessage)

    def connect(self, ip, password, name, salt):
        self._encryptor = Encryptor.Encryptor(password, salt)
        self._name = name
        try:
            self._communicator = Client.ClientCommunicator.ClientCommunicator(self, ip)
        except:
            pass

    def runServer(self, password, name, salt):
        self._name = name
        self._encryptor = Encryptor.Encryptor(password, salt)
        try:
            self._communicator = Server.ServerCommunicator.ServerCommunicator(self)
        except:
            pass


    def msg_received(self, address, data):
        try:
            decryptedData = self._encryptor.decrypt(data)
            self._messageLock.acquire()
            self._messageQueue.put(decryptedData)
            self._messageLock.release()
        except:
            self.reportStatusMessage('Received malformed message. Passphrase mismatch.')

    def reportStatusMessage(self, text):
        self._messageLock.acquire()
        self._messageQueue.put({Constants.CHAT_MSG_MESSAGE_KEY: text, Constants.CHAT_MSG_NICK_KEY : Constants.STATUS_SYSTEM_MESSAGE, Constants.CHAT_MSG_STATUS_KEY: Constants.STATUS_SYSTEM_MESSAGE})
        self._messageLock.release()
    
    def connectionTerminated(self, address):
        self._messageLock.acquire()
        self._messageQueue.put({Constants.CHAT_MSG_MESSAGE_KEY: address + ' has disconnected.', Constants.CHAT_MSG_NICK_KEY : Constants.STATUS_SYSTEM_MESSAGE, Constants.CHAT_MSG_STATUS_KEY: Constants.STATUS_SYSTEM_MESSAGE})
        self._messageLock.release()

    def pollMessage(self):
        #The chat message is passed around the Frontend, Controller and the Encryptor in JSON Format:
        # msg = {
        #   Constants.CHAT_MSG_MESSAGE_KEY : value,
        #   Constants.CHAT_MSG_NICK_KEY : value,
        #   Constants.CHAT_MSG_STATUS_KEY : value
        #  }

        try:
            self._messageLock.acquire()
            nextItem = self._messageQueue.get(block=False)
            self._messageLock.release()
            return nextItem
        except:
            self._messageLock.release()
            return None
