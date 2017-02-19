import pygame
import random as rand
from sprites import *
from values import *
from assets import *

'''
class: room to make up levels
    level: level object that the room belongs to
    room_type: integer representing the type of room
    enemy_number: interger number of enemies to be spawned in the room
'''
class Room():
    def __init__(self,level,room_type):

        self.room_type = room_type
        self.room_background_path = self.generate_room_background_path()
        self.room_background = None
        self.enemy_number = -1 
        self.enemy_count = 0
        self.enemy_sprite_group = pygame.sprite.Group()
        self.laser_sprite_group = pygame.sprite.Group()
        self.ally_sprite_group = pygame.sprite.Group()
        self.interactable_sprite_group = pygame.sprite.Group()
        self.enemies = []
        self.lasers = []
        self.portals = []
        self.portals_generated = False
        self.connections = [0,1,2,3]
        self.level = level
        self.room_background = pygame.image.load(self.room_background_path).convert()

    '''
    function: generate the string path to the background to be used
    '''
    def generate_room_background_path(self):
        result = None
        if self.room_type == 0:
            result = scene_1_start_room
        elif self.room_type == 2:
            result = scene_1_boss_room
        else:
            result = scene_1_img_name
        return result

    '''
    function: generate the room and enemies
        screen: pygame display to generate on
    '''
    def generate(self,screen,enemy_attr):
        self.generate_room(screen)
        self.generate_enemies(enemy_attr)
    
    '''
    function: generate the room
        screen: pygame display to generate on
    '''
    def generate_room(self,screen):
        screen.blit(self.room_background,(0,0))
    
    '''
    function: generate the enemies in the room
    '''
    def generate_enemies(self,enemy_attr):
        if self.enemy_number == -1:
            self.enemy_number = enemy_attr[0]
            self.enemy_count = enemy_attr[0]
        i=0
        while i < self.enemy_number:
            speed = enemy_attr[1] 
            fire_rate = enemy_attr[2] 
            displacement = 50
            enemy = Enemy(self,enemy_1_frames,ENEMY_1_ANI_TIME,displacement,speed,fire_rate,100+i*50,1)
            self.enemy_sprite_group.add(enemy)
            self.enemies.append(enemy)
            i += 1
    
    '''
    function: generate the rooms portals
    '''
    def generate_portals(self):
        for c in self.connections:
            loc = (100,100)
            if c == 0:
                loc = ((SCREEN_WIDTH/2)-20,0)
            elif c == 1:
                loc = (SCREEN_WIDTH-40,(SCREEN_HEIGHT/2)-20)
            elif c == 2:
                loc = ((SCREEN_WIDTH/2)-20,SCREEN_HEIGHT-40)
            elif c == 3:
                loc = (0,(SCREEN_HEIGHT/2)-20)
            portal = Portal(self,self.level,portal_unexplored_img_names,90,loc[0],loc[1])
            self.interactable_sprite_group.add(portal)
            self.portals.append(portal)
    
    '''
    function: generate the players laser
        player: player object to generate the lasers for
    '''
    def generate_player_laser(self,player):
        new_laser = Player_Laser(self,player_laser_img_name,20,(player.rect.x+(player.width/2)-(5/2)),player.rect.y)
        self.laser_sprite_group.add(new_laser)
        self.lasers.append(new_laser)

    '''
    function: draw the enemies for the room
        screen: pygame display to draw the enemies on
    '''
    def draw_enemies(self,screen):
        self.enemy_sprite_group.draw(screen)

    '''
    function: draw the lasers in the room
        screen: pygame display to draw the lasers in
    '''
    def draw_lasers(self,screen):
        self.laser_sprite_group.draw(screen)

    '''
    function: draw allies in the room
        screen: pygame display to draw the allies in
    '''
    def draw_allies(self,screen):
        self.ally_sprite_group.draw(screen)

    '''
    function: draw the portals in the room
        screen: pygame display to draw the portals on
        dt: time passed between cycles of the main loop
    '''
    def draw_portals(self,screen,dt):
        for p in self.portals:
            p.animate(dt)

        self.interactable_sprite_group.draw(screen)

    '''
    function: draw everything in the room
        screen: pygame display to draw it on
        dt: time passed between cycles of the main loop
    '''
    def draw_all(self,screen,dt):
        self.generate_room(screen)
        self.draw_enemies(screen)

        if not self.portals_generated and self.enemy_count == 0:
            self.enemy_number = 0
            self.generate_portals()
            self.portals_generated = True
            self.draw_portals(screen,dt)
        elif self.portals_generated:
            self.draw_portals(screen,dt)

        self.draw_lasers(screen)
        self.draw_allies(screen)



    def __repr__(self):
        return str(self.room_type)+ " " + str(self.connections) + " " + str(self.level.current_room_coor)

