#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sniffer.global_sniffer import NetworkSniffer

from scapy.all import *


class ARPNetworkSniffer(NetworkSniffer):

    def __init__(self, parent=None):
        super(ARPNetworkSniffer, self).__init__(parent)

        self.filter = "arp"

    def monitor_callback(self, pkt):
        if ARP in pkt and pkt[ARP].op in (1, 2):  # who-has or is-at
            self.packetCaptured.emit(pkt[ARP].hwsrc, pkt[ARP].psrc)
