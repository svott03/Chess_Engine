from cmath import inf
import chess
from evaluations import positionEvals as eval
import copy

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

col_values = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7
}

col_keys = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h"
}

piece_names = {
    1: "PAWN",
    2: "KNIGHT",
    3: "BISHOP",
    4: "ROOK",
    5: "QUEEN",
    6: "KING"
}

end_state = 44000

def total_material(board, end):
    total_material = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            total_material += piece_values[piece.piece_type]
    return total_material

def calculate_score(board, end):
    white_score = 0
    black_score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        row = int(7 - int(square)/8)
        col = int(int(square) - int(square)/8 * 8)
        if not piece:
            continue
        if piece.color == chess.WHITE:
            if piece.piece_type == 6:
                if not end:
                    white_score += piece_values[piece.piece_type] + getattr(eval, "KING_white_eval_middle")[row][col]
                else:
                    white_score += piece_values[piece.piece_type] + getattr(eval, "KING_white_eval_end")[row][col]
            else:
                white_score += piece_values[piece.piece_type] + getattr(eval, piece_names[piece.piece_type] + "_white_eval")[row][col]
        else:
            if piece.piece_type == 6:
                if not end:
                    black_score += piece_values[piece.piece_type] + getattr(eval, "KING_black_eval_middle")[row][col]
                else:
                    black_score += piece_values[piece.piece_type] + getattr(eval, "KING_black_eval_end")[row][col]
            else:
                black_score += piece_values[piece.piece_type] + getattr(eval, piece_names[piece.piece_type] + "_black_eval")[row][col]
    return white_score - black_score

def dfs(board, end, white_turn, alpha, beta, depth):
    if (board.is_checkmate()):
        if (not white_turn):
            print("White Wins!")
            return None, inf
        else:
            print("Black Wins!")
            return None, -inf
    elif(board.is_stalemate() or board.is_insufficient_material()):
        print("Draw!")
        return None, 0
    if depth == 0:
        return None, calculate_score(board, end)
    moves = board.legal_moves
    best_move = list(moves)[0]
    if (white_turn):
        max_score = -inf
        for move in moves:
            if (total_material(board, end) < end_state):
                end = True
            temp_board = copy.deepcopy(board)
            temp_board.push(move)
            junk, score = dfs(temp_board, end, False, alpha, beta, depth-1)
            if (score > max_score):
                max_score = score
                best_move = move
            alpha = max(score, alpha)
            if alpha >= beta:
                break
        return best_move, max_score
    else:
        min_score = inf
        for move in moves:
            if (total_material(board, end) < end_state):
                end = True
            temp_board = copy.deepcopy(board)
            temp_board.push(move)
            junk, score = dfs(temp_board, end, True, alpha, beta, depth-1)
            if (score < min_score):
                min_score = score
                best_move = move
            beta = min(score, beta)
            if (beta <= alpha):
                break
        return best_move, min_score

def bot_move(board, end_state):
    move, score = dfs(board, end_state, False, -inf, inf, 4)
    print(board.legal_moves)
    # check for promotion logic
    from_file = int(move.from_square)/8
    from_rank = int(int(move.from_square) - int(move.from_square)/8 * 8)
    to_file = int(move.to_square)/8
    to_rank = int(int(move.to_square) - int(move.to_square)/8 * 8)
    if (board.is_zeroing(move) and ((from_rank == 2 and to_rank == 1) or (from_rank == 7 and to_rank == 8))):
        move = chess.Move(chess.square(from_file, from_rank), chess.square(to_file, to_rank), chess.QUEEN)
    board.push(move)
    print(board)

# AI will push on the board then call update display if (move % 2) == 1 minimax(args)