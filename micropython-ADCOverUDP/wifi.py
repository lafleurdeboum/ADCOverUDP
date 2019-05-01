"""wifi.py - a simple abstraction layer over machine.WLAN
"""

import sys
import socket
import network
import board


SOCKET_TIMEOUT = None


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

def getBroadcast(ip, netmask):
    bca_bits = ip2bits(ip)
    netmask_bits = ip2bits(netmask)
    bca_bits &= netmask_bits
    bca_bits |= ~netmask_bits
    return bits2ip(bca_bits)


class UDPSocket(socket.socket):
    """Open an UDP Socket and bind it to address.

    address should be this machine interface's address, the one to listen _on_,
    not the one to listen _for_.
    """
    def __init__(self, address):
        super().__init__(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )
        super().setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
        )
        super().settimeout(SOCKET_TIMEOUT)
        super().bind(address)


class Connection:
    """Abstraction layer - not ment to be used directly.

    See WifiConnection and AccessPoint for usage. This is just a proxy to let
    one derive classes from network.WLAN (actually a C function).
    """
    def __init__(self, connectionType):
        self._device = network.WLAN(connectionType)
        self.active = self._device.active
        self.config = self._device.config
        self.connect = self._device.connect
        self.disconnect = self._device.disconnect
        self.ifconfig = self._device.ifconfig
        self.scan = self._device.scan
        self.status = self._device.status
        # network.WLAN.ifconfig() returns a tuple
        #       (ip, subnet, gateway, dns)
        self.ip = self.ifconfig()[0]
        self.broadcast = getBroadcast(*self.ifconfig()[0:2])
        self.essid = self.config("essid")

    def isconnected(self):
        """This method has to be called from the initial object to work.
        """
        return self._device.isconnected()

    def openUDPSocket(self, address):
        return UDPSocket(address)


class WifiConnection(Connection):
    """Connect to a known connection.

    the board.known_connections dict is stored in the file wifi.py.
    """
    def __init__(self):
        super().__init__(network.STA_IF)
        self.active(True)
        networks = self.scan()
        for name, *_ in networks:
            if name in board.known_connections:
                #print("Connecting to {}".format(name.decode("ascii")))
                self.connect(name, board.known_connections[name])
                break


class AccessPoint(Connection):
    """Create a wifi access point.

    The board.accessPointEssid and board.accessPointPassword are stored
    in the file wifi.py.
    """
    def __init__(self):
        super().__init__(network.AP_IF)
        self.active(True)
        self.config(
                essid=board.accessPointEssid,
                password=board.accessPointPassword,
                channel=11,
                authmode=network.AUTH_WPA2_PSK,
        )


