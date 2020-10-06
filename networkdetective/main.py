#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import sys
import traceback

from widgets.desktop_widget import DesktopWidget

from PyQt5.QtWidgets import QApplication

# TODO manage device status
# TODO packets stats by devices
# TODO auto move to bottom right when new device - reposition window
# TODO save last device, colors and window position to file


def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    logging.debug(args)
    logging.debug(traceback.print_tb(args[2]))


def main():
    app = QApplication(sys.argv)

    widget = DesktopWidget()
    widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    # install exception hook: without this, uncaught exception would cause application to exit
    sys.excepthook = trap_exc_during_debug

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)-8s (%(threadName)s) %(message)s')

    main()
