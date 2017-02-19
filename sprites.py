import pygame
from values import *

'''
class: controllable player
    image: path to the image for the sprite
    speed: speed of the player
    init_x: initial x coordinate of the player
    init_y: initial y coordinate of the player
'''
class Player(pygame.sprite.Sprite):
    def __init__(self,image,speed,health,init_x,init_y):
        super().__init__()

        self.health = health
        self.speed = speed
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = init_x
        self.rect.y = init_y
        self.x_change = 0
        self.y_change = 0

        self.damage_time = PLAYER_DAMAGE_TIME
        self.current_damage_time = 0

    '''
    function: behave by  adjusting the values
        speed: float speed of the game
    '''
    def behave(self,speed, dt):
        self.rect.x += self.x_change*speed
        self.rect.y += self.y_change*speed

        if self.rect.x >= SCREEN_WIDTH-20:
            self.rect.x = SCREEN_WIDTH-20
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= SCREEN_HEIGHT-20:
            self.rect.y = SCREEN_HEIGHT-20
        if self.rect.y <= 0:
            self.rect.y = 0

        self.current_damage_time += dt

    def on_collision(self, enemy):
        if self.rect.colliderect(enemy.rect):
            if self.current_damage_time >= self.damage_time: 
                self.take_damage(1) 
                self.current_damage_time = 0
    '''
    function: adjust x_change or y_change
        direction: integer 0 through 3 representing different directions
    '''
    def accelerate(self,direction):
        if direction == 0:
            self.y_change = -self.speed
        if direction == 1:
            self.y_change = self.speed
        if direction == 2:
            self.x_change = -self.speed
        if direction == 3:
            self.x_change = self.speed

    '''
    function: set x_change or y_change to 0
        direction: integer 0 through 3 representing different directions
    '''
    def deccelerate(self,direction):
        if direction == 0:
            self.y_change = 0
        if direction == 1:
            self.y_change = 0
        if direction == 2:
            self.x_change = 0
        if direction == 3:
            self.x_change = 0

    def take_damage(self, damage):
        self.health -= damage
'''
class: enemy to be spawned in rooms
    room: room object that the enemy will occupy
    image: string path to the image used
    speed: integer speed of the enemy
    displacement:
    init_x: integer initial x location of the enemy
    init_y: integer initial y location of the enemy
'''
class Enemy(pygame.sprite.Sprite):
    def __init__(self,room,frames,ani_time,displacement,speed,fire_rate,init_x,init_y):
        super().__init__()

        self.room = room
        self.x_speed = speed
        self.y_speed = speed
        self.fire_rate = fire_rate
        self.frames = frames
        self.current_frame_set = self.frames
        self.frame_idx = -1
        self.current_frame = self.frames[0]
        self.image = pygame.image.load(self.current_frame)
        self.rect = self.image.get_rect()
        self.ani_time = ani_time
        self.current_ani_time = 0
        self.max_displacement = displacement
        self.current_displacement = 0
        self.rect.x = init_x
        self.rect.y = init_y
        self.loc_init = (self.rect.x,self.rect.y)

    def animate(self, dt):
        if self.current_ani_time >= self.ani_time:
            self.frame_idx += 1

            if self.frame_idx >= len(self.current_frame_set):
                self.frame_idx = 0
            
            self.current_frame = self.current_frame_set[self.frame_idx]
            self.current_ani_time = 0
            self.image = pygame.image.load(self.current_frame)

            if self.current_frame_set != self.frames:
                self.current_frame_set = self.frames
            
        else:
            self.current_ani_time += dt


    '''
    function: behave by adjusting the objects values
        speed: float speed of the game
    '''
    def behave(self,speed, dt):
        self.animate(dt)
        self.current_displacement = abs(self.loc_init[0]-self.rect.x)

        if self.current_displacement>=self.max_displacement:
            self.x_speed = -self.x_speed

        if self.rect.y >= SCREEN_HEIGHT - self.image.get_height() or self.rect.y <= 0:
            self.y_speed = -self.y_speed

        self.rect.x += self.x_speed*speed
        self.rect.y += self.y_speed*speed

        if self.rect.x >= (self.loc_init[0]+self.max_displacement):
            self.rect.x = self.loc_init[0]+self.max_displacement
        elif self.rect.x <= (self.loc_init[0]-self.max_displacement):
            self.rect.x = self.loc_init[0]-self.max_displacement

