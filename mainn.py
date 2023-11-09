import math
import random
import tkinter as tk
import time

possible_actions = ["rock", "paper", "scissors"]
player_score = 0
computer_score = 0
rounds = 0
rounds_to_win = 3
user_action = 0

def get_computer_input():
    choix = random.choice(possible_actions)
    return choix

def get_user_input():
    return random.choice(possible_actions)

def timer_update(temps_restant):
    if temps_restant > 0:
        label_timer.config(text=str(temps_restant))
        root.after(1000, timer_update, temps_restant - 1)
    elif temps_restant == 0:
        label_timer.config(text="Go!")
        start_game()

# Fonction pour mettre à jour le score et le nombre de parties jouées
def mettre_a_jour_resultats(resultat):
    global player_score, computer_score, rounds
    if resultat == "player":
        player_score += 1
    elif resultat == "computer":
        computer_score += 1
    rounds += 1
    label_score.config(text=f"Joueur: {player_score} | Ordinateur: {computer_score}\nParties jouées: {rounds}")

# Fonction appelée lorsqu'on appuie sur le bouton Start
def start_game():
    choix_joueur = get_user_input()  # Remplacez ceci par votre fonction de reconnaissance de l'input de la caméra
    if choix_joueur not in ['pierre', 'papier', 'ciseaux']:
        return
    choix_ordinateur = get_computer_input()
    mettre_a_jour_resultats(determiner_gagnant(choix_joueur, choix_ordinateur))
    # Mettez ici votre code pour mettre à jour l'interface de la caméra du joueur avec choix_joueur

# Fonction pour déterminer le gagnant
def determiner_gagnant(choix_joueur, choix_ordi):
    if choix_joueur == choix_ordi:
        return "draw"
    elif (choix_joueur == "rock" and choix_ordi == "scissors") or \
         (choix_joueur == "paper" and choix_ordi == "rock") or \
         (choix_joueur == "scissors" and choix_ordi == "paper"):
        return "player"
    else:
        return "computer"



# Création de l'interface graphique
root = tk.Tk()
root.title("Pierre-Papier-Ciseaux")
root.geometry("400x200")

# Création des widgets
label_camera = tk.Label(root, text="Camera du joueur")
label_camera.pack(side=tk.LEFT)

button_start = tk.Button(root, text="Start", command=lambda: timer_update(3))
button_start.pack(side=tk.LEFT)

label_timer = tk.Label(root, text="")
label_timer.pack(side=tk.LEFT)

label_score = tk.Label(root, text="")
label_score.pack(side=tk.RIGHT)

# Lancement de la boucle principale
root.mainloop()