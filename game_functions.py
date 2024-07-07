import pygame
import random


# Colors
COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    'light text': (249, 246, 242),
    'dark text': (119, 110, 101),
    'other': (0, 0, 0),
    'bg': (250, 248, 239),
    'grid': (187, 173, 160),
    'light bg': (187, 173, 160)  
}
#create a 4x4 board initialized with zeros
def create_board():
    board = [[0 for _ in range(4)] for _ in range(4)]
    generate_tile(board)
    generate_tile(board)
    return board 

# spawn a new tile (2 or 4) on the board at a random empty location.
def generate_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

# execute a move (UP, DOWN, LEFT, RIGHT) on the board.
def move(board, direction):
    if direction == 'UP':
        return move_up(board)
    elif direction == 'DOWN':
        return move_down(board)
    elif direction == 'LEFT':
        return move_left(board)
    elif direction == 'RIGHT':
        return move_right(board)

def move_left(board):
    new_board = [compress(row) for row in board]
    score = sum(row[1] for row in new_board)
    new_board = [row[0] for row in new_board]
    return new_board, score

def move_right(board):
    new_board = [compress(row[::-1]) for row in board]
    score = sum(row[1] for row in new_board)
    new_board = [row[0][::-1] for row in new_board]
    return new_board, score

def move_up(board):
    transposed = list(map(list, zip(*board)))
    moved, score = move_left(transposed)
    return list(map(list, zip(*moved))), score

def move_down(board):
    transposed = list(map(list, zip(*board)))
    moved, score = move_right(transposed)
    return list(map(list, zip(*moved))), score

# compress a row  by moving all non-zero elements to the left.
def compress(row):
    new_row = [i for i in row if i != 0]
    score = 0
    i = 0
    while i < len(new_row) - 1:
        if new_row[i] == new_row[i + 1]:
            new_row[i] *= 2
            score += new_row[i]
            new_row.pop(i + 1)
        i += 1
    new_row += [0] * (4 - len(new_row))
    return (new_row, score)

# transpose a 4x4 game board.
def transpose(board):
    return [list(row) for row in zip(*board)]

# check if the game is over by determining if no more valid moves can be made.
def is_game_over(board):
    if any(0 in row for row in board):
        return False
    for i in range(4):
        for j in range(4):
            if (i < 3 and board[i][j] == board[i + 1][j]) or (j < 3 and board[i][j] == board[i][j + 1]):
                return False
    return True

# check if the player has won the game by reaching the 2048 tile.
def is_win(board):
    return any(2048 in row for row in board)

# draw the 2048 game board
def draw_board(screen, board, font, score, high_score):
    screen.fill(COLORS['bg'])
    TITLE_COLOR = pygame.Color(119, 110, 101)

    # draw title
    title_font = pygame.font.SysFont("Arial", 70, bold=True)
    title = title_font.render("2048", True, TITLE_COLOR)
    screen.blit(title, (20, 40))

    #draw subtitle
    subtitle_font = pygame.font.SysFont("Arial", 15)  
    subtitle = subtitle_font.render("Join the tiles, get to 2048!", True, 'darkred')
    subtitle_x = 20  
    subtitle_y = 40 + title.get_height() + 10 
    screen.blit(subtitle, (subtitle_x, subtitle_y))

    # Draw score and best score
        # create the font
    score_font =  pygame.font.SysFont("Arial", 15)  # Smaller font size for labels
    value_font =  pygame.font.SysFont("Arial", 20)  # Larger font size for values
    TEXT_COLOR = (238, 228, 218)
    WHITE = (255, 255, 255)
        # render the text 
    score_label = score_font.render("SCORE", True, TEXT_COLOR)
    best_label = score_font.render("BEST", True, TEXT_COLOR)
    score_value = value_font.render(str(score), True, WHITE)
    best_value = value_font.render(str(high_score), True, WHITE)

    # create background rectangles
    score_bg = pygame.Rect(210, 20, 80, 50)
    best_bg = pygame.Rect(300, 20, 80, 50)

    # draw background rectangles
    pygame.draw.rect(screen, COLORS['light bg'], score_bg,border_radius=5)
    pygame.draw.rect(screen, COLORS['light bg'], best_bg,border_radius=5)

    # calculate positions to center text in rectangles
    score_label_pos = score_label.get_rect(centerx=score_bg.centerx, top=score_bg.top + 5)
    best_label_pos = best_label.get_rect(centerx=best_bg.centerx, top=best_bg.top + 5)
    score_value_pos = score_value.get_rect(centerx=score_bg.centerx, bottom=score_bg.bottom - 5)
    best_value_pos = best_value.get_rect(centerx=best_bg.centerx, bottom=best_bg.bottom - 5)

    # draw the text
    screen.blit(score_label, score_label_pos)
    screen.blit(best_label, best_label_pos)
    screen.blit(score_value, score_value_pos)
    screen.blit(best_value, best_value_pos)

    
    # draw New Game button
    score1_font = pygame.font.SysFont("Arial", 20)
    pygame.draw.rect(screen, (143, 122, 102), (260, 120, 120, 40), border_radius=5)
    new_game_text = score1_font.render("New Game", True, COLORS['light text'])
    screen.blit(new_game_text, (270, 130))
    
    # draw grid background
    pygame.draw.rect(screen, COLORS['grid'], (20, 200, 360, 360), border_radius=5)
    
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            color = COLORS[value] if value in COLORS else COLORS['other']
            
            pygame.draw.rect(screen, color, (j * 90 + 25, i * 90 + 205, 80, 80))
            
            if value != 0:
                text_color = COLORS['light text'] if value > 4 else COLORS['dark text']
                number_font = pygame.font.Font(None, 55)
                text = number_font.render(str(value), True, text_color)
                text_rect = text.get_rect(center=(j * 90 + 67, i * 90 + 247))
                screen.blit(text, text_rect)


# draw the 'Game Over' screen
def draw_game_over(screen, font):
    overlay = pygame.Surface((400, 580), pygame.SRCALPHA) 
    overlay.set_alpha(200)
    overlay.fill((255, 255, 255,200))
    screen.blit(overlay, (0, 0))
    game_over_text = font.render("Game over!", True, COLORS['dark text'])
    screen.blit(game_over_text, (130, 250))
    
    # Draw Try again button
    pygame.draw.rect(screen, (143, 122, 102), (120, 300, 160, 40), border_radius=5)
    try_again_text = font.render("Try again", True, COLORS['light text'])
    screen.blit(try_again_text, (145, 310))

# draw the 'You win' screen
def draw_win(screen, font):
    overlay = pygame.Surface((400, 580), pygame.SRCALPHA) 
    overlay.set_alpha(200)
    overlay.fill((255, 255, 255))
    screen.blit(overlay, (0, 0))
    win_text = font.render("You win!", True, COLORS['dark text'])
    screen.blit(win_text, (150, 250))
    
    # Draw Continue button
    pygame.draw.rect(screen, (143, 122, 102), (120, 300, 160, 40), border_radius=5)
    continue_text = font.render("Continue", True, COLORS['light text'])
    screen.blit(continue_text, (145, 310))