#background frames for the title screen

'''
scene_0_background_img_names = []
for i in range(1,4):
    scene_0_background_img_names.append('assets/images/title_screen/title_bg_' + str(i) + '.png')
'''
scene_0_background_img_name = 'assets/images/title_screen/title_bg.png'
#game name image on the title screen
title_img_name = "assets/images/title_screen/title_logo.png"

#normal room background image
scene_1_img_name = "assets/images/level1_screen/scene_1_background.png"
#boss room background image
scene_1_boss_room = "assets/images/level1_screen/boss_room_temp.png"
#starting room background image
scene_1_start_room = "assets/images/level1_screen/start_room_temp.png"

#start button image
start_button_img_name = "assets/images/menu_buttons/start_button.png"
#quit button image
quit_button_img_name = "assets/images/menu_buttons/quit_button.png"
#continue button image
continue_button_img_name = "assets/images/menu_buttons/continue_button.png"

#pause menu background image
pause_menu_img_name = "assets/images/pause_menu/pause_menu.png"

#player ship image
player_img_name = "assets/images/sprites/player_ship/player_ship.png"
#enemy ship image

enemy_1_frames = []
for i in range(1,4):
    enemy_1_frames.append('assets/images/sprites/enemies/enemy_1/enemy_clean/enemy_clean_' + str(i) + '.png')
enemy_1_frames.append('assets/images/sprites/enemies/enemy_1/enemy_clean/enemy_clean_2.png')

enemy_img_name = "assets/images/sprites/enemies/enemy_1/enemy_clean/enemy_clean_1.png"
#player blaster image
player_laser_img_name = "assets/images/sprites/player_blaster/player_blaster.png"

#frames for portal animation
portal_unexplored_img_names = []
for i in range(1,4):
    portal_unexplored_img_names.append('assets/images/sprites/portal/portal_unexplored_' + str(i) + '.png')

#map overlay background image
map_overlay_img = "assets/images/map_overlay/map_overlay_bg.png"

#map icon for starting room
starting_room_img = "assets/images/map_overlay/room_starting_icon.png"
#map icon for boss room
boss_room_img = "assets/images/map_overlay/room_boss_icon.png"
#map icon for unexplored room
unexplored_room_img = "assets/images/map_overlay/room_unexplored_icon.png"
#map icon for explored room

explored_room_img = "assets/images/map_overlay/room_explored_icon.png"

half_heart_img = 'assets/images/ui/hearts/heart_half.png'
full_heart_img = 'assets/images/ui/hearts/heart_full.png'
