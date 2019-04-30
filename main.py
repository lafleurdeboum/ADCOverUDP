import wifi
import board
from hardware import Display, takeANap

# _print to OLED GPIO display if any, otherwise
# default to stdout :
_print = Display().print

if board.role == "server":
    connection = wifi.AccessPoint()
elif board.role == "client":
    connection = wifi.WifiConnection()

if board.action == "broadcast":
    import broadcastUDP
    # Alternate between unconnected and connected states :
    while True:
        _print("Setting socket")
        sock = connection.openUDPSocket((connection.ip, board.port))
        _print("Waiting clients on AP :\n%s" % connection.essid)
        while not connection.isconnected():
            takeANap()
        address = connection.broadcast, board.port
        _print("Sending ADC signal to\n%s\nport %s" % address)
        while connection.isconnected():
            broadcastUDP.broadcastADCoverUDP(sock, address)

elif board.action == "listen":
    import grabUDP
    # Alternate between unconnected and connected states :
    while True:
        while not connection.isconnected():
            takeANap()
        _print("Setting socket")
        address = connection.broadcast, board.port
        sock = connection.openUDPSocket(address)
        _print("Listening on AP\n%s\nport %s" % (connection.essid, board.port))
        while connection.isconnected():
            grabUDP.grabSignalOverUDP(sock, address)

