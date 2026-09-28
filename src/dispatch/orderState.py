from dataclasses import dataclass, field
from decimal import Decimal
from typing import ClassVar
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

@dataclass
class DeliveryOrder:
    pickup_address: str
    ship_to_address: str
    desc: str
    price: Decimal
    weight: Decimal
    volume: Decimal
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    order_state: OrderState = OrderState.CREATED

    _BASE_FARE : ClassVar[Decimal] = Decimal(5)
    _DISTANCE_FARE : ClassVar[Decimal] = Decimal("1.50")

    def __post_init__(self):
        self.price = self.validate(self.price)
        self.weight = self.validate(self.weight)
        self.volume = self.validate(self.volume)

    def validate(self, item: str | int):
        match item:
            case int():
                try:
                    return Decimal(item)
                except Exception:
                    raise ValueError("Cannot convert item to Decimal from int.")
            case str():
                try:
                    return Decimal(item)
                except Exception:
                    raise ValueError("Cannot convert item to Decimal from str.")
            case Decimal():
                return item
            case _:
                raise ValueError("Item must be an int or str.")


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

    def surge(self, amount: Decimal):
        self.surge_price = amount

    @classmethod
    def quote(cls, surge_price: Decimal = Decimal(0)) -> Decimal:
        return cls._BASE_FARE + cls._DISTANCE_FARE + surge_price

if (__name__ == "__main__"):
    print("This script is being run directly.")