from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PacketDecoded:
    portnum: str
    payload: str
    text: str
    bitfield: Optional[int] = None


@dataclass
class Packet:
    id: int
    nodeFrom: str
    fromId: str
    nodeTo: str
    toId: str
    decoded: PacketDecoded
    rxTime: datetime
    rxSnr: float
    rxRssi: int
    channel: Optional[str] = None
    wantAck: Optional[bool] = None
    hopLimit: Optional[int] = None
    hopStart: Optional[int] = None
    publicKey: Optional[str] = None
    pkiEncrypted: Optional[bool] = None
    nextHop: Optional[str] = None
    relayNode: Optional[str] = None