"""
retrieved in https://forum.micropython.org/viewtopic.php?t=5063
"""


import gc
import array
import machine
import time
import network
import socket


PORT = 8080

KNOWN_NETWORKS = {
    b"Jia": b"marseille2paris",
    b"flip": b"PilfPilf",
}


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
            print("Connecting to {}".format(name.decode("ascii")))
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
    print("Waiting for wifi connection")
    while not nic.isconnected():
        #time.sleep(.1)
        machine.idle()
        time.sleep_ms(20)
    print("Binding socket")
    sock.settimeout(1.0)
    print("done")
    ip, *_ = nic.ifconfig()
    sock.bind((ip, PORT))
    return sock


def main():
    print("Connecting wifi")
    nic, broadcast_address = setup_wifi()
    s = setup_socket(nic)
    address = (broadcast_address, PORT)
    message = "foob"
    then = time.time()
    count = 0
    print("Now sending to %s" % broadcast_address)
    while True:
        try:
            s.sendto(message, address)
            count += 1
        except OSError:
            print(count)
            raise
        except KeyboardInterrupt:
            print(count)
            raise
        # Hang a few milliseconds
        #machine.sleep(100)
        #machine.lightsleep()
        machine.idle()
        time.sleep_ms(10)
        if time.time() - then > 1:
            print(count, gc.mem_free())
            gc.collect()
            then += 1


if __name__ == "__main__":
    main()

