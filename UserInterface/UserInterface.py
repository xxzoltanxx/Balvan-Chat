import webview
from flask import Flask, request, render_template, jsonify
import Constants
import sys;

"""
A class which is a server for the frontend application.
It sends data to, and retrieves data from the presenter,
serving dynamic html pages as a desktop app. This is done through emulating
different browsers in app mode, and connecting it to a local backend.
(Via pywebview)
"""
class UserInterface:
    def __init__(self, presenter):
        self._presenter = presenter
        self._window = None
    
    """
    Will initialize the server and all of it's routes.
    """
    def _setupBackendServer(self):
        server = Flask('Backend', static_folder=Constants.STATIC_FOLDER, template_folder=Constants.TEMPLATE_FOLDER)
        
        """
        A route for the starting screen.
        """
        @server.route('/', methods = ['GET'])
        def displayLandingPage():
            return render_template('startMenu.html')

        """
        A route acting as a 'connect' choice in main menu.
        """
        @server.route('/connect', methods = ['GET'])
        def displayConnectPopup():
            return render_template('connect.html')

        """
        A route which is invoked when the user tries to connect to a server.
        """
        @server.route('/connect', methods = ['POST'])
        def connectToServer():
            data = request.get_json()

            nick = data.get(Constants.NICK_REQUEST_ARGNAME)
            password = data.get(Constants.PASSWORD_REQUEST_ARGNAME)
            ip = data.get(Constants.IP_REQUEST_ARGNAME)
            salt = data.get(Constants.SALT_REQUEST_ARGNAME)

            self._presenter.connect(ip, password, nick, salt)
            return jsonify(success=True)
        
        @server.route('/openChatScreen', methods=['GET'])
        def openChatScreen(self):
            return render_template('mainChatRoom.html')
        
        """
        A route acting as a 'start server' choice in main menu.
        """
        @server.route('/startserver', methods = ['Get'])
        def displayStartServerPopup():
            return render_template('runServer.html')

        """
        A route which is invoked when the user starts a server.
        """
        @server.route('/startServer', methods = ['POST'])
        def startServer():
            data = request.get_json()

            nick = data.get(Constants.NICK_REQUEST_ARGNAME)
            password = data.get(Constants.PASSWORD_REQUEST_ARGNAME)
            salt = data.get(Constants.SALT_REQUEST_ARGNAME)

            self._presenter.runServer(password, nick, salt)
            return jsonify(success=True)


        @server.route('/openChatRoomUI', methods = ['GET'])
        def openChatRoomUI():
            #Make the window larger for the in-chat window.
            self._window.resize(Constants.IN_CHAT_WINDOW_SIZE[0],Constants.IN_CHAT_WINDOW_SIZE[1])
            return render_template('mainChatRoom.html')
        
        
        """
        A route by which the frontend polls the messages in the presenter
        message queue.
        """
        @server.route('/pollMessages', methods = ['GET'])
        def pollMessages():
            if (self._presenter.shouldExit):
                sys.exit(1)
            json_message = self._presenter.pollMessage()
            if json_message != None:
                message_txt = json_message[Constants.CHAT_MSG_MESSAGE_KEY]
                status = json_message[Constants.CHAT_MSG_STATUS_KEY]
                nick = json_message[Constants.CHAT_MSG_NICK_KEY]
                if (nick == ''):
                    nick = Constants.DEFAULT_NICK
                return self._makeHTMLBubble(nick, message_txt, status)
            return ""
        
        """
        A route which is triggered when you send a chat message.
        """
        @server.route('/sendChatMessage', methods = ['POST'])
        def sendChatMessage():
            data = request.get_json()

            message = data.get(Constants.CHAT_MSG_MESSAGE_KEY)

            self._presenter.send(message)
            return jsonify(success=True)


        return server

    """
    Used for constructing frontend styled entries.
    """
    def _makeHTMLBubble(self, nick, message_txt, status):
        if (status == Constants.STATUS_OK):
            return f"<div style='display: inline-block'><div class='aboveBubble'>{nick}</div><div class='defaultChatBubble'><span>{message_txt}</span></div></div>"
        elif (status == Constants.STATUS_NOK):
            return f"<div style='display: inline-block'><div class='aboveBubble'>{nick}</div><div class='statusChatBubble'><span>Disconnected...'</span></div></div>"
        else:
            return f"<div style='display: inline-block'><div class='aboveBubble'>{nick}</div><div class='statusChatBubble'><span>{message_txt}</span></div></div>"

    """
    This method will display the application and block the main thread,
    reserving it for everything related to the window being shown.
    """
    def runAplication(self):
        self._window = webview.create_window(Constants.APPLICATION_NAME, self._setupBackendServer())
        self._window.frameless = True
        self._window.resizable = False
        webview.start()