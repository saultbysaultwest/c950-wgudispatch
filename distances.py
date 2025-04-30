import csv

class Distances:
    def __init__(self, csv_file):
        self.distance_array = self.load_location_data(csv_file)
    
    def load_location_data(self, csv_file):
        with open(csv_file, newline='') as file:
            reader = csv.reader(file)
            # Convert each row to a list of floats
            distance_matrix = [list(map(float, row)) for row in reader]
        return distance_matrix

    def distance(self, location1, location2):

        loc1 = int(location1) - 1
        loc2 = int(location2) - 1

        # do some basic error handling
        
        if loc1 < 0 or loc2 < 0 or loc1 >= len(self.distance_array) or loc2 >= len(self.distance_array):
            raise ValueError("Location indices are out of bounds.")
        
        if self.distance_array[loc1][loc2] == -1:
            return self.distance_array[loc2][loc1]
        else:
            return self.distance_array[loc1][loc2]

# # Usage
# csv_file = 'yourfile.csv'  # Replace 'yourfile.csv' with the path to your CSV file
# distances = Distances(csv_file)

# # Example call to the distance method
# print(distances.distance(1, 2))  # Replace 1 and 2 with actual location indices

if __name__ == "__main__":
    csv_file = 'wgu-distances.csv'
    distances = Distances(csv_file)
    print(distances.distance(8,9))
    print(distances.distance(9,25))
    print(distances.distance(25,9))
    print(distances.distance(1,8))
    print(distances.distance(1,9))
    print(distances.distance(1,25))
    print(distances.distance(1,22))