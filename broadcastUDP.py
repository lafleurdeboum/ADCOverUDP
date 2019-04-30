import gc
import machine
import time

import hardware
import networkHelpers


PORT = 8080

# _print to OLED GPIO display if any, otherwise
# default to stdout :
_print = hardware.OLED().print

adc = hardware.ADC()


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
    _print("Setting socket")
    sock = connection.openUDPSocket((connection.ip, port))
    address = connection.broadcast, port
    # Alternate between unconnected and connected states :
    while True:
        _print("Waiting clients on AP :\n%s" % connection.essid)
        while not connection.isconnected():
                takeANap()
        periodic_age = time.time()
        count = 0
        _print("Sending ADC signal to\n%s\nport %s" % address)
        # Disable garbage auto-collection, we'll handle it when we have time.
        gc.disable()
        while connection.isconnected():
            readValue = adc.readMeaningfulValue()
            try:
                sock.sendto(
                        bytes(readValue),
                        address
                )
                count += 1
            except OSError as e:
                print(count)
                raise e
            except KeyboardInterrupt as e:
                print(count)
                raise e
            takeANap()
            if time.time() - periodic_age > 1:  # This is 1 second.
                #_print("#%i - %i space" % (count, gc.mem_free()))
                gc.collect()
                periodic_age += 1
        # Re-enable grabage auto-collection.
        gc.enable()


if __name__ == "__main__":
    _print("setting wifi server up")
    accessPoint = wifi.AccessPoint()
    print("broadcast is %s" % accessPoint.broadcast)
    broadcastADCoverUDP(accessPoint, PORT)

