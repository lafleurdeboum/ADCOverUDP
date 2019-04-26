"""
retrieved in https://forum.micropython.org/viewtopic.php?t=5063
"""


import gc
import array
import machine
import time
import network
import socket
try:
    import esp32
    ADC_PIN = 32
    ADC = machine.ADC(machine.Pin(ADC_PIN))
    ADC.atten(machine.ADC.ATTN_11DB)
    READ_MIN = 400
    #self.adc.width(machine.ADC.WIDTH_9BIT)
except ImportError:
    ADC = machine.ADC(0)
    READ_MIN = 6

import Display


PORT = 8080

KNOWN_NETWORKS = {
    b"Jia": b"marseille2paris",
    b"flip": b"PilfPilf",
}

DISPLAY = Display.Display()

def _print(arg):
    DISPLAY.print(arg)

def pause():
    """Hang a few milliseconds"""
    #machine.sleep(0.01)
    #machine.lightsleep(10)
    machine.idle()
    time.sleep_ms(10)

def ip2bits(ip):
    res = 0
    for part in ip.split("."):
        res <<= 8
        res |= int(part)
    return res

def bits2ip(bits):
    res = []
    for _ in range(4):
        res.append(str(bits & 0xff))
        bits >>= 8
    return ".".join(reversed(res))

def read_adc():
    read_value = 0
    while read_value < READ_MIN:
        pause()
    return b"%04i" % ADC.read()

def setup_wifi():
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    networks = nic.scan()
    #broadcast_address = None
    broadcast_address = "192.168.1.255"
    #broadcast_address = ""
    for name, *_ in networks:
        if name in KNOWN_NETWORKS:
            nic.connect(name, KNOWN_NETWORKS[name])
            _print("Connecting to {}".format(name.decode("ascii")))
            ip, netmask, _, _ = nic.ifconfig()
            bca_bits = ip2bits(ip)
            netmask_bits = ip2bits(netmask)
            bca_bits &= netmask_bits
            bca_bits |= ~netmask_bits
            broadcast_address = bits2ip(bca_bits)
    return nic, broadcast_address


def setup_socket(nic):
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )
    _print("wifi not connected yet")
    while not nic.isconnected():
        pause()
    _print("Binding socket")
    sock.settimeout(1.0)
    _print("socket bound")
    ip, *_ = nic.ifconfig()
    sock.bind((ip, PORT))
    return sock


def main():
    _print("Connecting wifi")
    nic, broadcast_address = setup_wifi()
    s = setup_socket(nic)
    address = (broadcast_address, PORT)
    then = time.time()
    count = 0
    _print("Now sending to %s" % broadcast_address)
    while True:
        try:
            s.sendto(read_adc(), address)
            count += 1
        except OSError:
            _print(count)
            raise
        except KeyboardInterrupt:
            _print(count)
            raise
        pause()
        if time.time() - then > 1:
            _print("ran %i times\n%i space left" % (count, gc.mem_free()))
            gc.collect()
            then += 1


if __name__ == "__main__":
    main()

