import sys
from typing import Generator

from pydantic import ValidationError

from print_results import print_scan_result
from reader import CSVReader, InputReader
from data import HostData, ScanResult, PortInfo
from network.host_resolving import HostResolver, SocketHostResolver, ResolverError
from network.pinging import Pinger, PythonpingPinger, PingerError
from network.port_checking import PortChecker, SocketPortChecker


def get_info(
    host_data: HostData, pinger: Pinger, port_checker: PortChecker
) -> Generator[ScanResult, None, None]:
    for ip in host_data.host_ips:
        try:
            rtt = pinger.get_rtt(ip)
            for port in host_data.ports:
                yield ScanResult(
                    port_info=PortInfo(
                        is_open=port_checker.check_port(ip, port), port=port
                    ),
                    host_name=host_data.host_name,
                    host_ip=ip,
                    round_trip_time=rtt,
                )

            if not host_data.ports:
                yield ScanResult(
                    port_info=None,
                    host_name=host_data.host_name,
                    host_ip=ip,
                    round_trip_time=rtt,
                )
        except PingerError as e:
            print(f"Failed to ping '{ip}':", e, file=sys.stderr)


def load_data(
    reader: InputReader,
    host_resolver: HostResolver,
) -> Generator[HostData, None, None]:
    for data in reader.read():
        try:
            host_name, host_ips = host_resolver.resolve_host(data.host)
            host_data = HostData(
                host_name=host_name, host_ips=host_ips, ports=data.ports
            )
            print(host_data)
            yield host_data

        except ValidationError:
            print(f"Skipping {data} due to validation error", file=sys.stderr)
        except ResolverError as e:
            print(f"Failed to resolve host '{data.host}': {e}", file=sys.stderr)


def main(
    reader: InputReader,
    host_resolver: HostResolver,
    pinger: Pinger,
    port_checker: PortChecker
) -> None:
    for host_data in load_data(reader, host_resolver):
        for result in get_info(host_data, pinger, port_checker):
            print_scan_result(result)


if __name__ == "__main__":
    main(
        CSVReader("data.csv"),
        SocketHostResolver(),
        PythonpingPinger(),
        SocketPortChecker(),
    )
