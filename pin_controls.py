"""
:Author: Ernesto Ruiz

Jetson Nano pin setup and control

1. sets mode
2. sets channel as input or output
3. sets state if output else read state if input.

"""

import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

# lt_en_pin: Enable left pin
# lt_s_pin: Left step pin
# lt_dir_pin: Left direction pin
lt_en_pin = 12
lt_s_pin = 11
lt_dir_pin = None

# rt_en_pin: Enable right pin
# rt_s_pin: Right step pin
# rt_dir_pin: Right direction pin
rt_en_pin = 15
rt_s_pin = 13
rt_dir_pin = None

# up_en_pin: Enable up pin
# up_s_pin: Up step pin
# up_dir_pin: Up direction pin
up_en_pin = 31
up_s_pin = 32
up_dir_pin = None

# dn_en_pin: Enable down pin
# dn_s_pin: Down step pin
# dn_dir_pin: Down direction pin
dn_en_pin = 19
dn_s_pin = 21
dn_dir_pin = None

# LED pin
led_pin = 7

# List of pins
pin_list = [lt_en_pin, lt_s_pin, lt_dir_pin,
            rt_en_pin, rt_s_pin, rt_dir_pin,
            up_en_pin, up_s_pin, up_dir_pin,
            dn_en_pin, dn_s_pin, dn_dir_pin,
            led_pin]
pin_en_list = [lt_en_pin, rt_en_pin, up_en_pin, dn_en_pin]
pin_s_list = [lt_s_pin, rt_s_pin, up_s_pin, dn_s_pin]

# Set the pins in the list as output pins with initial signals set to low.
GPIO.setup(pin_list, GPIO.OUT, initial=GPIO.LOW)

# Horizontal & vertical camera angle change per step
x_step = .45
y_step = .1


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


def terminate():
    """Clean up GPIO pins for next use."""
    GPIO.cleanup()
