#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread

from scapy.all import *


class ARPNetworkDiscovery(QThread):

    def __init__(self, parent=None):
        super(ARPNetworkDiscovery, self).__init__(parent)

    def run(self):
        logging.debug('thread started active discovering...')
        scapy.all.srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst="192.168.1.0/24"), timeout=1, verbose=False)
