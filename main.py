import pygame
import sys
import os
from game_functions import *

def main():
    pygame.init()
    WIDTH, HEIGHT = 400, 580
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('2048')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # high score file 
    file_path = 'high_score.txt'
    try:
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as f:
                f.write('0')
        
        with open(file_path, 'r') as file:
            init_high = int(file.readline().strip())
    except (IOError, ValueError) as e:
        print(f"Error reading high score: {e}")
        init_high = 0

    high_score = init_high
    board = create_board()
    score = 0
    game_over = False
    won = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    if high_score > init_high:
                        with open(file_path, 'w') as file:
                            file.write(str(high_score))
                except IOError as e:
                    print(f"Error saving high score: {e}")
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 260 <= x <= 380 and 120 <= y <= 160:
                    # new Game button clicked
                    board = create_board()
                    score = 0
                    game_over = False
                    won = False
                elif game_over and 120 <= x <= 280 and 300 <= y <= 340:
                    # try again button clicked
                    board = create_board()
                    score = 0
                    game_over = False
                elif won and 120 <= x <= 280 and 300 <= y <= 340:
                    # continue button clicked
                    won = False
            # use either the arrow keys or 'w', 's', 'a', 'd' keys to move in the directions of up, down, left, or right.
            if event.type == pygame.KEYDOWN and not game_over and not won:
                try:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        new_board, move_score = move(board, 'UP')
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        new_board, move_score = move(board, 'DOWN')
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        new_board, move_score = move(board, 'LEFT')
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        new_board, move_score = move(board, 'RIGHT')
                    else:
                        new_board, move_score = None, 0

                    if new_board and new_board != board:
                        board = new_board
                        generate_tile(board)
                        score += move_score
                        if score > high_score:
                            high_score = score 
                        if is_win(board):
                            won = True
                        elif is_game_over(board):
                            game_over = True
                except Exception as e:
                    print(f"Error during move: {e}")

        try:
            # draw window frame
            pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, 30))
            pygame.draw.line(screen, (190, 190, 190), (0, 30), (WIDTH, 30))
            pygame.draw.circle(screen, (255, 95, 87), (20, 15), 7)
            pygame.draw.circle(screen, (255, 189, 46), (40, 15), 7)
            pygame.draw.circle(screen, (39, 201, 63), (60, 15), 7)

            title_font = pygame.font.Font(None, 20)
            window_title = title_font.render("2048", True, (100, 100, 100))
            screen.blit(window_title, (WIDTH // 2 - window_title.get_width() // 2, 10))

            draw_board(screen, board, font, score, high_score)
            if game_over:
                draw_game_over(screen, font)
            elif won:
                draw_win(screen, font)
        except Exception as e:
            print(f"Error drawing board: {e}")

        pygame.display.flip()
        clock.tick(30)

        if high_score > init_high:
            try:
                with open(file_path, 'w') as file:
                    file.write(str(high_score))
                init_high = high_score
            except IOError as e:
                print(f"Error saving high score: {e}")

if __name__ == "__main__":
    main()