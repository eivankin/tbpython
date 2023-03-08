import socket
from abc import ABC, abstractmethod
from ipaddress import IPv4Address, IPv6Address
from pydantic import IPvAnyAddress
from pydantic.errors import IPvAnyAddressError


class HostResolver(ABC):
    def resolve_host(
        self, host: str
    ) -> tuple[str | None, list[IPv4Address | IPv6Address]]:
        try:
            address = IPvAnyAddress.validate(host)
            return None, [address]
        except IPvAnyAddressError:
            return host, list(self.get_ip_addresses(host))

    @abstractmethod
    def get_ip_addresses(self, host: str) -> set[IPv4Address | IPv6Address]:
        pass


class SocketHostResolver(HostResolver):
    def get_ip_addresses(self, host: str) -> set[IPv4Address | IPv6Address]:
        try:
            info = socket.getaddrinfo(host, 0, 0, 0, 0)
            return set(IPvAnyAddress.validate(address[4][0]) for address in info)
        except socket.gaierror as e:
            raise ResolverError(e)


class ResolverError(Exception):
    pass
