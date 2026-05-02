import pygame

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    
    if target_color == new_color:
        return

    pixels_to_fill = [(x, y)]
    width, height = surface.get_size()

    while pixels_to_fill:
        curr_x, curr_y = pixels_to_fill.pop()

        if curr_x < 0 or curr_x >= width or curr_y < 0 or curr_y >= height:
            continue

        if surface.get_at((curr_x, curr_y)) == target_color:
            surface.set_at((curr_x, curr_y), new_color)
            pixels_to_fill.append((curr_x + 1, curr_y))
            pixels_to_fill.append((curr_x - 1, curr_y))
            pixels_to_fill.append((curr_x, curr_y + 1))
            pixels_to_fill.append((curr_x, curr_y - 1))