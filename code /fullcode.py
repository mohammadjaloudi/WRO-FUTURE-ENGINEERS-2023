import cv2
import numpy as np
import serial
import imutils
import time
from gpiozero import Button
from imutils.video import VideoStream
from collections import deque
from gpiozero import Motor

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

# Initialize motor control
motor = Motor(forward=12, backward=13)  # Adjust GPIO pins as needed

# Global variable to control the detection loop
detection_running = False

# Global variable to count rounds
round_counter = 0
max_rounds = 3  # Set the desired number of rounds

# Flag to indicate whether the robot is currently turning
turning = False

# Function to start color detection and motor movement
def start_detection():
    global detection_running, round_counter, turning
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

            # Check if a round has been completed
            if turning and round_counter < max_rounds:
                if not (green_center or red_center):
                    # No color detected, stop turning
                    turning = False
            elif round_counter >= max_rounds:
                stop_robot()  # Stop the robot if the desired rounds are completed

    except KeyboardInterrupt:
        pass

    vs.stop()
    ser.close()  # Close the serial connection
    motor.stop()  # Stop the motor
    cv2.destroyAllWindows()
    detection_running = False

# Function to detect green color
def detect_green(frame):
    # ... (rest of the code remains the same)

    if last_g_radius is not None:
        ser.write(b'L')  # Send 'L' to Arduino for left
        motor.forward()  # Start moving forward
        print("Start turn left from the center point:", last_g_center, "Color: green")
        turning = True

    return last_g_center, last_g_radius

# Function to detect red color
def detect_red(frame):
    # ... (rest of the code remains the same)

    if last_r_radius is not None:
        ser.write(b'R')  # Send 'R' to Arduino for right
        motor.forward()  # Start moving forward
        print("Start turn right from the center point:", last_r_center, "Color: red")
        turning = True

    return last_r_center, last_r_radius

# Function to stop the robot
def stop_robot():
    global round_counter
    round_counter += 1
    motor.stop()  # Stop the motor
    print("Round", round_counter, "completed")

# Callback function to start/stop color detection and motor movement when the button is pressed
def button_pressed():
    global detection_running, round_counter, turning
    if detection_running:
        detection_running = False
        motor.stop()  # Stop the motor when detection is stopped
        turning = False
    else:
        round_counter = 0  # Reset the round counter
        start_detection()

# Bind the button press event to the callback function
button.when_pressed = button_pressed

# Start the color detection loop
start_detection()
