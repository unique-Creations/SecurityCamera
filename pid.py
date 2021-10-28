"""
https://www.pyimagesearch.com/2019/04/01/pan-tilt-face-tracking-with-a-raspberry-pi-and-opencv/

Proportional-Integral-Derivative Controller

Controls the stepping motor to keep person(s) in the frame.
"""
import time


class PID:
    def __init__(self, kP=1, kI=0, kD=0):
        """
        PID class constructor

        :param kP:
        :param kI:
        :param kD:
        """
        self.kP = kP
        self.kI = kI
        self.kD = kD

    def initialize(self):
        """Initialize current and previous time"""
        self.cur_time = time.time()
        self.prev_time = self.cur_time
        # Previous Error
        self.prev_err = 0
        # Term result variables
        self.cP = 0
        self.cI = 0
        self.cD = 0

    def update(self, error, sleep=0.2):
        """
        Update PID controller.

        :param error: value of the difference between desired set point and sensor reading.
        :param sleep: value of delay time
        :return: Summation result of updated term values
        """
        # delay
        time.sleep(sleep)
        self.cur_time = time.time()
        delta_time = self.cur_time - self.prev_time
        delta_err = error - self.prev_err

        # P term
        self.cP = error

        # I term
        self.cI += error * delta_time

        # D term
        self.cD = (delta_err / delta_time) if delta_time > 0 else 0

        # save previous values
        self.prev_time = self.cur_time
        self.prev_err = error

        return sum([self.kP * self.cP, self.kI * self.cI, self.kD * self.cD])
