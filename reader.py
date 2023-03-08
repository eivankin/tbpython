from abc import ABC, abstractmethod
from io import TextIOWrapper

from data import RawData
import csv


class InputReader(ABC):
    @abstractmethod
    def __init__(self, file: TextIOWrapper, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def read(self) -> list[RawData]:
        pass


class CSVReader(InputReader):
    _rows: list[RawData]

    def __init__(
        self,
        file: TextIOWrapper,
        field_names=("host", "ports"),
        delimiter=";",
        list_delimiter=",",
        skip_header=True,
    ) -> None:
        with file as f:
            if skip_header:
                f.readline()
            reader = csv.DictReader(f, fieldnames=field_names, delimiter=delimiter)
            self._rows = []
            for row in reader:
                host = row[field_names[0]]
                ports = row[field_names[1]]
                ports = [x for x in ports.split(list_delimiter) if x] if ports else []
                self._rows.append(RawData(host=host, ports=ports))

    def read(self) -> list[RawData]:
        return self._rows
