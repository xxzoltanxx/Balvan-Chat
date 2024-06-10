import Services.Client
import Services.Client.ClientCommunicatorService
import Services.EncryptorService as EncryptorService
import Services.Server.ServerCommunicatorService
import Services.Client.ClientCommunicatorService
import Models.ChatMessages
import Constants
import threading
import queue

class ChatPresenter:
    def __init__(self, chatMessageModel):
        self._text = ''
        self._name = ''
        self.isConnected = False
        self.shouldExit = False
        self._chatMessages = chatMessageModel


        self._communicatorService = None
        self._encryptorService = None


    def getEncryptor(self):
        return self._encryptorService

    def getName(self):
        return self._name

    def send(self, text):
        data = {
            Constants.CHAT_MSG_NICK_KEY : self._name,
            Constants.CHAT_MSG_MESSAGE_KEY : text,
            Constants.CHAT_MSG_STATUS_KEY  : Constants.STATUS_OK
        }

        self._chatMessages.addToQueue(data)

        encryptedMessage = self._encryptorService.encrypt(data)
        self._communicatorService.sendMessage(encryptedMessage)

    def connect(self, ip, password, name, salt):
        self._encryptorService = EncryptorService.EncryptorService(password, salt)
        self._name = name
        try:
            self._communicatorService = Services.Client.ClientCommunicatorService.ClientCommunicatorService(self, ip)
        except:
            pass

    def runServer(self, password, name, salt):
        self._name = name
        self._encryptorService = EncryptorService.EncryptorService(password, salt)
        try:
            self._communicatorService = Services.Server.ServerCommunicatorService.ServerCommunicatorService(self)
        except:
            pass


    def msg_received(self, data):
        try:
            decryptedData = self._encryptorService.decrypt(data)
            self._chatMessages.addToQueue(decryptedData)
        except:
            self.reportStatusMessage('Received malformed message. Passphrase mismatch.')

    def reportStatusMessage(self, text):
        data = {Constants.CHAT_MSG_MESSAGE_KEY: text, Constants.CHAT_MSG_NICK_KEY : Constants.STATUS_SYSTEM_MESSAGE, Constants.CHAT_MSG_STATUS_KEY: Constants.STATUS_SYSTEM_MESSAGE}
        self._chatMessages.addToQueue(data)
    
    def connectionTerminated(self, address):
        data = {Constants.CHAT_MSG_MESSAGE_KEY: address + ' has disconnected.', Constants.CHAT_MSG_NICK_KEY : Constants.STATUS_SYSTEM_MESSAGE, Constants.CHAT_MSG_STATUS_KEY: Constants.STATUS_SYSTEM_MESSAGE}
        self._chatMessages.addToQueue(data)

    def pollMessage(self):
        return self._chatMessages.getNextMessage()
