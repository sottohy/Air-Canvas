import cv2
import os
import mediapipe as mp
import numpy as np

# Get list of header images 
myList = os.listdir("header")
overlayList = []
for imPath in myList:
    image = cv2.imread(f'header/{imPath}')
    overlayList.append(image)

# Default image
header = overlayList[0]

capture = cv2.VideoCapture(0)
capture.set(3, 1280) # Width
capture.set(4, 720) # Height

# Initializing the hands module and creating an instance of the hand tracking model
mphands = mp.solutions.hands
hands = mphands.Hands()
mpdraw = mp.solutions.drawing_utils

# Finds and draws hand landmarks
def find_hands(img):
    frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    results = hands.process(frame_rgb)  # Process frame to find hands

    # Checking number of hands
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            # hand has the landmark data that will be drawn on the frame, HAND_CONNECTIONS draws the connection lines
            mpdraw.draw_landmarks(img, hand, mphands.HAND_CONNECTIONS) 

    return img, results


# Finds landmark positions
def find_position(img, results, handNo=0):
    landmarks_list = []

    # Find and draw a circle at specific points
    if results.multi_hand_landmarks:
        currHand = results.multi_hand_landmarks[handNo]
        for i, lm in enumerate(currHand.landmark):
            h, w, c = img.shape
            cx = int(lm.x * w)
            cy = int(lm.y * h)

            landmarks_list.append([i, cx, cy])
                
    return landmarks_list


# Counts how many fingers are up
def fingers_up(lm_list):
    tip_ids = [4, 8, 12, 16, 20]
    fingers_state = []
        
    # Looping over the tip ids
    for id in range(5):
        # In case of thumb, check X instead of Y
        if id == 0:
            if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id]-1][1]:
                fingers_state.append(1) # Append 1 if up
            else: 
                fingers_state.append(0) # Append 0 if down
        
        # Rest of the fingers
        else:
            if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id]-2][2]:
                fingers_state.append(1) # Append 1 if up
            else:
                fingers_state.append(0) # Append 0 if down

    return fingers_state


draw_color = (255, 255, 255) # Default draw color
xcurr, ycurr = 0, 0 # Starting positions
canvas = np.zeros((720, 1280, 3), np.uint8) # Blank canvas

while True:
    isTrue, frame = capture.read()
    
    # Flip frame
    frame = cv2.flip(frame, 1) 

    # Get hand landmarks
    frame, res = find_hands(frame)

    # Get landmark positions
    landmarks_pos = find_position(frame, res)
    if len(landmarks_pos) != 0:
        # x and y coordinates of the tip of index finger (id 8)
        xi, yi = landmarks_pos[8][1], landmarks_pos[8][2]

        # x and y coordinates of the tip of middle finger (id 12)
        xm, ym = landmarks_pos[12][1], landmarks_pos[12][2]

        # Check which fingers are up
        fingers = fingers_up(landmarks_pos)
        print(fingers)

        # Checking if index and middle fingers are up (selecting colors)
        if fingers[1] and fingers[2]:
            xcurr, ycurr = 0, 0
            # Checking if the fingers are in the header section
            if ym < 125:
                if 10<xm<250: # Yellow
                    header = overlayList[1]
                    draw_color = (0, 220, 255) 
                elif 350<xm<550: # Orange
                    header = overlayList[2]
                    draw_color = (87, 147, 255)
                elif 670<xm<900: # Pink
                    header = overlayList[3]
                    draw_color = (223, 84, 255)
                elif 1000<xm<1270: # Eraser
                    header = overlayList[4]
                    draw_color = (0, 0, 0)

        elif fingers[1] == True and fingers[2] == False:
            if xcurr == 0 and ycurr == 0: # Very first itteration
                xcurr, ycurr = xi, yi

            if draw_color == (0, 0, 0): # If eraser
                brush_thickness = 70
            
            if draw_color != (0, 0, 0):
                cv2.circle(frame, (xi, yi), 10, draw_color, cv2.FILLED)
                brush_thickness = 10

            cv2.line(frame, (xcurr,ycurr), (xi, yi), draw_color, brush_thickness) 
            cv2.line(canvas, (xcurr,ycurr), (xi, yi), draw_color, brush_thickness) 
            xcurr, ycurr = xi, yi

        
    # Convert the canvas image to grayscale
    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    
    # Inverse the image (black and whites)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)

    # Convert the mask to a 3-channel image (BGR)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    # Add the image and the inverse image on top of each other
    frame = cv2.bitwise_and(frame, imgInv)

    # Add the image and the canvas on top of each other
    frame = cv2.bitwise_or(frame, canvas)

    frame[0:125, 0:1280] = header
    cv2.imshow("Frame", frame)
    #cv2.imshow("Canvas", canvas)

    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()