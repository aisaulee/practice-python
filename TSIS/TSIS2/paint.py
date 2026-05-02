import pygame
import math
from pygame.locals import *
from collections import deque
from datetime import datetime

pygame.init()
WIDTH, HEIGHT = 1000, 750 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ArtStudio Pro")
clock = pygame.time.Clock()


BG_DARK      = (30, 30, 35)     
PANEL_COLOR  = (45, 45, 50)      
ACCENT_COLOR = (0, 120, 215)    
TEXT_COLOR   = (220, 220, 220)
BTN_NORMAL   = (60, 60, 65)
BTN_HOVER    = (80, 80, 85)

tools = ['Brush', 'Pencil', 'Line', 'Rect', 'Circle', 'Square',
         'RightTri', 'EquiTri', 'Rhombus', 'Fill', 'Eraser', 'Text']
current_tool = "Brush"

canvas = pygame.Surface((980, 620))
canvas.fill((255, 255, 255))
canvas_rect = pygame.Rect(10, 110, 980, 620)

start_pos = None
last_pos  = None          

colors = [(0, 0, 0), (255, 50, 50), (50, 255, 50), (50, 50, 255),
          (255, 255, 50), (255, 50, 255), (50, 255, 255), (255, 165, 0),
          (128, 0, 128), (255, 255, 255)]
current_color = (0, 0, 0)

brush_sizes = {1: 2, 2: 6, 3: 12}
current_size_key = 1

text_active = False
text_pos    = (0, 0)
text_buffer = ""
font_main   = pygame.font.SysFont("Segoe UI", 18, bold=True)
font_small  = pygame.font.SysFont("Segoe UI", 14)

status_msg   = "Ready"
status_timer = 0

def flood_fill(surface, pos, new_color):
    x0, y0 = pos
    w, h = surface.get_size()
    if not (0 <= x0 < w and 0 <= y0 < h): return
    old_color = surface.get_at((x0, y0))[:3]
    new_color3 = new_color[:3]
    if old_color == new_color3: return
    surface.lock()
    queue = deque([(x0, y0)])
    visited = {(x0, y0)}
    while queue:
        x, y = queue.popleft()
        if surface.get_at((x, y))[:3] != old_color: continue
        surface.set_at((x, y), new_color)
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    surface.unlock()

def save_canvas():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"art_{ts}.png"
    pygame.image.save(canvas, filename)
    return filename

