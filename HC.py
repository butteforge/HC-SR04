import MTECH_GPIO as GPIO
import time
import numpy as numpy

repeat = True

trig = 20
echo = 21
beeperPin = 16

pingTime = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(beeperPin, GPIO.OUT)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

# .02m - 4m -> 150hz - 2000hz

avg = [5]

try:
    GPIO.pwm_start(beeperPin, 1, 50)
    while repeat:
        GPIO.output(trig, 0)
        time.sleep(2E-6)
        GPIO.output(trig, 1)
        time.sleep(10E-6)
        GPIO.output(trig, 0)
        while GPIO.input(echo) == 0:
            pass
        echoStartTime = time.time()
        while GPIO.input(echo) == 1:
            pass
        echoStopTime = time.time()
        pingDist = (echoStopTime-echoStartTime) * 343 / 2
        
        distToFreq = 150 + (pingDist / 4) * (2000 - 150) # lerp from .02-4m into 150-2000hz
        GPIO.pwm_change_frequency(beeperPin, distToFreq)

        # if (pingDist < 0.3): 
        #     GPIO.pwm_change_frequency(beeperPin, 300)
        # else:
        #     GPIO.pwm_change_frequency(beeperPin, 1)
        
        print(f"Meters: ", pingDist)
        time.sleep(0.2)
    GPIO.pwm_stop(beeperPin)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting")
