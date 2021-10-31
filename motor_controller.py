"""
Implements movement of the camera using the frames.
"""
from multiprocessing import Manager
from multiprocessing import Process
import pid
import pin_controls as pins
import frame_data
import argparse
import signal
import time
import sys

# Modifiable motor ranges
x_range = (-90, 90)
y_range = (-90, 90)


def signal_handler(sig, frame):

    sys.exit()


def center_person(args, objX, objY, centerX, centerY, vid):
    signal.signal(signal.SIGINT, signal_handler)
    time.sleep(2.0)

