from board import *

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            print(f"Selected piece at ({row}, {col}) with valid moves: {self.valid_moves}")
            return True
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
                self.valid_moves = self.board.get_valid_moves(self.selected)
                if not self.valid_moves:
                    self.change_turn()
                else:
                    # Check if there are any more captures possible
                    additional_captures = False
                    for move in self.valid_moves:
                        if self.valid_moves[move]:
                            additional_captures = True
                            break
                    if not additional_captures:
                        self.change_turn()
            else:
                self.change_turn()
            print(f"Moved piece to ({row}, {col})")
        else:
            return False
        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def get_all_valid_moves(self, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == color:
                    valid_moves = self.board.get_valid_moves(piece)
                    if valid_moves:
                        moves.append(valid_moves)
        return moves


    def check_winner(self):
        if self.board.white_left <= 0:
            print("Black wins!")
            return BLACK
        elif self.board.black_left <= 0:
            print("White wins!")
            return WHITE

        white_moves = self.get_all_valid_moves(WHITE)
        black_moves = self.get_all_valid_moves(BLACK)

        if not white_moves:
            print("Black wins!")
            return BLACK
        elif not black_moves:
            print("White wins!")
            return WHITE

        return None

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()
        winner = self.check_winner()
        if winner:
            print(f"Game Over! {winner} wins!")
            pygame.quit()
