# balloon_pop_backend.py

import random
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
speed = 15
score = 0
startTime = time.time()
totalTime = 30

def resetBalloon():
    return {
        'x': random.randint(100, 1180),  # 1280 - width of balloon image
        'y': 770  # 720 + 50, height of webcam frame + margin
    }

balloon_position = resetBalloon()

@app.route('/api/game_data', methods=['GET'])
def get_game_data():
    global score, balloon_position, speed, startTime

    timeRemain = int(totalTime - (time.time() - startTime))
    if timeRemain < 0:
        return jsonify({
            'score': score,
            'time': 'Time UP'
        })
    else:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        balloon_position['y'] -= speed  # Move the balloon up
        if balloon_position['y'] < 0:
            balloon_position = resetBalloon()
            speed += 1

        if hands:
            hand = hands[0]
            x, y = hand['lmList'][8]
            if 500 <= x <= 780 and 300 <= y <= 580:  # Adjust coordinates based on balloon image size
                balloon_position = resetBalloon()
                score += 10
                speed += 1

        return jsonify({
            'score': score,
            'time': timeRemain,
            'balloon_position': balloon_position
        })

if __name__ == '_main_':
    app.run(debug=True)