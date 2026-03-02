import MTECH_GPIO as GPIO
import time
from distanceSensor import DistanceSensor


def main():

    try:
        trigPin: int = 21
        echoPin: int = 20

        distance: DistanceSensor = DistanceSensor(trigPin, echoPin)
        repeat: bool = True

        while repeat:
            currentDistance = distance.getDistance()
            if currentDistance:
                print(currentDistance)

            time.sleep(.01)

    except KeyboardInterrupt:
        pass

main()