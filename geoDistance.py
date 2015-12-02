import urllib2
import xml.dom.minidom
from socket import gethostbyname
from math import *

def main(dest_name):
    location = locate_host(gethostbyname(dest_name))

def locate_host(IP_address):
    response = urllib2.urlopen("freegeoip.net/xml/{}".format(IP_address)).read
    response_doc = xml.dom.minidom.parseString(response)
    response.close()

    city = response_doc.getElementsByTagName("City")[0]
    region_name = response_doc.getElementsByTagName("RegionName")[0]
    country_name = response_doc.getElementsByTagName("CountryName")[0]
    latitude = response_doc.getElementsByTagName("Latitude")[0]
    longitude = response_doc.getElementsByTagName("Longitude")[0]

    print city, region_name, country_name, latitude, longitude
    return city, region_name, country_name, latitude, longitude

if __name__ == "__main__":
    main("google.com")
