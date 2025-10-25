import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
# Load background once
imgBG = cv2.imread("R\BG.png")
if imgBG is None:
    print("Error: Could not load background image.")
    exit()

# Set up webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False

while True:
    success, img = cap.read()
    if not success:
        print("Camera not detected.")
        break

    imgScaled = cv2.resize(img, (0, 0), fx=0.875, fy=0.875)
    imgScaled = imgScaled[:, 80:480]

    hands, img = detector.findHands(imgScaled)

    if startGame and hands:
        
        if stateResult is False:
            timer = time.time() - initalTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
            if timer >= 100:
                timer = 0
                stateResult = True
        
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        print(f"Fingers: {fingers}")

    imgBG_copy = imgBG.copy()
    imgBG_copy[234:654, 795:1195] = imgScaled

    cv2.imshow("Background", imgBG_copy)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        startGame = True
        timer = 0
        stateResult = False
        initalTime = time.time()
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
