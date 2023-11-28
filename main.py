import tkinter.font as tkFont
import time
import random
import tkinter as tk
import threading
from cvzone.HandTrackingModule import HandDetector
import cv2

is_game_running = False
player_score = 0
computer_score = 0
rounds = 0
possible_actions = ["rock", "paper", "scissors"]
user_input = None

def start_game():
    global is_game_running
    if is_game_running:
        return False
    is_game_running = True
    start_button["text"] = "Rock"
    root.update()
    time.sleep(0.5)

    start_button["text"] = "Paper"
    root.update()
    time.sleep(0.5)

    start_button["text"] = "Scissors"
    root.update()
    time.sleep(0.5)

    start_button["text"] = "Shoot!"
    root.update()

    computer_input = random.choice(possible_actions)

    update_score(determine_winner(computer_input), computer_input)
    is_game_running = False

def determine_winner(computer_input):
    # 0 = tie, 1 = player won, 2 = computer won, 3 = error
    global user_input

    if user_input == None:
        return 0
    elif user_input == computer_input:
        return 1
    elif (user_input == "rock" and computer_input == "scissors") or \
            (user_input == "paper" and computer_input == "rock") or \
            (user_input == "scissors" and computer_input == "paper"):
        return 2
    else:
        return 3

def update_score(result, computer_input):
    global user_input, player_score, computer_score, rounds
    if result == 0:
        start_button["text"] = "You didn't choose \n  click to play  \n again \n computer chose \n" + computer_input
        return False
    time.sleep(0.5)
    if result == 2:
        player_score += 1
        start_button[
            "text"] = "You won! \n  click to play  \n again \n computer chose \n" + computer_input + " and you chose \n" + user_input
    elif result == 3:
        computer_score += 1
        start_button[
            "text"] = "You lost! \n  click to play  \n again \n computer chose \n" + computer_input + " and you chose \n" + user_input
    else:
        start_button["text"] = "It's a tie! \n  click to play  \n again, \n you both chose \n" + computer_input
    rounds += 1
    label_player_score["text"] = player_score
    label_computer_score["text"] = computer_score
    label_rounds["text"] = rounds
    user_input = None

# Main window creation
root = tk.Tk()
root.title("")
width = 800  # Shortened the width
height = 600
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

# Creating graphical elements
start_button = tk.Button(root)
start_button["activebackground"] = "#528181"
start_button["bg"] = "#90ee90"
ft = tkFont.Font(family='System', size=24)
start_button["font"] = ft
start_button["fg"] = "#000000"
start_button["justify"] = "center"
start_button["text"] = "Start Game"
start_button["relief"] = "flat"
start_button.place(x=0, y=0, width=350, height=600)  # Adjusted the position and size
start_button["command"] = start_game

label_player_score = tk.Label(root)
ft = tkFont.Font(family='System', size=10)
label_player_score["font"] = ft
label_player_score["fg"] = "#333333"
label_player_score["justify"] = "center"
label_player_score["text"] = "0"
label_player_score.place(x=350, y=280, width=400, height=50)  # Adjusted the position

label_computer_score = tk.Label(root)
ft = tkFont.Font(family='System', size=10)
label_computer_score["font"] = ft
label_computer_score["fg"] = "#333333"
label_computer_score["justify"] = "center"
label_computer_score["text"] = "0"
label_computer_score.place(x=350, y=450, width=400, height=50)  # Adjusted the position

label_rounds = tk.Label(root)
ft = tkFont.Font(family='System', size=10)
label_rounds["font"] = ft
label_rounds["fg"] = "#333333"
label_rounds["justify"] = "left"
label_rounds["text"] = "0"
label_rounds.place(x=540, y=160, width=160, height=60)  # Adjusted the position

label_rounds_played = tk.Label(root)
ft = tkFont.Font(family='System', size=10)
label_rounds_played["font"] = ft
label_rounds_played["fg"] = "#333333"
label_rounds_played["justify"] = "right"
label_rounds_played["text"] = "Rounds played:"
label_rounds_played.place(x=390, y=160, width=200, height=60)  # Adjusted the position

label_vs = tk.Label(root)
ft = tkFont.Font(family='System', size=13)
label_vs["font"] = ft
label_vs["fg"] = "#333333"
label_vs["justify"] = "center"
label_vs["text"] = "VS"
label_vs.place(x=350, y=340, width=400, height=50)  # Adjusted the position

label_computer = tk.Label(root)
ft = tkFont.Font(family='System', size=13)
label_computer["font"] = ft
label_computer["fg"] = "#333333"
label_computer["justify"] = "center"
label_computer["text"] = "Computer"
label_computer.place(x=350, y=400, width=400, height=100)  # Adjusted the position

label_player = tk.Label(root)
ft = tkFont.Font(family='System', size=13)
label_player["font"] = ft
label_player["fg"] = "#333333"
label_player["justify"] = "center"
label_player["text"] = "Player"
label_player.place(x=350, y=200, width=400, height=100)  # Adjusted the position

label_score = tk.Label(root)
ft = tkFont.Font(family='System', size=18)
label_score["font"] = ft
label_score["fg"] = "#333333"
label_score["justify"] = "center"
label_score["text"] = "Score"
label_score["relief"] = "flat"
label_score.place(x=350, y=60, width=400, height=100)  # Adjusted the position

# Creating the camera feed panel
panel = tk.Label(root)
panel.place(x=700, y=0, width=200, height=600)  # Adjusted the position and size

def video_capture_thread():
    #Code Alassane

video_thread = threading.Thread(target=video_capture_thread)
video_thread.daemon = True  # The thread will terminate when the main program terminates
video_thread.start()

root.mainloop()
