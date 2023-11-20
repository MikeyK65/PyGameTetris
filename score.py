from settings import *
from os.path import join

class Score:
    def __init__(self):
        self.surface = pygame.Surface((SIDEBARWIDTH, GAMEHEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        self.rect = self.surface.get_rect(bottomright = (WINDOWWIDTH - PADDING, WINDOWHEIGHT - PADDING))
        self.displaySurface = pygame.display.get_surface()
        self.font = pygame.font.Font(join('graphics','Russo_One.ttf'), 30)

        self.incrementHeight = self.surface.get_height() / 3

        self.score = 0
        self.level = 1
        self.lines = 0


    def DisplayText(self,pos,text):
        textSurface = self.font.render(f'{text[0]}:{text[1]}', True, 'white')
        rectText = textSurface.get_rect(center = pos)
        self.surface.blit(textSurface , rectText)

    def run(self):
        self.surface.fill(GREY)
        for i, text in enumerate([('Score', self.score),('Level', self.level), ('Lines', self.lines)]):
            x = self.surface.get_width() / 2
            y = self.incrementHeight / 2 + i * self.incrementHeight
            self.DisplayText((x,y), text)
        
        self.displaySurface.blit (self.surface, self.rect)
        pygame.draw.rect (self.displaySurface, LINECOLOUR, self.rect, 2, 2)
