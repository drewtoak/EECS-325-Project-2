import urllib2
from socket import gethostbyname
from math import *

def main(dest_name):
    location = get_my_location(gethostbyname(dest_name))

def get_my_location(IP_address):
    response = urllib2.urlopen("freegeoip.net/xml/{}".format(IP_address)).read
    print response

if __name__ == "__main__":
    main("google.com")
