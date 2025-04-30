import csv

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class Location:
    id: int
    location_name: str
    street_address: str
    zip_code: str


def load_locations_from_csv(filepath):
    locations = []
    with open(filepath, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 4:
                location = Location(*row)
                locations.append(location)
    return locations


def get_location_id_by_street_address(street_address, locations):
    for location in locations:
        if location.street_address == street_address:
            return int(location.id)
    return None

if __name__ == "__main__":
    csv_file = 'wgu-locations.csv'
    locations = load_locations_from_csv(csv_file)
    print(locations[3])
    print(locations[2].location_name + ' ' + locations[2].street_address)
