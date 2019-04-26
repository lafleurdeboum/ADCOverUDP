import machine
import time

import network_helpers
import Display
import Relay


MAX_PAYLOAD = 4096

# _print to OLED GPIO display if any, otherwise
# default to stdout :
_print = Display.Display().Dprint

relay = Relay.setup_relay()

def pause():
    """Hang a few milliseconds"""
    #machine.sleep(0.01)
    #machine.lightsleep(10)
    machine.idle()
    time.sleep_ms(10)

def main():
    _print("Connecting wifi")
    nic, broadcast = network_helpers.setup_wifi()
    while not nic.isconnected():
        pause()

    _print("Setting socket")
    sock = network_helpers.setup_socket(nic)
    # We will need non-blocking calls to be able to re-check connection state :
    sock.settimeout(2.0)

    _print("Reading on AP\n%s\nport %s" %
            (nic.config("essid"), network_helpers.PORT)
    )
    payload = b""
    # Alternate between unconnected and connected states :
    while True:
        while nic.isconnected():
            try:
                payload = int(sock.recv(4).decode())
            except OSError as e:
                if e.args[0] == 110:            # ETIMEDOUT
                    # Connection timed out ; retry
                    continue
                else:
                    raise e
            # If signal goes above average, toggle relay :
            if payload > int(MAX_PAYLOAD/2):
                Relay.blink(relay)              # milliseconds
            pause()

        # Wait for the nic process to find a network back :
        while not nic.isconnected():
            pause()

if __name__ == "__main__":
    main()

