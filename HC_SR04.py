from Unit import Unit
import time
import MTECH_GPIO as GPIO

class HC_SR04:
    def __init__(self, echo, trigger):
        self.echo = echo
        self.trigger = trigger
        self.initializeDevice()

    def initializeDevice(self):
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    # grabs the input with interrupting the program
    def getDistance(self, unit=Unit.METER):
        GPIO.output(self.trigger, 0)
        time.sleep(2E-6)
        GPIO.output(self.trigger, 1)
        time.sleep(10E-6)
        GPIO.output(self.trigger, 0)
        startTime = time.time_ns()
        while GPIO.input(self.echo) == 0:
            if (time.time_ns() - startTime > 23_400_000): # out of range for the sensor (4 / 343 * 10^9 * 2)
                return -1
        echoStartTime = time.time_ns()
        while GPIO.input(self.echo) == 1:
            if (time.time_ns() - echoStartTime > 23_400_000): # out of range for the sensor (4 / 343 * 10^9 * 2)
                return -1
        echoStopTime = time.time_ns()
        pingDist = ((echoStopTime-echoStartTime) / 1_000_000_000) * 343 / 2

        match unit:
            case Unit.CENTIMETER:
                return round(pingDist * 100, 4)
            case Unit.FEET:
                return round(pingDist * (3.048), 4)
            case Unit.INCH:
                return round(pingDist * (3.048 * 12), 4)
            case _:
                return round(pingDist, 4)

    
