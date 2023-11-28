import cv2
import imutils
import time
import threading
import numpy as np
from keras.models import load_model

categories = ["paper", "rock", "scissors"]

active = False

# Load the model
model = load_model('TraitementDeSignaux/model.keras')

def process_image(frame):
    img = cv2.resize(frame, standard_size)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    edges = cv2.Canny(img_blur, 50, 50)
    edges = cv2.convertScaleAbs(edges)  # Convert image to 8-bit before finding contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(img_gray)
    cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)
    result = cv2.subtract(img_gray, cv2.bitwise_not(mask))  # Subtract mask from grayscale image
    return result

standard_size = (100, 100)

firstFrame = None
countdown_complete = threading.Event()

def countdown():
    global countdown_complete
    for i in range(3, 0, -1):
        print(f'Screenshot dans {i}')
        time.sleep(1)
    countdown_complete.set()
    print("Screenshot")

vs = cv2.VideoCapture(0)
time.sleep(1.0)

while True:

    ret, frame = vs.read()

    frame = imutils.resize(frame, width=500, height=600)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("a"):
        active = not active

    if key == ord("r"):
        countdown_complete.clear()
        countdown_thread = threading.Thread(target=countdown)
        countdown_thread.start()

    if countdown_complete.is_set() or active:

        screenshot_color = frame.copy()
        screenshot = process_image(screenshot_color) 

        label = model.predict(screenshot.reshape(1, 100, 100, 1))[0]
        gesture = label
        print(gesture)
        # Get the index of the maximum probability
        max_index = np.argmax(label)

        # Get the class name
        gesture = categories[max_index]

        print(gesture)

        screenshot = cv2.resize(screenshot, (500, 500))
        cv2.imshow("Screenshot", screenshot)

        countdown_complete.clear()

    cv2.imshow("camera", frame)

    if key == ord("q"):
        break


vs.release()
cv2.destroyAllWindows()
