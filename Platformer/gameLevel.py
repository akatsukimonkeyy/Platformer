#gameLevel.py
#Manage the player sprite, the platforms, the enemies...
import pygame
from scratches.platformer import gameSprites
class GameLevel:
    def __init__(self, screen):
        self.screen = screen
        background_image = pygame.image.load("images/manas.jpeg")
        self.background = pygame.transform.scale(background_image, screen.get_size())
        self.platforms = pygame.sprite.Group()
        self.player_objects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        #self.obstacles = pygame.sprite.Group()

        #build the level here
        self.player = gameSprites.Player(pygame.Vector2(100, 100), pygame.Vector2(50, 75),
                                         pygame.Vector2(0, 0), "images/player.png")
        self.player_objects.add(self.player)

        #add the platforms
        self.ground = gameSprites.GameObject(pygame.Vector2(0, 550), pygame.Vector2(screen.get_width(), 50), "images/ice_platform.png")
        self.platforms.add(gameSprites.GameObject(pygame.Vector2(0, 550), pygame.Vector2(screen.get_width(), 50),
                                             "images/ice_platform.png"))
        self.platforms.add(self.ground)
    def update(self, keys_pressed):
        self.player_objects.update(keys_pressed, self.platforms)
        self.platforms.update()


    def draw_level(self):
        self.screen.blit(self.background, (0, 0))
        self.platforms.draw(self.screen)
        self.player_objects.draw(self.screen)
