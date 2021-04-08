import pygame as pg

pg.init()

class TextInput:
    def __init__(self, fontSize, fontType, x, y, width, defaultText):
        self.font = pg.font.SysFont(fontType, fontSize)
        self.inputColour = (255, 255, 255)
        self.defaultColour = (120, 120, 120)
        
        self.defaultText = defaultText
        self.user_text = defaultText
        self.text_surface = self.font.render(self.user_text, True, self.defaultColour)

        self.rect = self.text_surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width

        self.pos = (x, y)

        self.clicked = False

        self.surface = pg.Surface((width, self.rect.height), pg.SRCALPHA)

        #print(self.rect.h, self.rect.w)

    def update(self, event):
        if self.clicked:
            if event.key == pg.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            else:
                self.user_text += event.unicode

    def collisionUpdate(self, mousePosition):
        if self.rect.collidepoint((mousePosition[0], mousePosition[1])):
            self.clicked = True
            if self.user_text == self.defaultText:
                self.user_text = ''
        else:
            self.clicked = False
            if len(self.user_text) == 0:
                self.user_text = self.defaultText

    def reset(self):
        self.user_text = self.defaultText
        self.clicked = False

    def draw(self, window):
        self.surface.fill((0,0,0,0))

        if self.user_text == self.defaultText:
            self.text_surface = self.font.render(self.user_text, True, self.defaultColour)
        else:
            self.text_surface = self.font.render(self.user_text, True, self.inputColour)
        pg.draw.rect(self.surface, (120, 120, 120), (0, 0, self.rect.width, self.rect.height), width = 1)

        self.surface.blit(self.text_surface, (0, 0))

        window.blit(self.surface, self.pos)