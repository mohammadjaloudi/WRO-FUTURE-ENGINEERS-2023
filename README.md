﻿# WRO-FUTURE-ENGINEERS-2023
Engineering materials
====
This repository contains engineering materials of a self-driven vehicle's model participating in the WRO Future Engineers competition in the season 2023.

## Content

* `t-photos` contains 2 photos of our participants in the team (an official one and one funny photo with all team members)
* `v-photos` contains 6 photos of the vehicle (from every side, from top and bottom)
* `video` contains the video.md file with the link to a video where driving demonstration exists
* `schemes` contains several schematic diagrams in form of JPEG of the electromechanical components illustrating all the elements (electronic components and motors) used in the vehicle and how they connect to each other.
* `code` contains code of control software for all components which were programmed to participate in the competition
* `Others` is for other talks which can be used to understand how to prepare the vehicle for the competition. It may include documentation how to connect to a
SBC/SBM and upload files there, datasets, hardware specifications, communication protocols descriptions etc.


## Introduction
I'll start with cameras code.
for the camera code we used cv2, numpy, imutils, time, gpiozero, imutils.video and collections libraries
we used cv2 or openCV libbrary for Initializing the Camera (VideoStream): The code uses the VideoStream class from imutils.video to initialize and capture video frames from a camera. The VideoStream class relies on OpenCV (cv2) for capturing and managing video streams.

vs = VideoStream(src=0).start()

Image Processing (e.g., Blurring, Color Space Conversion): OpenCV (cv2) provides a wide range of image processing functions, including Gaussian blur and color space conversion. In the code, cv2.GaussianBlur() is used to apply Gaussian blur to the captured video frames, and cv2.cvtColor() is used to convert the frames from BGR color space to HSV color space.

bf = cv2.GaussianBlur(frame, (11, 11), 0)
hsv_frame = cv2.cvtColor(bf, cv2.COLOR_BGR2HSV)

Masking and Morphological Operations: The code performs color-based object detection using masks and morphological operations. OpenCV (cv2) is used for creating masks with cv2.inRange(), as well as performing morphological operations like opening with cv2.morphologyEx().

g_mask = cv2.inRange(hsv_frame, g_min_hsv, g_max_hsv)
g_mask = cv2.morphologyEx(g_mask, cv2.MORPH_OPEN, k)

Contour Detection: OpenCV's cv2.findContours() function is used to find contours in the binary masks, which helps identify objects in the video frames.

