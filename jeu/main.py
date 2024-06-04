import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import coin
import constants

#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((constants.SCREEN_WIDTH + constants.SIDE_PANEL, constants.SCREEN_HEIGHT), pg.FULLSCREEN)
pg.display.set_caption("Pixel Defender")


#game variables
game_start = False
game_over = False
game_outcome = 0 # -1 is loss & 1 is win
level_started = False
last_enemy_spawn = pg.time.get_ticks()
last_update = pg.time.get_ticks()
placing_turrets = False
selected_turret = None
frame = 0
Blue_Cyan = (0, 120, 120)
BLACK = (0, 0, 0)
main_menu_status = True
setting_status = False
shop_status = False
inventory_status = False
Red_turret_button = "CANNON"
Purple_turret_button = "SNIPER"
Blue_turret_button = "MACHINE_GUN"
Red_turret = False
Purple_turret = False
Blue_turret = False


#load images
#map
map_image = pg.image.load('levels/map.png').convert_alpha()

canon_spritesheets = []
sniper_spritesheets = []
machineGun_spritesheets = []
for x in range(1, constants.TURRET_LEVELS + 1):
#canon spritesheets
    red_turret_sheet = pg.image.load(f'assets/images/turrets/red_turret_{x}.png').convert_alpha()
    canon_spritesheets.append(red_turret_sheet)
#sniper_spritesheets
    purple_turret_sheet = pg.image.load(f'assets/images/turrets/purple_turret_{x}.png').convert_alpha()
    sniper_spritesheets.append(purple_turret_sheet)
#machine gun spritesheets
    blue_turret_sheet = pg.image.load(f'assets/images/turrets/blue_turret_{x}.png').convert_alpha()
    machineGun_spritesheets.append(blue_turret_sheet)

#coin spritesheets
coin_sheet = pg.image.load('assets/images/coins/coin1.png').convert_alpha()
sprite_sheet = coin.Coin_SpriteSheet(coin_sheet)
coin_spritesheets = []
for x in range(constants.COIN_ANIMATION):
    coin_spritesheets.append(sprite_sheet.get_image(x, 33, 32, 1, BLACK))

