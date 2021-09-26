"""
@author: Ernesto Ruiz

simple GPIO tester
1. set mode
2. set channel as input or output
3. set state if output else read state if input.

"""

import Jetson.GPIO as GPIO

channel = 12

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(channel, GPIO.OUT, initial=GPIO.LOW)
    command = None

    while command != "q":
        command = input("Enter command (q to quit):")
        if command == "on":
            GPIO.output(channel, GPIO.HIGH)
        else:
            GPIO.output(channel, GPIO.LOW)
    GPIO.cleanup(channel)