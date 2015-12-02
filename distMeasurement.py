
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
        if result is not None:
            output_result = "Host: {}\nHops: {}\nRTT: {} ms\n".format(host, result[0], result[1])
            print output_result
            output_file.write(output_result + "\n")
        else:
            output_result = "Host: {}\nHost timed out.\n".format(host)
            print output_result
            output_file.write(output_result + "\n")

    input_file.close()
    output_file.close()

    # result = probe(gethostbyname(host_name))
    # if result is not None:
    #     if result[0] is not None:
    #         output_result = "Host: {}\nHops: {}\nRTT: {} ms\n".format(host_name, result[0], result[1])
    #         print output_result
    #     else:
    #         output_result = "Host: {}\nHost timed out.\n".format(host_name)
    #         print output_result
    # else:
    #     output_result = "Host: {}\nHost timed out.\n".format(host_name)
    #     print output_result

def probe(IP_address):
    ttl = TTL_START
    remaining_time = TIMEOUT
    dest = IP_address
    port = 33434

    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    send_socket.settimeout(TIMEOUT)
    recv_socket.settimeout(TIMEOUT)

    try:
        recv_socket.bind(("", port))
        send_socket.sendto("", (dest, port))
        sent_time = time.time()

        recv_packet = recv_address = None

        recv_packet, recv_address = recv_socket.recvfrom(1500)
        recvd_time = time.time()
        print "Recieved"
    except timeout:
        pass
    else:
        icmp_header = recv_packet[20:28]
        icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq = struct.unpack_from("bbHHh", icmp_header)

        ip_header = recv_packet[36:40]
        ip_ttl, ip_protocol, ip_checksum = struct.unpack_from("bbH", ip_header)

        number_hops = ttl - ip_ttl + 1
        rtt = 1000*(recvd_time - sent_time)

        dest_ip = struct.unpack_from('!4s', recv_packet[44:48])
        dest_port = struct.unpack_from("!H", recv_packet[50:52])

        print "Destination IP: {}\nDestination Port: {}\n".format(dest_ip, dest_port)

        return number_hops, rtt
    finally:
        send_socket.close()
        recv_socket.close()

if __name__ == "__main__":
    main()