#turret image for mouse cursor
red_cursor_turret = pg.image.load('assets/images/turrets/red_cursor_turret.png').convert_alpha()
purple_cursor_turret = pg.image.load('assets/images/turrets/purple_cursor_turret.png').convert_alpha()
blue_cursor_turret = pg.image.load('assets/images/turrets/blue_cursor_turret.png').convert_alpha()
#enemies
enemy_images = {
    "weak": pg.image.load('assets/images/enemies/zombie.png').convert_alpha(),
    "medium": pg.image.load('assets/images/enemies/thief.png').convert_alpha(),
    "strong": pg.image.load('assets/images/enemies/knight.png').convert_alpha(),
    "elite": pg.image.load('assets/images/enemies/robot.png').convert_alpha()
}
enemy_image = pg.image.load('assets/images/enemies/zombie.png').convert_alpha()
#buttons
start_image = pg.image.load('assets/images/buttons/start.png').convert_alpha()
shop_image = pg.image.load('assets/images/buttons/shop.png').convert_alpha()
inventory_image = pg.image.load('assets/images/buttons/inventory.png').convert_alpha()
buy_RedTurret_image = pg.image.load('assets/images/turrets/buy_red_turret.png').convert_alpha()
buy_PurpleTurret_image = pg.image.load('assets/images/turrets/buy_Purple_turret.png').convert_alpha()
buy_BlueTurret_image = pg.image.load('assets/images/turrets/buy_Blue_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
begin_image = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
fast_forward_image = pg.image.load('assets/images/buttons/fast_forward.png').convert_alpha()
setting_image = pg.image.load('assets/images/buttons/setting.png').convert_alpha()
close_interface_image = pg.image.load('assets/images/buttons/close_interface.png').convert_alpha()
close_setting_image = pg.image.load('assets/images/buttons/close_setting.png').convert_alpha()
close_app_image = pg.image.load('assets/images/buttons/close_app.png').convert_alpha()
leave_image = pg.image.load('assets/images/buttons/leave.png').convert_alpha()

#gui
heart_image = pg.image.load('assets/images/gui/heart.png').convert_alpha()
logo_image = pg.image.load('assets/images/gui/logo.png').convert_alpha()

#background music 
Background_music = pg.mixer.Sound ('assets/audio/background_music.mp3')
Background_music.set_volume(0)

#load sounds
shot_fx = pg.mixer.Sound ('assets/audio/shot.wav')
shot_fx.set_volume(0.5)

#load json data for level
with open('levels/map.tmj') as file:
    world_data = json.load(file)

#load fonts for displaying text on the screen
Title_interface = pg.font.Font('assets/fonts/minecraft.ttf', 60)
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_font = pg.font.SysFont("Consolas", 36)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    
def display_data():
    #draw panel
    pg.draw.rect(screen, "maroon", (constants.SCREEN_WIDTH, 0, constants.SIDE_PANEL, constants.SCREEN_HEIGHT))
    pg.draw.rect(screen, "grey0", (constants.SCREEN_WIDTH, 0, constants.SIDE_PANEL, 740), 2)
    screen.blit(logo_image, (constants.SCREEN_WIDTH, 740))
    #display data
    draw_text("WAVE: " + str(world.level) + "/15", text_font, "grey100", constants.SCREEN_WIDTH + 10, 10)
    screen.blit(heart_image, (constants.SCREEN_WIDTH + 10, 35))
    draw_text(str(world.health), text_font, "grey100", constants.SCREEN_WIDTH + 50, 40)
    screen.blit(coin_spritesheets[frame],(constants.SCREEN_WIDTH + 10, 65))
    draw_text(str(world.money), text_font, "grey100", constants.SCREEN_WIDTH + 50, 70)

def create_turret(mouse_pos, turret_type):
    mouse_tile_x = mouse_pos[0] // constants.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // constants.TILE_SIZE
    
    # Vérifiez si le joueur est en train de placer une tourelle et si les coordonnées de la souris sont dans la zone de jeu
    if placing_turrets and mouse_pos[0] < constants.SCREEN_WIDTH and mouse_pos[1] < constants.SCREEN_HEIGHT:
        # Calculate the tile number based on mouse position
        mouse_tile_num = (mouse_tile_y * constants.COLS) + mouse_tile_x
        
        # Check if the tile is grass and space is free
        if world.tile_map[mouse_tile_num] == 25:
            space_is_free = True
        else:
            space_is_free = False
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free:
            if Red_turret:
                new_Red_turret = Turret(canon_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx, turret_type="CANNON")
                turret_group.add(new_Red_turret)
                world.money -= constants.BUY_COST
                print(red_turret_sheet)
            elif Purple_turret:
                new_Purple_turret = Turret(sniper_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx, turret_type="SNIPER")
                turret_group.add(new_Purple_turret)
                world.money -= constants.BUY_COST
                print(purple_turret_sheet)
            elif Blue_turret:
                new_Blue_turret = Turret(machineGun_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx, turret_type="MACHINE_GUN")
                turret_group.add(new_Blue_turret)
                world.money -= constants.BUY_COST
                print(blue_turret_sheet)
        
            
def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // constants.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // constants.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret
        
def clear_selection():
    for turret in turret_group:
        turret.selected = False

#create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

#create buttons
start_button = Button(840, 415, start_image, True)
shop_button = Button(70, 350, shop_image, True)
inventory_button = Button(70, 500, inventory_image, True)
Red_turret_button = Button(constants.SCREEN_WIDTH + 30, 120, buy_RedTurret_image, True)
Purple_turret_button = Button(constants.SCREEN_WIDTH + 30, 240, buy_PurpleTurret_image, True)
Blue_turret_button = Button(constants.SCREEN_WIDTH + 30, 360, buy_BlueTurret_image, True)
cancel_button = Button(constants.SCREEN_WIDTH + 100, 160, cancel_image, True)
upgrade_button = Button(constants.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
begin_button = Button(constants.SCREEN_WIDTH + 80, 650, begin_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_forward_button = Button(constants.SCREEN_WIDTH + 50, 500, fast_forward_image, False)
setting_button = Button(constants.SCREEN_WIDTH + 240, 10, setting_image, True)
close_button = Button(1820, 25, close_app_image, True)
close_interface_button = Button(1700, 140, close_interface_image, True)
close_setting_button = Button(1170, 330, close_setting_image, True)
leave_button = Button(875, 600, leave_image, True)

#game loop
run = True
while run:
    
    #event handler
    for event in pg.event.get():
        #setting program

        #quit program
        if event.type == pg.QUIT:
            run = False
        #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
    
    if not game_start:
        if main_menu_status:
            #draw all button on screen
            screen.fill(Blue_Cyan)
            close_button.draw(screen)
            start_button.draw(screen)
            shop_button.draw(screen)
            inventory_button.draw(screen)
            
            #button close the game
            if close_button.click():
                exit()
            #button start the game and play the background music
            if start_button.click():
                game_start = True
                Background_music.play()
            #button open the shop
            if shop_button.click():
                main_menu_status = False
                shop_status = True
            #button open the inventory
            if inventory_button.click():
                main_menu_status = False
                inventory_status = True
            
        else:
            #shop panel
            if shop_status:
                pg.draw.rect(screen, Blue_Cyan, (0, 0, 1920, 1080))
                draw_text("SHOP", Title_interface, "black", 900, 150)
                inventory_button.draw(screen)
                if inventory_button.click():
                    shop_status = False
                    inventory_status = True
                close_interface_button.draw(screen)
                if close_interface_button.click():
                    main_menu_status = True
                    shop_status = False
                    
            #inventory panel
            if inventory_status:
                pg.draw.rect(screen, Blue_Cyan, (0, 0, 1920, 1080))
                draw_text("INVENTORY", Title_interface, "black", 850, 150)
                shop_button.draw(screen)
                if shop_button.click():
                    shop_status = True
                    inventory_status = False
                close_interface_button.draw(screen)
                if close_interface_button.click():
                    main_menu_status = True
                    inventory_status = False
        
    else:
        clock.tick(constants.FPS)
        
        ###############################
        #  UPDATING SECTION
        ###############################
        
        if not game_over :
            #check if player has lost
            if world.health <= 0:
                game_over = True
                game_outcome = -1 #loss
                #check if player has won
            if world.level > constants.TOTAL_LEVELS:
                game_over = True
                game_outcome = 1 #win
            
            #update groups
            enemy_group.update(world)
            turret_group.update(enemy_group, world)
            
            #update animation
            current_time = pg.time.get_ticks()
            if current_time - last_update >= constants.COIN_DELAY:
                frame += 1
                last_update = current_time
                if frame >= len(coin_spritesheets):
                    frame = 0
            
            #highlight selected turret
            if selected_turret:
                selected_turret.selected = True
        
        ###############################
        #  DRAWING SECTION
        ###############################
        
        #draw level
        world.draw(screen)
        
        #draw groups
        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)
            
        display_data()
        
        if game_over == False:
            #check if the level has been started or not
            if level_started == False:
                begin_button.draw(screen)
                if begin_button.click():
                    level_started  = True
                    
            else:
                #fast forward option
                world.game_speed = 1
                fast_forward_button.draw(screen)
                if fast_forward_button.click():
                    world.game_speed = 2
            #spawn enemies
                if pg.time.get_ticks() - last_enemy_spawn > constants.SPAWN_COOLDOWN:
                    if world.spawned_enemies < len(world.enemy_list):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                        enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        last_enemy_spawn = pg.time.get_ticks()
                
            #check if the wave is finished
            if world.check_level_complete() == True:
                world.money += constants.LEVEL_COMPLETE_REWARD
                world.level += 1
                level_started = False
                last_enemy_spawn = pg.time.get_ticks()
                world.reset_level()
                world.process_enemies()
                
            #draw buttons
            #button for placing turrets
            #for the "turret button" show cost of turret and draw the button
            draw_text(str(constants.BUY_COST), text_font, "grey100", constants.SCREEN_WIDTH + 200, 130)
            screen.blit(coin_spritesheets[frame], (constants.SCREEN_WIDTH + 150, 125))
            Red_turret_button.draw(screen)
            if Red_turret_button.click():
                placing_turrets = True
                Red_turret = True
            Purple_turret_button.draw(screen)
            if Purple_turret_button.click():
                placing_turrets = True
                Purple_turret = True
            Blue_turret_button.draw(screen)
            if Blue_turret_button.click():
                placing_turrets = True
                Blue_turret = True
                #if placing turrets then show the cancel button as well
            if placing_turrets:
                #show cursor turret
                if Red_turret :
                    cursor_rect = red_cursor_turret.get_rect()
                elif Purple_turret :
                    cursor_rect = purple_cursor_turret.get_rect()
                elif Blue_turret :
                    cursor_rect = blue_cursor_turret.get_rect()
                cursor_pos = pg.mouse.get_pos()
                cursor_rect.center = cursor_pos
                if cursor_pos[0] <= constants.SCREEN_WIDTH:
                    if Red_turret :
                        screen.blit(red_cursor_turret, cursor_rect)
                    elif Purple_turret :
                        screen.blit(purple_cursor_turret, cursor_rect)
                    elif Blue_turret :            
                        screen.blit(blue_cursor_turret, cursor_rect)
                cancel_button.draw(screen)        
                if cancel_button.click():
                    placing_turrets = False
                    Red_turret = False
                    Purple_turret = False
                    Blue_turret = False
                    
            #if a turret is selected then show the upgrade button
            if selected_turret:
                #if a turret can be upgraded then show the upgrade button
                if selected_turret.upgrade_level < constants.TURRET_LEVELS:
                    #show cost of upgrade and draw the button
                    draw_text(str(constants.UPGRADE_COST), text_font, "grey100", constants.SCREEN_WIDTH + 215, 195)
                    screen.blit(coin_spritesheets[frame], (constants.SCREEN_WIDTH + 260, 190))
                    upgrade_button.draw(screen)
                    if upgrade_button.click():
                        if world.money >= constants.UPGRADE_COST:
                            print(turret_group)
                            selected_turret.upgrade(turret_type="CANNON")
                            world.money -= constants.UPGRADE_COST
            
            #setting panel
            setting_button.draw(screen)
            if setting_button.click():
                setting_status = True
            if setting_status:
                pg.draw.rect(screen, "grey50", (650, 300, 600, 400), border_radius = 30)
                draw_text("SETTING", large_font, "black", 875, 330)
                #closing button
                close_setting_button.draw(screen)
                if close_setting_button.click():
                    setting_status = False
                leave_button.draw(screen)
                if leave_button.click():
                    game_start = False
                    Background_music.stop()
                    game_over = False
                    level_started = False
                    setting_status = False
                    placing_turrets = None
                    last_enemy_spawn = pg.time.get_ticks()
                    world = World(world_data, map_image)
                    world.process_data()
                    world.process_enemies()
                    #empty groups
                    enemy_group.empty()
                    turret_group.empty()
                    
            
        else:
            pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
            if game_outcome == -1:
                draw_text("GAME OVER", large_font, "grey0", 310, 230)
            elif game_outcome == 1:
                draw_text("YOU WIN!", large_font, "grey0", 315, 230)          
            #restart level
            restart_button.draw(screen)
            if restart_button.click():
                game_over = False
                level_started = False
                placing_turrets = False
                select_turret = None
                last_enemy_spawn = pg.time.get_ticks()
                world = World(world_data, map_image)
                world.process_data()
                world.process_enemies()
                #empty groups
                enemy_group.empty()
                turret_group.empty()
        
        #event handler
        for event in pg.event.get():
            #setting program
            
            #quit program
            if event.type == pg.QUIT:
                run = False
            #mouse click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                #check if mouse is on the game area
                if mouse_pos[0] < constants.SCREEN_WIDTH and mouse_pos[1] < constants.SCREEN_HEIGHT:
                    #clear selected turrets
                    selected_turret = None
                    clear_selection()
                    if placing_turrets == True:
                        #check if there is enough money for a turret
                        if world.money >= constants.BUY_COST:
                            create_turret(mouse_pos, turret_type="CANNON")
                    else:
                        selected_turret = select_turret(mouse_pos)
                    Red_turret = False
                    Purple_turret = False
                    Blue_turret = False
                    placing_turrets = False

    #update display
    pg.display.flip()
        
pg.quit()
