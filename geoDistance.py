import json
import requests
from socket import gethostbyname
from math import *

def main():
    # Get the location of the current computer.
    my_location = locate_self()
    print "Self:\nLatitude: {}\nLongitude: {}\n".format(my_location[0], my_location[1])

    if my_location[0] == None and my_location[1] == None:
        raise Exception("Your location could not be found.")

    input_file = open("target.txt")
    output_file = open("geoDistance_results.txt", "w")

    target_hosts = input_file.read().splitlines()

    # Iterate through each target host to loacte their location.
    for host in target_hosts:
        # Locate the host's loaction by their name.
        host_location = locate_host(gethostbyname(host))

        shortest_distance = None
        if host_location[0] != None and host_location[1] != None:
            # Get the shortest distance between this computer's IP and the host's IP.
            shortest_distance = calculate_distance(my_location, host_location)
        else:
            raise Exception("Host location could not be found.")

        output_result = "Host: {}\nIP address: {}\nDistance: {} km\n".format(host, gethostbyname(host), shortest_distance)
        print "Latitude: {}\nLongitude: {}".format(host_location[0], host_location[1])
        print output_result
        output_file.write(output_result + "\n")

    input_file.close()
    output_file.close()

# Locate the Latitude and Longitude of the given IP address.
def locate_host(IP_address):
    # Using the freegeoip.net web service to get the latitude and longitude of the IP.
    response = requests.get('http://freegeoip.net/json/{}'.format(IP_address))
    doc = json.loads(response.text)

    latitude = longitude = None

    latitude = doc['latitude']
    longitude = doc['longitude']

    return latitude, longitude

def locate_self():
    # Using the ip.42.pl web service to get the IP of this computer.
    request = requests.get('http://ip.42.pl/raw')
    my_IP_address = request.text

    my_location = locate_host(my_IP_address)

    return my_location

# Used the haversine formula found on the following link: http://www.movable-type.co.uk/scripts/latlong.html
# Calculates the shortest distance between two coordinates based off their latitude and longitude.
def calculate_distance(start_coordinate, end_coordinate):
    # Converted the latitude and longitude of the coordinates to radians.
    start_lat, start_long, end_lat, end_long = map(radians, [start_coordinate[0], start_coordinate[1], end_coordinate[0], end_coordinate[1]])

    # the difference between the pair of latitudes and longitudes.
    lat_distance = end_lat - start_lat
    long_distance = end_long - start_long

    # haversine formula.
    a = sin(lat_distance/2) * sin(lat_distance/2) + cos(start_lat) * cos(end_lat) * sin(long_distance/2) * sin(long_distance/2)
    c = 2 * asin(sqrt(a))

    # Convert to km.
    shortest_distance = c * 6367

    return shortest_distance

if __name__ == "__main__":
    main()
