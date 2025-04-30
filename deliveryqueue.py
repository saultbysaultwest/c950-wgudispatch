# import heapq
from distances import *
from package import *
from packagehash import *

class DeliveryQueue:
    def __init__(self, name, packageHashTable):
        self.list = []
        self.has_delivered = False
        self.name = name
        self.packageHash = packageHashTable

    # Pushes a new tuple to the heap. Tuple is (package_id, location)
    def push(self, package_id, location):
        self.list.append((package_id, location))
        # heapq.heappush(self.heap, (package_id, location))

    # Pops the smallest item from the heap
    def pop(self):
        if self.list:
            return self.list.pop(0)
        else:
            return None

    # Returns the next item without removing it
    def peek(self):
        if self.list:
            return self.list[0]
        else:
            return None

    def __len__(self):
        return len(self.list)
    
    def display_contents(self):
        print("\t## ",self.name, "queue contains:")
        for item in self.list:
            print("\t# package ",item[0]," going to location ",item[1])
        print("\n")

    def display_contents_status(self):
        print("\n\t\t Status of Packages: ")
        for item in self.list:
            this_id = item[0]
            this_pkg = self.packageHash.get(this_id)
            this_status = this_pkg.get_status()
            print("\t\t## ",this_id,"\t",this_status)
        print("\n")
    
    def set_all_status_to_on_delivery(self):
        for item in self.list:
            this_pkg = self.packageHash.get(item[0])
            this_pkg.set_status(Status.ON_DELIVERY)
            self.packageHash.set(item[0], this_pkg)

    def set_all_trucks(self, id):
        for item in self.list:
            this_pkg = self.packageHash.get(item[0])
            this_pkg.set_truck_delivered(id)
            self.packageHash.set(item[0], this_pkg)

    def sort_nearest_neighbor(self, dist):
        # self.display_contents()
        sorted_queue = []
        current_location = (0, 1)
        # print(current_location[1])

        while self.list:
            next_location = min(self.list, key=lambda loc: dist.distance(current_location[1], loc[1]))
            sorted_queue.append(next_location)
            self.list.remove(next_location)
            current_location = next_location
        
        self.list = sorted_queue
        # self.display_contents()


