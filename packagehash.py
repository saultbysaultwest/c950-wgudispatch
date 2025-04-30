from package import *
from hashtable import *
import csv
import os

# note that we are indexing to one instead of zero to match WGU package list

class PackageHash:

    def __init__(self, sizeOf):
        self.table = HashTable(sizeOf)
        self.package_id_list = []

    def get(self, key):
        return self.table.get(key)
    
    def set(self, key, obj):
        self.table.set(key, obj)

    def delete(self, key):
        self.table.delete(key)
    
    def len(self):
        return len(self.package_id_list)
    
    def add_id(self, id):
        self.package_id_list.append(id)

    def list_all_ids(self):
        print("## List of all package IDs")
        print("##", self.package_id_list,"\n")

    def get_all_ids(self):
        return self.package_id_list
    
    def get_all_ids_status(self):
        print("\n")
        print("Status of all packages: ")
        for pkg in self.package_id_list:
            this_pkg = self.table.get(pkg)
            this_status = this_pkg.get_status()
            this_time = this_pkg.get_package_time_delivered()
            this_address = this_pkg.street_address
            this_truck = this_pkg.get_truck_delivered()

            if this_pkg.get_has_delivered() == False:
                    if this_status == "On Delivery":
                        print("Package id",this_pkg.package_id," is out for delivery on truck", this_truck,"to address",this_address)
                    else:
                        print("Package id ",this_pkg.package_id, "has status of", this_status,"and has not been delivered.")
            else:
                print("Package id ",this_pkg.package_id,"has status of",this_status, "and was delivered at",this_time,"by truck",this_truck,"to address",this_address)
    
    def set_time_delivered(self, id, time):
        this_package = self.table.get(id)
        this_package.set_package_time_delivered(time)
        this_package.set_status(Status.HAS_DELIVERED)
        this_package.set_has_delivered()
        self.table.set(id, this_package)

    def get_time_delivered(self, id):
        this_package = self.table.get(id)
        return this_package.get_time_delivered()
    
    def set_truck_delivered(self, id, truck_id):
        this_package = self.table.get(id)
        this_package.set_truck_delivered(truck_id)
        self.table.set(id, this_package)

    def get_truck_delivered(self, id):
        this_package = self.table.get(id)
        return this_package.get_truck_delivered()        

    def show_pkg_info(self, id):
        this_package = self.table.get(id)
        print("\n")
        print("Summary of Package",this_package.package_id,":")
        print("\tDelivery address:",this_package.street_address)
        print("\tDelivery deadline:",this_package.delivery_deadline)
        print("\tDelivery city:",this_package.city)
        print("\tDelivery Zip code:",this_package.zip_code)
        print("\tPackage weight:",this_package.weight_kg,"kg")
        print("\tDelivery Status:", this_package.get_status())
        if this_package.get_status() == Status.HAS_DELIVERED:
            print("\tDelivery status: package delivered at",this_package.time_delivered)
    

    def load_from_csv(self, filepath):

        if not os.path.isfile(filepath):
            print(f"Error: file '[filepath]' does not exist.")
            return

        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)

            for row in reader:
                package = Package(*row)
                package_id = package.package_id           
                self.set(package_id, package)
                self.add_id(package_id)

        numberOfPackages = self.len()
        print("\n")
        print(f"{numberOfPackages} packages have been loaded.")
        print("\n")


## Debugging

if __name__ == '__main__':
    testTable = PackageHash(301)
    testTable.load_from_csv('wgu-packages.csv')

    package1 = testTable.get('1')
    print( package1 )
    package1.location = 1
    print( package1 )
    testTable.set('1', package1)
    packageTest = testTable.get('1')
    print( packageTest)

    numberOfPackages = testTable.len()

    print( f"Package 1 goes to {package1.street_address}.")
    print( f"There are {numberOfPackages} packages in this table.")
    testTable.list_all_ids()