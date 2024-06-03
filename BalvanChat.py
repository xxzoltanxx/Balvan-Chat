from UserInterfaceBackend import *
from Controller import *

controller = Controller()
frontend = UserInterfaceBackend(controller)
frontend.runAplication()
