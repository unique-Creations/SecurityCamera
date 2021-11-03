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
    print("Exiting...")
    sys.exit()


def center_person(objX, objY, centerX, centerY, scores, image, boxes):
    signal.signal(signal.SIGINT, signal_handler)
    time.sleep(2.0)
    while True:
        (h, w) = image.shape[:2]
        centerX.value, centerY.value = (w // 2, h // 2)
        person_loc = frame_data.person_coordinates(scores, image, boxes, (centerX.value, centerY.value))
        ((objX.value, objY.value), rect) = person_loc


def pid_process(output, p, i, d, per_coord, center_coord):
    signal.signal(signal.SIGINT, signal_handler)

    p = pid.PID(p.value, i.value, d.value)
    p.initialize()

    while True:
        error = center_coord.value - per_coord.value
        output.value = p.update(error)


def in_range(val, start, end):
    return start <= val <= end


def set_servos(pan, tlt):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
    # loop indefinitely
    while True:
        # the pan and tilt angles are reversed
        pan_angle = -1 * pan.value
        tilt_angle = -1 * tlt.value
        # if the pan angle is within the range, pan

        # TODO: Implement appropriate functions for movement
        if in_range(pan_angle, x_range[0], x_range[1]):
            # Pan camera
            pass
        # if the tilt angle is within the range, tilt
        if in_range(tilt_angle, y_range[0], y_range[1]):
            # tilt camera
            pass
