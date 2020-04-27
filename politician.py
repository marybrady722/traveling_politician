
import csv
import math
import random

with open("zipcodes.txt") as csv_file:
    zipcode_list = csv.reader(csv_file, delimiter=",")
    #creates dictionary where keys are zipcodes and values are a tuple of state, latitude, and longitude
    zipcodes = {}
    for row in zipcode_list:
        zipcodes[row[0]] = (row[2], row[3], row[4])

    #gets state, latittude, and longitude
    def get_information(zipcode):
        for item in zipcodes:
            if zipcode == item:
                return zipcodes[item]

    #calculates distance between zipcodes in meters
    def distance(zipcode1, zipcode2):
        """
        :param zipcode1: A zipcode that is present in the spreadsheet
        :param zipcode2: A zipcode that is present in the spreadsheet
        :return: The distance in miles between the two zipcodes
        """
        #gets lat and long coordinates from zipcode input
        lat1 = float(get_information(zipcode1)[1])
        long1 = float(get_information(zipcode1)[2])
        lat2 = float(get_information(zipcode2)[1])
        long2 = float(get_information(zipcode2)[2])
        lat_dif = abs(lat1 - lat2)
        long_dif = abs(long1 - long2)
        #uses Haversine formula
        a = ((math.sin(lat_dif/2))**2) + math.cos(lat1) * math.cos(lat2) * (math.sin(long_dif)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        R = 6371
        dist = R * c
        return dist


    def ideal_path(start_zipcode, end_zipcode,  zipcodes):
        """
        :param zipcodes: A list containing the zipcodes in the route except the start and end
        :param start_zipcode: zipcode of capital of the state that we start from
        :param end_zipcode: zipcode of the end point
        :return: The shortest route and its distance in meters
        """
        routes = {}
        #checks that all routes have been explored
        while len(routes) != math.factorial(len(zipcodes)):
            random_nums = {}
            ordered_route = [start_zipcode]
            #assigns a random number to each zipcode to sort zipcodes into unique ordered routes
            for zc in zipcodes:
                random_nums[zc] = random.randint(1, 101)
            #checks that the length of the potential route is the correct length
            while len(ordered_route) <= len(zipcodes) + 1:
                minimum = 102
                #orders zipcodes by minimum random number first
                for item in random_nums:
                    if random_nums[item] < minimum:
                        minimum = random_nums[item]
                for item in random_nums:
                    if random_nums[item] == minimum:
                        ordered_route.append(item)
                        break
                if len(random_nums) == 0:
                    break
                random_nums.pop(item)
            #adds ending point to each route
            ordered_route.append(end_zipcode)
            if str(ordered_route) not in routes:
                dist = 0
                #uses distance function to calculate distance of entire route
                ordered = []
                for num in range(0, len(ordered_route) - 1):
                    dist += distance(ordered_route[num], ordered_route[num+1])
                #gets state information from zipcode
                for item in ordered_route:
                    ordered.append(get_information(item)[0])
                routes[str(ordered)] = dist
        #finds shortest route
        minimum = min(routes.values())
        for route in routes:
            if routes[route] == minimum:
                shortest_route = route
                break
        return shortest_route, int(minimum)


#V.1.0 - Zero states between start and end points

def zero_between(start_point):
    """
    :param start_point: capital that is started from
    :return: distance between start point and Washington D.C.
    """

    return distance(start_point, 20515)

#V.1.1 - One state between start and end points

print(ideal_path('50319', '20515', ['95814']))

#V.1.2 - Two states between start and end points

print(ideal_path('50319', '20515', ['95814', '12242']))

#V.1.3 - Three states between start and end points

print(ideal_path('50319', '20515', ['95814', '12242', '98504']))