'''
class: level to contain an array of levels
    size: integer size of the level (side of a square)
'''
class Level():
    def __init__(self,size):

        self.current_room_coor = None
        self.size = size
        self.level_map = []
        self.locs = self.generate_locations()
        self.current_room = None
        self.generate_map()
        #self.user_map = map_overlay = Splash_Screen((0,0),0,map_overlay_backgrounds,[(starting_room,(305,225))],[])
        #self.current_room = self.rooms[0]

    '''
    function: generate locations of rooms
    '''
    def generate_locations(self):

        spaces = self.size*self.size
        room_count = spaces//2
        center = (self.size//2,self.size//2)
        floor_map = []
        coors = []
        #first run through, generate map full of coordinates, marking the center coordinate appropriatly
        for row in range(self.size):
            new_row = []
            for col in range(self.size):
                current_coor = (col,row)
                if current_coor == (center):
                    new_row.append((col,row,"*"))
                    coors.append((col,row,"*"))
                elif current_coor == (center[0]+1,center[1]) or current_coor == (center[0]-1,center[1]) or current_coor == (center[0],center[1]+1) or current_coor == (center[0],center[1]-1):
                    new_row.append((col,row))
                    coors.append((col,row))
                else:
                    new_row.append(None)
            floor_map.append(new_row)

        #generate rest of rooms
        #print(coors)
        coors_generated = 5

        while coors_generated < room_count:

            y=0
            for row in floor_map:
                room_gen = rand.randint(0,self.size-1)
                if row[room_gen] == None and coors_generated < room_count:
                    coor_candidate = (room_gen,y)
                    coor_added = False
                    for coor in coors:
                        if coor_candidate[1] == coor[1] and coor_candidate[0] == coor[0]+1 or coor_candidate[1] == coor[1] and coor_candidate[0] == coor[0]-1 or coor_candidate[0] == coor[0] and coor_candidate[1] == coor[1]+1 or coor_candidate[0] == coor[0] and coor_candidate[1] == coor[1]-1:
                            coors_generated += 1
                            coors.append(coor_candidate)
                            coor_added = True
                            row[room_gen] = coor_candidate
                            #print(coors)
                        if coor_added:
                            break
                #print(floor_map)
                y += 1

        #generate the boss room

        #find rooms that are the furthest from the starting room
        max_dist = 0
        boss_candidates = []
        for coor in coors:
            dist = abs(coor[0]-center[0]) + abs(coor[1]-center[1])
            #print(str(coor) + " " + str(dist))
            if dist > max_dist:
                max_dist = dist

        #add rooms with the maximum distance to the list of candidates
        for coor in coors:
            if abs(coor[0]-center[0]) + abs(coor[1]-center[1]) == max_dist:
                boss_candidates.append(coor)

        #choose a candidate
        boss_room = boss_candidates[rand.randint(0,len(boss_candidates)-1)]

        for coor in coors:
            if boss_room == coor:
                new_coor = (coor[0],coor[1],"x")
                coors.remove(coor)
                coors.append(new_coor)
                break

        print(boss_candidates)
        print(boss_room)
        for row in floor_map:
            print(row)

        return coors
    
    '''
    function: generate the levels map
    '''
    def generate_map(self):
        coor = (None,None)


        #generate map layout
        for y in range(self.size):
            new_row = []

            for x in range(self.size):
                coor = (x,y)
                added = False
                for l in self.locs:
                    if l[0] == coor[0] and l[1] == coor[1]:
                        if len(l) > 2:

                            if l[2] == "*":
                                self.current_room = Room(self,0)
                                self.current_room_coor = [coor[0],coor[1]]
                                new_row.append(self.current_room)
                                self.locs.remove(l)
                                added = True
                            elif l[2] == "x":
                                new_row.append(Room(self,2))
                                self.locs.remove(l)
                                added = True
                        else:
                            new_row.append(Room(self,1))
                            self.locs.remove(l)
                            added = True
                if not added:
                    new_row.append(None)

            self.level_map.append(new_row)

        #generate connections
        current_x = 0
        current_y = 0
        for y in self.level_map:

            for x in y:
                #print("coor: " + str(current_x) + "," + str(current_y))
                if x != None:
                    #generate top portal
                    if current_y == 0:
                        x.connections.remove(0)


                    elif current_y > 0:
                        if self.level_map[current_y-1][current_x] == None:
                            x.connections.remove(0)

                    #generate right portal
                    if current_x == len(y)-1:
                        x.connections.remove(1)
                    elif current_x < len(y)-1:
                        if self.level_map[current_y][current_x+1] == None:
                            x.connections.remove(1)

                    #generate bottom portal
                    if current_y == len(self.level_map)-1:
                        x.connections.remove(2)
                    elif current_y < len(self.level_map)-1:
                        if self.level_map[current_y+1][current_x] == None:
                            x.connections.remove(2)

                    #generate left portal
                    if current_x == 0:
                        x.connections.remove(3)
                    elif current_x > 0:
                        if self.level_map[current_y][current_x-1] == None:
                            x.connections.remove(3)


                current_x += 1
            current_x = 0
            current_y += 1
        #print(self.level_map)
