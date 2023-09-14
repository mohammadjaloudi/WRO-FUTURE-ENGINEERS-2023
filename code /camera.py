#this code is for camera and turning left or right when seiong block


import cv2
import numpy as np
import serial
import imutils
import time
from gpiozero import Button
from imutils.video import VideoStream
from collections import deque

# Initialize the camera using multithreading
vs = VideoStream(src=0).start()  # Use src=0 for the default camera (you can change this)
time.sleep(2.0)

# Define a kernel for morphological operations
k = np.ones((5, 5), np.uint8)

# Create deques to store tracked pillar points
gp = deque(maxlen=10)
rp = deque(maxlen=100)

# Define HSV color ranges for green and red
g_min_hsv = np.array([37, 38, 24])
g_max_hsv = np.array([99, 255, 255])

# Adjusted HSV color ranges for darker and less lenient red
r_min_hsv = np.array([0, 100, 100])
r_max_hsv = np.array([10, 255, 255])

# Define area thresholds for detection
g_area_thresh = 300
r_area_thresh = 300

# Initialize serial connection to Arduino (change the port as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Use the correct serial port

# Create a button object and specify the GPIO pin where the button is connected
button = Button(17)  # Replace 17 with the actual GPIO pin number

# Global variable to control the detection loop
detection_running = False

# Function to start color detection
def start_detection():
    global detection_running
    detection_running = True

    try:
        while detection_running:
            frame = vs.read()
            frame = imutils.resize(frame, width=300)

            green_center, green_radius = detect_green(frame)
            red_center, red_radius = detect_red(frame)

            key = cv2.waitKey(1)
            if key == ord("q"):
                break

    except KeyboardInterrupt:
        pass

    vs.stop()
    ser.close()  # Close the serial connection
    cv2.destroyAllWindows()
    detection_running = False

# Function to detect green color
def detect_green(frame):
    # Apply Gaussian blur and convert to HSV color space
    bf = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv_frame = cv2.cvtColor(bf, cv2.COLOR_BGR2HSV)

    # Green Mask
    g_mask = cv2.inRange(hsv_frame, g_min_hsv, g_max_hsv)
    g_mask = cv2.morphologyEx(g_mask, cv2.MORPH_OPEN, k)

    # Find contours in masks
    g_contours = cv2.findContours(g_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    g_contours = imutils.grab_contours(g_contours)

    last_g_center = None
    last_g_radius = None

    # Process green contours
    for g_contour in g_contours:
        max_area_contour = max(g_contours, key=cv2.contourArea)
        ((gx, gy), g_radius) = cv2.minEnclosingCircle(max_area_contour)
        gm = cv2.moments(max_area_contour)
        g_center = (int(gm["m10"] / gm["m00"]), int(gm["m01"] / gm["m00"]))

        if g_radius > 10:
            cv2.circle(frame, (int(gx), int(gy)), int(g_radius), (0, 255, 0), 2)
            cv2.circle(frame, g_center, 5, (0, 255, 255), -1)

            gp.appendleft(g_center)
            last_g_center = g_center
            last_g_radius = g_radius

    if last_g_radius is not None:
        ser.write(b'L')  # Send 'L' to Arduino for left
        print("Start turn left from the center point:", last_g_center, "Color: green")

    return last_g_center, last_g_radius

# Function to detect red color
def detect_red(frame):
    # Apply Gaussian blur and convert to HSV color space
    bf = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv_frame = cv2.cvtColor(bf, cv2.COLOR_BGR2HSV)

    # Red Mask (adjusted for darker and less lenient red)
    r_mask = cv2.inRange(hsv_frame, r_min_hsv, r_max_hsv)
    r_mask = cv2.morphologyEx(r_mask, cv2.MORPH_OPEN, k)

    # Find contours in masks
    r_contours = cv2.findContours(r_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    r_contours = imutils.grab_contours(r_contours)

    last_r_center = None
    last_r_radius = None

    # Process red contours
    for r_contour in r_contours:
        max_area_contour = max(r_contours, key=cv2.contourArea)
        ((rx, ry), r_radius) = cv2.minEnclosingCircle(max_area_contour)
        rm = cv2.moments(max_area_contour)
        r_center = (int(rm["m10"] / rm["m00"]), int(rm["m01"] / rm["m00"]))

        if r_radius > 10:
            cv2.circle(frame, (int(rx), int(ry)), int(r_radius), (0, 0, 255), 2)
            cv2.circle(frame, r_center, 5, (0, 255, 255), -1)

            rp.appendleft(r_center)
            last_r_center = r_center
            last_r_radius = r_radius

    if last_r_radius is not None:
        ser.write(b'R')  # Send 'R' to Arduino for right
        print("Start turn right from the center point:", last_r_center, "Color: red")

    return last_r_center, last_r_radius

# Callback function to start/stop color detection when the button is pressed
def button_pressed():
    global detection_running
    if detection_running:
        detection_running = False
    else:
        start_detection()

# Bind the button press event to the callback function
button.when_pressed = button_pressed

# Start the color detection loop
start_detection()
