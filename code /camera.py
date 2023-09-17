#this code is for camera and turning left or right when seiong block


import cv2
import numpy as np
import imutils
import time
from imutils.video import VideoStream
from collections import deque

# Initialize the camera using multithreading
vs = VideoStream(src=1).start()  # Use src=0 for the default camera (you can change this)
time.sleep(2.0)

# Define a kernel for morphological operations
k = np.ones((5, 5), np.uint8)

# Create deques to store tracked green and red points
gp = deque(maxlen=10)
rp = deque(maxlen=10)

# Define HSV color ranges for green and red
g_min_hsv = np.array([37, 38, 24])
g_max_hsv = np.array([99, 255, 255])

# Adjusted HSV color ranges for detecting red
r_min_hsv = np.array([0, 100, 100])
r_max_hsv = np.array([10, 255, 255])

# Define area thresholds for detection
g_area_thresh = 300
r_area_thresh = 300

# Global variable to control the detection loop
detection_running = True

# Create a window to display the camera feed
cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)

# Function to start color detection
def start_detection():
    global detection_running

    try:
        while detection_running:
            frame = vs.read()
            frame = imutils.resize(frame, width=300)

            green_center, green_radius, green_area = detect_color(frame, g_min_hsv, g_max_hsv, (0, 255, 0), g_area_thresh)
            red_center, red_radius, red_area = detect_color(frame, r_min_hsv, r_max_hsv, (0, 0, 255), r_area_thresh)

            # Display the camera feed in the window
            cv2.imshow("Camera Feed", frame)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break

            # Determine the farther object based on area
            if green_area is not None and red_area is not None:
                if green_area > red_area:
                    print("Farther Object: Green")
                else:
                    print("Farther Object: Red")
            elif green_area is not None:
                print("Farther Object: Green")
            elif red_area is not None:
                print("Farther Object: Red")

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
    max_area = None

    # Process contours
    for contour in contours:
        max_area_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(max_area_contour)
        m = cv2.moments(max_area_contour)
        center = (int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"]))

        if radius > 10 and cv2.contourArea(max_area_contour) > area_thresh:
            cv2.circle(frame, (int(x), int(y)), int(radius), color, 2)
            cv2.circle(frame, center, 5, (0, 255, 255), -1)

            if color == (0, 255, 0):
                gp.appendleft(center)
            elif color == (0, 0, 255):
                rp.appendleft(center)

            last_center = center
            last_radius = radius
            max_area = cv2.contourArea(max_area_contour)

    return last_center, last_radius, max_area

# Start the color detection loop
start_detection()

