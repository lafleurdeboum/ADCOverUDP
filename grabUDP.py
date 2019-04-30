import machine
import time

import networkHelpers
import hardware


MAX_PAYLOAD = 4096
PORT = 8080


# _print to OLED GPIO display if any, otherwise
# default to stdout :
_print = hardware.Display().print

relay = hardware.Relay()


def takeANap():
    """Hang a few milliseconds"""
    #machine.sleep(0.01)
    #machine.lightsleep(10)
    machine.idle()
    time.sleep_ms(10)

def grabSignalOverUDP(nic, port):
    _print("Setting socket")
    sock = networkHelpers.setupSocket(nic, port)
    # We will need non-blocking calls to be able to re-check connection state :
    sock.settimeout(2.0)

    _print("Reading on AP\n%s\nport %s" %
            (nic.config("essid"), port)
    )
    # Alternate between unconnected and connected states :
    while True:
        while not nic.isconnected():
            takeANap()
        while nic.isconnected():
            try:
                payload = sock.recv(4)
            except OSError as e:
                if e.args[0] == 110:            # ETIMEDOUT
                    # Connection timed out ; take A Nap and retry
                    takeANap()
                    continue
                else:
                    raise e
            except socket.timeout:
                takeANap()
                continue
            #DEBUG this returns an empty string - in fact b"\x00" * 4
            print(payload.decode())
            # If signal goes above average, toggle relay :
            # WARNING this would use this machine's adc's output range.
            #if int(payload) > int(hardware.ADC.OUTPUT_RANGE / 2):
            #    print("blinking ...")
            #    relay.blink()
            relay.blink()
            takeANap()


if __name__ == "__main__":
    _print("Connecting wifi")
    #nic, broadcast = networkHelpers.setupWifi()
    nic, _ = networkHelpers.setupWifi()
    grabSignalOverUDP(nic, PORT)
    main()

