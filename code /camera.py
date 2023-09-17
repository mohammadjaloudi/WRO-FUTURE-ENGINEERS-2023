#this code is for camera and turning left or right when seiong block


import cv2
import numpy as np
import imutils
import time
from imutils.video import VideoStream
from collections import deque
import math

# Initialize the camera using multithreading
vs = VideoStream(src=1).start()  # Use src=0 for the default camera (you can change this)
time.sleep(2.0)

# Define a kernel for morphological operations
k = np.ones((5, 5), np.uint8)

# For collecting red or green for the arduino
redColorClose = '0'
greenColorClose = '0'

# Create deques to store tracked red and green points
rp = deque(maxlen=10)
gp = deque(maxlen=10)

# Define HSV color ranges for green and red
g_min_hsv = np.array([37, 38, 24])
g_max_hsv = np.array([99, 255, 255])

# Combined HSV color range for all shades of red
red_min_hsv = np.array([0, 100, 100])
red_max_hsv = np.array([179, 255, 255])  # Covering the entire hue range for red

# Define area thresholds for detection
g_area_thresh = 300
r_area_thresh = 300

# Global variables to store detection results
ed = "N"  # Initialize as "Not detected"
een = "N"  # Initialize as "Not detected"
closest_color = "None"  # Initialize as "None"

# Global variable to control the detection loop
detection_running = True

# Create a window to display the camera feed
cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)

# Function to start color detection
def start_detection():
    global detection_running, ed, een, closest_color, greenColorClose, redColorClose

    try:
        while detection_running:
            frame = vs.read()
            frame = imutils.resize(frame, width=300)

            green_center, green_radius, _ = detect_color(frame, g_min_hsv, g_max_hsv, (0, 255, 0), g_area_thresh)
            red_center, red_radius, _ = detect_color(frame, red_min_hsv, red_max_hsv, (0, 0, 255), r_area_thresh)

            # Display the camera feed in the window
            cv2.imshow("Camera Feed", frame)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break

            # Calculate the distance between detected object centers
            if green_center is not None and red_center is not None:
                green_x, green_y = green_center
                red_x, red_y = red_center
                distance_green_red = math.sqrt((green_x - red_x) ** 2 + (green_y - red_y) ** 2)

                # Determine the closest color
                if distance_green_red < min(green_radius, red_radius):
                    closest_color = "RED"
                    redColorClose = 'R'
                elif distance_green_red < green_radius:
                    closest_color = "Green"
                    greenColorClose = 'L'
                elif distance_green_red < red_radius:
                    closest_color = "Red"
                    redColorClose = 'R'
                else:
                    closest_color = "Red"
                    redColorClose = 'R'

            else:
                # If only one color is detected, set closest_color accordingly
                if green_center is not None:
                    closest_color = "Green"
                    greenColorClose = 'L'
                elif red_center is not None:
                    closest_color = "Red"
                    redColorClose = 'R'
                else:
                    closest_color = "None"

            # Print the closest color in the loop
            print("Closest Color:", closest_color)

    except KeyboardInterrupt:
        pass

    vs.stop()
    cv2.destroyAllWindows()
    detection_running = False

# Function to detect color (both green and red)
def detect_color(frame, min_hsv, max_hsv, color, area_thresh):
    # Apply Gaussian blur and convert to HSV color space
    bf = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv_frame = cv2.cvtColor(bf, cv2.COLOR_BGR2HSV)

    # Color Mask
    mask = cv2.inRange(hsv_frame, min_hsv, max_hsv)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)

    # Find contours in masks
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    last_center = None
    last_radius = None

    # Process contours
    for contour in contours:
        max_area_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(max_area_contour)

        if radius > 10 and cv2.contourArea(max_area_contour) > area_thresh:
            cv2.circle(frame, (int(x), int(y)), int(radius), color, 2)
            cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 255), -1)

            if color == (0, 0, 255):
                rp.appendleft((int(x), int(y)))
            elif color == (0, 255, 0):
                gp.appendleft((int(x), int(y)))

            last_center = (int(x), int(y))
            last_radius = radius

    return last_center, last_radius, None

# Start the color detection loop
start_detection()

