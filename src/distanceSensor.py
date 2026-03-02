import MTECH_GPIO as GPIO
import time

class DistanceSensor:
    def __init__(self, trigPin: int, echoPin: int) -> None:
        # import threading

        self.trigPin: int = trigPin
        self.echoPin: int = echoPin
        self.maxRange: float = 4

        if GPIO._mode != GPIO.BCM:
            GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.trigPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)

    def __del__(self) -> None:
        GPIO.output(self.trigPin, 0)
        GPIO.cleanup()

    def getDistance(self) -> float | bool:
        # GPIO.output(self.trigPin, 0)
        # time.sleep(1e-5)
        GPIO.output(self.trigPin, 1)
        time.sleep(10e-6)
        GPIO.output(self.trigPin, 0)

        while GPIO.input(self.echoPin) == 0:
            pass
        startTime = time.time()
        while GPIO.input(self.echoPin) == 1:
            pass

        distMeters = ((time.time() - startTime) * 343) / 2

        if distMeters >= self.maxRange:
            return False

        return float(f"{distMeters:.4f}")