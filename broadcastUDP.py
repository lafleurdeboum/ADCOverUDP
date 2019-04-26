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

import wifi_helper
import Display

PORT = 8080
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

def get_broadcast(nic):
    ip, netmask, _, _ = nic.ifconfig()
    bca_bits = ip2bits(ip)
    netmask_bits = ip2bits(netmask)
    bca_bits &= netmask_bits
    bca_bits |= ~netmask_bits
    return bits2ip(bca_bits)

def setup_socket(nic):
    sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
    )
    sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
    )
    sock.settimeout(1.0)
    ip, *_ = nic.ifconfig()
    sock.bind((ip, PORT))
    return sock


def read_adc():
    read_value = 0
    while read_value < READ_MIN:
        pause()
        read_value = ADC.read()
    print(read_value)
    return b"%04i" % read_value


def main():
    _print("Connecting wifi")
    #nic = wifi_helper.setup_wifi()
    nic = wifi_helper.setup_ap()
    while not nic.isconnected():
        pause()

    broadcast_address = get_broadcast(nic)
    print("broadcast is %s" % broadcast_address)

    s = setup_socket(nic)
    address = (broadcast_address, PORT)
    then = time.time()
    count = 0
    while True:
        _print("Sending ADC signal to\n%s\nport %s" %
                address)
        while nic.isconnected():
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
                _print("#%i - %i space" % (count, gc.mem_free()))
                gc.collect()
                then += 1

        _print("Awaiting conn")
        while not nic.isconnected():
                pause()


if __name__ == "__main__":
    main()

