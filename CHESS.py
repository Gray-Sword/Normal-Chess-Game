import pygame
import chess
import time

pygame.init()

WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PIECES = {
    "White Pawn": pygame.image.load("assets/white_pawn.png"),
    "White Rook": pygame.image.load("assets/white_rook.png"),
    "White Knight": pygame.image.load("assets/white_knight.png"),
    "White Bishop": pygame.image.load("assets/white_bishop.png"),
    "White Queen": pygame.image.load("assets/white_queen.png"),
    "White King": pygame.image.load("assets/white_king.png"),
    "Black Pawn": pygame.image.load("assets/black_pawn.png"),
    "Black Rook": pygame.image.load("assets/black_rook.png"),
    "Black Knight": pygame.image.load("assets/black_knight.png"),
    "Black Bishop": pygame.image.load("assets/black_bishop.png"),
    "Black Queen": pygame.image.load("assets/black_queen.png"),
    "Black King": pygame.image.load("assets/black_king.png"),
}

for key in PIECES:
    PIECES[key] = pygame.transform.scale(PIECES[key], (SQUARE_SIZE, SQUARE_SIZE))

PIECE_NAMES = {
    chess.PAWN: "Pawn",
    chess.KNIGHT: "Knight",
    chess.BISHOP: "Bishop",
    chess.ROOK: "Rook",
    chess.QUEEN: "Queen",
    chess.KING: "King",
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

font = pygame.font.SysFont("Arial", 36)
timer_font = pygame.font.SysFont("Arial", 24)

def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                piece_name = ("White " if piece.color else "Black ") + PIECE_NAMES[piece.piece_type]
                screen.blit(PIECES[piece_name], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_start_menu():
    screen.fill(BLACK)
    title_text = font.render("Chess Game", True, WHITE)
    start_text = font.render("Start Game", True, GREEN)
    quit_text = font.render("Quit", True, RED)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 1.5))

    pygame.display.flip()

def draw_timer(white_time, black_time):
    white_minutes, white_seconds = divmod(white_time, 60)
    black_minutes, black_seconds = divmod(black_time, 60)

    white_time_text = timer_font.render(f"White: {white_minutes:02}:{white_seconds:02}", True, GREEN)
    black_time_text = timer_font.render(f"Black: {black_minutes:02}:{black_seconds:02}", True, RED)

    screen.blit(white_time_text, (20, 20))
    screen.blit(black_time_text, (WIDTH - 20 - black_time_text.get_width(), 20))

def game_loop():
    running = True
    clock = pygame.time.Clock()

    board = chess.Board()

    selected_square = None
    legal_moves = []
    
    white_time = 0
    black_time = 0
    white_start_time = time.time()
    black_start_time = time.time()
    
    turn = chess.WHITE

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                square = chess.square(col, 7 - row)

                if selected_square is None:
                    if board.piece_at(square):
                        selected_square = square
                        legal_moves = [move.to_square for move in board.legal_moves if move.from_square == square]
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        if turn == chess.WHITE:
                            white_time += time.time() - white_start_time
                            turn = chess.BLACK
                            black_start_time = time.time()
                        else:
                            black_time += time.time() - black_start_time
                            turn = chess.WHITE
                            white_start_time = time.time()
                    selected_square = None
                    legal_moves = []

        if turn == chess.WHITE:
            white_time += time.time() - white_start_time
            white_start_time = time.time()
        else:
            black_time += time.time() - black_start_time
            black_start_time = time.time()

        draw_board()

        if selected_square is not None:
            row, col = 7 - chess.square_rank(selected_square), chess.square_file(selected_square)
            pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            for move in legal_moves:
                row, col = 7 - chess.square_rank(move), chess.square_file(move)
                pygame.draw.rect(screen, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        draw_pieces(board)
        draw_timer(white_time, black_time)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def start_menu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if HEIGHT // 2 <= y <= HEIGHT // 2 + 40 and WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100:
                    running = False
                    game_loop()

                if HEIGHT // 1.5 <= y <= HEIGHT // 1.5 + 40 and WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100:
                    running = False

        draw_start_menu()

    pygame.quit()

start_menu()
