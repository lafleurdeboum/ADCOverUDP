import gc
import machine
import time

from hardware import ADC, takeANap


adc = ADC()

# _print to OLED GPIO display if any, otherwise
# default to stdout :
_print = hardware.OLED().print

def broadcastADCoverUDP(socket, address):
    """Send signal read on ADC on port port over UDP broadcast.
    """
    periodic_age = time.time()
    count = 0
    # Disable garbage auto-collection, we'll handle it when we have time.
    gc.disable()
    readValue = adc.readMeaningfulValue()
    try:
        socket.sendto(
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

