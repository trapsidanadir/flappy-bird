##
# @author Trapsida Nadir - tran2404 <tran2404@usherbrooke.ca>
 # @file Game Parameters
 # @desc Created on 2020-10-11 11:23:15 am
 # @copyright APPI SASU
 #
import os
import pygame

pygame.mixer.pre_init(channels = 1, buffer = 512)
pygame.font.init()
pygame.init()
screen = pygame.display.set_mode((576,1024))

WIDTH = None
HEIGHT = None

AI_STATS = {'GEN':0,'ALIVE_POP':0}
SCORE_TRESH = 100 #score to save in pickle file

BIRD_IMAGES = None
PIPE_IMAGE = None
FLOOR_IMAGE = None
BG_IMAGE = None
HOME_IMAGE = None

SOUNDS = {}

STAT_FONT = pygame.font.Font(os.path.join('assets',"fonts.ttf"), 50)

def initialize_parameters(width:int = None, height:int = None):
    
    birds_assets_names = ["bird1.png", "bird2.png", "bird3.png"]
    pipe_asset_name = "pipe.png"
    floor_asset_name = "floor.png"
    bg_asset_name = "bg.png"
    home_asset_name = "home.png"
    
    flap_sound_name = "flap.wav"
    die_sound_name = "die.wav"
    hit_sound_name = "hit.wav"
    point_sound_name = "point.wav"

    global WIDTH, HEIGHT, BIRD_IMAGES, PIPE_IMAGE, FLOOR_IMAGE, HOME_IMAGE, BG_IMAGE, SOUNDS

    WIDTH = width if width is not None else 600
    HEIGHT = height if height is not None else 800

    BIRD_IMAGES = [ pygame.transform.scale2x( \
        pygame.image.load( \
            os.path.join("assets", position))) \
                for position in birds_assets_names]

    PIPE_IMAGE =  pygame.transform.scale2x( \
        pygame.image.load( \
            os.path.join("assets", pipe_asset_name))) 
    
    FLOOR_IMAGE =  pygame.transform.scale2x( \
        pygame.image.load( \
            os.path.join("assets", floor_asset_name))) 
    
    BG_IMAGE =  pygame.transform.scale( \
        pygame.image.load( \
            os.path.join("assets", bg_asset_name)),(600, 900)) 
    
    HOME_IMAGE = pygame.transform.scale2x( \
            pygame.image.load( \
                os.path.join("assets", home_asset_name)).convert_alpha()) 

    SOUNDS['FLAP'] = pygame.mixer.Sound(os.path.join('sound', flap_sound_name))
    SOUNDS['DIE'] = pygame.mixer.Sound(os.path.join('sound', die_sound_name))
    SOUNDS['HIT'] = pygame.mixer.Sound(os.path.join('sound', hit_sound_name))
    SOUNDS['POINT'] = pygame.mixer.Sound(os.path.join('sound', point_sound_name))
    
initialize_parameters()
