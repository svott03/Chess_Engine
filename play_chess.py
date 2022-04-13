from tracemalloc import start
import solve
import pygame
import sys
import chess
import copy

# Global variables
WIDTH = 512
SQ_WIDTH = WIDTH // 8
WIN = pygame.display.set_mode((WIDTH, WIDTH))

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

# Creates instances of chess pieces, so far we got: pawn, king, rook and bishop
# The first parameter defines what team its on and the second, what type of piece it is

load_piece = {
    'p': pygame.image.load('resources/b_pawn.png'),
    'P': pygame.image.load('resources/w_pawn.png'),
    'k': pygame.image.load('resources/b_king.png'),
    'K': pygame.image.load('resources/w_king.png'),
    'r': pygame.image.load('resources/b_rook.png'),
    'R': pygame.image.load('resources/w_rook.png'),
    'b': pygame.image.load('resources/b_bishop.png'),
    'B': pygame.image.load('resources/w_bishop.png'),
    'q': pygame.image.load('resources/b_queen.png'),
    'Q': pygame.image.load('resources/w_queen.png'),
    'n': pygame.image.load('resources/b_knight.png'),
    'N': pygame.image.load('resources/w_knight.png'),
    '.': None}

square_images = {}
square_colors = {}


def init_squares(board):
    for row in range(8):
        for col in range(8):
            c = board.__str__()[row * 16 + 2 * col]
            square_images[row, col] = load_piece[c]
            square_colors[row, col] = WHITE if (row + col) % 2 == 0 else GREY

def legal_moves(x, y, board):
    moves = []
    for move in board.legal_moves:
        if move.from_square == 8 * (7 - x) + y:
            moves.append(move)
            square_colors[7 - move.to_square // 8, move.to_square % 8] = BLUE
    return moves

def update_display(board):
    for row in range(8):
        for col in range(8):
            # set square position and color, then draw it
            square = (col * SQ_WIDTH, row * SQ_WIDTH, SQ_WIDTH, SQ_WIDTH)
            pygame.draw.rect(WIN, square_colors[row, col], square)

            # get piece and draw its image
            c = board.__str__()[row * 16 + 2 * col]
            if load_piece[c]:
                WIN.blit(load_piece[c], (col * SQ_WIDTH, row * SQ_WIDTH))

    # draw grid
    for i in range(8):
        pygame.draw.line(WIN, BLACK, (0, i * SQ_WIDTH), (WIDTH, i * SQ_WIDTH))
        pygame.draw.line(WIN, BLACK, (i * SQ_WIDTH, 0), (i * SQ_WIDTH, WIDTH))

    pygame.display.update()


def remove_highlight():
    for row in range(8):
        for col in range(8):
            square_colors[row, col] = WHITE if (row + col) % 2 == 0 else GREY

def player_move(board):
    selected = False
    from_square = -1
    moves = []
    while True:
        pygame.time.delay(50)  # stops cpu dying
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                y, x = pygame.mouse.get_pos()
                y, x = y // SQ_WIDTH, x // SQ_WIDTH
                print(chess.square_name(8 * (7 - x) + y))
                if not selected:
                    moves = legal_moves(x, y, board)
                    from_square = 8 * (7 - x) + y
                    if moves:
                        selected = True
                else:
                    try:
                        move = board.find_move(from_square, 8 * (7 - x) + y)
                        board.push(move)
                        remove_highlight()
                        return
                    except ValueError:
                        print("bruh moment")
                    remove_highlight()
                    selected = False
        update_display(board)

def main(WIN, WIDTH):
    # setup
    pygame.display.set_caption("Chess")
    board = chess.Board(chess.STARTING_FEN)
    init_squares(board)
    end_state = False

    while not board.outcome():  # outcome is still None
        if board.turn == chess.WHITE:
            print("======== BLACK ========\n")
            # for move in sorted(board.legal_moves, key=lambda move: solve.minimax_key(board, move), reverse=True):
            #     print(move.uci(), board.piece_at(move.from_square))
            # print(board)
            player_move(board)
        elif board.turn == chess.BLACK:
            print("======== WHITE ========\n")
            solve.sorted_bot_move(board, end_state)
        update_display(board)

if __name__ == '__main__':
    main(WIN, WIDTH)
