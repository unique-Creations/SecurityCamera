"""
:Author: Ernesto Ruiz

Jetson Nano pin setup and control

1. sets mode
2. sets channel as input or output
3. sets state if output else read state if input.

"""

import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

# lt_en_pin: Enable left direction pin
# lt_s_pin: Left direction step pin
lt_en_pin = 12
lt_s_pin = 11

# rt_en_pin: Enable right direction pin
# rt_s_pin: Right direction step pin
rt_en_pin = 15
rt_s_pin = 13

# up_en_pin: Enable up direction pin
# up_s_pin: Up direction step pin
up_en_pin = 31
up_s_pin = 32

# dn_en_pin: Enable down direction pin
# dn_s_pin: Down direction step pin
dn_en_pin = 19
dn_s_pin = 21

# LED pin
led_pin = 7

# List of pins
pin_list = [lt_en_pin, lt_s_pin,
            rt_en_pin, rt_s_pin,
            up_en_pin, up_s_pin,
            dn_en_pin, dn_s_pin,
            led_pin]
pin_en_list = [lt_en_pin, rt_en_pin, up_en_pin, dn_en_pin]
pin_s_list = [lt_s_pin, rt_s_pin, up_s_pin, dn_s_pin]

# Set the pins in the list as output pins with initial signals set to low.
GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.LOW)


def led_on():
    """Sends a high signal on LED pin 7, which turns on the LED."""
    GPIO.output(led_pin, GPIO.HIGH)


def led_off():
    """Sends a low signal on LED pin 7, which turns off the LED."""
    GPIO.output(led_pin, GPIO.LOW)


def move_left():
    """Turn system left"""
    GPIO.output(pin_en_list, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW))


def move_right():
    """Turn system right"""
    GPIO.output(pin_en_list, (GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW))


def move_up():
    """Turn system up"""
    GPIO.output(pin_en_list, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW))


def move_down():
    """Turn system down"""
    GPIO.output(pin_en_list, (GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH))


# if __name__ == "__main__":
#     command = None
#     while command != "q":
#         command = input("Enter command (q to quit):")
#         if command == "l":
#             move_left()
#         elif command == "r":
#             move_right()
#         elif command == "u":
#             move_up()
#         elif command == "d":
#             move_down()
#     GPIO.output(pin_list, GPIO.LOW)
#     GPIO.cleanup()
