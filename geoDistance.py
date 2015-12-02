import urllib2
import json
import requests
from socket import gethostbyname
from math import *

def main(dest_name):
    my_location = locate_self()
    print "Self:\nLatitude: {}\nLongitude: {}\n".format(latitude, longitude)
    location = locate_host(gethostbyname(dest_name))
    print "Host:\nLatitude: {}\nLongitude: {}\n".format(latitude, longitude)

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

    if my_location[0] != None and my_location[1] != None:
        return my_location
    else:
        raise Exception("Your location could not be found.")

if __name__ == "__main__":
    main("google.com")
