#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtGui import QColor, QPalette, QPixmap, QIcon


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path + "/networkdetective/", relative_path)


class PyUtils(object):
    @staticmethod
    def setFontSize(widget, size, bold=False):
        font = widget.font()
        font.setPointSize(size)
        font.setBold(bold)
        widget.setFont(font)

    @staticmethod
    def setColor(widget, color, type=0):
        palette = widget.palette()
        if type <= 1:
            palette.setColor(widget.foregroundRole(), color)
        if type >= 1:
            widget.setAutoFillBackground(True)
            palette.setColor(widget.backgroundRole(), color)
        widget.setPalette(palette)

    @staticmethod
    def getColor(widget, type=0):
        if type == 0:
            return widget.palette().color(QPalette.Foreground)
        elif type == 2:
            return widget.palette().color(QPalette.Background)

    @staticmethod
    def contrastColor(color):
        # counting the perceptive luminance - human eye favors green color...
        a = 1 - (0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()) / 255
        alpha = color.alpha() / 255

        if 1 - a > alpha:
            d = 0
        else:
            d = 255

        return QColor(d, d, d)


class QIcon(QIcon):
    def __init__(self, fileName):
        super(QIcon, self).__init__(resource_path(fileName))


class QPixmap(QPixmap):
    def __init__(self, fileName):
        super(QPixmap, self).__init__(resource_path(fileName))
