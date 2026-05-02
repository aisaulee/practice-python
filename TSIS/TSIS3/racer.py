import pygame
import random
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

WIDTH, HEIGHT = 400, 600
FPS = 60

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
YELLOW = (255, 200, 0)
CYAN   = (0, 255, 255)
PURPLE = (128, 0, 128)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join(ASSETS_DIR, "player.png"))
            self.image = pygame.transform.scale(self.image, (45, 80))
        except:
            self.image = pygame.Surface((45, 80))
            self.image.fill(CYAN)
            
        self.rect = self.image.get_rect(center=(200, 520))
        
        self.vel_x = 0         
        self.accel = 0.8      
        self.friction = 0.9    
        self.max_speed = 10  

    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.vel_x -= self.accel
        elif keys[pygame.K_RIGHT]:
            self.vel_x += self.accel
        else:
            self.vel_x *= self.friction

        if self.vel_x > self.max_speed: self.vel_x = self.max_speed
        if self.vel_x < -self.max_speed: self.vel_x = -self.max_speed

        if abs(self.vel_x) < 0.1:
            self.vel_x = 0

        self.rect.x += self.vel_x

        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0 
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel_x = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_boost):
        super().__init__()
        try:
            img_name = random.choice(["enemy1.png", "enemy2.png", "enemy3.png"])
            self.image = pygame.image.load(os.path.join(ASSETS_DIR, img_name))
            self.image = pygame.transform.scale(self.image, (45, 80))
        except:
            self.image = pygame.Surface((45, 80))
            self.image.fill(PURPLE)
            pygame.draw.rect(self.image, WHITE, (0, 0, 45, 80), 2)
            
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), -100))
        self.speed = random.randint(4, 7) + speed_boost

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
            return True
        return False
    
def play_game(screen, username):
    score = 0
    distance = 0
    level = 1
    enemy_speed_boost = 0
    clock = pygame.time.Clock()
    
    player = Player()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    
    spawn_timer = 0
    bg_y = 0 
    road_speed = 0
    running = True
    while running:
        dt = clock.tick(FPS)
        distance += 1
        
        if score > level * 10:
            level += 1
            enemy_speed_boost += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        spawn_timer += dt
        if spawn_timer > max(400, 1200 - (level * 100)): 
            new_enemy = Enemy(enemy_speed_boost)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            spawn_timer = 0

        player.move()
        for en in enemies:
            if en.update():
                score += 1

        if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
            running = False

        screen.fill((10, 10, 20))
        
        bg_y = (bg_y + 5 + enemy_speed_boost) % 100
        for i in range(-100, HEIGHT, 100):
            pygame.draw.line(screen, (40, 40, 80), (100, i + bg_y), (100, i + bg_y + 50), 3)
            pygame.draw.line(screen, (40, 40, 80), (300, i + bg_y), (300, i + bg_y + 50), 3)

        all_sprites.draw(screen)

        font = pygame.font.SysFont("Verdana", 18, bold=True)
        screen.blit(font.render(f"SCORE: {score}", True, CYAN), (15, 15))
        screen.blit(font.render(f"LVL: {level}", True, YELLOW), (15, 40))

        pygame.display.update()

    return score, int(distance / 10)