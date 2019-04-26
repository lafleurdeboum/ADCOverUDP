"""network helpers.py for micropython

retrieved in https://forum.micropython.org/viewtopic.php?t=5063

These helpers build nics, that are instances of the machine.WLAN class. They
can either be AP (Access Point, providing network) or WIFI clients, using network.
They will behave quite the same anyway : it will try to connect in the background, 
and the nic you get back can be tested :

    while True:
        nic = setup_wifi()
        if nic.isconnected():
            do something useful
        else:
            pause()

"""

import sys
import socket

if sys.platform == "linux":
    class network:
        class WLAN:
            def active(self, yes=True):
                pass
            def scan(self):
                pass
else:
    import network


PORT = 8080
SOCKET_TIMEOUT = None

KNOWN_NETWORKS = {
    b"microP": b"micropython",
    #b"Jia": b"marseille2paris",
    #b"flip": b"PilfPilf",
}

FALLBACK_ESSID = "microP"
FALLBACK_PASSWD = "micropython"


#
#           NIC resolution
#

def setup_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    networks = wifi.scan()
    #broadcast_address = "255.255.255.255"
    #broadcast_address = "192.168.1.255"
    for name, *_ in networks:
        if name in KNOWN_NETWORKS:
            #print("Connecting to {}".format(name.decode("ascii")))
            wifi.connect(name, KNOWN_NETWORKS[name])
            break
    return wifi, get_broadcast(wifi)

def setup_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(
            essid=FALLBACK_ESSID,
            channel=11,
            authmode=network.AUTH_WPA2_PSK,
            password=FALLBACK_PASSWD
    )
    #ap.broadcast = get_broadcast(ap)
    return ap, get_broadcast(ap)


#
#           UDP query setup
#

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
    sock.settimeout(SOCKET_TIMEOUT)
    ip, *_ = nic.ifconfig()
    sock.bind((ip, PORT))
    return sock


#
#           IP resolution
#

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

