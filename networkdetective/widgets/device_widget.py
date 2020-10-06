#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

from device import *
from utils import *
from widgets.blinking_widget import BlinkingWidget

from PyQt5.QtWidgets import QLabel, QHBoxLayout
from PyQt5.QtNetwork import QHostInfo


class DeviceWidget(BlinkingWidget):

    def __init__(self, device, parent=None):
        super(DeviceWidget, self).__init__(parent)

        self.device = device
        QHostInfo.lookupHost(device.ip, self.setHostname)

        self.initUI(parent)

    def initUI(self, parent):
        self.setColor(parent.backgroundColor)

        self.labelStatus = QLabel(self)

        self.labelIp = QLabel(self.device.ip, self)
        self.labelIp.setFixedWidth(90)

        self.labelOS = QLabel(self)
        self.labelOS.setFixedWidth(24)

        self.labelName = QLabel(self.device.hostname, self)
        self.labelName.setFixedWidth(200)

        self.labelPacketCounter = QLabel(str(self.device.packet_count), self)
        self.labelPacketCounter.setContentsMargins(8, 0, 8, 0)

        self.labelTimestamp = QLabel(self.device.last_seen.strftime('%Y-%m-%d %H:%M:%S'), self)
        self.labelTimestamp.setContentsMargins(0, 0, 8, 0)

        self.layout = layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addWidget(self.labelStatus)
        layout.addWidget(self.labelIp)
        layout.addWidget(self.labelOS)
        layout.addWidget(self.labelName)
        layout.addStretch()
        layout.addWidget(self.labelPacketCounter)
        layout.addWidget(self.labelTimestamp)
        # layout.addWidget(QPushButton(QIcon("resources/megaphone.png"), None, self))
        # layout.addWidget(QPushButton(QIcon("resources/target.png"), None, self))
        # layout.addWidget(QPushButton(QIcon("resources/fingerprint.png"), None, self))
        self.setLayout(layout)

        self.__updateUI()

    def __updateUI(self):
        if self.device.status() == DeviceStatus.ONLINE:
            self.labelStatus.setPixmap(QPixmap('resources/status.png'))
        elif self.device.status() == DeviceStatus.OFFLINE:
            self.labelStatus.setPixmap(QPixmap('resources/status-offline.png'))
        elif self.device.status() == DeviceStatus.AWAY:
            self.labelStatus.setPixmap(QPixmap('resources/status-away.png'))
        else:
            self.labelStatus.setPixmap(QPixmap('resources/status-busy.png'))

        self.labelTimestamp.setText(self.device.last_seen.strftime('%Y-%m-%d %H:%M:%S'))
        self.labelPacketCounter.setText(str(self.device.packet_count))

    def updateLastSeen(self):
        now = datetime.now()
        self.device.last_seen = now
        self.__updateUI()

    def setHostname(self, host):
        hostname = host.hostName()
        hostname = hostname[:-4] if hostname[-4:] == ".lan" else hostname
        self.device.hostname = hostname if hostname and not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname) else "/"
        self.labelName.setText(self.device.hostname)

        if "linux" in self.device.hostname.lower():
            self.device.os = OperatingSystem.LINUX
        elif "-PC" in self.device.hostname or "PC-" in self.device.hostname:
            self.device.os = OperatingSystem.WINDOWS
        elif "android" in self.device.hostname.lower():
            self.device.os = OperatingSystem.ANDROID
        elif any((True for x in self.device.hostname.lower() if x in ["iphone", "macos", "macbook"])):
            self.device.os = OperatingSystem.MAC

        if self.device.os == OperatingSystem.WINDOWS:
            self.labelOS.setPixmap(QPixmap('resources/os/windows.png'))
        elif self.device.os == OperatingSystem.LINUX:
            self.labelOS.setPixmap(QPixmap('resources/os/linux.png'))
        elif self.device.os == OperatingSystem.MAC:
            self.labelOS.setPixmap(QPixmap('resources/os/macos.png'))
        elif self.device.os == OperatingSystem.ANDROID:
            self.labelOS.setPixmap(QPixmap('resources/os/android.png'))