'''
class: laser projectile from the player
   room: room object that the laser will occupy
   image: pygame image of the laser
   speed: integer speed of the laser
   x: integer x coordinate of the spawn location
   y: integer y coordinate of the spawn location
'''
class Player_Laser(pygame.sprite.Sprite):
    def __init__(self,room,image,speed,x,y):
        super().__init__()

        self.room = room
        self.speed = speed
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.time_spawned = 0

    '''
    function: behave by adjusting the values of the object
        speed: float speed of the game
        dt: float time between cycles of the main loop
    '''
    def behave(self,speed,dt):
        self.rect.y += -self.speed*speed
        self.time_spawned += dt
        if self.time_spawned >= 1000:
            self.room.laser_sprite_group.remove(self)
            self.room.lasers.remove(self)

    '''
    function: what to do when the object collides with an enemy
        enemy: enemy object that has been collided with
    '''
    def on_collision(self,enemy):
        if self.rect.colliderect(enemy.rect):
            self.room.laser_sprite_group.remove(self)
            self.room.enemy_sprite_group.remove(enemy)
            self.room.lasers.remove(self)
            self.room.enemies.remove(enemy)
            self.room.enemy_count -= 1

    def __repr__(self):
        return "X coor: " + str(self.rect.x) + " Y coor: " + str(self.rect.y) + " Time: " + str(self.time_spawned)

'''
class: portal to transport player to different rooms
    room: room object that the portal occupies
    level: level object that the room occupies
    frames: list of strings of paths to
    ani_time: float time time between frames in the animation
    x: integer initial x location of the portal
    y: integer initial y location of the portal
'''
class Portal(pygame.sprite.Sprite):
    def __init__(self,room,level,frames,ani_time,x,y):
        super().__init__()

        self.room = room
        self.frames = frames
        self.current_frame = frames[0]
        self.image = pygame.image.load(self.current_frame)
        self.frame_idx = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ani_time = ani_time
        self.current_ani_time = ani_time
        self.level = level

    '''
    function: animate the portal
        dt: float time passed in a mainloop cycle
    '''
    def animate(self,dt):
        if self.current_ani_time >= self.ani_time:
            self.current_ani_time = 0
            self.image = pygame.image.load(self.current_frame)

            self.frame_idx += 1
            if self.frame_idx >= len(self.frames):
                self.frame_idx = 0
            self.current_frame = self.frames[self.frame_idx]
        else:
            self.current_ani_time += dt

    '''
    function: what to do when a player collides with a portal
        player: player object that is collided with
        screen: pygame display object that is displayed on
    '''
    def on_collision(self,player,screen,enemy_attr):
        if self.rect.colliderect(player.rect):
            #print("portal touching player")
            if self.rect.x == (SCREEN_WIDTH/2)-20 and self.rect.y == 0:
                #print("top portal touching player")
                self.level.current_room_coor[1] -= 1
                self.level.current_room = self.level.level_map[self.level.current_room_coor[1]][self.level.current_room_coor[0]]
                self.level.current_room.generate(screen, enemy_attr)
                self.level.current_room.ally_sprite_group.add(player)
                player.rect.x = (SCREEN_WIDTH/2)-10
                player.rect.y = SCREEN_HEIGHT - 60

            if self.rect.x == SCREEN_WIDTH-40 and self.rect.y == (SCREEN_HEIGHT/2)-20:
                #print("right portal touching player")
                self.level.current_room_coor[0] += 1
                self.level.current_room = self.level.level_map[self.level.current_room_coor[1]][self.level.current_room_coor[0]]
                self.level.current_room.generate(screen,enemy_attr)
                self.level.current_room.ally_sprite_group.add(player)
                player.rect.x = 60
                player.rect.y = (SCREEN_HEIGHT/2)-10

            if self.rect.x == (SCREEN_WIDTH/2)-20 and self.rect.y == SCREEN_HEIGHT-40:
                #print("bottom portal touching player")
                self.level.current_room_coor[1] += 1
                self.level.current_room = self.level.level_map[self.level.current_room_coor[1]][self.level.current_room_coor[0]]
                self.level.current_room.generate(screen,enemy_attr)
                self.level.current_room.ally_sprite_group.add(player)
                player.rect.x = (SCREEN_WIDTH/2)-10
                player.rect.y = 60

            if self.rect.x == 0 and self.rect.y == (SCREEN_HEIGHT/2)-20:
                #print("left portal touching player")
                self.level.current_room_coor[0] -= 1
                self.level.current_room = self.level.level_map[self.level.current_room_coor[1]][self.level.current_room_coor[0]]
                self.level.current_room.generate(screen,enemy_attr)
                self.level.current_room.ally_sprite_group.add(player)
                player.rect.x = SCREEN_WIDTH - 60
                player.rect.y = (SCREEN_HEIGHT/2)-10
