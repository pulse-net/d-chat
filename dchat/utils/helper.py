"""
Helper methods.
"""
import socket


def get_ip() -> str:
    """
    Get the IP address of the current machine.
    :return: IP address
    """
    current_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    current_socket.connect(("8.8.8.8", 1))
    ip_addr: str = current_socket.getsockname()[0]
    current_socket.close()

    return ip_addr
