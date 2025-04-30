from dataclasses import dataclass, field
from enum import Enum, auto


class Status(Enum):
    AT_HUB = auto()
    ON_DELIVERY = auto()
    HAS_DELIVERED = auto()


@dataclass
class Package:
    package_id: str
    street_address: str
    city: str
    state: str
    zip_code: str
    delivery_available: int  # Time when package is available for delivery
    truck_required: int  # 0 if it doesn't matter
    delivery_deadline: int  # Time by which package must be delivered (e.g., 930 for 9:30 AM)
    weight_kg: float
    bundled: int  # 0 if it doesn't matter
    location: int
    status: Status = field(default=Status.AT_HUB)
    has_delivered: bool = field(default=False)
    time_delivered: str = field(default=None)
    truck_delivered: str = field(default=None)

    # def __init__(self):
    #    self.has_delivered = False
    #    self.time_delivered = None

    def set_has_delivered(self):
        self.has_delivered = True

    def get_has_delivered(self):
        return self.has_delivered

    def get_status(self):
        if (self.status == None):
            return "no status available"
        if (self.status == Status.AT_HUB):
            return "At Hub"
        if (self.status == Status.ON_DELIVERY):
            return "On Delivery"
        if (self.status == Status.HAS_DELIVERED):
            return "Has Delivered"

    def set_status(self, status):
        self.status = status

    def set_package_time_delivered(self, time):
        self.time_delivered = time
        self.set_status(Status.HAS_DELIVERED)

    def get_package_time_delivered(self):
        timestring = "None" if self.time_delivered is None else self.time_delivered 
        return self.time_delivered

    def set_truck_delivered(self, id):
        self.truck_delivered = id

    def get_truck_delivered(self):
        return self.truck_delivered