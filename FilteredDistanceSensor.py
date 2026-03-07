from HC_SR04 import HC_SR04
from Unit import Unit

class FilteredDistanceSensor:
    def __init__(self, sensor: HC_SR04, mode='mean', unit = Unit.METER):
        self.sensor = sensor
        self.mode = mode
        self.unit = unit
        self.buffer = []

    def getFilteredDistance(self):
        val = self.sensor.getDistance(self.unit)
        
        # Add to buffer if valid
        if val != -1:
            self.buffer.append(val)
            if len(self.buffer) > 20:
                self.buffer.pop(0) # Keep only 20 latest

        # Logic based on mode
        if not self.buffer: return None
        
        if self.mode == 'raw':
            return self.buffer[-1]
        elif self.mode == 'mean':
            return sum(self.buffer) / len(self.buffer)
        elif self.mode == 'median':
            sorted_data = sorted(self.buffer)
            return sorted_data[len(sorted_data) // 2]