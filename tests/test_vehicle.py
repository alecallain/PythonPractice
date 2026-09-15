from src.dispatch.vehicle import Vehicle

class TestVehicle:
    def test_init(self):
        vehicle = Vehicle('Truck', 200, 200)
        assert vehicle is not None