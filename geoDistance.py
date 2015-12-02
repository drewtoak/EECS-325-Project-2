import urllib2
import json
import requests
from socket import gethostbyname
from math import *

def main(dest_name):
    location = locate_host(gethostbyname(dest_name))

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
    response = 'http://freegeoip.net/json/{}'.format(IP_address)
    r = requests.get(response)
    j = json.loads(r.text)

    latitude = longitude = None

    latitude = j['latitude']
    longitude = j['longitude']

    print "Latitude: {}\nLongitude: {}\n".format(latitude, longitude)
    return latitude, longitude

if __name__ == "__main__":
    main("google.com")
