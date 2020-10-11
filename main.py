import sys
import src.game as game
import ai.ai as ai

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ai.run() if str(sys.argv[1]) == 'ai' else game.run()
    else:
        game.run()

