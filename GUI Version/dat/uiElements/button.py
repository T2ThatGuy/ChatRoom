import pygame as py

#   Button Class Inputs
#   xPos = X Position on the display (Center)
#   yPos = Y Position on the display (Center)
#   function = Should give it a number value which will be used in the code as a return value
#   ie. 1 once returned will go to the options menu etc
#   img = This is the image of the sprite
#   imgHov = This is the image of the sprite whilst it is being hovered over (Optional)
#   imgClick = This is the image that will be shown before the image returns to normal (Optional)
#
#   NOTE: All button image sizes should be the same!
#   NOTE: Positional values are based upon the center of the button!


#--- Button Class ---#
class Button():
    def __init__(self, xPos, yPos, function, img, imgHov = None, imgClick = None):
        #--- Positional Values ---#   
        self.xPos = xPos                    #--- X Position ---#
        self.yPos = yPos                    #--- Y Position ---#

        #--- Image Values ---#
        self.image = img                    #--- Current image = Normal Image ---#
        self.rect = self.image.get_rect()   #--- Collision Rectangle ---#
        self.rect.center = [xPos, yPos]     #--- Setting the centre of the collision box ---#

        self.imgNorm = img                  #--- Normal image ---#
        self.imgHov = imgHov                #--- Image for when hovered ---#
        self.imgClick = imgClick            #--- Image for when clicked ---#

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        #--- Functional Booleans ---#
        self.clicked = False                #--- Bool for when clicked ---#
        self.hovered = False                #--- Bool for when hovered ---#
        self.function = function            #--- Int that will be returned when clicked ---#
        self.isFunc = callable(function)

    #--- Update Function ---#
    def update(self, up = False, hover = False, down = False, surf = [0, 0]):
        #--- Get Mouse Values ---#
        mPos = py.mouse.get_pos()

        #--- Collision between the mouse and button ---#
        if mPos[0] >= self.xPos - (self.width / 2) + surf[0] and mPos[0] <= (self.xPos + self.width) - (self.width / 2) + surf[0] and mPos[1] <= (self.yPos + self.height) - (self.height / 2) + surf[1] and mPos[1] >= self.yPos - (self.height / 2) + surf[1]:
            if hover:
                self.hovered = True
                if self.play and not self.disableSound:
                    self.play = False
            if down:
                self.clicked = True
            if up:
                if self.isFunc:
                    self.function()
                else:
                    return self.function
        else:
            self.hovered = False
            self.clicked = False
            self.play = True

        #--- Updates the draw function so it uses the correct image ---#
        self.updateDraw()

    #--- Updates the Appearance ---#
    def updateDraw(self):
        if self.hovered and self.imgHov != None:
            self.image = self.imgHov
        elif self.clicked and self.imgClick != None:
            self.image = self.imgClick
        else:
            self.image = self.imgNorm

    #--- Draws the button to the screen ---#
    def draw(self, display):
        display.blit(self.image, self.rect)