from tracemalloc import start
import solve
import pygame
import sys
import chess

board = chess.Board(chess.STARTING_FEN)
print(board)

## Creates a chess piece class that shows what team a piece is on, what type of piece it is and whether or not it can be killed by another selected piece.
class Piece:
    def __init__(self, team, type, image, killable=False):
        self.team = team
        self.type = type
        self.killable = killable
        self.image = image

## Creates instances of chess pieces, so far we got: pawn, king, rook and bishop
## The first parameter defines what team its on and the second, what type of piece it is
bp = Piece('b', 'p', 'resources/b_pawn.png')
wp = Piece('w', 'P', 'resources/w_pawn.png')
bk = Piece('b', 'k', 'resources/b_king.png')
wk = Piece('w', 'K', 'resources/w_king.png')
br = Piece('b', 'r', 'resources/b_rook.png')
wr = Piece('w', 'R', 'resources/w_rook.png')
bb = Piece('b', 'b', 'resources/b_bishop.png')
wb = Piece('w', 'B', 'resources/w_bishop.png')
bq = Piece('b', 'q', 'resources/b_queen.png')
wq = Piece('w', 'Q', 'resources/w_queen.png')
bkn = Piece('b', 'n', 'resources/b_knight.png')
wkn = Piece('w', 'N', 'resources/w_knight.png')

starting_order = {(0, 0): pygame.image.load(br.image), (1, 0): pygame.image.load(bkn.image),
                  (2, 0): pygame.image.load(bb.image), (3, 0): pygame.image.load(bq.image),
                  (4, 0): pygame.image.load(bk.image), (5, 0): pygame.image.load(bb.image),
                  (6, 0): pygame.image.load(bkn.image), (7, 0): pygame.image.load(br.image),
                  (0, 1): pygame.image.load(bp.image), (1, 1): pygame.image.load(bp.image),
                  (2, 1): pygame.image.load(bp.image), (3, 1): pygame.image.load(bp.image),
                  (4, 1): pygame.image.load(bp.image), (5, 1): pygame.image.load(bp.image),
                  (6, 1): pygame.image.load(bp.image), (7, 1): pygame.image.load(bp.image),

                  (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
                  (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
                  (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
                  (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
                  (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
                  (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
                  (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
                  (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

                  (0, 6): pygame.image.load(wp.image), (1, 6): pygame.image.load(wp.image),
                  (2, 6): pygame.image.load(wp.image), (3, 6): pygame.image.load(wp.image),
                  (4, 6): pygame.image.load(wp.image), (5, 6): pygame.image.load(wp.image),
                  (6, 6): pygame.image.load(wp.image), (7, 6): pygame.image.load(wp.image),
                  (0, 7): pygame.image.load(wr.image), (1, 7): pygame.image.load(wkn.image),
                  (2, 7): pygame.image.load(wb.image), (3, 7): pygame.image.load(wq.image),
                  (4, 7): pygame.image.load(wk.image), (5, 7): pygame.image.load(wb.image),
                  (6, 7): pygame.image.load(wkn.image), (7, 7): pygame.image.load(wr.image),}

# chess.Board Handling
def update_state(board):
    print(board)
    visual = str(board)
    final_output = [[]]
    for i in range(8):
        temp = []
        for j in range(8):
            temp.append(visual[i * 16 + j*2])
        final_output.append(temp)
    for row in range(1, 9):
        for col in range(8):
            c = final_output[row][col]
            if (c == "p"):
                starting_order[col, row-1] = pygame.image.load(bp.image)
            elif (c == "P"):
                starting_order[col, row-1]  = pygame.image.load(wp.image)
            elif (c == "n"):
                starting_order[col, row-1]  = pygame.image.load(bkn.image)
            elif (c == "N"):
                starting_order[col, row-1]  = pygame.image.load(wkn.image)
            elif (c == "b"):
                starting_order[col, row-1]  = pygame.image.load(bb.image)
            elif (c == "B"):
                starting_order[col, row-1]  = pygame.image.load(wb.image)
            elif (c == "r"):
                starting_order[col, row-1] = pygame.image.load(br.image)
            elif (c == "R"):
                starting_order[col, row-1]  = pygame.image.load(wr.image)
            elif (c == "q"):
                starting_order[col, row-1]  = pygame.image.load(bq.image)
            elif (c == "Q"):
                starting_order[col, row-1]  = pygame.image.load(wq.image)
            elif (c == "k"):
                starting_order[col, row-1]  = pygame.image.load(bk.image)
            elif (c == "K"):
                starting_order[col, row-1]  = pygame.image.load(wk.image)
            elif (c == "."):
                starting_order[col, row-1]  = None

def legal_move(x, y, generated_moves, piece_to_move):
    for move in generated_moves:
        if (x == move[0] and y == move[1]):
            return True
    return False

def all_legal_moves(x, y, board):
    return_moves = []
    generated_moves = list(board.legal_moves)
    for move in generated_moves:
        if (int(str(move)[1]) == 8 - x and solve.col_values[str(move)[0]] == y):
            return_moves.append((8 - int(str(move)[3]), solve.col_values[str(move)[2]]))
    return return_moves

WIDTH = 512

WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("Chess")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))

    def setup(self, WIN):
        if starting_order[(self.row, self.col)]:
            if starting_order[(self.row, self.col)] == None:
                pass
            else:
                WIN.blit(starting_order[(self.row, self.col)], (self.x, self.y))

def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i+j)%2 ==1:
                grid[i][j].colour = GREY
    return grid

def draw_grid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    y, x = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)

def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid

def main(WIN, WIDTH):
    moves = 0
    selected = False
    piece_to_move=[]
    grid = make_grid(8, WIDTH)
    generated_moves = []
    end_state = False
    while True:
        if (moves % 2 == 1): 
            solve.bot_move(board, end_state)
            moves += 1
            update_state(board)
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y, x = Find_Node(pos, WIDTH)
                if selected == False:
                    try:
                        generated_moves = all_legal_moves(x, y, board)
                        for positions in generated_moves:
                            row, col = positions
                            grid[row][col].colour = BLUE
                        piece_to_move = x,y
                        selected = True
                    except:
                        piece_to_move = []
                        print('Can\'t select')
                else:
                    try:
                        if (legal_move(x, y, generated_moves, piece_to_move)):
                            row, col = piece_to_move
                            original_piece = solve.col_keys[col] + str(8 - row)
                            new_position = solve.col_keys[y] + str(8-x)
                            current_move = original_piece + new_position
                            # check if pawn for promotion
                            move = chess.Move(chess.square(col, 7 - row), chess.square(y, 7 - x))
                            if (board.is_zeroing(move) and ((row == 6 and x == 7) or (row == 1 and x == 0))):
                                move = chess.Move(chess.square(col, 7 - row), chess.square(y, 7 - x), chess.QUEEN)
                            board.push(move)
                            # Check End State
                            if (board.is_checkmate()):
                                if (moves % 2 == 0):
                                    print("white Wins!")
                                else:
                                    print("black Wins!")
                            elif(board.is_stalemate() or board.is_insufficient_material()):
                                print("draw!")
                            remove_highlight(grid)
                            # Show new state
                            update_state(board)
                            moves += 1
                            selected = False
                        else:
                            remove_highlight(grid)
                            selected = False
                            print("Deselected")
                    except:
                        remove_highlight(grid)
                        selected = False
                        print("Invalid move")
                    selected = False

            update_display(WIN, grid, 8, WIDTH)


main(WIN, WIDTH)