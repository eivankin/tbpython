import datetime as dt

from data import ScanResult

EMPTY_FIELD = "???"
SEPARATOR = " | "


def print_scan_result(scan_result: ScanResult) -> None:
    print(
        dt.datetime.now(),
        scan_result.host_name if scan_result.host_name else EMPTY_FIELD,
        scan_result.host_ip,
        f"{scan_result.round_trip_time} ms",
        sep=SEPARATOR,
        end="\n" if scan_result.port_info is None else SEPARATOR,
    )
    if scan_result.port_info is not None:
        print(
            scan_result.port_info.port,
            "Opened" if scan_result.port_info.is_open else "Unknown",
            sep=SEPARATOR,
        )
