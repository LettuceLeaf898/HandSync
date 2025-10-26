import cv2
from cvzone.HandTrackingModule import HandDetector
from flask import Flask, render_template, Response, redirect, url_for

# Load background once
imgBG = cv2.imread("R\\BG_play.png")
if imgBG is None:
    print("Error: Could not load background image.")
    exit()

# Flask setup
app = Flask(__name__)

# Webcam and detector will be initialized lazily inside generate_frames()
# to allow the Flask app to start in environments without a camera.

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
    # Initialize webcam and hand detector lazily so importing the module
    # doesn't require a camera to be connected.
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    detector = HandDetector(maxHands=2, detectionCon=0.5)

    try:
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
            # imgBG_copy = imgBG.copy()
            # imgBG_copy[234:654, 795:1195] = imgScaled

            # # Show snap counters
            # cv2.putText(imgBG_copy, f"Left Snaps: {snapCountLeft}", (50, 150),
            #             cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5)
            # cv2.putText(imgBG_copy, f"Right Snaps: {snapCountRight}", (50, 250),
            #             cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 100, 255), 5)

            

            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', imgScaled)
            frame = buffer.tobytes()

            # Yield frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        try:
            cap.release()
        except Exception:
            pass


@app.route('/')
def index():
    """Main page route"""
    return render_template('index.html')

@app.route('/index.html')
def index_html():
    return redirect(url_for('index'))


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


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/about.html')
def about_html():
    return redirect(url_for('about'))

@app.route('/instructions')
def instructions():
    """Instructions page"""
    return render_template('instructions.html')

@app.route('/instructions.html')
def instructions_html():
    return redirect(url_for('instructions'))

@app.route('/modeselect')
def modeselect():
    """Mode select page"""
    return render_template('modeselect.html')


@app.route('/modeselect.html')
def modeselect_html():
    """Support requests that include the .html suffix by redirecting to the route without it."""
    return redirect(url_for('modeselect'))


@app.route('/play')
def play():
    """Play menu or landing page"""
    return render_template('play.html')

@app.route('/play.html')
def play_html():
    return redirect(url_for('play'))



@app.route('/play/coordination.html')
def play_coordination_html():
    return redirect(url_for('play_coordination'))


@app.route('/play-coordination.html')
def play_dash_coordination_html():
    return redirect(url_for('play_coordination'))


@app.route('/play/coordination')
def play_coordination():
    """Play coordination mode"""
    return render_template('play-coordination.html')


@app.route('/play/rhythm')
def play_rhythm():
    """Play rhythm mode"""
    return render_template('play-rhythm.html')


@app.route('/play-rhythm.html')
def play_dash_rhythm_html():
    return redirect(url_for('play_rhythm'))

@app.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html')

@app.route('/settings.html')
def settings_html():
    return redirect(url_for('settings'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
