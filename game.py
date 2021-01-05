import pygame
import os
import random
import shelve

pygame.font.init()


WIDTH, HEIGHT = 850, 950
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")


#Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))

#player ship
YELLOW_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets","pixel_ship_yellow.png")), (60,60))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

#Explosion
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join("assets", "explosion.png")), (60,60))
#BG
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


class Laser():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x - 20, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def on_screen(self, height):
        return (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship():
    COOLDOWN = 20

    def __init__(self, x, y, health = 100 ):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0




    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)


    def move_lasers(self,vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj): # collision to the players ship 
                obj.health -= 1
                WIN.blit(EXPLOSION, (laser.x, laser.y + 15))
                pygame.display.update()
                pygame.time.delay(250)
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):

    def __init__(self, x, y, health = 5):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        WIN.blit(EXPLOSION, (laser.x, laser.y - 10))
                        pygame.display.update()
                        pygame.time.delay(15)
                        self.lasers.remove(laser)

                    
                            
class Enemy(Ship): 
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health = 1):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel
        
    def special(self):
        if self.ship_img == RED_SPACE_SHIP:
            if self.y >= random.randrange(100, 200) and self.y <= random.randrange(200, 250) and self.x + 100 <= WIDTH:
                self.x += 1 
            elif self.y >= random.randrange(250, 300) and self.y <= random.randrange(300, 350) and self.x - 100 >= 0:
                self.x -= 1 
            elif self.y >= random.randrange(350, 400) and self.y <= random.randrange(400, 450) and self.x + 100 <= WIDTH:
                self.x += 1 
            elif self.y >= random.randrange(450, 500) and self.y <= random.randrange(500, 550) and self.x - 100 >= 0:
                self.x -= 1       
            elif self.y >= random.randrange(550, 600) and self.y <= random.randrange(600, 650) and self.x + 100 <= WIDTH:
                self.x += 1 
            elif self.y >= random.randrange(650, 700) and self.y <= random.randrange(700, 750) and self.x - 100 >= 0:
                self.x -= 1

        if self.ship_img == GREEN_SPACE_SHIP:
            if self.y >= random.randrange(50, 250) and self.y <= random.randrange(250, 450) and self.x - 100 >= 0:
                self.x -= 3 
            elif self.y >= random.randrange(450, 550) and self.y <= random.randrange(500, 650) and self.x + 100 <= WIDTH:
                self.x += 3 
            elif self.y >= random.randrange(650, 750) and self.y <= random.randrange(750, 850) and self.x - 100 >= 0:
                self.x -= 3 
            
        if self.ship_img == BLUE_SPACE_SHIP:
            if self.y >= random.randrange(300, 600)  and self.x - 100 >= 0:
                self.y += 10 
            elif self.y >= random.randrange(450, 550) and self.x + 100 <= WIDTH:
                self.y += 10


    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1




def collide(obj1, obj2,):
    offset_x = obj2.x - obj1.x + 15
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    score = 0
    start_life = lives
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 75)
    enemies = []
    wave_length = 5
    
    enemy_vel = 1
    player_vel = 5
    laser_vel = 5

    player = Player(375, 800)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    with open('score.txt') as file_object:
        contents = file_object.read()
    
    highscore = int(contents) 


    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        score_label = main_font.render(f"{score}", 1, (255, 255, 255))
        high_label = main_font.render(f"{highscore}", 1, (212,175,55))


        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (WIDTH // 2 + score_label.get_width(), 10))
        WIN.blit(high_label, (WIDTH // 2 - high_label.get_width(), 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("Game Over!!", 1, (255,255,255))
            score_label = lost_font.render("Your Score: {}".format(final_score), 1,(255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width() / 2, 350))
            WIN.blit(score_label, (WIDTH/2 - score_label.get_width() / 2, 375))
        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()
        start_level = level
        lives = player.health
        start_life = lives

        if lives <= 0: # determines if when player lost
            lost = True
            lost_count += 1
            final_score = score
            if final_score > int(highscore):
                filename = 'score.txt'
                with open(filename, 'w') as file_object:
                    file_object.write(str(final_score))

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) != wave_length and len(enemies) > 0:  # scoring for destroying a single ship
            score += (wave_length - len(enemies)) * 10
            wave_length -= 1
            if len(enemies) - 1 == 0:
                score += 10

        if len(enemies) == 0: # ends the level
            level += 1
            wave_length = (5 * level) + random.randint(1,9)

            # create the enemies for the level 
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: #left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_height() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_UP]:
            player.shoot()

        # movement of the of the enemy ships and lasers 
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.special()
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 1.5*60)  == 1:
                enemy.shoot()
            if enemy.health == 0:
                enemies.remove(enemy)


        if collide(enemy, player):
            lives -= 1
            enemies.remove(enemy)
        elif enemy.y + enemy.get_height() > HEIGHT:
            enemies.remove(enemy)


        lives = player.health

        if start_level != level and level > 1 and start_life == lives:
            lives_left = main_font.render(f"Lives Left :{lives}", 1, (255, 255, 255))
            WIN.blit(lives_left, (WIDTH // 2 - lives_left.get_width() / 2, HEIGHT // 2 - 25))
            bonus_score = main_font.render(f"Bonus Score :{lives * 10}", 1, (255, 255, 255))
            WIN.blit(bonus_score, (WIDTH // 2 - lives_left.get_width() / 2, HEIGHT // 2 + 25))
            pygame.display.update()
            score += lives * 10
            pygame.time.delay(1500)
        
        if lives != start_life:
            for enemy in enemies[:]:
                enemy.lasers.clear()



        player.move_lasers(- laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press any button to start... ", 1, (255,255,255))
        move_label = title_font.render("Use W,A,S,D to move", 1, (255,255,255))
        fire_label = title_font.render("Fire with Up Arrow", 1, (255,255,255,))
        WIN.blit(title_label, (WIDTH //2 - title_label.get_width() / 2, 350))
        WIN.blit(move_label, (WIDTH // 2 - title_label.get_width() / 2, 400))
        WIN.blit(fire_label, (WIDTH // 2 - title_label.get_width() / 2, 450))
        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()



    pygame.quit()

main_menu()

