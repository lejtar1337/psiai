import math

class TicTacToe:
    def __init__(self, size=3, max_depth=None, human_first=True):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.human = 'X' if human_first else 'O'
        self.computer = 'O' if human_first else 'X'
        self.current_player = 'X'
        self.max_depth = max_depth if max_depth is not None else (9 if size == 3 else 4)

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * (self.size * 2 - 1))

    def check_winner(self, player):
        for i in range(self.size):
            if all(self.board[i][j] == player for j in range(self.size)): return True
            if all(self.board[j][i] == player for j in range(self.size)): return True
        if all(self.board[i][i] == player for i in range(self.size)): return True
        if all(self.board[i][self.size - 1 - i] == player for i in range(self.size)): return True
        return False

    def is_draw(self):
        return all(self.board[i][j] != ' ' for i in range(self.size) for j in range(self.size))

    def get_empty_cells(self):
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == ' ']

    def evaluate(self):
        if self.check_winner(self.computer): return 10
        if self.check_winner(self.human): return -10
        return 0
    
    def minimax(self, depth, is_maximizing):
        score = self.evaluate()
        if score == 10: return score - depth
        if score == -10: return score + depth
        if self.is_draw() or depth >= self.max_depth: return 0

        if is_maximizing:
            best = -math.inf
            for i, j in self.get_empty_cells():
                self.board[i][j] = self.computer
                best = max(best, self.minimax(depth + 1, False))
                self.board[i][j] = ' '
            return best
        else:
            best = math.inf
            for i, j in self.get_empty_cells():
                self.board[i][j] = self.human
                best = min(best, self.minimax(depth + 1, True))
                self.board[i][j] = ' '
            return best

    def best_move(self):
        best_val = -math.inf
        move = (-1, -1)
        for i, j in self.get_empty_cells():
            self.board[i][j] = self.computer
            move_val = self.minimax(0, False)
            self.board[i][j] = ' '
            if move_val > best_val:
                best_val = move_val
                move = (i, j)
        return move

    def play(self):
        while True:
            self.print_board()
            if self.check_winner(self.human):
                print("Wygrałeś!")
                break
            if self.check_winner(self.computer):
                print("Wygrał komputer!")
                break
            if self.is_draw():
                print("Remis!")
                break

            if self.current_player == self.human:
                try:
                    r, c = map(int, input(f"Twój ruch (wiersz kolumna, 0-{self.size-1}): ").split())
                    if self.board[r][c] == ' ':
                        self.board[r][c] = self.human
                        self.current_player = self.computer
                    else:
                        print("Pole zajęte!")
                except (ValueError, IndexError):
                    print("Błędne dane.")
            else:
                print("Ruch komputera...")
                r, c = self.best_move()
                self.board[r][c] = self.computer
                self.current_player = self.human

if __name__ == "__main__":
    size = int(input("Rozmiar planszy (np. 3): ") or 3)
    depth_input = input(f"Max głębokość Minimax (Enter = domyślnie {'9' if size==3 else '4'}): ")
    max_depth = int(depth_input) if depth_input else None
    human_first = input("Zaczynasz? (t/n): ").lower() != 'n'
    
    game = TicTacToe(size=size, max_depth=max_depth, human_first=human_first)
    game.play()