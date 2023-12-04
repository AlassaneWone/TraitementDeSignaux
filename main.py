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
    """
    PRE: 'frame' is a color (BGR) image obtained from a webcam or a file.
    POST: Returns the processed image in grayscale with contours highlighted.
    """
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
    """
    PRE: 'label_gesture', 'label_computer_choice', and 'label_result' are tkinter Label widgets.
    POST: 'label_result', 'label_player_score', and 'label_computer_score' are updated with the outcome of the round and the new scores.
    """
    global screenshot_countdown, player_score, computer_score

    player_gesture = label_gesture.cget("text").split(":")[1].strip()
    computer_choice = label_computer_choice.cget("text").split(":")[1].strip()

    if player_gesture == computer_choice:
        result_text = "Draw"
    elif (
        (player_gesture == "rock" and computer_choice == "scissors") or
        (player_gesture == "paper" and computer_choice == "rock") or
        (player_gesture == "scissors" and computer_choice == "paper")
    ):
        result_text = "You Won!"
        player_score += 1
    else:
        result_text = "The compter won!"
        computer_score += 1

    label_result.config(text=f"Outcome: {result_text}")
    label_result.pack(pady=10)

    label_player_score.config(text=f"Player: {player_score}")
    label_computer_score.config(text=f"Computer: {computer_score}")


def show_camera():
    """
    PRE: 'vs' is a VideoCapture object that has been initialized with a video source (like a webcam).
         'panel' is a tkinter Label or similar widget that can display images.
         'root' is a tkinter root or Toplevel window.
    POST: 'panel' is updated with a new frame from the video source.
    """
    frame = vs.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    frame = ImageTk.PhotoImage(frame)
    panel.config(image=frame)
    panel.image = frame
    root.after(10, show_camera)


def capture_screenshot():
    """
    PRE: 'vs' is a VideoCapture object that has been initialized with a video source (like a webcam).
         'panel_camera', 'label_probability', 'label_gesture', and 'label_computer_choice' are tkinter Label widgets.
         'model' is a trained machine learning model that can predict gestures from images.
         'categories' is a list of gesture names in the order that 'model' uses.
    POST: 'panel_camera', 'label_probability', 'label_gesture', and 'label_computer_choice' are updated with new information.
          A new thread is started to determine the winner of the round.
    """
    frame = vs.read()
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

    label_probability.config(text=f"Probability : Paper:{(label[0]*100):.2f}%, Rock:{(label[1]*100):.2f}%, Scissors:{(label[2]*100):.2f}%")
    label_gesture.config(text=f"Geste détecté : {gesture}")
    label_computer_choice.config(text=f"Computer : {random.choice(categories)}")

    countdown_thread = threading.Thread(target=countdown, args=(label_gesture, label_computer_choice, label_result))
    countdown_thread.start()

# Tkinter window creation
root = tk.Tk()
root.title("Rock-Paper-Scissors")

# Label creation
label_score = tk.Label(root, text="Score:")
label_score.pack(pady=10)

label_player_score = tk.Label(root, text="Player: 0")
label_player_score.pack(pady=10)

label_computer_score = tk.Label(root, text="Computer: 0")
label_computer_score.pack(pady=10)

# Create a panel to display the camera in real time
panel = tk.Label(root)
panel.pack(padx=10, pady=10)

label_probability = tk.Label(root, text="Probabilité : ")
label_probability.pack(pady=10)

# Create a text box to display the detected gesture
label_gesture = tk.Label(root, text="Detected gesture : ")
label_gesture.pack(pady=10)

# Create text box to display computer selection
label_computer_choice = tk.Label(root, text="Computer : ")
label_computer_choice.pack(pady=10)

# Create a text box to display the result
label_result = tk.Label(root, text="Outcome : ")
label_result.pack(pady=10)

# Initialize video capture
vs = cv2.VideoCapture(0)
time.sleep(1.0)

# Create window for processed camera
camera_window = tk.Toplevel(root)
camera_window.title("Camera Feed")

# Create a panel to display the processed camera
panel_camera = tk.Label(camera_window)
panel_camera.pack(padx=10, pady=10)

# Create button to capture screenshot
toggle_button = tk.Button(root, text="Capture Screenshot", command=capture_screenshot)
toggle_button.pack(pady=10)

# Launch the main loop of the Tkinter interface
root.after(10, show_camera)
root.mainloop()

# Clean stop of video capture when application is closed
vs.release()
cv2.destroyAllWindows()



