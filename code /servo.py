#this code is for servo motor using serial that come from arduino of ultrasonic sensors


import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for servo control and ultrasonic sensors
servo_pin = 17  # Use the appropriate GPIO pin
left_sensor_trigger = 18  # Use the GPIO pin for the left sensor's trigger
left_sensor_echo = 22  # Use the GPIO pin for the left sensor's echo
right_sensor_trigger = 23  # Use the GPIO pin for the right sensor's trigger
right_sensor_echo = 24  # Use the GPIO pin for the right sensor's echo
front_sensor_trigger = 25  # Use the GPIO pin for the front sensor's trigger
front_sensor_echo = 26  # Use the GPIO pin for the front sensor's echo

# Define GPIO pins for DC motor control
left_motor_pin1 = 5  # Left motor control pin 1
left_motor_pin2 = 6  # Left motor control pin 2
right_motor_pin1 = 13  # Right motor control pin 1
right_motor_pin2 = 19  # Right motor control pin 2

# Set up the servo
GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50)  # 50 Hz PWM frequency
servo.start(0)

# Set up the ultrasonic sensor pins
GPIO.setup(left_sensor_trigger, GPIO.OUT)
GPIO.setup(left_sensor_echo, GPIO.IN)
GPIO.setup(right_sensor_trigger, GPIO.OUT)
GPIO.setup(right_sensor_echo, GPIO.IN)
GPIO.setup(front_sensor_trigger, GPIO.OUT)
GPIO.setup(front_sensor_echo, GPIO.IN)

# Set up the DC motor control pins
GPIO.setup(left_motor_pin1, GPIO.OUT)
GPIO.setup(left_motor_pin2, GPIO.OUT)
GPIO.setup(right_motor_pin1, GPIO.OUT)
GPIO.setup(right_motor_pin2, GPIO.OUT)

# Initialize the car's direction
car_direction = "forward"

def measure_distance(trigger_pin, echo_pin):
    # Send a pulse on the trigger pin
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    # Measure the duration of the echo pulse
    pulse_start_time = time.time()
    pulse_end_time = time.time()
    
    while GPIO.input(echo_pin) == 0:
        pulse_start_time = time.time()
    
    while GPIO.input(echo_pin) == 1:
        pulse_end_time = time.time()
    
    pulse_duration = pulse_end_time - pulse_start_time

    # Calculate distance in centimeters (you can adjust the speed of sound as needed)
    speed_of_sound = 34300  # Speed of sound in cm/s
    distance = (pulse_duration * speed_of_sound) / 2

    return distance

def move_servo(angle):
    duty = (angle / 18) + 2  # Convert angle to duty cycle (adjust as needed)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Adjust delay as needed

def move_car(direction):
    # Implement logic to control DC motors here
    # Adjust motor control pins based on the desired direction
    if direction == "forward":
        GPIO.output(left_motor_pin1, GPIO.HIGH)
        GPIO.output(left_motor_pin2, GPIO.LOW)
        GPIO.output(right_motor_pin1, GPIO.HIGH)
        GPIO.output(right_motor_pin2, GPIO.LOW)
    elif direction == "right":
        GPIO.output(left_motor_pin1, GPIO.HIGH)
        GPIO.output(left_motor_pin2, GPIO.LOW)
        GPIO.output(right_motor_pin1, GPIO.LOW)
        GPIO.output(right_motor_pin2, GPIO.HIGH)
    # Add more cases for other directions (left, reverse, etc.)

try:
    while True:
        # Measure distances from the ultrasonic sensors
        left_distance = measure_distance(left_sensor_trigger, left_sensor_echo)
        right_distance = measure_distance(right_sensor_trigger, right_sensor_echo)
        front_distance = measure_distance(front_sensor_trigger, front_sensor_echo)

        # Check if an obstacle is detected in front or too close on the sides
        if left_distance < 80 and front_distance < 30:
            car_direction = "right"  # Turn right
        elif right_distance < 80 and front_distance < 30:
            car_direction = "left"  # Turn left
        else:
            car_direction = "forward"  # Keep moving forward

        # Move the servo according to the car's direction
        move_servo(90 if car_direction == "right" else 0 if car_direction == "left" else 45)

        # Move the car based on the car_direction
        move_car(car_direction)

except KeyboardInterrupt:
    pass

# Cleanup GPIO
servo.stop()
GPIO.cleanup()

# Cleanup GPIO and close serial connection
servo.stop()
GPIO.cleanup()
ser.close()
