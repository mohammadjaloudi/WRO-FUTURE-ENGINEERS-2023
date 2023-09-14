#this code is for servo motor using serial that come from arduino of ultrasonic sensors


import RPi.GPIO as GPIO
import serial
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pin for servo control
servo_pin = 17  # Use the appropriate GPIO pin

# Set up the servo
GPIO.setup(servo_pin, GPIO.OUT)
servo = GPIO.PWM(servo_pin, 50)  # 50 Hz PWM frequency
servo.start(0)

# Set up serial communication with the Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Use the correct serial port

def move_servo(angle):
    duty = (angle / 18) + 2  # Convert angle to duty cycle (adjust as needed)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Adjust delay as needed

try:
    while True:
        # Read sensor data from Arduino
        arduino_data = ser.readline().decode().strip()
        if arduino_data:
            print("Arduino Data:", arduino_data)
            
            # Parse and process sensor data from Arduino here if needed

            # Control servo motor based on sensor data
            # Example: If sensor data indicates a turn, move the servo
            if "TurnRight" in arduino_data:
                move_servo(90)  # Adjust the angle as needed for your application
            elif "TurnLeft" in arduino_data:
                move_servo(0)   # Adjust the angle as needed for your application
            elif "MoveForward" in arduino_data:
                move_servo(45)  # Adjust the angle as needed for your application

except KeyboardInterrupt:
    pass

# Cleanup GPIO and close serial connection
servo.stop()
GPIO.cleanup()
ser.close()
