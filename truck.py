from dataclasses import dataclass, field
from typing import List, Tuple
from enum import Enum, auto
from deliveryqueue import *
from distances import *
from package import *
from packagehash import *


class State(Enum):
    AWAITING_DISPATCH = auto()
    READY_TO_DELIVER_NEXT = auto()
    EN_ROUTE = auto()
    ARRIVED_AT_LOCATION = auto()
    RETURNING_TO_HUB = auto()
    END_OF_DAY = auto()

@dataclass
class Truck:
    distances: Distances = field(repr=False)
    packageHash: PackageHash = field(repr=False)
    id: int
    this_package: Package = field(default=None)
    delivery_list: List[Tuple] = field(default_factory=list)
    # package_list: List[Package] = field(default_factory=list)
    state: State = field(default=State.AWAITING_DISPATCH)
    speed: float = 18.0/60.0
    time_elapsed: int = 0
    previous_location: int = 1      # remember that locations are indexed by 1, not 0
    next_location: int = 1
    total_distance: float = 0.0
    next_distance: float = 0.0
    current_distance: float = 0.0
    
    def print_summary(self):
        print("Truck number: " + str(self.id))
        print("Total Distance traveled: ", self.total_distance, " miles")
        print("\n")

    def set_new_destination(self, target: int):
        self.next_location = target
    
    def load_packages(self, package_manifest):
        self.delivery_list = package_manifest

        self.delivery_list.set_all_status_to_on_delivery()
        self.delivery_list.set_all_trucks(self.id)
        
        print("\tLoading truck",self.id,"with following manifest:\n")
        self.delivery_list.display_contents()
    
        if len(self.delivery_list) > 0:
            print("\tafter sorting truck with nearest neighbor algorithm:\n")
            self.delivery_list.sort_nearest_neighbor(self.distances)
            self.delivery_list.display_contents()
            temp_package = self.delivery_list.pop()
            # self.this_package = self.package_list[int(temp_package[0])-1]
            # print("Loading",temp_package,"into truck",self.id)
            self.this_package = self.packageHash.get(temp_package[0])
            self.state = State.READY_TO_DELIVER_NEXT


    def get_state(self):
        return self.state
    
    def finished_for_day(self):
        self.state = State.END_OF_DAY

    def print_status(self):
        print("\t\t--- Status Update: Truck",self.id)

        if len(self.delivery_list) > 0:
            print("\t\t--- truck has the following packages loaded: ")
            self.delivery_list.display_contents_status()

        print("\t\t------ truck is currently")
        if self.state == State.ARRIVED_AT_LOCATION:
            print("\t\t------ on location at",self.this_package.location)
        
        if self.state == State.AWAITING_DISPATCH:
            print("\t\t------ awaiting dispatch")
        
        if self.state == State.EN_ROUTE:
            print("\t\t------ en route from location",self.previous_location,"to location",self.next_location)
            print("\t\t-------- and has traveled",round(self.current_distance,2),"out of",self.next_distance,"miles")
        
        if self.state == State.END_OF_DAY:
            print("\t\t------ in end of day status")
        
        if self.state == State.READY_TO_DELIVER_NEXT:
            print("\t\t------ at location",self.previous_location,"ready to deliver to location",self.next_location)
        
        if self.state == State.RETURNING_TO_HUB:
            print("\t\t------ returning to Hub",round(self.current_distance,2),"out of",self.next_distance,"miles.")
        print("\n")


    def tick(self, time_string):
        if self.state != State.END_OF_DAY:

            # truck is awaiting dispatch

            if self.state == State.AWAITING_DISPATCH:
                print("Truck awaiting dispatch")
                pass

            # packages delivered, truck is returning to hub

            if self.state == State.RETURNING_TO_HUB:
                self.current_distance += self.speed
                if self.current_distance >= self.next_distance:
                    self.current_distance = self.next_distance
                    self.total_distance += self.current_distance
                    self.total_distance = round(self.total_distance, 2)
                    print("Truck",self.id,"has returned to Hub.")
                    print("Truck",self.id,"has traveled a total of",self.total_distance,"miles")
                    self.previous_location = 1
                    self.next_location = 1
                    self.state = State.AWAITING_DISPATCH
        
            # truck is ready to check for next package

            if self.state == State.READY_TO_DELIVER_NEXT:
                print("Truck", self.id,"ready to deliver package " +
                       self.this_package.package_id,"to location", self.this_package.location)
                self.previous_location = self.next_location
                self.next_location = self.this_package.location
                self.next_distance = self.distances.distance(self.previous_location, self.next_location)
                self.current_distance = 0
                self.state = State.EN_ROUTE

            if self.state == State.EN_ROUTE:
                self.current_distance += self.speed
                if self.current_distance >= self.next_distance:
                    self.current_distance = self.next_distance
                    self.total_distance += self.current_distance
                    self.total_distance = round(self.total_distance, 2)
                    self.state = State.ARRIVED_AT_LOCATION

            # truck has arrived at the location and needs to deliver package(s)

            if self.state == State.ARRIVED_AT_LOCATION:
                self.packageHash.set_time_delivered( self.this_package.package_id, time_string )
                print("Truck",self.id,"has delivered package", self.this_package.package_id + 
                      " to location", self.this_package.location)
                print("Truck", self.id, "has traveled", self.current_distance,"miles")
                print("  for a total distance of", self.total_distance,"miles")
                if len(self.delivery_list) > 0:
                    temp_package = self.delivery_list.pop()
                    # print(temp_package)
                    # self.this_package = self.package_list[int(temp_package[0])-1]
                    self.this_package = self.packageHash.get(temp_package[0])
                    self.state = State.READY_TO_DELIVER_NEXT
                else:
                    print("Truck",self.id,"is now returning to Hub.")
                    self.previous_location = self.next_location
                    self.next_location = 1
                    self.next_distance = self.distances.distance(self.previous_location, self.next_location)
                    self.current_distance = 0
                    self.state = State.RETURNING_TO_HUB

        self.time_elapsed += 1
