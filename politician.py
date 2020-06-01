#add more comments
#fix github
import csv
import math
import random

with open("zipcodes.txt") as csv_file:
    zipcode_list = csv.reader(csv_file, delimiter=",")
    #uses provided csv file to create dictionary
    zipcodes = {}
    for row in zipcode_list:
        #creates dictionary such that keys are zipcodes and values are a tuple of state, latitude, and longitude
        zipcodes[row[0]] = (row[2], row[3], row[4])

    #gets state, latittude, and longitude
    def get_information(zipcode):
        for item in zipcodes:
            #checks each item in dictionary
            if zipcode == item:
                #returns tuple associated with that item
                return zipcodes[item]

    #calculates distance between zipcodes in meters
    def distance(zipcode1, zipcode2):
        """
        :param zipcode1: A zipcode that is present in the spreadsheet
        :param zipcode2: A zipcode that is present in the spreadsheet
        :return: The distance in miles between the two zipcodes
        """
        #gets lat and long coordinates from zipcode input
        #gets information as floats
        lat1 = float(get_information(zipcode1)[1])
        long1 = float(get_information(zipcode1)[2])
        lat2 = float(get_information(zipcode2)[1])
        long2 =float(get_information(zipcode2)[2])
        #gets radian value of latitude
        radlat1 = math.radians(float(get_information(zipcode1)[1]))
        radlat2 = math.radians(float(get_information(zipcode2)[1]))
        lat_dif = math.radians(lat2 - lat1)
        long_dif = math.radians(long2 - long1)
        #implements Haversine formula to calculate distance between 2 locations using latitude and longitude
        a = ((math.sin(lat_dif/2))**2) + (math.cos(radlat1) * math.cos(radlat2) * (math.sin(long_dif/2)**2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        #R = radius of earth in meters
        R = 6371e3
        dist = R * c
        #converts to km
        dist = dist * 0.001
        #converts to miles
        #can comment this line out if you prefer meters
        dist = dist * 0.62137
        return dist

    def ideal_path(start_zipcode, end_zipcode,  zipcodes):
        """
        :param zipcodes: A list containing the zipcodes in the route except the start and end
        :param start_zipcode: zipcode of capital of the state that we start from
        :param end_zipcode: zipcode of the end point
        :return: The shortest route and its distance in meters
        """
        #initializes dictionary that will store routes
        routes = {}
        #checks that all routes have been explored
        while len(routes) != math.factorial(len(zipcodes)):
            random_nums = {}
            #adds the starting point to eah route
            ordered_route = [start_zipcode]
            #assigns a random number to each zipcode to sort zipcodes into unique ordered routes
            for zc in zipcodes:
                random_nums[zc] = random.randint(1, 101)
            #checks that the length of the potential route is the correct length
            while len(ordered_route) <= len(zipcodes) + 1:
                #sets minimum to be one above the highest number generated randomly
                minimum = 102
                #orders zipcodes by minimum random number first
                for item in random_nums:
                    #checks if the number assigned to current zipcode is smaller than the minimum
                    if random_nums[item] < minimum:
                        #if number assigned to zipcode is smaller, minimum is updated
                        minimum = random_nums[item]
                #adds the zipcode with the minimum number assigned to the route
                for item in random_nums:
                    if random_nums[item] == minimum:
                        ordered_route.append(item)
                        break
                #checks that we haven't gone through each zipcode yet
                if len(random_nums) == 0:
                    break
                #removes the zipcode with the lowest random number from the dictionary
                random_nums.pop(item)
            #adds ending point to each route
            ordered_route.append(end_zipcode)
            #checks that the generated route doesn't already exist
            if str(ordered_route) not in routes:
                dist = 0
                #uses distance function to calculate distance of entire route
                ordered = []
                for num in range(0, len(ordered_route) - 1):
                    #uses distance function betwee every two points in route
                    dist += distance(ordered_route[num], ordered_route[num+1])
                #gets state information from zipcode
                for item in ordered_route:
                    #gets state of each zipcode
                    ordered.append(get_information(item)[0])
                #maps route to its distance
                routes[str(ordered)] = dist
        #finds distance of the shortest route
        minimum = min(routes.values())
        for route in routes:
            if routes[route] == minimum:
                #find the route with the shortest distance
                shortest_route = route
                break
        #returns shortest route and distance in miles
        #return distance as an integer and adds units for ease of viewing
        return ('Shortest Route: ' + shortest_route + ' Distance: ' + str(int(minimum)) + ' miles')


#V.1.0 - Zero states between start and end points
#When there are only two points, we can use the distance function with the start and end point
def zero_between(start_point):
    """
    :param start_point: capital that is started from
    :return: distance between start point and Washington D.C.
    """
    #uses distance function from start point to Washington D.C.
    dist = distance(start_point, '20515')
    #gets state of start point and adds to route along with Washington D.C.
    route = [get_information(start_point)[0], 'DC']
    #uses string and integer type for consistency
    return ('Shortest Route: ' + str(route) + ' Distance: ' + str(int(dist)) + ' miles')

print(zero_between('50319'))

#V.1.1 - One state between start and end points

print(ideal_path('50319', '20515', ['95814']))

#V.1.2 - Two states between start and end points

print(ideal_path('50319', '20515', ['95814', '12242']))

#V.1.3 - Three states between start and end points

print(ideal_path('50319', '20515', ['95814', '12242', '98504']))

#All 49 states between start and end points

#states = ['36104', '99801', '85001', '72201', '95814', '80202', '6103', '19901', '32301',
          #'30303', '96813', '83702', '62701', '46225', '66603', '40601', '70802', '4330',
          #'21401', '2201', '48933']
#print(ideal_path('50319', '20515', states))
