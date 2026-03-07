import MTECH_GPIO as GPIO
import time
import statistics


class HC_SR04:
    speedOfSound = 343 # this is in meters/second
    def __init__(self, triggerPin:int, echoPin:int, unit = 0): #create a list of ints that can be used to label units, unit = 0 is cm
        self.echoPin = echoPin
        self.triggerPin = triggerPin
        GPIO.setup(self.echoPin, GPIO.IN) 
        GPIO.setup(self.triggerPin, GPIO.OUT) 
        self.buffer = []
        self.units = {
            0: ("cm", 100), 
            1: ("m", 1), 
            2: ("in", 39.3701), 
            3: ("ft", 3.28084)
            }

        self.unit = unit
    
    def getDistance(self):
        # Output on high for 10E-6 seconds
        GPIO.output(self.triggerPin, False)
        time.sleep(2E-6)
        GPIO.output(self.triggerPin, True)
        time.sleep(10E-6)
        GPIO.output(self.triggerPin, False)

        # Wait for echo to go HIGH
        start_wait = time.perf_counter()
        while GPIO.input(self.echoPin) == 0:
            # replace 0.1 with 2 * 4meters *speed of sound
            if time.perf_counter() - start_wait > 0.03:
                print("\nNo echo received")
                return None

        start = time.perf_counter()

        # Wait for echo to go LOW
        while GPIO.input(self.echoPin) == 1:
            if time.perf_counter() - start > 0.03:
                #print("Out of range             ", end = "\r")
                return None

        stop = time.perf_counter()

        travelTime = stop - start
        distance_m = (travelTime * speedOfSound) / 2
        distance = distance_m * self.units[self.unit][1] 

        # Add reading to buffer
        self.buffer.append(distance)

        # keep last 5 readings
        if len(self.buffer) > 3:
            self.buffer.pop(0)

        return statistics.median(self.buffer)

    def getDistanceFiltered(self, samples=5):
        readings = []

        for _ in range(samples):
            d = self.getDistance()

            if d is not None:
                readings.append(d)

            time.sleep(0.005)  # small delay between pings

        if not readings:
            return None

        return statistics.median(readings)

    def printDistance(self, distance):
        if (distance <= 400):
            unitLabel = self.units[self.unit][0]
            print(f"Travel Distance: {distance:.2f} {unitLabel}          ", end="\r")


GPIO.setmode(GPIO.BCM)
echoPin = 24
triggerPin = 23

sensor = HC_SR04(triggerPin, echoPin, 3)
try:
    while (True):
        distance = sensor.getDistanceFiltered()
        if (distance is not None and distance <= 400):
            sensor.printDistance(distance)

        time.sleep(0.002)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nGPIO cleanup successful")
