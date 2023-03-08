from abc import ABC, abstractmethod
from ipaddress import IPv4Address, IPv6Address
import socket


class PortChecker(ABC):
    @abstractmethod
    def check_port(self, host: IPv4Address | IPv6Address, port: int) -> bool:
        pass


class SocketPortChecker(PortChecker):
    __timeout: int

    def __init__(self, timeout: int = 2):
        self.__timeout = timeout

    def check_port(self, host: IPv4Address | IPv6Address, port: int) -> bool:
        family = socket.AF_INET if isinstance(host, IPv4Address) else socket.AF_INET6
        try:
            # TCP
            with socket.socket(family, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.__timeout)
                sock.connect((str(host), port))
            return True
        except socket.error:
            return False
