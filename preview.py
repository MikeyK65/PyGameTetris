from settings import *
from pygame.image import load
from os import path

class Preview:
    def __init__(self): #, nextShapes):
        self.surface = pygame.Surface((SIDEBARWIDTH, GAMEHEIGHT * PREVIEW_HEIGHT_FRACTION - PADDING))
        self.rect = self.surface.get_rect(topright = (WINDOWWIDTH - PADDING, PADDING))
        self.displaySurface = pygame.display.get_surface()
        #self.nextShapes = nextShapes

        self.shapeSurfaces = {shape: load(path.join ('graphics',f'{shape}.png')).convert_alpha() for shape in TETROMINOES.keys()}

        self.sectionHeight = self.surface.get_height() / 3

    def displayPieces (self, shapes):
        for i,shape in enumerate(shapes):
            shapeSurface = self.shapeSurfaces[shape]
            x = self.surface.get_width() / 2
            y = (self.sectionHeight / 2) + (i * self.sectionHeight)
            rect = shapeSurface.get_rect(center = (x,y))
            self.surface.blit(shapeSurface, rect)
            

    def run(self, nextShapes):
        self.surface.fill(GREY)
        self.displayPieces(nextShapes)
        self.displaySurface.blit (self.surface, self.rect)
        pygame.draw.rect(self.displaySurface, LINECOLOUR, self.rect, 2,2)
