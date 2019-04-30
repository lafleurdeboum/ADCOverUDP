"""Relay.py - micropython on esp to run a relay that switches power.

Usage :

    import Relay
    relay = Relay.setup_relay()
    Relay.blink(relay)

I'm using pin labelled D2 on my esp8266 ; that's Pin(4) in micropython (?)
"""


import machine
import time


#RELAY_PIN = 4              # D2 on the Wemos TTGO 0.91 OLED - used by the OLED
RELAY_PIN = 15              # That's D8
BLINK_LENGTH = 10           # In milliseconds


class Relay:
    def __init__(self, duration=BLINK_LENGTH):
        self.pin = machine.Pin(RELAY_PIN, machine.Pin.OUT, value=0)
        self.duration = duration
    def on(self):
        self.pin.on()
    def off(self):
        self.pin.off()
    def blink(self):
        self.on()
        time.sleep_ms(self.duration)
        self.off()


if __name__ == "__main__":
    relay = Relay()
    print("Blinking relay now.")
    relay.blink()

