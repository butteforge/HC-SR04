import MTECH_GPIO as GPIO
import time

# Pins and GPIO setup
inputPin = 24
outputPin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(inputPin, GPIO.IN) 
GPIO.setup(outputPin, GPIO.OUT) 

# Loop: getting distance from HC-SR04
try:
    while True:
        # Output on high for 10E-6 seconds
        GPIO.output(outputPin, False)
        time.sleep(2E-6)
        GPIO.output(outputPin, True)
        time.sleep(10E-6)
        GPIO.output(outputPin, False)

        # Wait for signal
        while GPIO.input(inputPin) == 0:
            pass

        # Mark start of signal
        start = time.time()

        # Wait for signal end
        while GPIO.input(inputPin) == 1:
            pass

        # Mark end of signal
        stop = time.time()

        # Calculate and display travel time
        travelTime = stop - start
        print("Travel Time:", str(int(travelTime * 1E6)))

        # Buffer
        time.sleep(0.2)

# Use Ctrl + C to end and cleanup
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nGPIO cleanup successful")
