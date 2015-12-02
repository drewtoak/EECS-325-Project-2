
from socket import *
import sys
import struct
import time
import select

TTL_START = 32
TIMEOUT = 2.0
RETRIES = 7

def main():
    input_file = open("target.txt")
    output_file = open("results.txt", "w")

    output_file.write("Name: Andrew Hwang\n" + "EECS 325 Project 2\n" + "\n")

    target_hosts = input_file.read().splitlines()

    for host in target_hosts:
        result = probe(gethostbyname(host))
        if result is not None:
            output_result = "Host: {}\nHops: {}\nRTT: {} ms\n{}".format(host, result[0], result[1], result[2])
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
    port = 33434

    for retry in xrange(RETRIES):
        send_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        recv_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

        send_socket.setsockopt(SOL_IP, IP_TTL, ttl)

        send_socket.settimeout(TIMEOUT)
        recv_socket.settimeout(TIMEOUT)

        try:
            recv_socket.bind(("", port))
            send_socket.sendto("", (IP_address, port))
            sent_time = time.time()

            recv_packet = recv_address = None

            recv_packet, recv_address = recv_socket.recvfrom(1500)
            recvd_time = time.time()
            print "Recieved"

            icmp_header = recv_packet[20:28]
            icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq = struct.unpack_from("bbHHh", icmp_header)

            ip_header = recv_packet[36:40]
            ip_ttl, ip_protocol, ip_checksum = struct.unpack_from("bbH", ip_header)

            number_hops = ttl - ip_ttl + 1
            rtt = 1000*(recvd_time - sent_time)

            long_ip = struct.unpack('!L', recv_packet[44:48])[0]
            dest_ip = inet_ntoa(struct.pack('!L', long_ip))
            dest_port = struct.unpack("!H", recv_packet[50:52])[0]

            print "Destination IP: {}\nDestination Port: {}".format(dest_ip, dest_port)

            verified = None
            if dest_ip == IP_address and dest_port == port:
                verified = "The Destination IP address: {} and port number: {} were verified.\n".format(dest_ip, dest_port)
            else:
                verified = "The Destination IP address and port number were not verified.\n"

            return number_hops, rtt, verified
        except (timeout, error):
            pass
        finally:
            send_socket.close()
            recv_socket.close()
    else:
        return None


if __name__ == "__main__":
    main()