g_contours = cv2.findContours(g_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
g_contours = imutils.grab_contours(g_contours)

Drawing and Visualization: OpenCV (cv2) is used to draw circles and contours on the video frames for visualization purposes. For example, it draws green and red circles around detected objects.

cv2.circle(frame, (int(gx), int(gy)), int(g_radius), (0, 255, 0), 2)
cv2.circle(frame, g_center, 5, (0, 255, 255), -1)

Window Management: OpenCV (cv2) is used for displaying the video frames in windows (cv2.imshow()) and managing user input (e.g., waiting for a key press to exit the program).

cv2.imshow('Original Image', image)

we used numpy library Array Manipulation: NumPy provides powerful array manipulation capabilities. In this code, it's used for creating and manipulating arrays to perform operations like creating the kernel for morphological operations (k = np.ones((5, 5), np.uint8)) and working with HSV color ranges (g_min_hsv, g_max_hsv, r_min_hsv, r_max_hsv).

Mathematical Operations: NumPy offers a wide range of mathematical functions that can be applied to arrays. In computer vision and image processing tasks, you often need to perform mathematical operations on pixel values, and NumPy simplifies this process. In this code, it's used for tasks like calculating the mean of coordinates (g_center and r_center) and performing array comparisons and thresholding.

Efficiency: NumPy is highly efficient for numerical and array operations. It's designed to perform operations on large datasets with speed. In image processing, where you're dealing with pixel values and performing various operations on them, efficiency is crucial. NumPy allows for vectorized operations, which can be significantly faster than using plain Python lists.

Integration with OpenCV: OpenCV, a popular computer vision library, often works seamlessly with NumPy arrays. Many OpenCV functions return NumPy arrays, and you can use NumPy to manipulate the data and perform further operations.

For instance, in this code, NumPy is used to create masks for green and red color ranges (g_mask and r_mask), apply morphological operations on these masks, and handle the coordinates and radii of detected objects. It simplifies the code and makes it more efficient for image processing tasks.

we used imutils for Video Stream Handling: The imutils.video module is used to handle video streams from a camera. Specifically, the VideoStream class from imutils.video is employed to initialize and start the video stream.

from imutils.video import VideoStream

# Initialize the camera using multithreading
vs = VideoStream(src=0).start()

This simplifies camera initialization and allows for easy multithreading when capturing frames.

Resizing Frames: The imutils.resize() function is used to resize video frames to a specific width. This resizing can help reduce the computational load when processing frames, and it's often used to standardize the frame size.

frame = imutils.resize(frame, width=300)

Contour Handling: The imutils.grab_contours() function is used to extract contours from masks generated by OpenCV. It simplifies the process of obtaining contours from the results of cv2.findContours(). This can make the code more concise and readable.

g_contours = cv2.findContours(g_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
g_contours = imutils.grab_contours(g_contours)

Other Utilities: imutils provides other utility functions and convenience functions for tasks like rotation, translation, and displaying images. While not explicitly used in this code, these utilities can be handy for various computer vision tasks.

we used time library for Delaying Execution: The time.sleep() function is used to introduce a delay or pause in the execution of the code. In this specific case, it's used to delay the start of the camera stream by 2 seconds.
import time

# Delay the camera stream start by 2 seconds
time.sleep(2.0)

This delay allows time for the camera to initialize properly before capturing frames.

Measuring Elapsed Time: Although not explicitly shown in the provided code, the time module can be used to measure the elapsed time during certain operations. For example, you could use time.time() to record a timestamp before and after a particular code block and calculate the time it took to execute that block.

import time

start_time = time.time()

# Code block to be timed
# ...

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")

This can be useful for performance profiling and optimizing specific parts of your code.

we used gpiozero for Button Handling: The primary usage of gpiozero in this code is for handling a button press. The Button class from gpiozero is used to create a button object, which can be connected to a physical button connected to a GPIO pin on the Raspberry Pi.

from gpiozero import Button

# Create a button object and specify the GPIO pin where the button is connected
button = Button(17)  # Replace 17 with the actual GPIO pin number

This code initializes a button object connected to GPIO pin 17.

Button Press Callback: A callback function is defined, which is executed when the button is pressed. The Button object from gpiozero allows you to specify a callback function to be called when the button state changes (e.g., when it's pressed).

# Callback function to start/stop color detection when the button is pressed
def button_pressed():
    global detection_running
    if detection_running:
        detection_running = False
    else:
        start_detection()

# Bind the button press event to the callback function
button.when_pressed = button_pressed

In this code, when the button is pressed (button.when_pressed), the button_pressed function is called. This function toggles the detection_running variable, effectively starting or stopping the color detection process.

GPIO Pin Configuration: The gpiozero library abstracts the low-level GPIO pin management, making it easier to work with GPIO pins. It allows you to specify the pin number, set pull-up or pull-down resistors, and easily handle events like button presses.

we used collections livrary for Deque for Tracked Points: Two instances of the deque class from the collections module are created to store tracked points - one for green points (gp) and another for red points (rp).

from collections import deque

# Create deques to store tracked pillar points
gp = deque(maxlen=10)
rp = deque(maxlen=100)

Deques are useful for efficiently maintaining a fixed-size collection of items. In this case, they are used to store the coordinates of tracked green and red points. The use of maxlen ensures that the deque will only retain the specified number of most recent points, discarding older ones when new points are added.


Appending Tracked Points: In the color detection functions (detect_green and detect_red), tracked points (centers of detected objects) are appended to the respective deques. This allows for storing a history of tracked points.

gp.appendleft(g_center)  # Append the green center to the deque
rp.appendleft(r_center)  # Append the red center to the deque


By keeping track of recent points, you can perform various tasks, such as calculating the average position, tracking movement, or visualizing the history of detected points.

now Ill explain servo motor code;

we used RPi.GPIO for GPIO.setmode(GPIO.BCM): This line sets the GPIO pin numbering mode to Broadcom SOC channel numbers. The Raspberry Pi supports two pin numbering modes: BCM (Broadcom SOC channel) and BOARD (physical pin numbers). GPIO.BCM is often used for consistency and because it maps to the GPIO pin numbers as labeled on the Raspberry Pi board.

GPIO pin setup and control functions: Throughout the code, you see functions like GPIO.setup(), GPIO.output(), and GPIO.input(). These functions are used to configure GPIO pins, set their states (high or low), and read their states, respectively.

PWM control: The RPi.GPIO library is used for PWM control of the servo motor. You can see this in the lines where the servo is initialized using GPIO.PWM() and where the servo's duty cycle is adjusted with servo.ChangeDutyCycle().

GPIO cleanup: At the end of the program, GPIO.cleanup() is called to release and clean up any resources associated with GPIO pins. This step is essential to ensure that the GPIO pins are left in a safe state.

we used time library for Delaying Execution: The time.sleep(seconds) function is used to introduce delays or pauses in the execution of your code. This is useful for scenarios where you need to wait for a specific duration, such as allowing hardware to initialize or creating time intervals between actions. For example:

Measuring Time: The time.time() function is used to measure the current time in seconds since the epoch (a predefined point in time, usually the beginning of the year 1970). You can use this function to record timestamps before and after specific code blocks to measure the elapsed time, which is helpful for performance profiling and benchmarking. 

start_time = time.time()
# Code block to be timed
end_time = time.time()
elapsed_time = end_time - start_time


you can see examples of both delaying execution (e.g., time.sleep(0.5)) and measuring time (e.g., recording timestamps before and after measuring ultrasonic sensor distances).

now it's time for unltrasonic sensors:

we used RPi.GPIO for GPIO Pin Control: The Raspberry Pi has GPIO (General Purpose Input/Output) pins that can be used to interact with various hardware components, including sensors, motors, LEDs, and more. The RPi.GPIO library allows you to control and interact with these GPIO pins from your Python code. In this code, it's used to configure the trigger and echo pins of the ultrasonic sensor as outputs and inputs, respectively.

Pulse Generation: To trigger the ultrasonic sensor and measure the distance, the code needs to generate precise short pulses on the trigger pin. The GPIO.output() function from RPi.GPIO is used to set the trigger pin to high for a brief moment and then back to low, creating the required pulse.

Reading Echo Signal: The ultrasonic sensor responds by sending an echo signal, which is received by the Raspberry Pi through the echo pin. RPi.GPIO is used to monitor the state of the echo pin and measure the duration of the echo pulse accurately.

Cleanup: Properly cleaning up GPIO pins is essential when your program exits, whether it exits normally or due to an interruption (e.g., Ctrl+C). The GPIO.cleanup() function from RPi.GPIO ensures that GPIO pins are released and reset to their default states when the program finishes, preventing any potential conflicts or issues with other GPIO-based applications or scripts.

we used time library for Delays and Timing: The time.sleep(seconds) function is used to introduce delays in the code. It pauses the execution of the program for the specified number of seconds. This is commonly used to control the timing of actions, such as waiting for a sensor to stabilize, controlling the rate of measurements, or creating timed intervals between actions.

time.sleep(0.1)  # Introduces a 100 ms (0.1 seconds) delay


Measuring Time Duration: The time.time() function is used to measure the elapsed time between events. It returns the current time in seconds since the "epoch" (a reference point in time, typically the system's startup time). By recording timestamps before and after specific actions, you can calculate the duration of those actions.

start_time = time.time()

# Perform some actions here

end_time = time.time()
elapsed_time = end_time - start_time


Timestamps: You can use time.time() or time.ctime() to obtain timestamps for events or log entries. Timestamps are useful for recording when events occurred.

timestamp = time.ctime()
print(f"Event occurred at: {timestamp}")
