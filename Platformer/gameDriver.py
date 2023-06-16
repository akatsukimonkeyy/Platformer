#gameDriver.py
#manages the state of the game
import pygame
from scratches.platformer import gameState


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    #TODO: start from a menu state
    state = gameState.GameState(screen)
    while state.game_running:
        state.manage_events(pygame.event.get())
        state.update.state()
        state.draw_state()
if __name__ == '__main__':
    main()