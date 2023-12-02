import cv2
import tkinter as tk
import threading
from PIL import Image, ImageTk
import time
import imutils
import numpy as np
from keras.models import load_model
import random

categories = ["paper", "rock", "scissors"]

screenshot_countdown = 5

# Load the model
model = load_model('model.keras')

standard_size = (100, 100)

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
    global screenshot_countdown, player_score, computer_score

    for i in range(screenshot_countdown, 0, -1):
        print(f'Screenshot dans {i} secondes')
        time.sleep(1)
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

# Fonction pour afficher la caméra en temps réel
def show_camera():
    ret, frame = vs.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(frame)
    panel.config(image=frame)
    panel.image = frame
    root.after(10, show_camera)  # Update every 10 milliseconds

# Fonction pour capturer un screenshot
def capture_screenshot():
    ret, frame = vs.read()
    # Capture du screenshot et traitement de l'image
    screenshot_color = frame.copy()
    screenshot = process_image(screenshot_color)

    label = model.predict(screenshot.reshape(1, 100, 100, 1))[0]
    max_index = np.argmax(label)
    gesture = categories[max_index]

    screenshot = cv2.resize(screenshot, (500, 500))

    image = cv2.cvtColor(screenshot, cv2.COLOR_GRAY2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    panel_camera.config(image=image)
    panel_camera.image = image

    label_gesture.config(text=f"Geste détecté : {gesture}")
    label_computer_choice.config(text=f"Ordinateur : {random.choice(categories)}")

    countdown_thread = threading.Thread(target=countdown, args=(label_gesture, label_computer_choice, label_result))
    countdown_thread.start()

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Rock-Paper-Scissors")

# Création des labels
label_player_score = tk.Label(root, text="Joueur: 0")
label_player_score.pack(pady=10)

label_computer_score = tk.Label(root, text="Ordinateur: 0")
label_computer_score.pack(pady=10)

# Création du panneau pour afficher la caméra en temps réel
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

# Initialisation de la capture vidéo
vs = cv2.VideoCapture(0)
time.sleep(1.0)

# Création de la fenêtre pour la caméra traitée
camera_window = tk.Toplevel(root)
camera_window.title("Camera Feed")

# Création du panneau pour afficher la caméra traitée
panel_camera = tk.Label(camera_window)
panel_camera.pack(padx=10, pady=10)

# Création du bouton pour capturer le screenshot
toggle_button = tk.Button(root, text="Capture Screenshot", command=capture_screenshot)
toggle_button.pack(pady=10)

# Lancement de la boucle principale de l'interface Tkinter
root.after(10, show_camera)  # Initial call to start the camera feed
root.mainloop()

# Arrêt propre de la capture vidéo à la fermeture de l'application
vs.release()
cv2.destroyAllWindows()



