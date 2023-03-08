import datetime as dt

from data import ScanResult


def print_scan_result(scan_result: ScanResult, empty_field: str = "???",
                      separator: str = " | ") -> None:
    print(
        dt.datetime.now(),
        scan_result.host_name if scan_result.host_name else empty_field,
        scan_result.host_ip,
        f"{scan_result.round_trip_time:.2f} ms",
        sep=separator,
        end="\n" if scan_result.port_info is None else separator,
    )
    if scan_result.port_info is not None:
        print(
            scan_result.port_info.port,
            "Opened" if scan_result.port_info.is_open else "Unknown",
            sep=separator,
        )
