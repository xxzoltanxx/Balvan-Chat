from Models import ChatMessages
from UserInterface.UserInterface import *
from Providers.ChatProvider import *

"""
A facade pattern class which contains (will contain all Providers, Models, and Views)
Services are for now injected directly inside the providers
"""

class BalvanChat:
    def __init__(self):
        self._model = ChatMessages.ChatMessages()
        self._provider = ChatProvider(self._model)
        self._view = UserInterface(self._provider)

    def run(self):
        self._view.runAplication()

balvanChat = BalvanChat()
balvanChat.run()