from string import ascii_letters as ASCII_CHAR
from dat.uiElements.chatInput import TextInput
from dat.uiElements.button import Button
import pygame as pg

class MainMenu:
    def __init__(self, app):
        self.appRef = app

        self.buttons = [
            Button(200, 100, 'CHAT', pg.image.load('imgs/playNorm.png').convert()),
            Button(200, 700, 'quit', pg.image.load('imgs/quitNorm.png').convert())
        ]

        self.textInput = TextInput(32, "Arial", 10, 753, 300, 'Input Username Here')

    def onLoop(self):
        """
        Main Menu Main Loop 

        Main loop of the main menu used to 

        Returns:
        <str>: -> Next game state to go to || If it should quit 
        <str>: -> Chat room to join 
        """
        
        
        while not self.appRef.quit:
            
            #--- Events ---
            for events in pg.event.get():
                if events.type == pg.QUIT:
                    self.appRef.quit = True
                    return None, None

                if events.type == pg.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        response = btn.update(up = True)

                        if response == 'CHAT':
                            return response, 'default'

                        elif response == 'quit':
                            self.appRef.quit = True
                            return None, None

                if events.type == pg.MOUSEBUTTONUP:
                    self.textInput.collisionUpdate(pg.mouse.get_pos())

                if events.type == pg.KEYDOWN:
                    self.textInput.update(events)

                    if not self.textInput.clicked:
                        self.setUsername()

                if events.type == pg.KEYUP:
                    if events.key == pg.K_RETURN:
                        self.setUsername()

            #--- Main Script / Code ---

            #--- Draw Display ---
            self.appRef.display.fill((50, 50, 50))

            for btn in self.buttons:
                btn.draw(self.appRef.display)

            self.textInput.draw(self.appRef.display)

            pg.display.update()
            self.appRef.clock.tick(60)

    def setUsername(self):
        if self.textInput.user_text != 'Input Username Here' and self.hasCharacters(self.textInput.user_text):
                self.appRef.username = self.textInput.user_text

    def hasCharacters(self, string):
        if any(s in ASCII_CHAR for s in string):
            return True