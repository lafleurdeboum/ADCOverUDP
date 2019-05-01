import machine
import time

from hardware import Relay, OLED, takeANap


MAX_PAYLOAD = 4096
relay = Relay()


# _print to OLED GPIO display if any, otherwise
# default to stdout :
_print = OLED().print

def grabSignalOverUDP(socket, address):
    """Read a signal sent to this machine's port.

    One apparently doesn't receive broadcast signals if one binds to a local ip.
    One should bind to the broadcast address, like this :
    """
    _print("Setting socket")
    address = connection.broadcast, port
    sock = connection.openUDPSocket(address)
    # We will need non-blocking calls to be able to re-check connection state :
    socket.settimeout(2.0)
    try:
        payload = socket.recv(4)
    except OSError as e:
        if e.args[0] == 110:            # ETIMEDOUT
            # Connection timed out ; take A Nap and retry
            takeANap()
            return
        else:
            raise e
    except socket.timeout:
        takeANap()
        return
    #DEBUG this returns an empty string - in fact b"\x00" * 4
    print(payload.decode())
    # If signal goes above average, toggle relay :
    # WARNING this would use this machine's adc's output range.
    #if int(payload) > int(hardware.ADC.OUTPUT_RANGE / 2):
    #    print("blinking ...")
    #    relay.blink()
    relay.blink()
    takeANap()

