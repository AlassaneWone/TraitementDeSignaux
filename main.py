import tkinter.font as tkFont
import time
import random
import tkinter as tk
import threading
from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

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

# Création de la fenêtre principale
root = tk.Tk()
root.title("")
width = 600
height = 300
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

# Création des éléments graphiques
start_button = tk.Button(root)
start_button["activebackground"] = "#528181"
start_button["bg"] = "#90ee90"
ft = tkFont.Font(family='System', size=24)
start_button["font"] = ft
start_button["fg"] = "#000000"
start_button["justify"] = "center"
start_button["text"] = "Start Game"
start_button["relief"] = "flat"
start_button.place(x=200, y=0, width=200, height=300)
start_button["command"] = start_game

label_player_score = tk.Label(root)
ft = tkFont.Font(family='System', size=10)
label_player_score["font"] = ft
label_player_score["fg"] = "#333333"
label_player_score["justify"] = "center"
label_player_score["text"] = "0"
label_player_score.place(x=400, y=140, width=200, height=25)

label_computer_score = tk.Label(root)
ft = tkFont.Font(family='System', size=10)
label_computer_score["font"] = ft
label_computer_score["fg"] = "#333333"
label_computer_score["justify"] = "center"
label_computer_score["text"] = "0"
label_computer_score.place(x=400, y=190, width=200, height=25)

label_rounds = tk.Label(root)
ft = tkFont.Font(family='System', size=10)
label_rounds["font"] = ft
label_rounds["fg"] = "#333333"
label_rounds["justify"] = "left"
label_rounds["text"] = "0"
label_rounds.place(x=520, y=80, width=80, height=30)

label_rounds_played = tk.Label(root)
ft = tkFont.Font(family='System', size=10)
label_rounds_played["font"] = ft
label_rounds_played["fg"] = "#333333"
label_rounds_played["justify"] = "right"
label_rounds_played["text"] = "Rounds played:"
label_rounds_played.place(x=420, y=80, width=100, height=30)

label_vs = tk.Label(root)
ft = tkFont.Font(family='System', size=13)
label_vs["font"] = ft
label_vs["fg"] = "#333333"
label_vs["justify"] = "center"
label_vs["text"] = "VS"
label_vs.place(x=400, y=170, width=200, height=25)

label_computer = tk.Label(root)
ft = tkFont.Font(family='System', size=13)
label_computer["font"] = ft
label_computer["fg"] = "#333333"
label_computer["justify"] = "center"
label_computer["text"] = "Computer"
label_computer.place(x=400, y=200, width=200, height=50)

label_player = tk.Label(root)
ft = tkFont.Font(family='System', size=13)
label_player["font"] = ft
label_player["fg"] = "#333333"
label_player["justify"] = "center"
label_player["text"] = "Player"
label_player.place(x=400, y=100, width=200, height=50)

label_score = tk.Label(root)
ft = tkFont.Font(family='System', size=18)
label_score["font"] = ft
label_score["fg"] = "#333333"
label_score["justify"] = "center"
label_score["text"] = "Score"
label_score["relief"] = "flat"
label_score.place(x=400, y=30, width=200, height=50)

def video_capture_thread():
    global cap, detector, user_input
    while True:
        # Get image frame
        success, img = cap.read()
        # Find the hand and its landmarks
        hands, img = detector.findHands(img)  # with draw

        if hands:
            # Information for the first hand detected
            hand1 = hands[0]  # Get the first hand detected
            lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
            bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
            center1 = hand1['center']  # Center coordinates of the first hand
            handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

            # Count the number of fingers up for the first hand
            fingers1 = detector.fingersUp(hand1)
            # print(f'H1 = {fingers1}', end=" ")  # Print the count of fingers that are up

            if (fingers1[0] == 0 and
                    fingers1[1] == 1 and
                    fingers1[2] == 1 and
                    fingers1[3] == 0 and
                    fingers1[4] == 0):
                user_input = 'scissors'
                print('ciseaux')
            elif (fingers1[0] == 0 and
                  fingers1[1] == 0 and
                  fingers1[2] == 0 and
                  fingers1[3] == 0 and
                  fingers1[4] == 0):
                user_input = 'rock'
                print('pierre')
            elif ((fingers1[0] == 1 or fingers1[0] == 0) and
                  fingers1[1] == 1 and
                  fingers1[2] == 1 and
                  fingers1[3] == 1 and
                  fingers1[4] == 1):
                user_input = 'paper'
                print('feuille')
            else:
                user_input = None
                print('pas de signe détecté')

        # Display
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

video_thread = threading.Thread(target=video_capture_thread)
video_thread.daemon = True  # Le thread se terminera lorsque le programme principal se termine
video_thread.start()

root.mainloop()