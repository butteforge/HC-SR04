import time
import os
from collections import deque
import MTECH_GPIO as GPIO
import numpy as numpy
from HC_SR04 import HC_SR04
from Unit import Unit
from FilteredDistanceSensor import FilteredDistanceSensor

# -----------------------------
# Settings
# -----------------------------
MAX_DISTANCE = 250       # Maximum graph distance in cm
GRAPH_WIDTH = 180         # Number of horizontal columns
HISTORY_LENGTH = 80      # Number of measurements displayed
UPDATE_RATE = 0.1        # Seconds between measurements

history = deque(maxlen=HISTORY_LENGTH)

trig = 20
echo = 21

pingTime = 0

GPIO.setmode(GPIO.BCM)

sensor = HC_SR04(echo, trig)
filterSensor = FilteredDistanceSensor(sensor, 'raw', Unit.CENTIMETER)



# -----------------------------
# Draw terminal graph
# -----------------------------
def draw_graph():
    os.system("clear")

    print("HC-SR04 SONAR")
    print("=" * (GRAPH_WIDTH + 15))

    if not history:
        return

    # Draw newest measurement
    distance = history[-1]

    print(f"Distance: {distance:7.2f} cm")
    print()

    # Current distance as horizontal bar
    bar_length = int(
        (distance / MAX_DISTANCE) * GRAPH_WIDTH
    )

    bar_length = max(0, min(GRAPH_WIDTH, bar_length))

    print(
        "0 cm "
        + "#" * bar_length
        + " " * (GRAPH_WIDTH - bar_length)
        + f" {MAX_DISTANCE} cm"
    )

    print()
    print("Distance history:")
    print()

    # Draw vertical graph
    graph_height = 15

    # Create rows from top to bottom
    for row in range(graph_height, -1, -1):

        threshold = (row / graph_height) * MAX_DISTANCE

        line = ""

        # Y-axis label
        line += f"{threshold:5.0f} |"

        for distance in history:
            if distance >= threshold:
                line += "█"
            else:
                line += " "

        print(line)

    print("      +" + "-" * len(history))
    print("       oldest" + " " * max(0, len(history) - 15) + " newest")

    print()
    print("Press Ctrl+C to exit")

try:

    while True:

        distance = filterSensor.getFilteredDistance()

        # Ignore obviously invalid readings
        if distance is not None and 0 < distance <= MAX_DISTANCE:
            history.append(distance)

        draw_graph()

        time.sleep(UPDATE_RATE)

except KeyboardInterrupt:
    print("\n\nSonar stopped.")