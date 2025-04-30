# 
# 

from typing import List
import datetime

from package import *           # this imports the Status class as well
from truck import *             # this imports the State class as well
from locations import *
from distances import *
from deliveryqueue import *
from queueofqueues import *
from hashtable import *
from packagehash import *
from kronos import *


print("WGU Dispatch by [redacted]")
print("Student ID: [redacted]")

# commandline interface where we either let the program run as normal
# or we accept a time of day that we halt execution at and print the status of
# all packages


def validate_time(time_str):
    try:
        new_time_str = time_str.replace("am", "").replace("pm", "").strip()
        valid_HHMM_time = datetime.datetime.strptime(new_time_str, '%H:%M').time()
        military_time = valid_HHMM_time.strftime('%H%M')
        if "pm" in time_str and int(military_time) < 1200:
            military_time = int(military_time) + 1200
        return military_time
    except ValueError:
        return None

def get_user_input():
    while True:
        user_input = input("Enter '1' to run normally, or a time (HH:MM) for status, or '2' to exit: ")
        if user_input == "1":
            return "run"
        elif user_input == '2':
            return "exit"
        elif validate_time(user_input) is not None:
            return validate_time(user_input)
        else:
            print("Invalid input. Please enter a valid time (HH:MM) or '1' or '2'.")

print("""
      Please enter '1' if you wish the program to run as normal \n
      Please enter a time in HH:MM format to pause program execution
      and print the status of all packages at that time
      If entering an afternoon time, please add pm or use military time. \n
      For example: "13:30" and "1:30 pm" will both indicate 1:30 in the afternoon.\n
      Please press '2' to exit program.
      """)

user_choice = get_user_input()

if user_choice == "run":
    pause_at_time = False
    time_to_pause = 9999
elif user_choice == "exit":
    print("Thank you for using this program!")
    exit()
else:
    pause_at_time = True
    time_to_pause = int(user_choice)
    print(f"Program will be halted at timecode {user_choice}\n")


# load the location data

locations = load_locations_from_csv('wgu-locations.csv')

print( locations )

# load the distance data and helper function

distances = Distances('wgu-distances.csv')


# load the packages

## packageList = load_packages_from_csv('wgu-packages.csv')

packageHashTable = PackageHash(301)
packageHashTable.load_from_csv('wgu-packages.csv')

packageList = packageHashTable.get_all_ids()


# we need to start by giving all packages a location


for i in packageList:
    package = packageHashTable.get(i)
    package.location = get_location_id_by_street_address(package.street_address, locations)
    packageHashTable.set(i, package)


# debug

packageHashTable.list_all_ids()


# Initialize the truck objects

truck1 = Truck(id=1, distances=distances, packageHash = packageHashTable)
truck2 = Truck(id=2, distances=distances, packageHash = packageHashTable)
truck3 = Truck(id=3, distances=distances, packageHash = packageHashTable)


# the strategy from here is to split our packages up into separate queues
# one of the strategies behind the A* search algorithm is to pre-process the
# data, so we are doing that by noticing that there is a geographical split
# between zip codes north of the hub and zip codes south of it.

# separate queues are kept to also meet other business requirements like
# priority deadlines, bundling, and needing to use a specific truck

# now we need to split the packages up into multiple delivery queues

queuePriority900 = DeliveryQueue("Priority 900", packageHashTable)    # For priority deliveries 900
queuePriority1030 = DeliveryQueue("Priority 1030", packageHashTable)  # For priority deliveries 1030
queueDelayed905 = DeliveryQueue("Delayed 905", packageHashTable)      # For deliveries delayed until 905
queueDelayed1020 = DeliveryQueue("Delayed 1020", packageHashTable)    # For deliveries delayed until 1020
queueTruck2orBundled = DeliveryQueue("Truck 2", packageHashTable)     # specifically for Truck 2
queueNorth = DeliveryQueue("North Zip Codes", packageHashTable)       # general delivery "north"
queueSouth = DeliveryQueue("South Zip Codes", packageHashTable)       # general delivery "south"
queueGeneral = DeliveryQueue("General Deliveries", packageHashTable)  # general delivery elsewhere
queueGeneral2 = DeliveryQueue("General Deliveries", packageHashTable)  # general delivery elsewhere

# "north" zip codes

north_zip_codes = ["84102","84103","84104","84111"]
north_zip_set = set(north_zip_codes)

def is_north_zip_code(zip_code):
    return zip_code in north_zip_set

# "south" zip codes

south_zip_codes = ["84117","84121","84107","84124"]
south_zip_set = set(north_zip_codes)

