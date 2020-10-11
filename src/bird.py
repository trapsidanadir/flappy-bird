import pygame
from src.params import *

class Bird():

    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 3
    ROT_VEL = 20
    ANIMATION_TIME = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMAGES[0]

    def jump(self):
        self.vel = -11.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count +=1

        new_pos = self.vel*self.tick_count + 1.5*self.tick_count**2

        new_pos = 16 if new_pos >= 16 else new_pos - 2 if new_pos < 0 else new_pos

        self.y += new_pos

        if new_pos < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else : 
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count +=1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMAGES[0]   
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMAGES[1]   
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMAGES[2]      
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMAGES[1]      
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMAGES[0] 
            self.img_count = 0         
        
        if self.img_count <= -80:
            self.img = self.IMAGES[1] 
            self.img_count = self.ANIMATION_TIME*2    

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
