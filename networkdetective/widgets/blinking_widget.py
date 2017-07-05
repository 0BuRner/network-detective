#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget

from networkdetective.utils import PyUtils


class BlinkingWidget(QWidget):
    def __init__(self, parent=None):
        super(BlinkingWidget, self).__init__(parent)

        self.animation = anim = QtCore.QPropertyAnimation(self, "color".encode("utf-8"), self)
        anim.setDuration(300)
        anim.setLoopCount(15)
        anim.setStartValue(self.color)
        anim.setEndValue(QColor(255, 255, 255, 127))
        anim.setKeyValueAt(0.5, QColor(0, 255, 0, 127))

    def getColor(self):
        return PyUtils.getColor(self, 2)

    def setColor(self, color):
        PyUtils.setColor(self, color, 2)

    def setBackgroundColor(self, color):
        PyUtils.setColor(self, color, 2)

    def setForegroundColor(self, color):
        PyUtils.setColor(self, color, 0)

    color = QtCore.pyqtProperty(QColor, getColor, setColor)

    def blink(self):
        # self.animation.start()
        pass
