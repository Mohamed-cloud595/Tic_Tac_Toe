
import tkinter as tk
import random

# Constants
PLAYER_X = 'X'
PLAYER_O = 'O'
SYMBOLS = [PLAYER_X, PLAYER_O]

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        # Game state
        self.player = random.choice(SYMBOLS)
        self.player_score = 0
        self.ai_score = 0

        # UI Elements
        self.label = tk.Label(text=f"{self.player} turn", font=('Consolas', 32))
        self.label.pack(pady=10)

        self.score_label = tk.Label(text=self.get_score_text(), font=('Consolas', 20))
        self.score_label.pack(pady=5)

        self.restart_btn = tk.Button(text='Restart', font=('Consolas', 16), command=self.start_game)
        self.restart_btn.pack(pady=5)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

        if self.player == PLAYER_O:
            self.root.after(500, self.ai_move)

    def create_board(self):
        """Initialize the button grid."""
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.board_frame, text='', font=('Consolas', 48),
                                width=4, height=1, command=lambda row=r, col=c: self.next_turn(row, col))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def start_game(self):
        """Reset the board and start a new game."""
        self.player = random.choice(SYMBOLS)
        self.label.config(text=f"{self.player} turn")

        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text="", bg='#f0f0f0')

        if self.player == PLAYER_O:
            self.root.after(500, self.ai_move)

    def next_turn(self, row, col):
        """Process a player's or AI's move."""
        if self.buttons[row][col]['text'] == "" and not self.check_winner():
            self.buttons[row][col]['text'] = self.player
            result = self.check_winner()

            if result is False:
                self.switch_player()
                self.label.config(text=f"{self.player} turn")
                if self.player == PLAYER_O:
                    self.root.after(500, self.ai_move)
            elif result == 'tie':
                self.label.config(text="Tie! No winner.")
            else:
                self.label.config(text=f"{self.player} wins!")
                if self.player == PLAYER_X:
                    self.player_score += 1
                else:
                    self.ai_score += 1
                self.update_score()

    def switch_player(self):
        """Switch active player."""
        self.player = PLAYER_O if self.player == PLAYER_X else PLAYER_X

    def ai_move(self):
        """Make AI move (random or smart)."""
        # Uncomment to use smart AI logic
        # if self.try_winning_move():
        #     return

        empty = [(r, c) for r in range(3) for c in range(3) if self.buttons[r][c]['text'] == ""]
        if empty:
            row, col = random.choice(empty)
            self.next_turn(row, col)

    def try_winning_move(self):
        """Attempt a winning move for AI."""
        for r in range(3):
            for c in range(3):
                if self.buttons[r][c]['text'] == "":
                    self.buttons[r][c]['text'] = self.player
                    if self.check_winner():
                        return True
                    self.buttons[r][c]['text'] = ""
        return False

    def check_winner(self):
        """Check for a win or tie. Return True (win), 'tie', or False."""
        # Winning combinations: rows, columns, diagonals
        lines = []

        # Rows and Columns
        for i in range(3):
            lines.append([self.buttons[i][0], self.buttons[i][1], self.buttons[i][2]])
            lines.append([self.buttons[0][i], self.buttons[1][i], self.buttons[2][i]])

        # Diagonals
        lines.append([self.buttons[0][0], self.buttons[1][1], self.buttons[2][2]])
        lines.append([self.buttons[0][2], self.buttons[1][1], self.buttons[2][0]])

        for line in lines:
            if all(btn['text'] == self.player and btn['text'] != "" for btn in line):
                for btn in line:
                    btn.config(bg='cyan')
                return True

        # Check for tie
        if all(self.buttons[r][c]['text'] != "" for r in range(3) for c in range(3)):
            for r in range(3):
                for c in range(3):
                    self.buttons[r][c].config(bg='red')
            return 'tie'

        return False

    def update_score(self):
        """Update score display."""
        self.score_label.config(text=self.get_score_text())

    def get_score_text(self):
        return f"You: {self.player_score}  computer: {self.ai_score}"

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
