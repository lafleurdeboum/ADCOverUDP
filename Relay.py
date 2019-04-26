"""relay.py - micropython on esp to run a relay that switches power.

Usage :

    relay = setup_relay()
    blink(relay)

I'm using pin labelled D2 on my esp8266 ; that's Pin(4) in micropython (?)
"""


import machine
import time


RELAY_PIN = 4
BLINK_LENGTH = 0.1              # In seconds


def setup_relay():
    return machine.Pin(RELAY_PIN, machine.Pin.OUT)

def blink(relay):
    relay.on()
    time.sleep(BLINK_LENGTH)
    relay.off()

if __name__ == "__main__":
    relay = setup_relay()
    blink(relay)

