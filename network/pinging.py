from abc import ABC, abstractmethod
from ipaddress import IPv4Address, IPv6Address
import platform
import subprocess


class Pinger(ABC):
    @abstractmethod
    def get_rtt(self, ip: IPv4Address | IPv6Address) -> float:
        pass


class SubprocessPinger(Pinger):
    __is_windows: bool

    def __init__(self):
        self.__is_windows = platform.system().lower() == "windows"

    def get_rtt(self, ip: IPv4Address | IPv6Address) -> float:
        command = ["ping", "-n" if self.__is_windows else "-c", "1", str(ip)]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode("utf-8")
        if result.returncode != 0:
            error = result.stderr.decode("utf-8")
            if not error:
                error = output.split("\n")[1]
            raise PingerError(error)
        rtt_stats = output.split("\n")[-2]
        if not self.__is_windows:
            # parse iputils ping output
            rtt_avg = float(rtt_stats.split("/")[-3])
        else:
            # parse windows ping output
            rtt_avg = float(rtt_stats.split("=")[-1].split()[0])
        return rtt_avg


class PythonpingPinger(Pinger):
    def __init__(
        self,
    ):
        try:
            import pythonping

            self.__pyping = pythonping
        except ImportError:
            raise PingerError(
                "library 'pythonping' is required for PythonpingPinger, "
                "install it or use other pinger class"
            )

    def get_rtt(self, ip: IPv4Address | IPv6Address) -> float:
        if isinstance(ip, IPv6Address):
            raise PingerError("PythonpingPinger does not support IPv6")
        try:
            result = self.__pyping.ping(str(ip), count=1)
            return result.rtt_avg * 1000
        except PermissionError:
            raise PingerError(
                "administrator privileges are required for PythonpingPinger, "
                "try to run this program as administrator (in Windows) or as root (in Linux) "
                "or use other pinger class"
            )


class PingerError(Exception):
    pass
