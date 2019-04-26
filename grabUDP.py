import machine
import time

import network_helpers
import Display


_print = Display.Display().print
#DISPLAY = Display.Display()
#def _print(arg):
#    DISPLAY.print(arg)

def pause():
    """Hang a few milliseconds"""
    #machine.sleep(0.01)
    #machine.lightsleep(10)
    machine.idle()
    time.sleep_ms(10)

def main():
    _print("Connecting wifi")
    nic = network_helpers.setup_wifi()
    while not nic.isconnected():
        pause()

    _print("Setting socket")
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.bind(("192.168.4.255", 8080))
    #s.bind(("192.168.1.255", 8080))
    #s.bind(("", 8080))
    sock = network_helpers.setup_socket(nic)
    sock.settimeout(None)

    _print("Reading")
    payload = b""
    while True:
        payload = sock.recv(4).decode()
        print(payload)
        pause()

if __name__ == "__main__":
    main()

