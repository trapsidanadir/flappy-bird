import os
import neat

from src.game import ai_fitness

NBR_EPOCHS = 50

def run():
    global NBR_EPOCHS
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'ai_config.txt')


    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                        config_file)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(ai_fitness,NBR_EPOCHS)

    print(winner)
