from src.dispatch.driver import Driver
from src.dispatch.vehicle import Vehicle

class TestDriver:
    def test_init(self):
        vehicle = Vehicle('Truck', 200, 200)
        driver = Driver(vehicle)
        assert driver is not None