# import urllib2
import json
import requests
from socket import gethostbyname
from math import *

def main():
    my_location = locate_self()
    print "Self:\nLatitude: {}\nLongitude: {}\n".format(my_location[0], my_location[1])
    if my_location[0] == None and my_location[1] == None:
        raise Exception("Your location could not be found.")

    input_file = open("target.txt")
    output_file = open("geoDistance_results.txt", "w")

    target_hosts = input_file.read().splitlines()

    for host in target_hosts:
        host_location = locate_host(gethostbyname(host))
        print "Host:\nLatitude: {}\nLongitude: {}".format(host_location[0], host_location[1])
        shortest_distance = None
        if host_location[0] != None and host_location[1] != None:
            shortest_distance = calculate_distance(my_location, host_location)
        else:
            raise Exception("Host location could not be found.")

        output_result = "Host: {}\nIP address: {}\nDistance: {}\n".format(host, gethostbyname(host), shortest_distance)
        print output_result
        output_file.write(output_result + "\n")

    input_file.close()
    output_file.close()


def locate_host(IP_address):
    # response_doc = urllib2.urlopen('http://freegeoip.net/xml/{}'.format(IP_address))
    #
    # latitude = longitude = None
    #
    # for line in response_doc:
    #     if "Latitude" in line:
    #         latitude = float(line.replace("<Latitude>", "").replace("</Latitude>", ""))
    #     elif "Longitude" in line:
    #         longitude = float(line.replace("<Longitude>", "").replace("</Longitude>", ""))
    #
    # response_doc.close()

    response = requests.get('http://freegeoip.net/json/{}'.format(IP_address))
    doc = json.loads(response.text)

    latitude = longitude = None

    latitude = doc['latitude']
    longitude = doc['longitude']

    return latitude, longitude

def locate_self():
    request = requests.get('http://ip.42.pl/raw')
    my_IP_address = request.text

    my_location = locate_host(my_IP_address)

    return my_location

def calculate_distance(start_coordinate, end_coordinate):
    start_lat, start_long, end_lat, end_long = map(radians, [start_coordinate[0], start_coordinate[1], end_coordinate[0], end_coordinate[1]])

    lat_distance = end_lat - start_lat
    long_distance = end_long - start_long

    a = sin(lat_distance/2) * sin(lat_distance/2) + cos(start_lat) * cos(end_lat) * sin(long_distance/2) * sin(long_distance/2)
    c = 2 * asin(sqrt(a))

    shortest_distance = c * 6367

    return shortest_distance

if __name__ == "__main__":
    main()
