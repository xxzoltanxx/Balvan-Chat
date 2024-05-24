from abc import ABC, abstractmethod
class Communicator(ABC):
    @abstractmethod
    def msg_received(self, address, data):
        pass

    @abstractmethod
    def sendMessage(self, data):
        pass

    @abstractmethod
    def connectionTerminated(self, address):
        pass

    