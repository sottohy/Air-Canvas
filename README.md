# Air Canvas

Air Canvas is a Python application that allows you to draw in the air using hand gestures captured by a webcam. This project uses OpenCV and MediaPipe for hand tracking and gesture recognition.

## Features

- Draw on a virtual canvas using your hand.
- Change colors or erase drawings using specific hand gestures.
- Real-time hand tracking and gesture recognition.

## Requirements

- Python 3.7 or later
- OpenCV
- MediaPipe
- NumPy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sottohy/Air-Canvas.git
   cd air-canvas
2. Install the required packages:
   ```
   pip install opencv-python mediapipe numpy
3. Place your header images in a folder named header in the root directory. The images will be used for selecting colors and the eraser.


## Usage
1. Run the application:
   ```
   python air_canvas.py
2. The webcam feed will open, and you can start drawing using your hand gestures.


## Gestures
- Drawing: Raise only the index finger.
- Selecting Colors: Raise both the index and middle fingers and move your hand to the desired color in the header section.


## Code Overview
- find_hands(): Finds and draws hand landmarks on the given image.
- find_position(): Finds the landmark positions of the detected hands.
- fingers_up(): Determines which fingers are up based on the landmark positions.
- Main loop: Captures webcam frames, processes hand landmarks, checks gestures, and updates the canvas accordingly.


## Demo
https://github.com/sottohy/Air-Canvas/assets/91037437/6655ff33-9fc9-49d8-868d-9a2c50485b0f


