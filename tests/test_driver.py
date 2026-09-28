from src.dispatch.driver import Driver
from src.dispatch.vehicle import Vehicle, VEHICLE_TYPES

class TestDriver:
    def test_init(self):
        vehicle = Vehicle(VEHICLE_TYPES.BIKE, 200, 200)
        driver = Driver(vehicle)
        assert driver is not None