import string
import random
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button, PhotoImage
import itertools

class Hangman(tk.Tk):

    # initialise 
    word = ""  
    board = []  
    board_final = []  
    guesses = ['Guesses:']  
    lives = 5  
    game_over = False  

    # Word list
    words = ['jazz', 'crypto', 'quiz', 'chessboard', 'mystery', 'foreign', 'candle', 'friends', 'silver', 'surprise', 'holiday']

    def __init__(self):
        super().__init__()

        # Window setup
        self.title("HANGMAN")
        self.geometry("690x530")
        self.resizable(0, 0)
        self.configure(bg="#f295a1")
        self.font1 = ('Helvetica', 27, 'bold')

        # Header
        tk.Label(self, text='HANGMAN', width=32, height=1, font=self.font1, fg="white", bg='#ed304b').grid(row=0, column=0, columnspan=6)

        # Question
        tk.Label(self, text="Can you guess the word?", bg='#f295a1', font='Helvetica 12 italic bold').grid(row=1, column=0, columnspan=6)

        self._set_word()  
        self._create_board(self.word)  
        self._set_final_board(self.word)

        messagebox.showinfo("Welcome!", "Get ready to guess the word and save the stick figure! No pressure...")

    def _set_word(self):
         #Get random word
        self.word = random.choice(self.words)  

    def _set_final_board(self, word):
        self.board_final = list(word)

    def _create_board(self, word):
        self.board = ['_' if char != ' ' else ' ' for char in word]

    def _update_board(self, guess, pos):
        self.board[pos] = guess

    def _process_guess(self, guess):
        if guess in self.guesses:  
            messagebox.showinfo("Oops!", f"You already tried '{guess}'. Try something new!")
        elif guess in self.board_final:  
            for pos, char in enumerate(self.board_final):
                if char == guess:
                    self._update_board(guess, pos)
            self.guesses.append(guess)
        else:
            # Decrease heart
            self.lives -= 1
            self.guesses.append(guess)

    def _check_status(self):
        if self.lives == 0:
            self.game_over = True
            # Disable buttons
            self._disable_buttons()  
            messagebox.showinfo("GAME OVER!", f"GAME OVER: Thanks for playing! \nAnswer: {''.join(self.board_final)}\nBetter luck next time!")
        elif self.board == self.board_final:
            self.game_over = True
            # Disable buttons
            self._disable_buttons()  
            # Show GIF
            self._show_gif("win.gif", "Congratulations, you won!")  

    def _get_guess(self, letter):
        if len(letter) == 1 and letter.isalpha():
            self._process_guess(letter.lower())
        else:
            messagebox.showinfo("Error", "Guess must be a single letter!")
        gui_board['text'] = ' '.join(self.board)
        gui_guesses['text'] = ', '.join(self.guesses)
        gui_lives['text'] = 'Lives: ' + '❤️' * self.lives
        self._check_status()  # Check end game status

    def _disable_buttons(self):
        for btn in btns:
            btn.config(state="disabled", bg="grey", fg="white")

    def _restart_game(self):
        # Reset game
        self.word = ""
        self.board = []
        self.board_final = []
        self.guesses = ['Guesses:']
        self.lives = 5  # Reset lives
        self.game_over = False

        # Reset word and board
        self._set_word()
        self._create_board(self.word)
        self._set_final_board(self.word)

        # Update UI
        gui_board['text'] = ' '.join(self.board)
        gui_guesses['text'] = ', '.join(self.guesses)
        gui_lives['text'] = 'Lives: ' + '❤️' * self.lives

        # Enable buttons
        for btn in btns:
            btn.config(state="normal", bg="#ed304b", fg="white")

        messagebox.showinfo("Restart", "Let's start fresh! Good luck!")

    def _show_gif(self, gif_path, msg):
        # Create a new window
        dialog = Toplevel(self)
        dialog.title("GIF Dialog")
        
        # Load GIF frames
        images = []
        try:
            for i in itertools.count():
                img = PhotoImage(file=gif_path, format=f'gif - {i}')
                images.append(img)
        except tk.TclError:
            pass

        # Display GIF
        lbl_img = Label(dialog)
        lbl_img.pack()
        
        def _animate(frame=0):
            lbl_img.config(image=images[frame])
            frame = (frame + 1) % len(images)
            dialog.after(100, _animate, frame)
        
        _animate()
        
        # Display message
        lbl_msg = Label(dialog, text=msg, padx=20, pady=10)
        lbl_msg.pack()
        
        # Close button
        Button(dialog, text="Close", command=dialog.destroy).pack()

game = Hangman()  

alpha = list(string.ascii_lowercase)  
btns = []  

gui_board = tk.Label(game, text=' '.join(game.board), font="Courier 30 bold", bg='#f295a1')
gui_board.grid(row=2, column=0, columnspan=6)

gui_guesses = tk.Label(game, text=', '.join(game.guesses), font="Helvetica 12 bold", bg='#f295a1')
gui_guesses.grid(row=3, column=0, columnspan=6)

gui_lives = tk.Label(game, text='Lives: ' + '❤️' * game.lives, font="Helvetica 14 bold", bg='#f295a1')
gui_lives.grid(row=4, column=0, columnspan=6)

def on_click(btn):
    btn.config(state="disabled", bg="grey", fg="white")
    game._get_guess(btn['text'].lower())

def add_btn(x, y, i):
    btn = tk.Button(game, text=alpha[i].upper(), width=5, height=2, bg="#ed304b", fg="white", font="Helvetica 12 bold", command=lambda: on_click(btn))
    btn.grid(row=y, column=x, padx=5, pady=5)
    btns.append(btn)

def setup_buttons():  
    for i in range(26):
        x = i % 6
        y = 5 + i // 6
        add_btn(x, y, i)

setup_buttons()

# Restart Button
tk.Button(game, text="Restart", width=15, height=2, bg="#ed304b", fg="white", font="Helvetica 12 bold", relief="raised", bd=4, command=game._restart_game).grid(row=9, column=0, columnspan=6, padx=5, pady=10)

game.mainloop()
