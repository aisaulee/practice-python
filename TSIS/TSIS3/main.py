import pygame
import sys
from ui import main_menu, leaderboard_screen, settings_screen, game_over_screen, text_input_screen
from racer import play_game, WIDTH, HEIGHT
from persistence import save_score

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cyber Racer")
    username = text_input_screen(screen, "Enter your name:")
    if not username:
        username = "Player"

    while True:
        choice = main_menu(screen)
        
        if choice == "Play":
            while True:
                score, distance = play_game(screen, username)
                
                save_score(username, score, distance)
                
                action = game_over_screen(screen, score, distance)
                
                if action == "retry":
                    continue
                elif action == "menu":
                    break     
                    
        elif choice == "Leaderboard":
            leaderboard_screen(screen)
            
        elif choice == "Settings":
            settings_screen(screen)
            
        elif choice == "Quit":
            break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()