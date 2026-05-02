import pygame
import random
from config import WIDTH, HEIGHT, CELL, COLS, ROWS, FOOD_PER_LEVEL

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

class Snake:
    def __init__(self, settings):
        self.body = [Point(COLS // 2, ROWS // 2)]
        self.direction = Point(1, 0)
        self.score = 0
        self.level = 1
        self.foods_eaten = 0
        self.alive = True

        self.color = tuple(int(c) for c in settings.get("snake_color", [50, 200, 50]))
        self.head_color = tuple(int(c) for c in settings.get("head_color", [220, 50, 50]))
        
        self.speed_effect = None
        self.speed_effect_end = 0
        self.shield_active = False

    def handle_key(self, key):
        if key == pygame.K_UP and self.direction.y == 0:
            self.direction = Point(0, -1)
        elif key == pygame.K_DOWN and self.direction.y == 0:
            self.direction = Point(0, 1)
        elif key == pygame.K_LEFT and self.direction.x == 0:
            self.direction = Point(-1, 0)
        elif key == pygame.K_RIGHT and self.direction.x == 0:
            self.direction = Point(1, 0)

    def move(self, obstacles):
        head = self.body[0]
        new_head = Point(head.x + self.direction.x, head.y + self.direction.y)

        if new_head.x < 0 or new_head.x >= COLS or new_head.y < 0 or new_head.y >= ROWS:
            self.alive = False
            return

        if new_head in self.body or new_head in obstacles:
            if not self.shield_active:
                self.alive = False
                return
            else:
                self.shield_active = False

        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self, amount=1):
        for _ in range(amount):
            self.body.append(Point(self.body[-1].x, self.body[-1].y))

    def shorten(self, amount=1):
        for _ in range(amount):
            if len(self.body) > 1:
                self.body.pop()
            else:
                return False
        return True

    def draw(self, surface):
        for i, p in enumerate(self.body):
            color = self.head_color if i == 0 else self.color
            pygame.draw.rect(surface, color, (p.x * CELL, p.y * CELL, CELL, CELL))

    def current_fps(self):
        base = 10 
        
        if self.speed_effect == "boost": 
            return base + 5
        
        return base

    def apply_powerup(self, kind):
        now = pygame.time.get_ticks()
        if kind == "boost":
            self.speed_effect = "boost"
            self.speed_effect_end = now + 5000
        elif kind == "shield":
            self.shield_active = True

class Food:
    def __init__(self, snake_body, obstacles):
        self.respawn(snake_body, obstacles)
        self.score_val = 1
        self.color = (255, 200, 0) 

    def respawn(self, snake_body, obstacles):
        while True:
            self.pos = Point(random.randint(0, COLS-1), random.randint(1, ROWS-1))
            if self.pos not in snake_body and self.pos not in obstacles:
                break
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        return False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, 
                           (self.pos.x * CELL + CELL//2, self.pos.y * CELL + CELL//2), CELL//2 - 2)

class PoisonFood(Food):
    def __init__(self, snake_body, obstacles):
        super().__init__(snake_body, obstacles)
        self.color = (150, 0, 255)
        self.active = True

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 7000

    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, self.color, (self.pos.x * CELL + 4, self.pos.y * CELL + 4, CELL - 8, CELL - 8))

class PowerUp:
    def __init__(self, snake_body, obstacles, existing_pos=None):
        self.kind = random.choice(["boost", "shield"])
        self.color = (0, 255, 255) if self.kind == "boost" else (255, 255, 255)
        self.active = True
        self.spawn_time = pygame.time.get_ticks()
        while True:
            self.pos = Point(random.randint(0, COLS-1), random.randint(1, ROWS-1))
            if self.pos not in snake_body and self.pos not in obstacles and self.pos != existing_pos:
                break

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 8000

    def draw(self, surface):
        if not self.active: return
        x, y = self.pos.x * CELL, self.pos.y * CELL
        
        c = tuple(int(val) for val in self.color)

        pygame.draw.rect(surface, c, (x + 2, y + 2, CELL - 4, CELL - 4), border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), (x, y, CELL, CELL), 1, border_radius=4)

def generate_obstacles(level, snake_body, old_obstacles):
    new_obs = list(old_obstacles)
    count = level 
    for _ in range(count):
        while True:
            p = Point(random.randint(0, COLS-1), random.randint(1, ROWS-1))
            if p not in snake_body and p not in new_obs:
                new_obs.append(p)
                break
    return new_obs

def draw_obstacles(surface, obstacles):
    for p in obstacles:
        pygame.draw.rect(surface, (100, 100, 100), (p.x * CELL, p.y * CELL, CELL, CELL))
        pygame.draw.rect(surface, (150, 150, 150), (p.x * CELL + 4, p.y * CELL + 4, CELL - 8, CELL - 8))