#Главный цикл
running = True
while running:
    dt = clock.tick(120)
    mx, my = pygame.mouse.get_pos()
    brush_size = brush_sizes[current_size_key]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == KEYDOWN:
            if text_active:
                if event.key == K_RETURN:
                    img = font_main.render(text_buffer, True, current_color)
                    canvas.blit(img, text_pos)
                    text_active = False
                    text_buffer = ""
                elif event.key == K_ESCAPE:
                    text_active = False
                    text_buffer = ""
                elif event.key == K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                elif event.unicode and event.unicode.isprintable():
                    text_buffer += event.unicode
                continue

            mods = pygame.key.get_mods()
            if event.key == K_s and (mods & KMOD_CTRL):
                fn = save_canvas()
                status_msg = f"Exported: {fn}"
                status_timer = 3000

            if event.key == K_1: current_size_key = 1
            if event.key == K_2: current_size_key = 2
            if event.key == K_3: current_size_key = 3
            if event.key == K_ESCAPE: start_pos = None

        if event.type == MOUSEBUTTONDOWN:
            for i, tool in enumerate(tools):
                rect = pygame.Rect(10 + i * 82, 10, 78, 35)
                if rect.collidepoint(mx, my):
                    current_tool = tool
                    text_active = False
            for i, color in enumerate(colors):
                rect = pygame.Rect(10 + i * 40, 55, 35, 35)
                if rect.collidepoint(mx, my):
                    current_color = color

            for key in brush_sizes:
                rect = pygame.Rect(450 + (key - 1) * 60, 55, 55, 35)
                if rect.collidepoint(mx, my):
                    current_size_key = key

            if canvas_rect.collidepoint(mx, my):
                cp = (mx - canvas_rect.x, my - canvas_rect.y)
                if current_tool == "Text":
                    text_active, text_pos, text_buffer = True, cp, ""
                elif current_tool == "Fill":
                    flood_fill(canvas, cp, current_color)
                else:
                    start_pos = cp
                    last_pos  = cp

        elif event.type == MOUSEMOTION:
            if pygame.mouse.get_pressed()[0] and canvas_rect.collidepoint(mx, my):
                cp = (mx - canvas_rect.x, my - canvas_rect.y)
                if current_tool in ("Brush", "Pencil"):
                    pygame.draw.line(canvas, current_color, last_pos, cp, brush_size)
                    last_pos = cp
                elif current_tool == "Eraser":
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, cp, brush_size * 4)
                    last_pos = cp

        elif event.type == MOUSEBUTTONUP:
            if start_pos and canvas_rect.collidepoint(mx, my):
                ep = (mx - canvas_rect.x, my - canvas_rect.y)
                dx, dy = ep[0] - start_pos[0], ep[1] - start_pos[1]

                if current_tool == "Line":
                    pygame.draw.line(canvas, current_color, start_pos, ep, brush_size)
                elif current_tool == "Rect":
                    r = (min(start_pos[0], ep[0]), min(start_pos[1], ep[1]), abs(dx), abs(dy))
                    pygame.draw.rect(canvas, current_color, r, brush_size)
                elif current_tool == "Circle":
                    rad = int(math.hypot(dx, dy))
                    pygame.draw.circle(canvas, current_color, start_pos, rad, brush_size)
                elif current_tool == "Square":
                    side = max(abs(dx), abs(dy))
                    sx = start_pos[0] if dx > 0 else start_pos[0] - side
                    sy = start_pos[1] if dy > 0 else start_pos[1] - side
                    pygame.draw.rect(canvas, current_color, (sx, sy, side, side), brush_size)
                elif current_tool == "RightTri":
                    pygame.draw.polygon(canvas, current_color, [start_pos, (start_pos[0], ep[1]), ep], brush_size)
                elif current_tool == "EquiTri":
                    h = int(dx * math.sqrt(3) / 2)
                    pygame.draw.polygon(canvas, current_color, [start_pos, (start_pos[0]+dx, start_pos[1]), (start_pos[0]+dx//2, start_pos[1]-h)], brush_size)
                elif current_tool == "Rhombus":
                    pts = [(start_pos[0]+dx//2, start_pos[1]), (start_pos[0]+dx, start_pos[1]+dy//2), (start_pos[0]+dx//2, start_pos[1]+dy), (start_pos[0], start_pos[1]+dy//2)]
                    pygame.draw.polygon(canvas, current_color, pts, brush_size)

            start_pos = None
            last_pos  = None

    screen.fill(BG_DARK)
    
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, 100))
    
    pygame.draw.rect(screen, (0,0,0), canvas_rect.inflate(4, 4), border_radius=5)
    screen.blit(canvas, canvas_rect)

    for i, tool in enumerate(tools):
        rect = pygame.Rect(10 + i * 82, 10, 78, 35)
        is_active = current_tool == tool
        bg = ACCENT_COLOR if is_active else (BTN_HOVER if rect.collidepoint(mx, my) else BTN_NORMAL)
        pygame.draw.rect(screen, bg, rect, border_radius=6)
        txt = font_small.render(tool, True, TEXT_COLOR)
        screen.blit(txt, (rect.x + (rect.width - txt.get_width())//2, rect.y + 8))

    for i, color in enumerate(colors):
        rect = pygame.Rect(10 + i * 40, 55, 35, 35)
        pygame.draw.rect(screen, color, rect, border_radius=4)
        if current_color == color:
            pygame.draw.rect(screen, TEXT_COLOR, rect, 3, border_radius=4)

    size_labels = {1: "Small", 2: "Med", 3: "Large"}
    for key in brush_sizes:
        rect = pygame.Rect(450 + (key - 1) * 60, 55, 55, 35)
        is_active = current_size_key == key
        bg = (100, 100, 110) if is_active else BTN_NORMAL
        pygame.draw.rect(screen, bg, rect, border_radius=6)
        if is_active: pygame.draw.rect(screen, ACCENT_COLOR, rect, 2, border_radius=6)
        t = font_small.render(size_labels[key], True, TEXT_COLOR)
        screen.blit(t, (rect.x + 8, rect.y + 10))

    pygame.draw.rect(screen, current_color, (WIDTH - 70, 55, 50, 35), border_radius=4)
    pygame.draw.rect(screen, TEXT_COLOR, (WIDTH - 70, 55, 50, 35), 2, border_radius=4)

    if start_pos and current_tool not in ("Brush", "Pencil", "Eraser", "Fill", "Text"):
        ox, oy = canvas_rect.x, canvas_rect.y
        ep = (mx - ox, my - oy)
        
    if status_timer > 0:
        status_timer -= dt
        s_txt = font_small.render(status_msg, True, (0, 255, 150))
        screen.blit(s_txt, (10, HEIGHT - 25))

    pygame.display.update()

pygame.quit()