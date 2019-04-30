import gc
import array
import machine
import time
import sys

import ADC
import networkHelpers
import Display


PORT = 8080

# _print to OLED GPIO display if any, otherwise
# default to stdout :
_print = Display.Display().print


adc = ADC.ADC()


def takeANap():
    """Hang 10 milliseconds.
    """
    #machine.sleep(0.01)
    #machine.lightsleep(10)
    machine.idle()
    time.sleep_ms(10)

def broadcastADCOverUDP(nic, address):
    """Send signal read on ADC over UDP broadcast, port PORT.
    """
    sock = networkHelpers.setupSocket(nic, address[1])
    while True:
        _print("Serving on AP :\n%s" % nic.config("essid"))
        while not nic.isconnected():
                takeANap()
        periodic_age = time.time()
        count = 0
        _print("Sending ADC signal to\n%s\nport %s" %
                address)
        while nic.isconnected():
            try:
                sock.sendto(bytes(adc.readMeaningfulValue()), address)
                count += 1
            except OSError as e:
                print(count)
                raise e
            except KeyboardInterrupt as e:
                print(count)
                raise e
            takeANap()
            if time.time() - periodic_age > 1:
                #_print("#%i - %i space" % (count, gc.mem_free()))
                gc.collect()
                periodic_age += 1


if __name__ == "__main__":
    _print("setting wifi server up")
    #nic = networkHelpers.setupWifi()
    nic, broadcast = networkHelpers.setupAccessPoint()
    print("broadcast is %s" % broadcast)
    address = (broadcast, PORT)
    broadcastADCOverUDP(nic, address)

