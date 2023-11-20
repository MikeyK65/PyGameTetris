import pygame

class Timer:
    def __init__(self, duration, repeated = False, func = None):
        self.repeated = repeated
        self.func = func
        self.duration = duration

        self.startTime = 0
        self.active = False

    def activate (self):
        self.active = True
        self.startTime = pygame.time.get_ticks()

    def deactivate (self):
        self.active = False
        self.startTime = 0

    def update (self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.startTime >= self.duration and self.active:
            # call function
            if self.func and self.startTime != 0:
                self.func()

            # reset timer
            self.deactivate()

            # repeat timer if flag set
            if self.repeated:
                self.activate()

                