from Models import ChatMessages
from UserInterface.UserInterface import *
from Presenters.ChatPresenter import *

"""
A facade pattern class which contains (will contain all Presenters, Models, and Views)
Services are for now injected directly inside the presenters
"""

class BalvanChat:
    def __init__(self):
        self._model = ChatMessages.ChatMessages()
        self._presenter = ChatPresenter(self._model)
        self._view = UserInterface(self._presenter)

    def run(self):
        self._view.runAplication()

balvanChat = BalvanChat()
balvanChat.run()