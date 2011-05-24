import time
import random
import sys
from Game import Game

def main():
    random.seed( time.time() )
    game = Game(10,10,10)
    while game.running:
        game.update()
    game.exit()
    sys.exit(0)

if __name__ == '__main__':
    main()