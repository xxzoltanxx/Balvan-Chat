import threading
import queue
import time
from Constants import *

class ClientConnection:
    def __init__(self, conn, addr, serverCommunicator, communicatorMutex):
        self._connection = conn
        self._address = addr
        self._sendLock = threading.Lock()
        self._sendBuffer = queue.Queue()
        self._serverCommunicator = serverCommunicator
        self._communicatorMutex = communicatorMutex
        self.shouldTerminate = False

        self.t1 = threading.Thread(target = self.receiverLoop, daemon=True)
        self.t2 = threading.Thread(target = self.sendLoop, daemon=True)

        self.t1.start()
        self.t2.start()

    def addToSend(self, string):
        self._sendLock.acquire()
        self._sendBuffer.put(string)
        self._sendLock.release()

    def receiverLoop(self):
        while not self.shouldTerminate:  
            data = b''
            try:
                data = self._connection.recv(MAX_SIZE_MESSAGE)
            except:
                pass
            if (self._communicatorMutex != None):
                self._communicatorMutex.acquire()
            if len(data) == 0:
                self.shouldTerminate = True
                self._serverCommunicator.connectionTerminated(self._address)
            else:
                self._serverCommunicator.msg_received(self._address, data)
            if (self._communicatorMutex != None):
                self._communicatorMutex.release()

    def sendLoop(self):
        while not self.shouldTerminate:
            try:
                self._sendLock.acquire()
                stringToSend = self._sendBuffer.get(block=False)
                self._sendLock.release()
                self._connection.sendall(stringToSend)
            except:
                self._sendLock.release()
            
            time.sleep(SEND_COOLDOWN)
            
                


