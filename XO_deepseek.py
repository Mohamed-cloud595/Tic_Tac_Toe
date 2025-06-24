from tkinter import *
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, window):
        self.window = window
        self.window.title("Tic-Tac-Toe Pro")
        self.window.resizable(False, False)
        self.window.configure(bg='#f0f0f0')
        
        # Game variables
        self.symbols = ['X', 'O']
        self.player = random.choice(self.symbols)
        self.player_score = 0
        self.ai_score = 0
        self.tie_games = 0
        self.game_active = True
        
        # Colors
        self.bg_color = '#f0f0f0'
        self.btn_color = '#ffffff'
        self.win_color = '#4CAF50'
        self.tie_color = '#FFC107'
        self.text_color = '#333333'
        
        # Fonts
        self.title_font = ('Arial', 24, 'bold')
        self.score_font = ('Arial', 16)
        self.btn_font = ('Arial', 40, 'bold')
        
        # Create UI
        self.create_widgets()
        
        # Start first game
        self.start_game()
        
    def create_widgets(self):
        # Title label
        self.title_label = Label(self.window, text="Tic-Tac-Toe Pro", 
                                font=self.title_font, bg=self.bg_color, fg=self.text_color)
        self.title_label.pack(pady=(10, 5))
        
        # Score frame
        score_frame = Frame(self.window, bg=self.bg_color)
        score_frame.pack(pady=5)
        
        self.player_score_label = Label(score_frame, text=f"You: {self.player_score}", 
                                      font=self.score_font, bg=self.bg_color, fg='#2196F3')
        self.player_score_label.pack(side=LEFT, padx=10)
        
        self.tie_label = Label(score_frame, text=f"Ties: {self.tie_games}", 
                              font=self.score_font, bg=self.bg_color, fg=self.tie_color)
        self.tie_label.pack(side=LEFT, padx=10)
        
        self.ai_score_label = Label(score_frame, text=f"Computer: {self.ai_score}", 
                                   font=self.score_font, bg=self.bg_color, fg='#F44336')
        self.ai_score_label.pack(side=LEFT, padx=10)
        
        # Turn indicator
        self.turn_label = Label(self.window, text="", font=self.score_font, 
                               bg=self.bg_color, fg=self.text_color)
        self.turn_label.pack(pady=5)
        
        # Game board frame
        self.board_frame = Frame(self.window, bg=self.bg_color)
        self.board_frame.pack(pady=10)
        
        # Create game buttons
        self.game_btns = []
        for row in range(3):
            btn_row = []
            for col in range(3):
                btn = Button(self.board_frame, text='', font=self.btn_font, 
                            width=3, height=1, bg=self.btn_color, relief='ridge',
                            command=lambda r=row, c=col: self.next_turn(r, c))
                btn.grid(row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10)
                btn_row.append(btn)
            self.game_btns.append(btn_row)
        
        # Control buttons frame
        control_frame = Frame(self.window, bg=self.bg_color)
        control_frame.pack(pady=10)
        
        self.restart_btn = Button(control_frame, text='New Game', font=self.score_font, 
                                 command=self.start_game, bg='#E0E0E0')
        self.restart_btn.pack(side=LEFT, padx=5)
        
        self.mode_btn = Button(control_frame, text='Switch to Smart AI', font=self.score_font, 
                              command=self.toggle_ai_mode, bg='#E0E0E0')
        self.mode_btn.pack(side=LEFT, padx=5)
        
        # AI mode
        self.smart_ai = False
    
    def toggle_ai_mode(self):
        self.smart_ai = not self.smart_ai
        mode_text = "Switch to Random AI" if self.smart_ai else "Switch to Smart AI"
        self.mode_btn.config(text=mode_text)
        messagebox.showinfo("AI Mode Changed", 
                          f"AI is now in {'Smart' if self.smart_ai else 'Random'} mode")
    
    def next_turn(self, row, col):
        if not self.game_active:
            return
            
        if self.game_btns[row][col]['text'] == "":
            self.game_btns[row][col]['text'] = self.player
            self.game_btns[row][col]['fg'] = '#2196F3' if self.player == 'X' else '#F44336'
            
            # Check for winner or tie after each move
            result = self.check_winner()
            if result == True:
                self.handle_win()
            elif result == 'tie':
                self.handle_tie()
            else:
                self.switch_player()
                self.turn_label.config(text=f"{self.player}'s turn")
                
                # AI move if it's their turn
                if self.player == 'O' and self.game_active:
                    if self.smart_ai:
                        self.ai_smart_move()
                    else:
                        self.ai_move()
    
    def switch_player(self):
        self.player = 'O' if self.player == 'X' else 'X'
    
    def ai_move(self):
        empty_spots = [(r, c) for r in range(3) for c in range(3) if self.game_btns[r][c]['text'] == ""]
        if empty_spots:
            row, col = random.choice(empty_spots)
            self.next_turn(row, col)
    
    def ai_smart_move(self):
        # First, check if AI can win in the next move
        for row in range(3):
            for col in range(3):
                if self.game_btns[row][col]['text'] == "":
                    self.game_btns[row][col]['text'] = 'O'
                    if self.check_winner():
                        self.game_btns[row][col]['text'] = ""
                        self.next_turn(row, col)
                        return
                    self.game_btns[row][col]['text'] = ""
        
        # Then, check if player can win in the next move and block them
        for row in range(3):
            for col in range(3):
                if self.game_btns[row][col]['text'] == "":
                    self.game_btns[row][col]['text'] = 'X'
                    if self.check_winner():
                        self.game_btns[row][col]['text'] = 'O'
                        self.game_btns[row][col]['fg'] = '#F44336'
                        # Check if this move ends the game
                        result = self.check_winner()
                        if result == True:
                            self.handle_win()
                        elif result == 'tie':
                            self.handle_tie()
                        else:
                            self.switch_player()
                            self.turn_label.config(text=f"{self.player}'s turn")
                        return
                    self.game_btns[row][col]['text'] = ""
        
        # Try to take the center if available
        if self.game_btns[1][1]['text'] == "":
            self.next_turn(1, 1)
            return
        
        # Try to take a corner if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for row, col in corners:
            if self.game_btns[row][col]['text'] == "":
                self.next_turn(row, col)
                return
        
        # Take any available edge
        self.ai_move()
    
    def check_winner(self):
        # Check rows
        for row in range(3):
            if (self.game_btns[row][0]['text'] == self.game_btns[row][1]['text'] == 
                self.game_btns[row][2]['text'] != ""):
                return True
        
        # Check columns
        for col in range(3):
            if (self.game_btns[0][col]['text'] == self.game_btns[1][col]['text'] == 
                self.game_btns[2][col]['text'] != ""):
                return True
        
        # Check diagonals
        if (self.game_btns[0][0]['text'] == self.game_btns[1][1]['text'] == 
            self.game_btns[2][2]['text'] != ""):
            return True
        
        if (self.game_btns[0][2]['text'] == self.game_btns[1][1]['text'] == 
            self.game_btns[2][0]['text'] != ""):
            return True
        
        # Check for tie (only if no winner and board is full)
        if all(self.game_btns[r][c]['text'] != "" for r in range(3) for c in range(3)):
            return 'tie'
        
        return False
    
    def highlight_winning_cells(self):
        # Check rows
        for row in range(3):
            if (self.game_btns[row][0]['text'] == self.game_btns[row][1]['text'] == 
                self.game_btns[row][2]['text'] != ""):
                for col in range(3):
                    self.game_btns[row][col].config(bg=self.win_color)
                return
        
        # Check columns
        for col in range(3):
            if (self.game_btns[0][col]['text'] == self.game_btns[1][col]['text'] == 
                self.game_btns[2][col]['text'] != ""):
                for row in range(3):
                    self.game_btns[row][col].config(bg=self.win_color)
                return
        
        # Check diagonals
        if (self.game_btns[0][0]['text'] == self.game_btns[1][1]['text'] == 
            self.game_btns[2][2]['text'] != ""):
            for i in range(3):
                self.game_btns[i][i].config(bg=self.win_color)
            return
        
        if (self.game_btns[0][2]['text'] == self.game_btns[1][1]['text'] == 
            self.game_btns[2][0]['text'] != ""):
            self.game_btns[0][2].config(bg=self.win_color)
            self.game_btns[1][1].config(bg=self.win_color)
            self.game_btns[2][0].config(bg=self.win_color)
            return
    
    def handle_win(self):
        self.highlight_winning_cells()
        self.game_active = False
        
        if self.player == 'X':
            self.player_score += 1
            winner_text = "You win!"
        else:
            self.ai_score += 1
            winner_text = "Computer wins!"
        
        self.turn_label.config(text=winner_text)
        self.update_score()
        messagebox.showinfo("Game Over", winner_text)
    
    def handle_tie(self):
        self.game_active = False
        for row in range(3):
            for col in range(3):
                self.game_btns[row][col].config(bg=self.tie_color)
        
        self.tie_games += 1
        self.turn_label.config(text="It's a tie!")
        self.update_score()
        messagebox.showinfo("Game Over", "It's a tie!")
    
    def update_score(self):
        self.player_score_label.config(text=f"You: {self.player_score}")
        self.ai_score_label.config(text=f"Computer: {self.ai_score}")
        self.tie_label.config(text=f"Ties: {self.tie_games}")
    
    def start_game(self):
        self.game_active = True
        self.player = random.choice(self.symbols)
        
        # Reset board
        for row in range(3):
            for col in range(3):
                self.game_btns[row][col].config(text="", bg=self.btn_color, fg='black')
        
        self.turn_label.config(text=f"{self.player}'s turn")
        
        # If AI goes first
        if self.player == 'O':
            if self.smart_ai:
                self.ai_smart_move()
            else:
                self.ai_move()

# Create and run the game
if __name__ == "__main__":
    root = Tk()
    game = TicTacToe(root)
    root.mainloop()