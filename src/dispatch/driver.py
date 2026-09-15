class Driver:
    def __init__(self, vehicle, is_available: bool = False):
        self.vehicle = vehicle
        self.is_available = is_available

    def available(self):
        self.is_available = not self.is_available
