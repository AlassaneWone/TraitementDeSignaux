import cv2
import imutils
import time
import threading
import numpy as np
from keras.models import load_model
from PIL import Image, ImageTk
import tkinter as tk
import random

categories = ["paper", "rock", "scissors"]

active = False
screenshot_countdown = 5

# Load the model
model = load_model('model.keras')

standard_size = (100, 100)

countdown_complete = threading.Event()

player_score = 0
computer_score = 0

def process_image(frame):
    img = cv2.resize(frame, standard_size)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    edges = cv2.Canny(img_blur, 50, 50)
    edges = cv2.convertScaleAbs(edges)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(img_gray)
    cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)
    result = cv2.subtract(img_gray, cv2.bitwise_not(mask))
    return result

def countdown(label_gesture, label_computer_choice, label_result):
    global countdown_complete, screenshot_countdown, player_score, computer_score

    for i in range(screenshot_countdown, 0, -1):
        print(f'Screenshot dans {i} secondes')
        time.sleep(1)
    countdown_complete.set()
    print("Screenshot")

    # Logique pour déterminer le gagnant après la capture d'écran
    player_gesture = label_gesture.cget("text").split(":")[1].strip()
    computer_choice = label_computer_choice.cget("text").split(":")[1].strip()

    # Logique du jeu (pierre-papier-ciseaux)
    if player_gesture == computer_choice:
        result_text = "Égalité"
    elif (
        (player_gesture == "rock" and computer_choice == "scissors") or
        (player_gesture == "paper" and computer_choice == "rock") or
        (player_gesture == "scissors" and computer_choice == "paper")
    ):
        result_text = "Vous gagnez!"
        player_score += 1
    else:
        result_text = "L'ordinateur gagne!"
        computer_score += 1

    label_result.config(text=f"Résultat: {result_text}")
    label_result.pack(pady=10)  # Affichage du résultat

    label_player_score.config(text=f"Joueur: {player_score}")
    label_computer_score.config(text=f"Ordinateur: {computer_score}")

def capture_screenshot(root, vs, panel, label_gesture, label_computer_choice, label_result):
    global active, countdown_complete, screenshot_countdown

    ret, frame = vs.read()
    frame = imutils.resize(frame, width=500, height=600)

    screenshot_color = frame.copy()
    screenshot = process_image(screenshot_color)

    label = model.predict(screenshot.reshape(1, 100, 100, 1))[0]
    max_index = np.argmax(label)
    gesture = categories[max_index]

    # Choix aléatoire de l'ordinateur
    computer_choice = random.choice(categories)

    screenshot = cv2.resize(screenshot, (500, 500))

    image = cv2.cvtColor(screenshot, cv2.COLOR_GRAY2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    panel.config(image=image)
    panel.image = image

    label_gesture.config(text=f"Geste détecté : {gesture}")
    label_computer_choice.config(text=f"Ordinateur : {computer_choice}")

    countdown_complete.clear()
    screenshot_countdown = 5

    countdown_thread = threading.Thread(target=countdown, args=(label_gesture, label_computer_choice, label_result))
    countdown_thread.start()

    cv2.imshow("camera", frame)

def start_countdown():
    root.after(5000, capture_screenshot, root, vs, panel, label_gesture, label_computer_choice, label_result)

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Rock-Paper-Scissors")

# Création des labels
label_player_score = tk.Label(root, text="Joueur: 0")
label_player_score.pack(pady=10)

label_computer_score = tk.Label(root, text="Ordinateur: 0")
label_computer_score.pack(pady=10)

# Création du panneau pour afficher la capture d'écran
panel = tk.Label(root)
panel.pack(padx=10, pady=10)

# Création de la zone de texte pour afficher le geste détecté
label_gesture = tk.Label(root, text="Geste détecté : ")
label_gesture.pack(pady=10)

# Création de la zone de texte pour afficher le choix de l'ordinateur
label_computer_choice = tk.Label(root, text="Ordinateur : ")
label_computer_choice.pack(pady=10)

# Création de la zone de texte pour afficher le résultat
label_result = tk.Label(root, text="Résultat : ")
label_result.pack(pady=10)

# Création du bouton pour activer/désactiver la capture d'écran
toggle_button = tk.Button(root, text="Capture Screenshot", command=start_countdown)
toggle_button.pack(pady=10)

# Initialisation de la capture vidéo
vs = cv2.VideoCapture(0)
time.sleep(1.0)

# Lancement de la boucle principale de l'interface Tkinter
root.mainloop()

# Arrêt propre de la capture vidéo à la fermeture de l'application
vs.release()
cv2.destroyAllWindows()

