from dat.uiElements.chatInput import TextInput
from dat.uiElements.chatBox import ChatBox
from string import ascii_letters as ASCII_CHAR
import pygame as pg, pickle, threading

class ChatScreen:
    def __init__(self, app):
        self.appRef = app

        self.chatBox = ChatBox()
        self.chatInput = TextInput(32, "Arial", 10, 753, 300, 'Input Text Here')

    def joinChat(self, chatName):
        return self.onLoop()

    def onLoop(self):
        counterMax = 0
        counter = 0

        receive_thread = threading.Thread(target = self.receive)
        receive_thread.start()
        

        while not self.appRef.quit:
            for events in pg.event.get():
                if events.type == pg.QUIT:
                    self.appRef.quit = True
                    self.appRef.network.disconnect()
                    return None

                if events.type == pg.KEYDOWN:
                    self.chatInput.update(events)

                if events.type == pg.MOUSEBUTTONUP:
                    self.chatInput.collisionUpdate(pg.mouse.get_pos())

                if events.type == pg.KEYUP:
                    if events.key == pg.K_RETURN:
                        if self.chatInput.user_text != 'Input Text Here' and self.hasCharacters(self.chatInput.user_text):
                            self.sendMessage(self.chatInput.user_text)
                            self.chatInput.reset()
                    
                    if events.key == pg.K_ESCAPE:
                        self.disconnect()
                        return 'MENU'
                    
                    if events.key == pg.K_1:
                        counterMax = 20

                self.chatBox.onUpdate(pg.mouse.get_pos(), events)

            if counter != counterMax:
                self.sendMessage(str('Test: ' + str(counter)))
                counter += 1

            self.appRef.display.fill((50, 50, 50))
            self.chatInput.draw(self.appRef.display)
            self.chatBox.onDraw(self.appRef.display)

            pg.display.update()
            self.appRef.clock.tick(60)

    def hasCharacters(self, string):
        if any(s in ASCII_CHAR for s in string):
            return True

    def sendMessage(self, message):
        tempArray = {
            'Message': 'New Message',
            'Data': {
                'Username': self.appRef.username,
                'Msg': message
            }
        }

        try:
            self.appRef.network.client.send(pickle.dumps(tempArray))
        except:
            pass

    def addMessage(self, message):
        self.chatBox.newMessage(message['Msg'], message['Username'])

    def receive(self):
        self.appRef.network.connect()

        while True:
            try:
                reply = self.appRef.network.client.recv(4096)
                reply = pickle.loads(reply)

                if reply['Message'] == 'NICK':
                    tempDict = {
                        'Message': 'Set Username',
                        'Data': self.appRef.username
                    }

                    data = pickle.dumps(tempDict)
                    self.appRef.network.client.send(data)

                elif reply['Message'] == 'New Message':
                    self.addMessage(reply['Data'])
                    
            except Exception as e:
                print('[ERROR] An Error occurred whilst receiving data from the server:', e)
                self.appRef.network.disconnect()
                quit()

'''
Receives {
    'Message': message
    'data': {
        'username': user
        'message': message from user
    }
}

All of the above is received in a pickle package
'''