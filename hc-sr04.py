import MTECH_GPIO as GPIO
import time

# Pins and GPIO setup
inputPin = 24
outputPin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(inputPin, GPIO.IN) 
GPIO.setup(outputPin, GPIO.OUT) 

speedOfSound = 343 # this is in meteres/second


# Loop: getting distance from HC-SR04
try:
    while True:
        # Output on high for 10E-6 seconds
        GPIO.output(outputPin, False)
        time.sleep(2E-6)
        GPIO.output(outputPin, True)
        time.sleep(10E-6)
        GPIO.output(outputPin, False)

        # Wait for echo to go HIGH
        start_wait = time.time()
        while GPIO.input(inputPin) == 0:
            if time.time() - start_wait > 0.03:
                print("No echo received")
                break

        start = time.time()

        # Wait for echo to go LOW
        while GPIO.input(inputPin) == 1:
            if time.time() - start > 0.03:
                print("Out of range")
                break

        stop = time.time()

        travelTime = stop - start
        distance = (travelTime * speedOfSound / 2) * 100

        if distance <= 400:
            print(f"Travel Distance: {distance:.2f} cm")

        # Buffer
        time.sleep(0.2)
        lastDistance = distance
# Use Ctrl + C to end and cleanup
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nGPIO cleanup successful")