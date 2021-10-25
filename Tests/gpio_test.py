"""
@author: Ernesto Ruiz

simple GPIO tester
1. set mode
2. set channel as input or output
3. set state if output else read state if input.

"""

import Jetson.GPIO as GPIO

left = 12
right = 15
up = 31
down = 19
if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(left, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(right, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(up, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(down, GPIO.OUT, initial=GPIO.LOW)
    command = None

    while command != "q":
        command = input("Enter command (q to quit):")
        if command == "l":
            GPIO.output(up, GPIO.HIGH)
            GPIO.output(down, GPIO.LOW)
            GPIO.output(left, GPIO.HIGH)
            GPIO.output(right, GPIO.LOW)
        elif command == "r":
            GPIO.output(up, GPIO.LOW)
            GPIO.output(down, GPIO.LOW)
            GPIO.output(left, GPIO.LOW)
            GPIO.output(right, GPIO.HIGH)
        elif command == "u":
            GPIO.output(up, GPIO.HIGH)
            GPIO.output(down, GPIO.LOW)
            GPIO.output(left, GPIO.LOW)
            GPIO.output(right, GPIO.LOW)
        elif command == "d":
            GPIO.output(up, GPIO.LOW)
            GPIO.output(down, GPIO.HIGH)
            GPIO.output(left, GPIO.LOW)
            GPIO.output(right, GPIO.LOW)
    GPIO.output(left, GPIO.LOW)
    GPIO.output(right, GPIO.LOW)
    GPIO.output(up, GPIO.LOW)
    GPIO.output(down, GPIO.LOW)
    GPIO.cleanup(left)
    GPIO.cleanup(right)
    GPIO.cleanup(up)
    GPIO.cleanup(down)