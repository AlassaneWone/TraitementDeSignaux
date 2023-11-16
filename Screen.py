import cv2
import imutils
import time
import threading

firstFrame = None
countdown_complete = threading.Event()

def countdown():
    global countdown_complete
    for i in range(3, 0, -1):
        print(f'Screenshot dans {i}')
        time.sleep(1)
    countdown_complete.set()

vs = cv2.VideoCapture(0)
time.sleep(2.0)

while True:
    ret, frame = vs.read()

    frame = imutils.resize(frame, width=500)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        countdown_complete.clear()
        countdown_thread = threading.Thread(target=countdown)
        countdown_thread.start()

    if countdown_complete.is_set():
        screenshot = frame.copy()
        screenshot = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(screenshot, 50, 200)
        cv2.imshow("Screenshot", edges)
        countdown_complete.clear()

    cv2.imshow("camera", frame)

    if key == ord("q"):
        break

vs.release()
cv2.destroyAllWindows()
