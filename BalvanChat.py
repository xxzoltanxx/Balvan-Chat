from UserInterface import *
from Controller import *

controller = Controller()
frontend = UserInterface(controller)
frontend.runAplication()
