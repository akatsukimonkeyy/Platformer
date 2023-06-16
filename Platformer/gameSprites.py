#gameSprites.py
#Describe out player, enemy, platform
#Manage collisions, some of the physics

import pygame

class GameObject(pygame.sprite.Sprite):
    CAMERA = pygame.Vector2(0, 0)
    def __init__(self, position, size, image_file):
        super().__init__()
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.image = pygame.transform.scale(pygame.image.load(image_file))
        self.left_facing_image = pygame.transform.flip(self.image, True, False)
        self.right_facing_image = self.image
        self.image = self.left_facing_image

    def change_direction_right_left(self):
        if self.image == self.left_facing_image:
            self.image = self.right_facing_image
        else:
            self.image = self.left_facing_image

    def update(self):
        #make the relative position based on the camera
        relative_position_x = self.position[0] - GameObject.CAMERA[0]
        relative_position_y = self.position[1] - GameObject.CAMERA[1]
        self.rect = pygame.Rect((relative_position_x, relative_position_y), self.position, self.size)

class MovingGameObject(GameObject):

    GRAVITY = pygame.Vector2(0, 0.5)
    FRICTION = pygame.Vector2(0.1, 0)

    def __init__(self, position, size, velocity, image_file):
        super().__init__(position, size, image_file)
        self.velocity = velocity
        self.grounded = False
        self.ground = None

    def update(self, platforms):
        #apply gravity
        if not self.grounded:
            self.velocity += MovingGameObject.GRAVITY
        if self.grounded:
            if self.velocity[0] > 0: #moving right; frction should be negative(to the left)
                self.velocity -= MovingGameObject.FRICTION
                if self.velocity[0] < 0:
                    self.velocity = 0
            elif self.velocity[0] < 0: #moving left; friction is positive:
                self.velocity += MovingGameObject.FRICTION
                if self.velocity[0] > 0:
                    self.velocity[0] = 0
        self.position = self.position + self.velocity
        #check collisions
        super().update()
        colliding_with_platforms = pygame.sprite.spritecollide(self, platforms, False)
        #check if above or below
        if not len(colliding_with_platforms) == 0:
            self.position = self.position - self.velocity #undo last motion before collision
        for pl in colliding_with_platforms:

            if self.rect.bottom <= pl.rect.top and not self.grounded: #above the platform
                self.grounded = True
                self.ground = pl
                self.position[1] = pl.rect.top - self.rect.height
                self.velocity[1] = 0 #stop on impact
                super().update() #update rectangle and image
            elif self.rect.top >= pl.rect.bottom: #below the platform
                self.position[1] = pl.rect.bottom
                self.velocity[0] = 0 #stop on impact
                super().update()
            elif self.rect.bottom <= pl.rect.centrery: #sideward approach
                self.grounded = True
                self.ground = pl
                self.position[1] = self.position[1] = pl.rect.top - self.rect.height
                self.velocity[1] = 0
                super().update()
            else: # bounce ballsl
                self.velocity[0] = -.5 * self.velocity[0]

        #are we sitll grounded?
        if self.grounded and self.ground not in colliding_with_platforms:
            self.grounded = False
            self.ground = None

class Player(MovingGameObject):
    MAX_SPEED_X = 7
    JUMP_SPEED = pygame.Vector2(0, -17)


    def __init__(self, position, size, velocity, image_file):
        super().__init__(position, size, velocity, image_file)

    def update(self, keys_pressed, platforms):
        self.handle_keys_pressed((keys_pressed))
        super().update(platforms) #apply physics, move rectangle
        self.move_camera()

    #Do something for each key pressed
    def handle_keys_pressed(self, keys_pressed):
        for key in keys_pressed:
            if chr(key) == 'a' and self.grounded:
                self.image = self.left_facing_image
                self.velocity += pygame.Vector2(-5, 0)
                if self.velocity < -Player.MAX_SPEED_X:
                    self.velocity[0] = -Player.MAX_SPEED_X
            elif chr(key) == 'd' and self.grounded:
                self.image = self.right_facing_image
                self.velocity += pygame.Vector2(5, 0)
                if self.velocity > -Player.MAX_SPEED_X:
                    self.velocity[0] = -Player.MAX_SPEED_X
            elif chr(key) == 'w':
                if self.grounded:
                    self.velocity += Player.JUMP_SPEED #upward
                    self.grounded = False

            elif chr(key) == 's':
                if self.grounded:
                    self.velocity = pygame.Vector2(0, 0) #stop
            #TODO: Add jumping, maybe flying

    def move_camera(self):
        GameObject.CAMERA[0] = self.position[0] - 300 #300 from the edge


