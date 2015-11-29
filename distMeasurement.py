
from socket import *
import sys
import struct

TTL_START = 1
MAX-HOP = 64

def main():
    input_file = open("target.txt")
    output_file = open("results.txt", "w")

    output_file.write("Name: Andrew Hwang\n" + "EECS 325 Project 2\n" + "\n")

    target_hosts = input_file.read().splitlines()

    for host in target_hosts:

def probe(IP_address, ttl):
    dest = gethostbyname(IP_address)

    while True:
        send_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        recv_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

        send_socket.setsockopt(SOL_IP, IP_TTL, ttl)

        send_socket.sendto("", (dest, 33434))


if __name__ == "__main__":
    main()
