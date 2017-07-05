#!/usr/bin/python3
# -*- coding: utf-8 -*-

from networkdetective.sniffer.global_sniffer import NetworkSniffer

from scapy.all import *
from scapy.layers.inet import IP


class ICMPNetworkSniffer(NetworkSniffer):

    def __init__(self, parent=None):
        super(ICMPNetworkSniffer, self).__init__(parent)

        self.filter = "icmp"

    def monitor_callback(self, pkt):
        self.packetCaptured.emit(pkt[Ether].src, pkt[IP].src)
