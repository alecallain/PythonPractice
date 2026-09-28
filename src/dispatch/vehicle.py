from dataclasses import dataclass
from enum import Enum

from src.dispatch.orderState import DeliveryOrder


class VEHICLE_TYPES(Enum):
    BIKE = 1
    CAR = 2
    VAN = 3

@dataclass
class Vehicle:
    vehicle_type: VEHICLE_TYPES
    max_weight: int
    max_volume: int

    def __post_init__(self):
        if not isinstance(self.vehicle_type, VEHICLE_TYPES):
            raise TypeError(f"Vehicle type must be {VEHICLE_TYPES}")
        if self.max_weight <= 0:
            raise ValueError("max_weight must be greater than 0.")
        if self.max_volume <= 0:
            raise ValueError("max_volume must be greater than 0.")

    def can_carry(self, order: DeliveryOrder):
        if order.weight > self.max_weight or order.volume > self.max_volume:
            return False
        return True

