#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
from enum import Enum


class OperatingSystem(Enum):
    WINDOWS = 0
    LINUX = 1
    MAC = 2
    ANDROID = 3


class DeviceStatus(Enum):
    OFFLINE = 0  # if not responding to discovery packets OR - at initialization (session restore) ?
    ONLINE = 1  # At creation
    BUSY = 2
    AWAY = 3


class Device(object):

    def __init__(self, mac, ip):
        self.os = None
        self.mac = mac
        self.ip = ip
        self.hostname = None
        self.first_seen = datetime.now()
        self.last_seen = datetime.now()
        self.packet_count = 1

    def status(self):
        timespan = (self.last_seen - datetime.now()).total_seconds()
        if timespan < 10 * 60:
            return DeviceStatus.ONLINE
        elif timespan >= 10 * 60:
            return DeviceStatus.AWAY
        else:
            return DeviceStatus.BUSY

    def count_packet(self):
        self.packet_count = self.packet_count + 1