def is_south_zip_code(zip_code):
    return zip_code in south_zip_set


## sort packages into delivery queues

for i in packageList:

    package = packageHashTable.get(i)

    print("package ",package.package_id,"goes to location ",package.location," in zip code", package.zip_code)

    if int(package.delivery_deadline) == 900:
        queuePriority900.push(package.package_id, package.location)

    elif int(package.delivery_available) == 905:
        queueDelayed905.push(package.package_id, package.location)

    elif int(package.delivery_deadline) == 1030:
        queuePriority1030.push(package.package_id, package.location)

    elif int(package.delivery_available) == 1020:
        queueDelayed1020.push(package.package_id, package.location)

    elif int(package.truck_required) == 2 or int(package.bundled) == 1:
        queueTruck2orBundled.push(package.package_id, package.location)

    elif is_north_zip_code(package.zip_code):
        queueNorth.push(package.package_id, package.location)
    
    elif is_south_zip_code(package.zip_code):
        queueSouth.push(package.package_id, package.location)

    else:
        if len(queueGeneral) > 10:
            queueGeneral2.push( package.package_id, package.location)
        else:
            queueGeneral.push(package.package_id, package.location)

    ## end of sorting logic


# print("Queue 1 contents:")
# queue930.display_contents()
# ... etc

## Create QueueofQueues to reduce program logic/conditionals in business loop

priorityQueue = QueueOfQueues("Priority")
delayedQueue = QueueOfQueues("Delayed")
truck2Queue = QueueOfQueues("Truck 2 and Bundled")
generalQueue = QueueOfQueues("General")


priorityQueue.add_queue(queuePriority900)
priorityQueue.add_queue(queuePriority1030)

truck2Queue.add_queue(queueTruck2orBundled)

generalQueue.add_queue(queueNorth)
generalQueue.add_queue(queueSouth)
generalQueue.add_queue(queueGeneral)
generalQueue.add_queue(queueGeneral2)


#### here we need the delivery loop - trucks loaded and ticked for progress

master_time = Kronos(hours=8, minutes=0, meridian=0)
end_of_day = Kronos(hours=10, minutes=0, meridian=1)
end_of_day_timestamp = end_of_day.get_timestamp()


all_delivered = False
delayed905added = False
delayed1020added = False


#### here is our delivery logic to get the queues to each truck

def route_truck(target_truck):
    if (target_truck.get_state()) == State.AWAITING_DISPATCH:
        if (priorityQueue.has_queue()) is not None:
            target_truck.load_packages(priorityQueue.get_queue())
        
        elif (delayedQueue.has_queue()) is not None:
            target_truck.load_packages(delayedQueue.get_queue())
        
        elif ((truck2Queue.has_queue()) is not None) and (target_truck.id == 2):
            target_truck.load_packages(truck2Queue.get_queue())

        elif (generalQueue.has_queue()) is not None:
            target_truck.load_packages(generalQueue.get_queue())
        
        else:
            target_truck.finished_for_day()

current_time = master_time.get_timestamp()
current_time_string = master_time.get_time_string()

while (current_time < end_of_day_timestamp) and all_delivered is False:

    # time check

    print("\t\t\t\t\t\t\t\t\t\tTime is now", current_time_string)


    # pause at time logic

    if pause_at_time is True and time_to_pause == current_time:
        truck1.print_summary()
        truck2.print_summary()
        packageHashTable.get_all_ids_status()
        exit()

    # check for delayed queues

    if current_time >= 905 and delayed905added is False:
        delayedQueue.add_queue(queueDelayed905)
        print("Delayed Queue 905 added")
        delayed905added = True
    
    if current_time >= 1020 and delayed1020added is False:
        delayedQueue.add_queue(queueDelayed1020)
        print("Delayed Queue 1020 added")
        delayed1020added = True
    
    route_truck(truck1)
    route_truck(truck2)

    truck1.tick(current_time_string)
    truck2.tick(current_time_string)

    if (current_time == 900) or (current_time == 1000) or (current_time == 1150):
        truck1.print_status()
        truck2.print_status()

    if (truck1.get_state() == State.END_OF_DAY) and (truck2.get_state() == State.END_OF_DAY):
        all_delivered = True

    master_time.tick()
    current_time = master_time.get_timestamp()
    current_time_string = master_time.get_time_string()


print("All deliveries have finished.")
# print(current_time, current_time_string, end_of_day_timestamp)
truck1.print_summary()
truck2.print_summary()

# packageHashTable.show_pkg_info('1')

packageHashTable.get_all_ids_status()