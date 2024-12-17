import pygame
import random

def main():
    pygame.init()

    clock = pygame.time.Clock()
    fps = 60
    #game window
    bottom_panel = 150
    screen_width = 800
    screen_height = 400 + bottom_panel

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Battle')

    #define game variables
    current_fighter = 1
    total_fighters = 2
    action_cooldown = 0
    action_wait_time = 90
    attack = False
    clicked = False

    #define fonts
    font = pygame.font.SysFont('Times New Roman', 26)

    #define colors
    white = (255, 255, 255)
    green = (0, 255, 0)

    #load images
    #background images
    background_img = pygame.image.load('images/rpg_backdrop.png').convert_alpha()
    #panel image
    panel_img = pygame.image.load('images/panel.png').convert_alpha()





    # create function for drawing text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    def draw_end_message(text, font, color):
        text_img = font.render(text, True, color)
        text_rect = text_img.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_img, text_rect)


    #fuction for drawing background
    def draw_bg():
        screen.blit(background_img, (0, 0))
    #function for drawing panel
    def draw_panel():
        #draw panel rectangle
        screen.blit(panel_img, (0, screen_height - bottom_panel))
        #show knight stats
        draw_text(f'{knight.name} HP: {knight.hp}', font, white, 100, screen_height - bottom_panel + 10)
        #show name and health
        draw_text(f'{tyranno.name} HP: {tyranno.hp}', font, white, 550, screen_height - bottom_panel + 10)

    #fighter class
    class Fighter():
        def __init__(self, x, y, name, max_hp, strength):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.strength = strength
            self.alive = True
            self.animation_list = []
            self.frame_index = 0
            self.action = 0 #0:idle, 1:attack, 2:death
            self.update_time = pygame.time.get_ticks()
            #load idle image
            temp_list = []
            for i in range(1):
                img = pygame.image.load(f'images/Chrono/Idle/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            #load attack images
            temp_list = []
            for i in range(5):
                img = pygame.image.load(f'images/Chrono/Attack/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
        
        def update(self):
            animation_cooldown = 100
            #handle animation
            #update image
            self.image = self.animation_list[self.action][self.frame_index]
            #check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            #if animation has run out, then reset back to start
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.idle()

        def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


        def attack(self, target):
            #deal damage to enemy
            rand = random.randint(-5, 5)
            damage = self.strength + rand
            target.hp -= damage
            #set variables to attack animation
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def draw(self):
            screen.blit(self.image, self.rect)
    #Boss class
    class Boss():
        def __init__(self, x, y, name, max_hp, strength):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.strength = strength
            self.alive = True
            self.animation_list = []
            self.frame_index = 0
            self.action = 0 #0:idle, 1:attack, 2:death
            self.update_time = pygame.time.get_ticks()
            #load idle image
            temp_list = []
            for i in range(1):
                img = pygame.image.load(f'images/Tyranno/Idle/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            #load attack images
            temp_list = []
            for i in range(5):
                img = pygame.image.load(f'images/Tyranno/Attack/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 1, img.get_height() * 1))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            animation_cooldown = 100
            #handle animation
            #update image
            self.image = self.animation_list[self.action][self.frame_index]
            #check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            #if animation has run out, then reset back to start
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.idle()

        def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        
        def attack(self, target):
            #deal damage to enemy
            rand = random.randint(-5, 5)
            damage = self.strength + rand
            target.hp -= damage
            if target.hp < 1:
                target.hp = 0
                target.alive = False

            #set variables to attack animation
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def draw(self):
            screen.blit(self.image, self.rect)


    class HealthBar():
        def __init__(self, x, y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp

        def draw(self, hp):
            #update with new health
            self.hp = hp
            #calculate health ratio
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, white, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


    knight = Fighter(400, 330, 'Chrono', 200, 10)
    tyranno = Boss(400, 200, 'Tyranno', 500, 20)

    knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
    tyranno_health_bar = HealthBar(550, screen_height - bottom_panel + 40, tyranno.hp, tyranno.max_hp)


    run = True
    while run:

        clock.tick(fps)

        if tyranno.hp <= 0:
            draw_bg()
            draw_end_message("You Won!", pygame.font.SysFont('Times New Roman', 50), green)
            pygame.display.update()
            pygame.time.delay(3000)  # Pause for 3 seconds
            run = False  # Exit the game loop
        elif knight.hp <= 0:
                draw_bg()
                draw_end_message("You Died", pygame.font.SysFont('Times New Roman', 50), (255, 0, 0))  # Red color
                pygame.display.update()
                pygame.time.delay(3000)  # Pause for 3 seconds
                run = False  # Exit the game loop
        else:
            #draw background
            draw_bg()
            #draw panel
            draw_panel()
            #draw health bar
            knight_health_bar.draw(knight.hp)
            tyranno_health_bar.draw(tyranno.hp)

            #draw fighters
            knight.update()
            knight.draw()
            
            tyranno.update()
            tyranno.draw()

        
            # Handle player attacks instantly on click
            if knight.alive:
                pos = pygame.mouse.get_pos()
                if tyranno.rect.collidepoint(pos) and clicked:
                    knight.attack(tyranno)
    
            if tyranno.alive and knight.alive:
               action_cooldown += 1
            if action_cooldown >= action_wait_time:
                tyranno.attack(knight)
                action_cooldown = 0
            
        #  if current_fighter > total_fighters:
        #     current_fighter = 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                else: 
                    clicked = False
        pygame.display.update()
    pygame.quit()
# Only run the game if this script is executed directly
if __name__ == "__main__":
    main()