from tkinter import *
import random

def next_turn(row, col):    #this function will determine the place of X or O and determine the turn of the player
    global player, player_score, ai_score
    if game_btns[row][col]['text'] == "" and check_winner() == False:
        game_btns[row][col]['text'] = player
        if check_winner() == False:
            player_switch()
            label.config(text=(player + " turn"))
            if player == 'O':
                ai_move()
        elif check_winner() == True:
            label.config(text=(player + ' wins!'))
            if player == 'X':
                player_score += 1
            else:
                ai_score += 1
            update_score()
        elif check_winner() == 'tie':
            label.config(text="Tie , NO winner!")

def player_switch():     #this function will switch the player
    global player
    player = 'O' if player == 'X' else 'X'

def ai_move():            #this function will move the AI player(pc)
    empty_spots = [(r, c) for r in range(3) for c in range(3) if game_btns[r][c]['text'] == ""]
    if empty_spots:
        row, col = random.choice(empty_spots)
        next_turn(row, col)

def check_winner():       #this function will check if there is a winner or not and return true
    #check all 3 herizontal conditions
    for row in range(3):
        if game_btns[row][0]['text'] == game_btns[row][1]['text'] == game_btns[row][2]['text'] != "":
            game_btns[row][0].config(bg='cyan')
            game_btns[row][1].config(bg='cyan')
            game_btns[row][2].config(bg='cyan')
            return True
        
    #check all 3 vertical conditions
    for col in range(3):
        if game_btns[0][col]['text'] == game_btns[1][col]['text'] == game_btns[2][col]['text'] != "":
            game_btns[0][col].config(bg='cyan')
            game_btns[1][col].config(bg='cyan')
            game_btns[2][col].config(bg='cyan')
            return True
        
    #check both diagonals condition
    if game_btns[0][0]['text'] == game_btns[1][1]['text'] == game_btns[2][2]['text']!= "":
        game_btns[0][0].config(bg='cyan')
        game_btns[1][1].config(bg='cyan')
        game_btns[2][2].config(bg='cyan')
        return True
    
    elif game_btns[0][2]['text'] == game_btns[1][1]['text'] == game_btns[2][0]['text']!= "":
        game_btns[0][2].config(bg='cyan')
        game_btns[1][1].config(bg='cyan')
        game_btns[2][0].config(bg='cyan')
        return True
    
    #if there is no empty places
    if all(game_btns[r][c]['text'] != "" for r in range(3) for c in range(3)):
        for row in range(3):
            for col in range(3):
                game_btns[row][col].config(bg='red') 
        return 'tie'
    return False

def start_game():   #this function will start the game
    global player
    player = random.choice(symbol)
    label.config(text=(player + " turn"))
    for row in range(3):
        for col in range(3):
            game_btns[row][col].config(text="", bg='#f0f0f0')
    if player == 'O':
        ai_move()

def ai_smart_move():       #this function will make the AI player(pc) smarter
    for row in range(3):
        for col in range(3):
            if game_btns[row][col]['text'] == "":
                game_btns[row][col]['text'] = player
                if check_winner() == True:
                    return
                game_btns[row][col]['text'] = ""
    ai_move()
    
def update_score():     #this function will update the score
    score_label.config(text=f"You: {player_score}  Computer: {ai_score}")

window = Tk()
window.title("Tic-Tac-Toe")

symbol = ['X', 'O']
player = random.choice(symbol)
player_score = 0
ai_score = 0

game_btns = [
    [0 , 0 , 0],
    [0 , 0 , 0],
    [0 , 0 , 0]
]

label = Label(text=(player + ' turn'), font=('consolas', 40))
label.pack(side='top')

score_label = Label(text=f"You: {player_score}  Computer: {ai_score}", font=('consolas', 20))
score_label.pack(side='top')

restart_btn = Button(text='restart', font=('consolas', 20), command=start_game)
restart_btn.pack(side='top')

btns_frame = Frame(window)
btns_frame.pack()

for row in range(3):
    for col in range(3):
        game_btns[row][col] = Button(btns_frame, text='', font=('consolas', 50), width=4, height=1,
                                     command=lambda row=row, col=col: next_turn(row, col))
        game_btns[row][col].grid(row=row, column=col)

if player == 'O':
    ai_move()

window.mainloop()
