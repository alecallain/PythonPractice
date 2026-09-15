from enum import Enum
import uuid

class OrderState(Enum):
    CREATED = 1
    SEARCHING = 2
    ASSIGNED = 3
    PICKED_UP = 4
    IN_TRANSIT = 5
    DELIVERED = 6
    CANCELLED = 7

class DeliveryOrder:
    BASE_FARE = 5.00
    DISTANCE_FARE = 1.50

    def __init__(self, pickup_address, ship_to_address, desc, price):
        self.id = str(uuid.uuid4())
        self.order_state = OrderState.CREATED
        self.pickup_address = pickup_address
        self.ship_to = ship_to_address
        self.desc = desc
        self.price = price

    def transition(self, new_state):
        if isinstance(new_state, OrderState):
            if ((self.order_state == OrderState.IN_TRANSIT or
                 self.order_state == OrderState.DELIVERED) and
                    new_state == OrderState.CANCELLED):
                raise ValueError("Invalid state transition from IN_TRANSIT or DELIVERED to CANCELLED.")
            else:
                self.order_state = new_state
        else:
            raise ValueError("Invalid state transition. Must be an instance of OrderState.")

    def cancel(self):
        if self.order_state in [OrderState.CREATED, OrderState.SEARCHING, OrderState.ASSIGNED]:
            self.order_state = OrderState.CANCELLED
        else:
            raise ValueError("Cannot cancel order in its current state.")

    def surge(self, amount):
        self.surge_price = amount

    @staticmethod
    def quote(pickup, ship_to_address, desc) -> int:
        return BASE_FARE + DISTANCE_FARE + surge_price


if (__name__ == "__main__"):
    print("This script is being run directly.")