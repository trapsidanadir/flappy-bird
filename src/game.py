import time
import os 
import random


import pygame
import neat
import pickle

from src.params import *
from src.bird import Bird
from src.pipes import Pipe
from src.floor import Floor


def draw_window(win,birds, pipes, floor, score, alive=True, stats = False):
    win.blit(BG_IMAGE, (0,0))
    floor.draw(win)

    if alive:
        [pipe.draw(win) for pipe in pipes]
        
        [bird.draw(win) for bird in birds]

    else:
        win.blit(HOME_IMAGE, HOME_IMAGE.get_rect(center=(WIDTH/2, HEIGHT/2)))
    
    if stats:
        gen = STAT_FONT.render('Gen: '+str(AI_STATS['GEN']),True,(255,255,255))
        win.blit(gen, (5, 30))

        alive = STAT_FONT.render('Alive: '+str(len(birds)),True,(255,255,255))
        win.blit(alive, (5, (gen.get_height()+30+10)))

        text = STAT_FONT.render('Score:' + str(score), True,(255,255,255))
        win.blit(text, (WIDTH - (10 + text.get_width()), 30))
    
    else:
        text = STAT_FONT.render(str(score), True,(255,255,255))
        win.blit(text, (WIDTH//2 , 30))
            
    pygame.display.update()


def play(win, clock):
    
    scene_params = {'floor':Floor(730), 'pipes':[Pipe(700)], 'bird':[Bird(WIDTH//2,HEIGHT//2)], 'score':0}
    alive = False

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if alive:
                        SOUNDS['FLAP'].play()
                        scene_params['bird'][0].jump()
                    
                    else:
                        alive = True
                    
                        score = 0
                        scene_params['bird'] = [Bird(WIDTH//2,HEIGHT//2)]
                        scene_params['pipes'] = [Pipe(700)]
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if alive:
                    SOUNDS['FLAP'].play()
                    scene_params['bird'][0].jump()
                    
                else:
                    alive = True
                
                    score = 0
                    scene_params['bird'] = [Bird(WIDTH//2,HEIGHT//2)]
                    scene_params['pipes'] = [Pipe(700)]

        scene_params['floor'].move()

        add_pipe = False
        passed_pipes = []
        if alive:
            
            
            for pipe in scene_params['pipes']:
                if pipe.collide(scene_params['bird'][0]):
                    SOUNDS['HIT'].play()
                    
                    alive = False
                    scene_params['score'] = 0
                
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    passed_pipes.append(pipe)
                
                if not pipe.passed and pipe.x < scene_params['bird'][0].x :
                    pipe.passed = True
                    add_pipe = True

                pipe.move() if alive else None

                if scene_params['bird'][0].y + scene_params['bird'][0].img.get_height() >= 730 or scene_params['bird'][0].y < 0:
                    alive = False
                    scene_params['score'] = 0
                    SOUNDS['DIE'].play()
                        
        
        if add_pipe:
            scene_params['score']+=1
            SOUNDS['POINT'].play()
            scene_params['pipes'].append(Pipe(600))
        
        for passed_pipe in passed_pipes:
             scene_params['pipes'].remove(passed_pipe)

        
        scene_params['bird'][0].move() if alive else None
        draw_window(win,scene_params['bird'],scene_params['pipes'],scene_params['floor'], scene_params['score'], alive=alive)
    

def ai_fitness(genomes, config):
    global AI_STATS, SCORE_TRESH
    SOUNDS['DIE'].play()
    AI_STATS['GEN'] += 1

    win =  pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()

    ai_params = {'networks':[], 'genomes':[], 'birds':[]}

    scene_params = {'floor':Floor(730), 'pipes':[Pipe(700)], 'score':0}

    for _ , genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
        ai_params['genomes'].append(genome)
        ai_params['networks'].append(network)
        ai_params['birds'].append(Bird(250,350))

    run = True
    while run and len(ai_params['birds']) > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        scene_params['floor'].move()

        pipe_index = 0
        if len(ai_params['birds']) > 0:
            if len(scene_params['pipes']) > 1 \
                and ai_params['birds'][0].x > scene_params['pipes'][0].x + \
                        scene_params['pipes'][0].PIPE_TOP.get_width():
                            pipe_index = 1
        
        else:
            run = False
            break

        add_pipe = False
        passed_pipes = []
        for pipe in scene_params['pipes']:
            for index, bird in enumerate(ai_params['birds']):
                if pipe.collide(bird):
                    ai_params['genomes'][index].fitness -= 1
                    ai_params['birds'].pop(index)
                    ai_params['networks'].pop(index)
                    ai_params['genomes'].pop(index)
                        
                if not pipe.passed and pipe.x < bird.x :
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                passed_pipes.append(pipe)

            pipe.move()
        
        if add_pipe:
            scene_params['score']+=1
            
            [ (lambda x: x + 5)(genome.fitness) for genome in ai_params['genomes'] ]
            
            scene_params['pipes'].append(Pipe(600))
        
        for index, bird in enumerate(ai_params['birds']):
            bird.move()
            ai_params['genomes'][index].fitness += 0.1
            output = ai_params['networks'][index].activate((bird.y, 
                abs(bird.y-scene_params['pipes'][pipe_index].height), 
                    abs(bird.y-scene_params['pipes'][pipe_index].bottom)))
            
            bird.jump() if output[0] > 0.6 else None

            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                ai_params['birds'].pop(index)
                ai_params['networks'].pop(index)
                ai_params['genomes'].pop(index)
        
        for passed_pipe in passed_pipes:
             scene_params['pipes'].remove(passed_pipe)

        if scene_params['score'] > SCORE_TRESH:
            save_file = os.path.join('ai','pretrained.pickle')
            pickle.dump(ai_params['networks'][0],open("pretrained.pickle", "wb"))
            break

        draw_window(win,ai_params['birds'],scene_params['pipes'],scene_params['floor'], scene_params['score'], 
            stats=True)


def run():
    win =  pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()

    play(win, clock)

    pygame.quit()

