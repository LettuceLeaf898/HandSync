import cv2
from cvzone.HandTrackingModule import HandDetector
from flask import Flask, render_template, Response

# Load background once
imgBG = cv2.imread("R\\BG_play.png")
if imgBG is None:
    print("Error: Could not load background image.")
    exit()

# Flask setup
app = Flask(__name__)

# Set up webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Hand detector (detect both hands)
detector = HandDetector(maxHands=2, detectionCon=0.5)

# Game / snap logic variables
startGame = True  # Auto-start for web version
snapCountLeft = 0
snapCountRight = 0

# Separate snap detection states for each hand
snapReadyLeft = True
snapReadyRight = True

snapThreshold = 40  # Distance threshold (pixels)


def generate_frames():
    """Generator function to yield video frames"""
    global snapCountLeft, snapCountRight, snapReadyLeft, snapReadyRight, startGame
    
    while True:
        success, img = cap.read()
        if not success:
            print("Camera not detected.")
            break
        
        flipped = cv2.flip(img, 1)
        
        # Crop and resize camera frame
        imgScaled = cv2.resize(flipped, (0, 0), fx=0.875, fy=0.875)
        imgScaled = imgScaled[:, 80:480]

        hands, img = detector.findHands(imgScaled, flipType=False)

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

        # Overlay camera feed on background
        imgBG_copy = imgBG.copy()
        imgBG_copy[234:654, 795:1195] = imgScaled

        # Show snap counters
        cv2.putText(imgBG_copy, f"Left Snaps: {snapCountLeft}", (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5)
        cv2.putText(imgBG_copy, f"Right Snaps: {snapCountRight}", (50, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 100, 255), 5)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', imgBG_copy)
        frame = buffer.tobytes()

        # Yield frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    """Main page route"""
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/reset')
def reset():
    """Reset snap counters"""
    global snapCountLeft, snapCountRight
    snapCountLeft = 0
    snapCountRight = 0
    return 'Counters reset!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
