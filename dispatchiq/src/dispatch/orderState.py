from enum import Enum

class OrderState(Enum):
    CREATED = 1
    SEARCHING = 2
    ASSIGNED = 3
    PICKED_UP = 4
    IN_TRANSIT = 5
    DELIVERED = 6
    CANCELLED = 7

class DeliveryOrder:
    def __init__(self, order_state, pickup_addr, dropoff_addr, desc):
        self.order_state = order_state
        self.pickup_addr = pickup_addr
        self.dropoff_addr = dropoff_addr
        self.desc = desc

    def transition(self, new_state):
        if isinstance(new_state, OrderState):
            if ((self.order_state == OrderState.IN_TRANSIT or \
                  self.order_state == OrderState.DELIVERED) and \
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


if (__name__ == "__main__"):
    print("This script is being run directly.")