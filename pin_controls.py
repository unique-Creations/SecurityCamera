"""
@author: Ernesto Ruiz

simple GPIO tester
1. set mode
2. set channel as input or output
3. set state if output else read state if input.

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


def set_pin_out(pins: list):
    """
    Set the pins in the list as output pins with initial signals set to low.

    :param pins: list of pins
    """
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)


def led_on():
    """Sends a high signal on LED pin 7, which turns on the LED."""
    GPIO.output(led_pin, GPIO.HIGH)


def led_off():
    """Sends a low signal on LED pin 7, which turns off the LED."""
    GPIO.output(led_pin, GPIO.LOW)


if __name__ == "__main__":
    set_pin_out(pin_list)

    while command != "q":
        command = input("Enter command (q to quit):")
        if command == "l":
            GPIO.output(up_en_pin, GPIO.HIGH)
            GPIO.output(dn_en_pin, GPIO.LOW)
            GPIO.output(lt_en_pin, GPIO.HIGH)
            GPIO.output(rt_en_pin, GPIO.LOW)
        elif command == "r":
            GPIO.output(up_en_pin, GPIO.LOW)
            GPIO.output(dn_en_pin, GPIO.LOW)
            GPIO.output(lt_en_pin, GPIO.LOW)
            GPIO.output(rt_en_pin, GPIO.HIGH)
        elif command == "u":
            GPIO.output(up_en_pin, GPIO.HIGH)
            GPIO.output(dn_en_pin, GPIO.LOW)
            GPIO.output(lt_en_pin, GPIO.LOW)
            GPIO.output(rt_en_pin, GPIO.LOW)
        elif command == "d":
            GPIO.output(up_en_pin, GPIO.LOW)
            GPIO.output(dn_en_pin, GPIO.HIGH)
            GPIO.output(lt_en_pin, GPIO.LOW)
            GPIO.output(rt_en_pin, GPIO.LOW)
    GPIO.output(lt_en_pin, GPIO.LOW)
    GPIO.output(rt_en_pin, GPIO.LOW)
    GPIO.output(up_en_pin, GPIO.LOW)
    GPIO.output(dn_en_pin, GPIO.LOW)
    GPIO.cleanup(lt_en_pin)
    GPIO.cleanup(rt_en_pin)
    GPIO.cleanup(up_en_pin)
    GPIO.cleanup(dn_en_pin)