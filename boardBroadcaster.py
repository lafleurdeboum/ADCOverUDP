name = "pyboard"

#role = "server"
role = "client"

action = "broadcast"
#action = "listen"
port = 8080

known_connections = {
    b"microP": b"micropython",
    #b"Jia": b"marseille2paris",
    #b"flip": b"PilfPilf",
}

accessPointEssid = "microP"
accessPointPassword = "micropython"

