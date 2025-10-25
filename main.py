import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

# Load background once
imgBG = cv2.imread("R\\BGH.png")

if imgBG is None:
    print("Error: Could not load background image.")
    exit()

# Set up webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Hand detector (detect both hands)
detector = HandDetector(maxHands=2, detectionCon=0.8)

# Game / snap logic variables
startGame = False
snapCountLeft = 0
snapCountRight = 0

# Separate snap detection states for each hand
snapReadyLeft = True
snapReadyRight = True

snapThreshold = 40  # Distance threshold (pixels)

while True:
    success, img = cap.read()
    if not success:
        print("Camera not detected.")
        break
    
    # Crop and resize camera frame b   
    imgScaled = cv2.resize(img, (0, 0), fx=0.875, fy=0.875)
    imgScaled = imgScaled[:, 80:480]
    
    # Overlay camera feed on background
    imgBG_copy = imgBG.copy()
    imgBG_copy[234:654, 795:1195] = imgScaled
    
    

    hands, img = detector.findHands(imgScaled, flipType=True)

    if startGame and hands:
        for hand in hands:
            lmList = hand["lmList"]
            handType = hand["type"]  # "Left" or "Right"

            # Thumb tip (4) and middle finger tip (12)
            x1, y1 = lmList[4][0:2]
            x2, y2 = lmList[12][0:2]

            # Compute distance between thumb and middle finger
            length, _, _ = detector.findDistance((x1, y1), (x2, y2), img)

            # Snap detection for left hand
            if handType == "Left":
                if length < snapThreshold and snapReadyLeft:
                    snapReadyLeft = False
                elif length > snapThreshold + 20 and not snapReadyLeft:
                    snapCountLeft += 1
                    print(f"Left hand snap! Count = {snapCountLeft}")
                    snapReadyLeft = True

            # Snap detection for right hand
            elif handType == "Right":
                if length < snapThreshold and snapReadyRight:
                    snapReadyRight = False
                elif length > snapThreshold + 20 and not snapReadyRight:
                    snapCountRight += 1
                    print(f"Right hand snap! Count = {snapCountRight}")
                    snapReadyRight = True

    

    # Show snap counters
    cv2.putText(imgBG_copy, f"Left Snaps: {snapCountLeft}", (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5)
    cv2.putText(imgBG_copy, f"Right Snaps: {snapCountRight}", (50, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 100, 255), 5)

    cv2.imshow("Background", imgBG_copy)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        startGame = True
        snapCountLeft = 0
        snapCountRight = 0
        print("Snap detection started.")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
