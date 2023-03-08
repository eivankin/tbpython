from pydantic import BaseModel, IPvAnyAddress, validator


class HostData(BaseModel):
    host_name: str | None = None
    host_ips: list[IPvAnyAddress]
    ports: list[int]

    @validator("ports", each_item=True)
    def validate_port(cls, v: int) -> int:
        assert 0 <= v <= 65535, "Port must be between 0 and 65535"
        return v


class RawData(BaseModel):
    host: str
    ports: list[str]

    @validator("ports", each_item=True)
    def validate_port(cls, v: str) -> str:
        assert len(v) > 0
        return v


class PortInfo(BaseModel):
    port: int
    is_open: bool


class ScanResult(BaseModel):
    host_name: str | None
    host_ip: IPvAnyAddress
    round_trip_time: float
    port_info: PortInfo | None
