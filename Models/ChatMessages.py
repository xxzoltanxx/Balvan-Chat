import threading
import queue

#The chat message is passed around the Frontend, Presenter and the Encryptor Service in JSON Format:
# msg = {
#   Constants.CHAT_MSG_MESSAGE_KEY : value,
#   Constants.CHAT_MSG_NICK_KEY : value,
#   Constants.CHAT_MSG_STATUS_KEY : value
#  }

class ChatMessages:
    def __init__(self):
        self._messageLock = threading.Lock()
        self._messageQueue = queue.Queue()

    #add a message to the queue
    def addToQueue(self, data):
        self._messageLock.acquire()
        self._messageQueue.put(data)
        self._messageLock.release()

    #Get the next message, if any.
    def getNextMessage(self):
        try:
            self._messageLock.acquire()
            nextItem = self._messageQueue.get(block=False)
            self._messageLock.release()
            return nextItem
        except:
            self._messageLock.release()
            return None