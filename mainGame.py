from settings import *
from sys import exit
from os.path import join

from random import choice

from game import Game
from score import Score
from preview import Preview

class Main:
    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption ("pyTris!")
        self.clock = pygame.time.Clock()

        self.nextShapes = [choice(list(TETROMINOES.keys())) for shape in range (3)]

        self.game = Game(self.getNextShape, self.updateScore)
        self.score = Score()
        self.preview = Preview() #self.nextShapes)

        #audio
        self.music = pygame.mixer.Sound(join('sound','music.wav'))
        self.music.set_volume(0.05)
        self.music.play(-1)   # -1 = perpetual music


    def updateScore(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def getNextShape(self):
        nextShape = self.nextShapes.pop(0)
        self.nextShapes.append(choice(list(TETROMINOES.keys())))

        return nextShape
    

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Update display
            self.surface.fill (GREY)

            self.game.run()
            self.score.run()
            self.preview.run(self.nextShapes)

            pygame.display.update()
            self.clock.tick()

if __name__ == '__main__':
    main = Main()
    main.run()
