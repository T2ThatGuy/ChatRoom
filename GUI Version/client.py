from dat.core.chatScreen import ChatScreen
from dat.core.mainMenu import MainMenu
from network import Network
from sys import exit
import pygame as pg

"""

--- Main Application Class---

currentState: string -> references the curren state the app is in MENU / CHAT

clock: pygame clock object -> Allows the screen to be locked to a set refresh rate
display: pygame display object

quit: boolean -> If true quite the game

"""


#--- Main Application Class ---
class App:
    def __init__(self):
        self.currentState = 'MENU'

        self.display = pg.display.set_mode((400, 800))
        self.clock = pg.time.Clock()

        self.network = Network()

        self.quit = False

        self.username = 'T2ThatGuy'

        self.mainLoop()

    def mainLoop(self):
        chatName = None
        mainMenu = MainMenu(self)

        while not self.quit:
            chatScreen = ChatScreen(self)
            
            if self.currentState == 'MENU':
                self.currentState, chatName = mainMenu.onLoop()

            elif self.currentState == 'CHAT':
                self.currentState = chatScreen.joinChat(chatName)

        pg.quit()
        exit()

if __name__ == '__main__':
    application = App()