import network
import socket


PORT = 8080

KNOWN_NETWORKS = {
    b"microP": b"micropython",
    #b"Jia": b"marseille2paris",
    #b"flip": b"PilfPilf",
}

FALLBACK_ESSID = "microP"
FALLBACK_PASSWD = "micropython"


def setup_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    networks = wifi.scan()
    #broadcast_address = "255.255.255.255"
    broadcast_address = "192.168.1.255"
    for name, *_ in networks:
        if name in KNOWN_NETWORKS:
            wifi.connect(name, KNOWN_NETWORKS[name])
            print("Connecting to {}".format(name.decode("ascii")))
            break
    return wifi


def setup_ap():
    nic = network.WLAN(network.AP_IF)
    nic.active(True)
    nic.config(
            essid=FALLBACK_ESSID,
            channel=11,
            authmode=network.AUTH_WPA2_PSK,
            password=FALLBACK_PASSWD
    )
    return nic


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
    sock.settimeout(2.0)
    ip, *_ = nic.ifconfig()
    sock.bind((ip, PORT))
    return sock

