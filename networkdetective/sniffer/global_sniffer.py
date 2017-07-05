#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from PyQt5.QtCore import QThread, pyqtSignal

from scapy.all import *
from scapy.layers.inet import IP


class NetworkSniffer(QThread):
    """ Abstract class """
    packetCaptured = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(NetworkSniffer, self).__init__(parent)

        self.filter = "ip multicast or arp or icmp or port 1900"

    """ Abstract method """
    def monitor_callback(self, pkt):
        if ARP in pkt:
            self.packetCaptured.emit(pkt[ARP].hwsrc, pkt[ARP].psrc)
        elif IP in pkt:
            self.packetCaptured.emit(pkt[Ether].src, pkt[IP].src)

    def run(self):
        logging.debug('thread started sniffing...')
        scapy.all.sniff(prn=self.monitor_callback, filter=self.filter, store=0)