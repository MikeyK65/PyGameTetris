#from pygame.sprite import _Group
from typing import Any
from settings import *
import random
from sys import exit
from os.path import join

from timer import Timer

class Game:
    def __init__(self, getNextShape, updateScore):
        self.surface = pygame.Surface((GAMEWIDTH, GAMEHEIGHT))
        self.displaySurface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))

        self.sprites = pygame.sprite.Group()

        self.getNextShape = getNextShape
        self.updateScore = updateScore

        #lines
        self.lineSurface = self.surface.copy()
        self.lineSurface.fill ((0,255,0))
        self.lineSurface.set_colorkey ((0,255,0))
        self.lineSurface.set_alpha(120)

        self.fieldData = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        #for row in self.fieldData:
        #    print(row)

        # Create teromino
        self.tetromino = Tetromino(random.choice(list(TETROMINOES)), self.sprites, self.createNewTetronimo, self.fieldData)

        self.downSpeed = UPDATE_START_SPEED
        self.downSpeedFaster = self.downSpeed * 0.3
        self.downPressed = False
        self.timers = {
            "verticalMove":Timer(UPDATE_START_SPEED, True, self.moveDown),
            "horizontalMove":Timer(MOVE_WAITTIME),
            "rotateShape":Timer(ROTATE_WAITTIME)
        }

        self.timers["verticalMove"].activate()

        # Score
        self.currentLevel = 1
        self.currentScore = 0
        self.currentLines = 0

        # sound
        self.landingSound = pygame.mixer.Sound(join('sound','landing.wav'))
        self.landingSound.set_volume(0.1)


    def calculateScore (self, numLines):
        self.currentLines += numLines
        self.currentScore += SCOREDATA[numLines] * self.currentLevel

        # every 10 lines increase level
        if self.currentLines / 10 > self.currentLevel:
            self.currentLevel += 1

        self.updateScore(self.currentLines, self.currentScore, self.currentLevel)

    def checkGameOver(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                exit()

    def createNewTetronimo(self):
        self.landingSound.play()
        self.checkGameOver()
        self.checkFinishedRows()
        self.tetromino = Tetromino(self.getNextShape(), self.sprites, self.createNewTetronimo, self.fieldData)
        

    def timerUpdate(self):
        for timer in self.timers.values():
            timer.update()

    def moveDown(self):
        self.tetromino.moveDown(1)

    def input (self):
        keys = pygame.key.get_pressed()

        if not self.timers["horizontalMove"].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.moveHorizontal(-1)
                self.timers["horizontalMove"].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.moveHorizontal(1)
                self.timers["horizontalMove"].activate()

        if not self.timers["rotateShape"].active:
             if keys[pygame.K_UP]:
                 self.tetromino.rotateShape()
                 self.timers["rotateShape"].activate()

        if not self.downPressed and keys[pygame.K_DOWN]:
            self.timers['verticalMove'].duration = self.downSpeedFaster
            self.downPressed = True

        if self.downPressed and not keys[pygame.K_DOWN]:
            self.timers['verticalMove'].duration = self.downSpeed
            self.downPressed = False

    def run(self):

        self.timerUpdate()
        self.sprites.update()
        self.input()

        self.surface.fill(GREY)
        self.sprites.draw(self.surface)
        self.drawGrid()
        self.displaySurface.blit(self.surface, (PADDING,PADDING))
        pygame.draw.rect (self.displaySurface, LINECOLOUR, self.rect, 2, 2)

    def drawGrid(self):
        for col in range (1, COLUMNS):
            x = col * CELLSIZE
            pygame.draw.line(self.lineSurface, LINECOLOUR, (x,0), (x, self.surface.get_height()), 1)

        for row in range (1, ROWS):
            y = row * CELLSIZE
            pygame.draw.line(self.lineSurface, LINECOLOUR, (0,y), (self.surface.get_width(), y), 1)

        self.surface.blit(self.lineSurface, (0,0))

    def checkFinishedRows(self):
        # Get row full indexes from fieldData
        deleteRows = []

        for i, row in enumerate(self.fieldData):
            if all(row):
                deleteRows.append(i)

        if deleteRows:
            for deleteRow in deleteRows:
                # remove full row
                for block in self.fieldData[deleteRow]:
                    block.kill()

                # Move blocks down
                for row in self.fieldData:
                    for block in row:
                        if block and block.pos.y < deleteRow:
                            block.pos.y += 1

            self.calculateScore(len(deleteRows))

            # rebuild fieldData
            self.fieldData = [[0 for x in range(COLUMNS)] for y in range(ROWS)]   # Clear fieldData
            for block in self.sprites:
                self.fieldData[int(block.pos.y)][int(block.pos.x)] = block

        

class Tetromino:
    def __init__(self, shape, group, createNewTetronimo, fieldData):
        self.blockPositions = TETROMINOES[shape]["shape"]
        self.colour = TETROMINOES[shape]["colour"]
        self.shape = shape

        self.createNewTetronimo = createNewTetronimo
        self.fieldData = fieldData
        self.blocks = [Block(group, pos, self.colour) for pos in self.blockPositions]

    # Collisions
    def nextMoveHorizontalCollide (self, blocks, delta):
        collisionList = [block.horizontalCollide(int(block.pos.x + delta), self.fieldData) for block in self.blocks]
        return True if any(collisionList) else False

    def nextMoveVerticalCollide (self, blocks, delta):
        collisionList = [block.verticalCollide(int(block.pos.y + delta), self.fieldData) for block in self.blocks]
        return True if any(collisionList) else False

    # Movements
    def moveDown(self, delta):
        if not self.nextMoveVerticalCollide(self.blocks, delta):
            for block in self.blocks:
                block.pos.y += delta
        else:
            for block in self.blocks:
                self.fieldData[int(block.pos.y)][int(block.pos.x)] = block
            self.createNewTetronimo()


    def moveHorizontal (self, delta):
        if not self.nextMoveHorizontalCollide(self.blocks, delta):
            for block in self.blocks:
                block.pos.x += delta

    def rotateShape(self):
        if self.shape != 'O':
            # Find pivot point
            pivotPoint = self.blocks[0].pos

            newBlockPositions = [block.rotate(pivotPoint) for block in self.blocks]

            # Check bounds
            for pos in newBlockPositions:
                # off side of screen
                if pos.x < 0 or pos.x >= COLUMNS:
                    return

                # Other shapes
                if self.fieldData[int(pos.y)][int(pos.x)]:
                    return

                # At the bottom??
                if pos.y > ROWS:
                    return

            for i, block in enumerate(self.blocks):
                block.pos = newBlockPositions[i]

class Block (pygame.sprite.Sprite):
    def __init__(self, group, pos, colour):
        super().__init__(group)
        self.image = pygame.Surface ((CELLSIZE, CELLSIZE))
        self.image.fill(colour)
        self.pos = pygame.Vector2 (pos) + BLOCKOFFSET

        self.rect = self.image.get_rect(topleft = self.pos * CELLSIZE)

    def rotate(self, pivotPosition):
        #distance = self.pos - pivotPosition
        #rotated = distance.rotate (90)
        #newPos = pivotPosition + rotated
        #return newPos
        return pivotPosition + (self.pos - pivotPosition).rotate(90)

    def update(self):
        self.rect.topleft = self.pos * CELLSIZE

    def horizontalCollide (self, xPos, fieldData):
        if not 0 <= xPos < COLUMNS:
            return True
        
        if fieldData[int(self.pos.y)][xPos]:
            return True
        
    def verticalCollide (self, yPos, fieldData):
        if yPos >= ROWS:
            return True
    
        if yPos >= 0 and fieldData[yPos][int(self.pos.x)]:
            return True
