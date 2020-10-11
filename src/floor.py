import pygame
from src.params import *

class Floor():
    VEL = 5
    WIDTH = FLOOR_IMAGE.get_width()
    HEIGHT = FLOOR_IMAGE.get_height()
    IMG = FLOOR_IMAGE

    def __init__(self, y):
      self.y = y
      self.x1 = 0
      self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 +self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 +self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))