import MTECH_GPIO as GPIO
import numpy as numpy
from HC_SR04 import HC_SR04
from Unit import Unit
from FilteredDistanceSensor import FilteredDistanceSensor

repeat = True

trig = 20
echo = 21

pingTime = 0

GPIO.setmode(GPIO.BCM)

sensor = HC_SR04(echo, trig)
filterSensor = FilteredDistanceSensor(sensor, 'raw', Unit.METER)

try:
    while True:
        print(filterSensor.getFilteredDistance())
except KeyboardInterrupt:
    pass 
