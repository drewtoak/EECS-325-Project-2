import urllib2
from socket import gethostbyname
from math import *

def main(dest_name):
    location = locate(gethostbyname(dest_name))

def locate(IP_address):
    response = urllib2.urlopen("freegeoip.net/xml/{}".format(IP_address)).read
    

if __name__ == "__main__":
    main("google.com")
