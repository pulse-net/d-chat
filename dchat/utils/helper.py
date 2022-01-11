import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect(("8.8.8.8", 1))
    IP = s.getsockname()[0]
    s.close()

    return IP
