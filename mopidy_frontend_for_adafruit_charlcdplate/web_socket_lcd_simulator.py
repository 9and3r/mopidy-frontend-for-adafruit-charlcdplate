# https://github.com/dpallot/simple-websocket-server
import json
from threading import Thread

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from InputManager import InputManager

clients = []
last_message = None
pressed_keys = {InputManager.SELECT: False, InputManager.RIGHT: False, InputManager.DOWN: False, InputManager.UP: False, InputManager.LEFT: False}


class WebSockectLCDSimulator:

    def __init__(self):
        self.server = SimpleWebSocketServer('', 8000, WebSocketServer)

    def on_start(self):
        thread = Thread(target=self.runServer)
        thread.start()

    def runServer(self):
        self.server.serveforever()

    def message(self, message):

        #TODO Find special characters and replace with others. For example Volume\x01 to u'Volume\u2600'

        data = unicode(json.dumps({'jsonrpc': '2.0', 'method': 'message', 'params': message }))
        global last_message
        last_message = data
        for client in clients:
            client.sendMessage(data)

    def create_char(self, location, pattern):
        data = unicode(json.dumps({'jsonrpc': '2.0', 'method': 'create_char', 'params': {location: location, pattern: pattern}}))
        for client in clients:
            client.sendMessage(data)

    def on_stop(self):
        self.server.close()

    def is_pressed(self, button):
        if button not in set((InputManager.SELECT, InputManager.RIGHT, InputManager.DOWN, InputManager.UP, InputManager.LEFT)):
            raise ValueError('Unknown button, must be SELECT, RIGHT, DOWN, UP, or LEFT.')
        return pressed_keys[button]


class WebSocketServer(WebSocket):

    def handleMessage(self):
        message = json.loads(self.data)
        if message['params'] in set((InputManager.SELECT, InputManager.RIGHT, InputManager.DOWN, InputManager.UP, InputManager.LEFT)):
            if message['method'] == 'keydown':
                pressed_keys[message['params']] = True
            elif message['method'] == 'keyup':
                pressed_keys[message['params']] = False

    def handleConnected(self):
        global last_message
        print self.address, 'connected'
        clients.append(self)
        if last_message is not None:
            self.sendMessage(last_message)


    def handleClose(self):
        print self.address, 'closed'
        clients.remove(self)
        self.connected = False

