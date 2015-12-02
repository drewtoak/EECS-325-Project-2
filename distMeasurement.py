
from socket import *
import sys
import struct
import time
import select

TTL_START = 32
TIMEOUT = 2.0

def main():
    input_file = open("target.txt")
    output_file = open("results.txt", "w")

    output_file.write("Name: Andrew Hwang\n" + "EECS 325 Project 2\n" + "\n")

    target_hosts = input_file.read().splitlines()

    for host in target_hosts:
        result = probe(gethostbyname(host))
        if result[0] is not None:
            output_result = "Host: {}\nHops: {}\nRTT: {} ms\n".format(host, result[0], result[1])
            print output_result
            output_file.write(output_result + "\n")
        else:
            output_result = "Host: {}\nHost timed out.\n".format(host)
            print output_result
            output_file.write(output_result + "\n")

    input_file.close()
    output_file.close()

def probe(IP_address):
    ttl = TTL_START
    remaining_time = TIMEOUT
    dest = gethostbyname(IP_address)

    send_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    recv_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

    send_socket.setsockopt(SOL_IP, IP_TTL, ttl)

    try:
        recv_socket.bind("", 33434)
        send_socket.sendto("", (dest, 33434))
        sent_time = time.time()

        ready = select.select([recv_socket], [], [], remaining_time)

        recv_packet = recv_address = None

        recv_packet, recv_address = recv_socket.recvfrom(1500)
        recvd_time = time.time()
    except timeout:
        pass
    else:
        icmp_header = recv_packet[20:28]
        icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq = struct.unpack_from("bbHHh", icmp_header)

        ip_header = recv_packet[36:40]
        ip_ttl, ip_protocol, ip_checksum = struct.unpack_from("bbH", ip_header)

        number_hops = ttl - ip_ttl + 1
        rtt = 1000*(recvd_time - sent_time)

        return number_hops, rtt
    finally:
        send_socket.close()
        recv_socket.close()

if __name__ == "__main__":
    main()
