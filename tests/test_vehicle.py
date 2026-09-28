import pytest

from src.dispatch.vehicle import Vehicle, VEHICLE_TYPES

class TestVehicle:
    def test_init(self):
        vehicle = Vehicle(VEHICLE_TYPES.BIKE, 200, 200)
        assert vehicle is not None

    def test_max_weight(self):
        with pytest.raises(ValueError):
            Vehicle(VEHICLE_TYPES.BIKE, -1, 200)

    def test_max_volume(self):
        with pytest.raises(ValueError):
            Vehicle(VEHICLE_TYPES.BIKE, 200, -5)