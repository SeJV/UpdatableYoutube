#!/usr/bin/env python

import logging
import os
import sys
import time

from update_youtube_video import UpdateYoutubeVideoDeamon


if __name__ == '__main__':

    action = sys.argv[1]
    logfile = os.path.join(os.getcwd(), "sleepy.log")
    pidfile = os.path.join(os.getcwd(), "sleepy.pid")

    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    d = UpdateYoutubeVideoDeamon(pidfile=pidfile)

    if action == "start":
        d.start()

    elif action == "stop":
        d.stop()

    elif action == "restart":
        d.restart()
