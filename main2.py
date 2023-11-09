import tkinter as tk
import tkinter.font as tkFont
import time
import math
import random
import tkinter as tk
import time


class App:
    def __init__(self, root):
        # setting variables
        self.is_game_running = False
        self.player_score = 0
        self.computer_score = 0
        self.rounds = 0
        self.possible_actions = ["rock", "paper", "scissors"]

        # setting title
        root.title("")
        # setting window size
        width = 600
        height = 300
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.start_button = tk.Button(root)
        self.start_button["activebackground"] = "#528181"
        self.start_button["bg"] = "#90ee90"
        ft = tkFont.Font(family='System', size=24)
        self.start_button["font"] = ft
        self.start_button["fg"] = "#000000"
        self.start_button["justify"] = "center"
        self.start_button["text"] = "Start Game"
        self.start_button["relief"] = "flat"
        self.start_button.place(x=200, y=0, width=200, height=300)
        self.start_button["command"] = self.start_game

        label_score = tk.Label(root)
        ft = tkFont.Font(family='System', size=18)
        label_score["font"] = ft
        label_score["fg"] = "#333333"
        label_score["justify"] = "center"
        label_score["text"] = "Score"
        label_score["relief"] = "flat"
        label_score.place(x=400, y=30, width=200, height=50)

        label_player = tk.Label(root)
        ft = tkFont.Font(family='System', size=13)
        label_player["font"] = ft
        label_player["fg"] = "#333333"
        label_player["justify"] = "center"
        label_player["text"] = "Player"
        label_player.place(x=400, y=100, width=200, height=50)

        label_computer = tk.Label(root)
        ft = tkFont.Font(family='System', size=13)
        label_computer["font"] = ft
        label_computer["fg"] = "#333333"
        label_computer["justify"] = "center"
        label_computer["text"] = "Computer"
        label_computer.place(x=400, y=200, width=200, height=50)

        self.label_player_score = tk.Label(root)
        ft = tkFont.Font(family='System', size=10)
        self.label_player_score["font"] = ft
        self.label_player_score["fg"] = "#333333"
        self.label_player_score["justify"] = "center"
        self.label_player_score["text"] = "playerscore"
        self.label_player_score.place(x=400, y=140, width=200, height=25)

        self.label_computer_score = tk.Label(root)
        ft = tkFont.Font(family='System', size=10)
        self.label_computer_score["font"] = ft
        self.label_computer_score["fg"] = "#333333"
        self.label_computer_score["justify"] = "center"
        self.label_computer_score["text"] = "computerscore"
        self.label_computer_score.place(x=400, y=190, width=200, height=25)

        label_rounds_played = tk.Label(root)
        ft = tkFont.Font(family='System', size=10)
        label_rounds_played["font"] = ft
        label_rounds_played["fg"] = "#333333"
        label_rounds_played["justify"] = "right"
        label_rounds_played["text"] = "Rounds played:"
        label_rounds_played.place(x=420,y=80,width=100,height=30)

        self.label_rounds = tk.Label(root)
        ft = tkFont.Font(family='System', size=10)
        self.label_rounds["font"] = ft
        self.label_rounds["fg"] = "#333333"
        self.label_rounds["justify"] = "left"
        self.label_rounds["text"] = "0"
        self.label_rounds.place(x=520,y=80,width=80,height=30)

        label_vs = tk.Label(root)
        ft = tkFont.Font(family='System', size=13)
        label_vs["font"] = ft
        label_vs["fg"] = "#333333"
        label_vs["justify"] = "center"
        label_vs["text"] = "VS"
        label_vs.place(x=400, y=170, width=200, height=25)

    def get_user_input(self):
        return random.choice(self.possible_actions)

    def start_game(self):
        if self.is_game_running:
            return False
        self.is_game_running = True
        self.start_button["text"] = "Rock"
        root.update()
        time.sleep(0.5)

        self.start_button["text"] = "Paper"
        root.update()
        time.sleep(0.5)

        self.start_button["text"] = "Scissors"
        root.update()
        time.sleep(0.5)

        self.start_button["text"] = "Shoot!"
        root.update()

        computer_input = random.choice(self.possible_actions)
        user_input = self.get_user_input()

        self.update_score(self.determine_winner(user_input, computer_input), computer_input)
        self.is_game_running = False

    def determine_winner(self, user_input, computer_input):
        # 0 = tie, 1 = player won, 2 = computer won
        if user_input == computer_input :
            return 0
        elif (user_input == "rock" and computer_input  == "scissors") or \
                (user_input == "paper" and computer_input  == "rock") or \
                (user_input == "scissors" and computer_input  == "paper"):
            return 1
        else:
            return 2

    def update_score(self, result, computer_input):
        time.sleep(0.5)
        if result == 1:
            self.player_score += 1
            self.start_button["text"] = "You won! \n  click to play  \n again"
        elif result == 2:
            self.computer_score += 1
            self.start_button["text"] = "You lost! \n  click to play  \n again"
        else:
            self.start_button["text"] = "It's a tie! \n  click to play  \n again"
        self.rounds += 1
        self.label_player_score["text"] = self.player_score
        self.label_computer_score["text"] = self.computer_score
        self.label_rounds["text"] = self.rounds


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()