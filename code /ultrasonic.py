import RPi.GPIO as GPIO
import time

# Set GPIO mode (BCM mode)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for the sensor
trig_pin = 18  # GPIO pin for the trigger
echo_pin = 24  # GPIO pin for the echo

# Set up GPIO pins
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

def measure_distance():
    # Ensure the trigger pin is low
    GPIO.output(trig_pin, GPIO.LOW)
    time.sleep(0.1)

    # Generate a short 10us pulse on the trigger pin to trigger the sensor
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)

    # Wait for the echo pin to go high (start of the pulse)
    while GPIO.input(echo_pin) == GPIO.LOW:
        pulse_start = time.time()

    # Wait for the echo pin to go low (end of the pulse)
    while GPIO.input(echo_pin) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate the duration of the pulse
    pulse_duration = pulse_end - pulse_start

    # Calculate the distance in centimeters (speed of sound is 34300 cm/s)
    distance = (pulse_duration * 34300) / 2

    return distance

try:
    while True:
        # Measure distance
        dist = measure_distance()

        # Print the distance
        print(f"Distance: {dist:.2f} cm")

        # Add a delay to control the measurement rate (e.g., 1 measurement per second)
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()  # Cleanup GPIO on Ctrl+C exit

# Cleanup GPIO on program exit
GPIO.cleanup()
