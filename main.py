import chess
import chess.svg

board = chess.Board()

print(*board.legal_moves)

print(chess.Move.from_uci("a8a1") in board.legal_moves)


print(board.push_san("e4"))

print(board.push_san("e5"))

print(board.push_san("Qh5"))

print(board.push_san("Nc6"))

print(board.push_san("Bc4"))

print(board.push_san("Nf6"))

print(board.push_san("Qxf7"))


print(board.is_checkmate())

print(chess.svg.board(board), file=open('board.svg', 'w'))
