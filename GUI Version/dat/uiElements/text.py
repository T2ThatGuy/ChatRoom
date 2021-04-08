import pygame as pg

pg.init()

def blit_text(surface, text, pos, font, color=pg.Color('black')):
    word_height = 0
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0] # The width of a space.
    print(font.size(text)[1])
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 1, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def displayText(display, pos, text, size = 24, colour = (0, 0, 0), font = "Arial"):
    fontObj = pg.font.SysFont(font, size)

    textSurface = fontObj.render(text, 1, colour)
    display.blit(textSurface, pos)

display = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
FPS = 60

tempSurface = pg.Surface((200, 400))
fontObj = pg.font.SysFont("Arial", 24)

while True:
    for events in pg.event.get():
        if events.type == pg.QUIT:
            pg.quit()
            quit()

    display.fill((0, 0, 0))
    tempSurface.fill((0, 0, 0))

    #displayText(display, (10, 10), 'This is not\ncash money!', colour = (255, 255, 255))
    blit_text(tempSurface, 'This is an entire paragraph for the test of the multiple lines code written for the messaging app!', (10, 10), fontObj, (255, 255, 255))

    display.blit(tempSurface, (0, 0))

    pg.display.update()
    clock.tick(FPS)

