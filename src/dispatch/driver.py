from src.dispatch.orderState import DeliveryOrder
from src.dispatch.vehicle import Vehicle

class Driver:
    def __init__(self, vehicle : Vehicle, order : DeliveryOrder | None = None, is_available: bool = True):
        self.vehicle = vehicle
        self.order = order
        self.is_available = is_available

    def toggle_availability(self):
        self.is_available = not self.is_available

    def assign_order(self, order : DeliveryOrder):
        self.order = order

    def assigned_order(self):
        return self.order

    def clear_order(self):
        self.order = None
