"""Relay.py - micropython on esp to run a relay that switches power.

Usage :

    import Relay
    relay = Relay.setup_relay()
    relay.on()
    time.sleep_ms(10)
    relay.off()

or simply

    Relay.blink(relay)

I'm using pin labelled D2 on my esp8266 ; that's Pin(4) in micropython (?)
"""


import machine
import time


#RELAY_PIN = 4              # That's D2 on the Wemos TTGO 0.91 OLED - used by the OLED
RELAY_PIN = 15              # That's D8
BLINK_LENGTH = 10           # In milliseconds


def setup_relay():
    """Returns a descriptor to trigger the relay.
    """
    return machine.Pin(RELAY_PIN, machine.Pin.OUT, value=0)

def blink(relay, duration=BLINK_LENGTH):
    """Blink the relay on/off during duration milliseconds.
    """
    relay.on()
    time.sleep_ms(duration)
    relay.off()

if __name__ == "__main__":
    relay = setup_relay()
    blink(relay)

