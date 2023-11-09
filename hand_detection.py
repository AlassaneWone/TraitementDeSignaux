from cvzone.HandTrackingModule import HandDetector
import cv2

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
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
            print('ciseaux')
        elif (fingers1[0] == 0 and
              fingers1[1] == 0 and
              fingers1[2] == 0 and
              fingers1[3] == 0 and
              fingers1[4] == 0):
            print('pierre')
        elif ((fingers1[0] == 1 or fingers1[0] == 0) and
              fingers1[1] == 1 and
              fingers1[2] == 1 and
              fingers1[3] == 1 and
              fingers1[4] == 1):
            print('feuille')
        else:
            print('pas de signe détecté')

    # Display
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
