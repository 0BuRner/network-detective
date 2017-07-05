#!/usr/bin/python3
# -*- coding: utf-8 -*-

from networkdetective.device import *
from networkdetective.widgets.device_widget import DeviceWidget
from networkdetective.sniffer.global_sniffer import NetworkSniffer
from networkdetective.discovery.arp_discovery import ARPNetworkDiscovery
from networkdetective.utils import *

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QColorDialog, QPushButton, QLabel, QLayout, QHBoxLayout, QGridLayout, QSlider
from PyQt5.QtGui import QColor


class DesktopWidget(QWidget):

    title = "Network Detective"

    m_nMouseClick_X_Coordinate = 0
    m_nMouseClick_Y_Coordinate = 0

    transparency = 50
    backgroundColor = QColor(255, 255, 255, transparency)

    def __init__(self):
        super(DesktopWidget, self).__init__()

        self.devices = []

        self.threadSniffer = NetworkSniffer()
        self.threadSniffer.start()
        self.threadSniffer.packetCaptured.connect(self.packetCapturedEvent)

        self.threadDiscovery = ARPNetworkDiscovery()

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon("resources/app_icon.png"))
        self.setWindowTitle(self.title)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)

        self.buttonQuit = QPushButton(QIcon("resources/cross-button.png"), None, self)
        self.buttonQuit.clicked.connect(QtCore.QCoreApplication.instance().quit)

        self.buttonRefresh = QPushButton(QIcon("resources/arrow-repeat.png"), None, self)
        self.buttonRefresh.clicked.connect(self.threadDiscovery.start)  # TODO refresh red status and choose method

        labelTitleIcon = QLabel(self)
        labelTitleIcon.setPixmap(QPixmap("resources/app_icon_20.png").scaled(QSize(20, 20),  QtCore.Qt.KeepAspectRatio))
        labelTitleIcon.setCursor(QtCore.Qt.SizeAllCursor)

        labelTitle = QLabel(self.title, self)
        labelTitle.setContentsMargins(8, 0, 8, 0)

        sliderTransparency = QSlider(QtCore.Qt.Horizontal, self)
        sliderTransparency.setRange(0, 255)
        sliderTransparency.setMaximumHeight(12)
        sliderTransparency.setValue(self.transparency)
        sliderTransparency.valueChanged.connect(self.changeTransparency)

        buttonColorPicker = QPushButton(self)
        buttonColorPicker.setIcon(QIcon("resources/color.png"))
        buttonColorPicker.clicked.connect(self.openColorPicker)

        toolsLayout = QHBoxLayout()
        toolsLayout.addWidget(labelTitleIcon)
        toolsLayout.addWidget(labelTitle)
        toolsLayout.addStretch()
        toolsLayout.addWidget(sliderTransparency)
        toolsLayout.addStretch()
        toolsLayout.addWidget(buttonColorPicker)
        toolsLayout.addWidget(self.buttonRefresh)
        toolsLayout.addWidget(self.buttonQuit)

        self.mainLayout = mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.setSpacing(1)
        mainLayout.addItem(toolsLayout)

        self.setLayout(mainLayout)

    def __findDeviceWidget(self, mac):
        items = [self.mainLayout.itemAt(i) for i in range(1, self.mainLayout.count())]
        return next((item.widget() for item in items if item.widget().device.mac == mac), None)

    def __addDevice(self, mac, ip):
        device = Device(mac, ip)
        deviceWidget = DeviceWidget(device, self)
        deviceWidget.blink()
        self.devices.append(device)
        self.mainLayout.addWidget(deviceWidget)

    def __updateDevice(self, mac):
        deviceWidget = self.__findDeviceWidget(mac)
        deviceWidget.updateLastSeen()
        deviceWidget.device.count_packet()

    def packetCapturedEvent(self, mac, ip):
        device_found = next((device for device in self.devices if device.ip == ip), None)
        if device_found:
            self.__updateDevice(mac)
        else:
            self.__addDevice(mac, ip)

    def changeTransparency(self, value):
        self.backgroundColor.setAlpha(value)
        items = [self.mainLayout.itemAt(i) for i in range(1, self.mainLayout.count())]
        for item in items:
            widget = item.widget()
            widget.setBackgroundColor(self.backgroundColor)
            widget.setForegroundColor(PyUtils.contrastColor(self.backgroundColor))

    def openColorPicker(self):
        alpha = self.backgroundColor.alpha()
        self.backgroundColor = QColorDialog.getColor()
        self.changeTransparency(alpha)

    @pyqtSlot()
    def mousePressEvent(self, event):
        self.m_nMouseClick_X_Coordinate = event.x()
        self.m_nMouseClick_Y_Coordinate = event.y()

    @pyqtSlot()
    def mouseMoveEvent(self, event):
        self.move(event.globalX() - self.m_nMouseClick_X_Coordinate, event.globalY() - self.m_nMouseClick_Y_Coordinate)
