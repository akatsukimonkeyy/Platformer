#gameState.py
#Manage the level
#keep track of lives, levels completed
from scratches.platformer import gameLevel
import pygame

class GameState():
    ACTIOANABLE_KEYS = [pygame.K_w, pygame.K_a, pygame.K_s,
                        pygame.K_d, pygame.K_SPACE, pygame.K_j]
    def __init__(self, screen):
        self.game_running = True
        self.screen = screen
        self.level = gameLevel.GameLevel(screen)
        #any variables that are going to persist from level to level
        self.number_of_lives = 3

        self.clock = pygame.time.Clock()
        self.max_fps = 45
        self.keys_pressed = []

    def manage_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game_running == False
            elif event.type == pygame.KEYDOWN:
                if event.key in GameState.ACTIOANABLE_KEY and event.key not in self.keys_pressed:
                    self.keys_pressed.append(event.key) #ensures that each key is only added once
            elif event.type == pygame.KEYUP:
                if event.key in GameState.ACTIOANABLE_KEYS:
                    self.keys_pressed.remove(event.key)

    def update_state(self):
        self.level.update(self.keys_pressed)

    def draw_state(self):
        self.level.draw_level()
        pygame.display.flip()
        self.clock.tick(self.max_fps)