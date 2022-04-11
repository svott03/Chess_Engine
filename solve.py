from cmath import inf
import chess
from evaluations import positionEvals as eval

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
    "H": 7
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
        if not piece:
            continue
        if piece.color == chess.WHITE:
            row = piece[1] - 1
            col = col_values[piece[0]]
            if piece.piece_type == 6:
                if not end:
                    white_score += piece_values[piece.piece_type] + getattr(eval, "King_white_eval_middle")[row][col]
                else:
                    white_score += piece_values[piece.piece_type] + getattr(eval, "King_white_eval_end")[row][col]
            else:
                white_score += piece_values[piece.piece_type] + getattr(eval, piece_names[piece.piece_type] + "_white_eval")[row][col]
        else:
            if piece.piece_type == 6:
                if not end:
                    black_score += piece_values[piece.piece_type] + getattr(eval, "King_black_eval_middle")[row][col]
                else:
                    black_score += piece_values[piece.piece_type] + getattr(eval, "King_black_eval_end")[row][col]
            else:
                black_score += piece_values[piece.piece_type] + getattr(eval, piece_names[piece.piece_type] + "_black_eval")[row][col]
    return white_score - black_score

#ABS
def dfs(board, end, white_turn, alpha, beta, depth):
    if depth == 0 or board.is_varient_end():
        return None, calculate_score(board, end)
    moves = board.legal_moves
    best_move = moves[0]
    if (white_turn):
        max_score = -inf
        for move in moves:
            if (total_material(board, end) < end_state):
                end = True
            temp_board = board
            temp_board.push(move)
            score = dfs(temp_board, end, False, alpha, beta, depth)
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
            temp_board = board
            temp_board.push(move)
            score = dfs(temp_board, end, True, alpha, beta, depth)
            if (score < min_score):
                min_score = score
                best_move = move
            beta = min(score, beta)
            if (beta <= alpha):
                break
        return best_move, min_score