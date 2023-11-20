import pygame

COLUMNS = 10
ROWS = 20
CELLSIZE = 40
GAMEWIDTH, GAMEHEIGHT = COLUMNS * CELLSIZE, ROWS*CELLSIZE

SIDEBARWIDTH = 200
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

PADDING = 20
WINDOWWIDTH = GAMEWIDTH + SIDEBARWIDTH + PADDING * 3
WINDOWHEIGHT = GAMEHEIGHT + PADDING * 2

UPDATE_START_SPEED = 200
MOVE_WAITTIME = 60
ROTATE_WAITTIME = 200
BLOCKOFFSET =   pygame.Vector2 (COLUMNS // 2, -1)

YELLOW = "#F1E60D"
RED = "#E51B20"
BLUE = "#204B9B"
GREEN = "#65B32E"
PURPLE = "#7B217F"
CYAN = "#6CC6D9"
ORANGE = "#F07E13"
GREY = "#1C1C1C"
LINECOLOUR = "#FFFFFF"


# Shapes
TETROMINOES = {
    'T' : {"shape": [(0,0),(-1,0),(1,0),(0,-1)], "colour":PURPLE},
    'O' : {"shape": [(0,0),(0,-1),(1,0),(1,-1)], "colour":YELLOW},
    'J' : {"shape": [(0,0),(0,-1),(0,1),(-1,1)], "colour":BLUE},
    'L' : {"shape": [(0,0),(0,-1),(0,1),(1,1)], "colour":ORANGE},
    'I' : {"shape": [(0,0),(0,-1),(0,-2),(0,1)], "colour":CYAN},
    'S' : {"shape": [(0,0),(-1,0),(0,-1),(1,-1)], "colour":GREEN},
    'Z' : {"shape": [(0,0),(1,0),(0,-1),(-1,-1)], "colour":RED},
}

SCOREDATA = {1:40, 2:100, 3:300, 4:1200}
