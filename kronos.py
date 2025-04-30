class Kronos:
    def __init__(self, hours: int = 12, minutes: int = 0, meridian: int = 0):
        self.hours = hours
        self.minutes = minutes
        self.meridian = meridian  # 0 for AM, 1 for PM

    def tick(self):

        self.minutes += 1

        if self.minutes >= 60:
            self.minutes -= 60
            self.hours += 1
        
        if self.hours >= 13:
            self.hours -= 12
            self.meridian = (self.meridian + 1) % 2

    def get_time_string(self):
        meridian_string = "am" if self.meridian == 0 else "pm"
        return f"{self.hours}:{self.minutes:02d} {meridian_string}"

    def get_timestamp(self):
        hoursandminutes = self.hours * 100 + self.minutes
        postmeridian = 1200 if self.meridian > 0 else 0
        return hoursandminutes + postmeridian
    
    def set_timestamp(self, timestamp):
        timestamp = int(timestamp)
        self.meridian = 0

        if timestamp > 1200:
            timestamp -= 1200
            self.meridian = 1
        
        self.minutes = int(timestamp % 100)

        self.hours = int((timestamp - self.minutes)/100)



## test code

if __name__ == "__main__":
    time1 = Kronos(hours = 8, minutes = 0, meridian = 0)

    time2 = Kronos(hours = 11, minutes = 59, meridian = 0)

    print( time2.get_time_string())
    print( time2.get_timestamp())

    time2.tick()

    print( time2.get_time_string())
    print( time2.get_timestamp())
