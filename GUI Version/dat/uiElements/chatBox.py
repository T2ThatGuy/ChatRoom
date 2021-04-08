import pygame as pg

class ChatBox:
    def __init__(self):
        self.surface = pg.Surface((380, 733), pg.SRCALPHA)
        self.pos = (10, 10)

        self.rect = pg.Rect(10, 10, 380, 733)
        
        self.messages = []
        self.messageImg = []

        self.message_box_offset = 0
        self.total_message_height = 0
        self.messageCounter = 0

    def onUpdate(self, mouse, events):
    
        if self.isScrollable():
            total_message_difference = self.total_message_height - 723 - self.message_box_offset
            if self.rect.collidepoint(mouse[0], mouse[1]):
                if events.type == pg.MOUSEBUTTONDOWN:
                    if events.button == 4:  #Scroll Wheel Up
                        if total_message_difference + 10 > 0:
                            self.message_box_offset += 10
                    
                    if events.button == 5: #Scroll Wheel Down
                        if self.message_box_offset - 10 > 0:
                            self.message_box_offset -= 10
                        elif self.message_box_offset > 0:
                            self.message_box_offset = 0

    def isScrollable(self):
        if self.total_message_height > 723:
            return True

        return False

    def newMessage(self, msg, username):
        #Add message to array
        self.messages.append([username, msg])

        #Render Message
        self.messageImg.append(self.renderFullMessage(self.renderUsername(username), self.renderMessage(msg, 360)))
        
    
    def renderFullMessage(self, usernameRender, messageRender):
        username_render_height = usernameRender.get_height()
        message_render_height = messageRender.get_height()
        
        messageSurface = pg.Surface((360, username_render_height + message_render_height), pg.SRCALPHA)

        messageSurface.blit(usernameRender, (0, 0))

        messageY = username_render_height
        messageSurface.blit(messageRender, (0, messageY))

        self.total_message_height += username_render_height + message_render_height + 5

        return messageSurface

    def renderUsername(self, username, size = 24, colour = (255, 255, 255), font = "Arial"):
        fontObj = pg.font.SysFont(font, size)
        usernameSurface = fontObj.render(username, 1, colour)

        return usernameSurface

    def renderMessage(self, msg, width, size = 18, font = 'Arial', colour = (255, 255, 255)):
        words = [word.split(' ') for word in msg.splitlines()]

        fontObj = pg.font.SysFont(font, size)
        charHeight = fontObj.size(msg)[1]
        space = fontObj.size(' ')[0]

        max_width = width

        lineSurface = pg.Surface((max_width, charHeight), pg.SRCALPHA)
        lineArray = []

        x = 0
        totalY = 0

        for line in words:
            for word in line:
                word_surface = fontObj.render(word, 1, colour)
                word_width, word_height = word_surface.get_size()

                if x + word_width >= max_width:
                    #Adds current line to lines array
                    lineArray.append(lineSurface)

                    #Resets the line surface
                    lineSurface = pg.Surface((max_width, charHeight), pg.SRCALPHA)
                    x = 0
                    totalY += charHeight

                lineSurface.blit(word_surface, (x, 0))
                x += word_width + space
            
            #Adds current line to lines array
            lineArray.append(lineSurface)

            #Resets the line surface
            lineSurface = pg.Surface((max_width, charHeight), pg.SRCALPHA)
            x = 0
            totalY += charHeight

        finalSurface = pg.Surface((width, totalY), pg.SRCALPHA)
        
        finalY = 0

        for line in lineArray:
            finalSurface.blit(line, (0, finalY))           
            finalY += line.get_height()

        return finalSurface

    def onDraw(self, display):
        #Clear Surface
        self.surface.fill((0, 0, 0, 0))

        #Set Positional Values for Text
        messageBuffer = 5

        #Draw Outer Bounds
        pg.draw.rect(self.surface, (255, 255, 255), (0, 0, 380, 733), width = 1)

        #Draw Messages
        msg_surface = pg.Surface((360, 723), pg.SRCALPHA)
        currentY = 723

        length = len(self.messageImg)

        if length > 0:
            for msg in self.messageImg[::-1]:
                msg_height = msg.get_height()
                currentY -= msg_height

                msg_surface.blit(msg, (0, currentY + self.message_box_offset))

                currentY -= messageBuffer

        self.surface.blit(msg_surface, (10, 0))
        display.blit(self.surface, self.pos)
    