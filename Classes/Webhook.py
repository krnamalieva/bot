from dataclasses import dataclass
from geo import Ip

@dataclass(frozen=True)
class Webhook:
    url: str
    ip: Ip
